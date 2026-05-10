from __future__ import annotations

from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

from agents.memory_agent import MemoryAgent
from agents.planner_agent import PlannerAgent
from agents.profile_agent import ProfileAgent
from agents.ranking_agent import RankingAgent
from agents.reasoning_agent import ReasoningAgent
from agents.retrieval_agent import RetrievalAgent
from agents.summarizer_agent import SummarizerAgent
from components.cards import render_card
from components.chat import render_chat_history, render_query_input, render_suggested_prompts
from components.login import render_login
from components.sidebar import render_sidebar
from models.llm import ResponseGenerator
from rag.chunk import chunk_documents, load_scholarships, save_processed_chunks
from rag.embed import build_faiss_index, load_index_and_store
from rag.retrieve import Retriever
from utils.constants import SUPPORTED_LANGUAGES
from utils.helpers import scholarships_to_csv, scholarships_to_pdf
from utils.i18n import t
from utils.theme import get_global_css, get_theme
from utils.translator import detect_language, from_english, to_english

load_dotenv()
st.set_page_config(page_title="BharatLLM", page_icon="🎓", layout="wide")


def init_state() -> None:
    defaults = {
        "logged_in": False,
        "onboarding_done": False,
        "chat_history": [],
        "bookmarks": [],
        "results": [],
        "query_history": [],
        "ui_language": "English",
        "theme_mode": "dark",
        "long_term_memory": {
            "preferred_language": "English",
            "preferred_state": "All India",
            "preferred_domains": [],
            "recent_turn_summaries": [],
        },
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def apply_theme() -> None:
    theme = get_theme(st.session_state.theme_mode)
    st.markdown(get_global_css(theme), unsafe_allow_html=True)


@st.cache_resource(show_spinner="Loading scholarship index...")
def ensure_vectorstore() -> tuple:
    raw_path = Path("data/raw/scholarships.json")
    chunks_path = "data/processed/chunks.json"
    index_path = "vectorstore/faiss_index/index.faiss"
    store_path = "vectorstore/faiss_index/store.pkl"
    should_rebuild = not Path(index_path).exists() or not Path(store_path).exists()
    if not should_rebuild and raw_path.exists():
        should_rebuild = raw_path.stat().st_mtime > Path(index_path).stat().st_mtime
    if should_rebuild:
        docs = load_scholarships(str(raw_path))
        chunks = chunk_documents(docs, chunk_size=500, chunk_overlap=80)
        save_processed_chunks(chunks, chunks_path)
        build_faiss_index(chunks_path, index_path, store_path)
    return load_index_and_store(index_path, store_path)


def run_query(
    query: str,
    profile: dict,
    retrieval_agent: RetrievalAgent,
    ranking_agent: RankingAgent,
    llm: ResponseGenerator,
    planner_agent: PlannerAgent,
    reasoning_agent: ReasoningAgent,
    summarizer_agent: SummarizerAgent,
    memory_agent: MemoryAgent,
) -> None:
    target_lang = SUPPORTED_LANGUAGES.get(profile.get("language", "English"), "en")
    detected = detect_language(query, fallback="en")
    query_en = to_english(query, source_lang=detected if detected else "auto")
    memory = memory_agent.update_preferences(st.session_state, profile)
    plan = planner_agent.run(query=query, query_en=query_en, profile=profile, memory=memory)
    st.session_state.chat_history.append({"role": "user", "content": query})
    if query not in st.session_state.query_history:
        st.session_state.query_history.append(query)
    with st.spinner(t("ai_analyzing", profile.get("language", "English"))):
        retrieved = retrieval_agent.run(query=query_en, profile=profile, top_k=24)
        ranked = ranking_agent.rank(retrieved, profile=profile, top_n=10)
        grounding_brief = reasoning_agent.build_grounding_brief(plan.to_dict(), profile, ranked)
        st.session_state.results = ranked
        if not ranked:
            answer_en = (
                "I couldn't find scholarships that exactly match your profile. "
                "Try broadening your filters — set state to 'All India' or education to 'Any'."
            )
        else:
            answer_en = llm.generate(
                query_en,
                profile,
                ranked,
                st.session_state.chat_history,
                plan=plan.to_dict(),
                grounding_brief=grounding_brief,
            )
        if not answer_en or not answer_en.strip():
            answer_en = summarizer_agent.fallback_answer(ranked)
        memory_agent.remember_turn(st.session_state, summarizer_agent.summarize_turn(query, ranked))
        if answer_en and answer_en.strip():
            answer = from_english(answer_en, target_lang=target_lang)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})


def render_dashboard() -> None:
    profile_raw = render_sidebar()
    profile = ProfileAgent().normalize(profile_raw)
    language = profile.get("language", st.session_state.get("ui_language", "English"))
    index, store = ensure_vectorstore()
    retrieval_agent = RetrievalAgent(Retriever(index=index, store=store))
    ranking_agent = RankingAgent()
    llm = ResponseGenerator()
    planner_agent = PlannerAgent()
    reasoning_agent = ReasoningAgent()
    summarizer_agent = SummarizerAgent()
    memory_agent = MemoryAgent()

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class='dash-header'>
            <div class='dash-title'>🎓 {t('title', language).replace('🎓 ', '')}</div>
            <div class='dash-subtitle'>{t('subtitle', language)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Query input (top, always visible) ───────────────────────────────────
    input_query = render_query_input(language)
    prompt_query = render_suggested_prompts(language)
    active_query = input_query or prompt_query
    if active_query:
        run_query(
            active_query,
            profile,
            retrieval_agent,
            ranking_agent,
            llm,
            planner_agent,
            reasoning_agent,
            summarizer_agent,
            memory_agent,
        )
        st.rerun()

    # ── Chat history ─────────────────────────────────────────────────────────
    render_chat_history(st.session_state.chat_history, language)

    # ── Results ──────────────────────────────────────────────────────────────
    results = st.session_state.results
    has_queried = len(st.session_state.query_history) > 0

    if not has_queried:
        st.markdown(
            f"<div class='empty-state'>💡 {t('start_message', language)}</div>",
            unsafe_allow_html=True,
        )
    elif not results:
        st.markdown(
            f"<div class='empty-state'>🔍 {t('best_matches', language)}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f"<div class='section-heading'>{t('recommended_heading', language)}</div>", unsafe_allow_html=True)
        for rank, item in enumerate(results, start=1):
            saved = render_card(item, rank, language)
            if saved and item not in st.session_state.bookmarks:
                st.session_state.bookmarks.append(item)
        st.divider()
        csv_data = scholarships_to_csv(results)
        pdf_data = scholarships_to_pdf(results)
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                t("download_csv", language),
                data=csv_data,
                file_name="bharatllm_results.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with col2:
            st.download_button(
                t("download_pdf", language),
                data=pdf_data,
                file_name="bharatllm_results.pdf",
                mime="application/pdf",
                use_container_width=True,
            )


def main() -> None:
    init_state()
    apply_theme()
    if not st.session_state.logged_in:
        render_login()
        return
    render_dashboard()


if __name__ == "__main__":
    main()

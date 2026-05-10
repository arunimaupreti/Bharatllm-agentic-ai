from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class QueryPlan:
    original_query: str
    normalized_query: str
    intents: List[str]
    retrieval_strategy: str
    answer_style: str
    needs_citations: bool = True

    def to_dict(self) -> Dict:
        return {
            "original_query": self.original_query,
            "normalized_query": self.normalized_query,
            "intents": self.intents,
            "retrieval_strategy": self.retrieval_strategy,
            "answer_style": self.answer_style,
            "needs_citations": self.needs_citations,
        }


class PlannerAgent:
    """Turns a user request into an explicit RAG execution plan."""

    INTENT_KEYWORDS = {
        "eligibility": ["eligible", "eligibility", "qualify", "can i apply", "fit"],
        "deadline": ["deadline", "last date", "closing", "month"],
        "benefit": ["amount", "benefit", "highest", "money", "fee"],
        "gender": ["girl", "girls", "female", "women"],
        "domain": ["engineering", "medical", "agriculture", "legal", "government", "education"],
        "regional": ["hindi", "hinglish", "tamil", "regional", "state"],
    }

    def run(self, query: str, query_en: str, profile: Dict, memory: Dict | None = None) -> QueryPlan:
        lowered = query_en.lower()
        intents = [
            intent
            for intent, keywords in self.INTENT_KEYWORDS.items()
            if any(keyword in lowered for keyword in keywords)
        ]
        if not intents:
            intents = ["scholarship_search"]

        strategy = "hybrid_semantic_keyword"
        if "deadline" in intents:
            strategy = "hybrid_semantic_keyword_deadline_boost"
        elif "benefit" in intents:
            strategy = "hybrid_semantic_keyword_benefit_boost"

        preferred_language = (memory or {}).get("preferred_language") or profile.get("language", "English")
        answer_style = f"concise, grounded, culturally aware, reply in {preferred_language}"

        return QueryPlan(
            original_query=query,
            normalized_query=query_en,
            intents=intents,
            retrieval_strategy=strategy,
            answer_style=answer_style,
        )

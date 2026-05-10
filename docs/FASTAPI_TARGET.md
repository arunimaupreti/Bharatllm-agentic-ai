# FastAPI Production Target

This is the recommended backend shape when BharatLLM graduates from the Streamlit demo into a production service.

```python
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from agents.planner_agent import PlannerAgent
from agents.ranking_agent import RankingAgent
from agents.reasoning_agent import ReasoningAgent
from agents.retrieval_agent import RetrievalAgent
from models.llm import ResponseGenerator
from rag.retrieve import Retriever


app = FastAPI(title="BharatLLM API")


class ChatRequest(BaseModel):
    query: str
    profile: dict
    language: str = "English"


class ChatResponse(BaseModel):
    answer: str
    citations: list[str]
    results: list[dict]


def require_api_key(x_api_key: str | None = None):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API key")


@app.post("/chat", response_model=ChatResponse, dependencies=[Depends(require_api_key)])
async def chat(request: ChatRequest):
    planner = PlannerAgent()
    ranker = RankingAgent()
    reasoner = ReasoningAgent()
    llm = ResponseGenerator()

    # Load the Retriever from app startup state in production.
    retriever: Retriever = app.state.retriever
    retrieval_agent = RetrievalAgent(retriever)

    plan = planner.run(request.query, request.query, request.profile)
    retrieved = retrieval_agent.run(request.query, request.profile, top_k=24)
    ranked = ranker.rank(retrieved, request.profile, top_n=10)
    grounding = reasoner.build_grounding_brief(plan.to_dict(), request.profile, ranked)
    answer = llm.generate(request.query, request.profile, ranked, [], plan.to_dict(), grounding)
    citations = [item.get("link", "") for item in ranked if item.get("link")]
    return ChatResponse(answer=answer, citations=citations, results=ranked)
```

Production additions:

- Initialize vector index once in FastAPI lifespan startup.
- Add Redis cache keys by normalized query, profile hash, and language.
- Add request limits by API key and user ID.
- Store long-term memory in Postgres with explicit user consent.
- Keep secrets in environment variables or a cloud secret manager.

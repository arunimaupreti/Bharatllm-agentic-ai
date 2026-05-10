# Recommendation API Endpoints

Use these endpoints when BharatLLM is moved from Streamlit to FastAPI.

```python
from fastapi import FastAPI
from pydantic import BaseModel

from recommendation_engine import RecommendationEngine

app = FastAPI(title="BharatLLM Recommendation API")


class Profile(BaseModel):
    education_level: str
    income: int
    marks: int = 0
    state: str = "All India"
    category: str = "All"
    gender: str = "Not specified"
    nationality: str = "Indian"
    age: int = 0
    course_type: str = "Any"
    institute_type: str = "Any"


class RecommendRequest(BaseModel):
    query: str
    profile: Profile
    include_not_eligible: bool = False


@app.post("/recommendations")
async def recommendations(request: RecommendRequest):
    candidates = await app.state.vector_search.search_async(
        request.query,
        request.profile.model_dump(),
        top_k=50,
    )
    engine = RecommendationEngine(include_not_eligible=request.include_not_eligible)
    return {
        "results": engine.recommend(candidates, request.profile.model_dump(), top_n=10)
    }
```

Production notes:

- Run strict eligibility rules before final ranking.
- Cache embeddings by normalized scholarship text hash.
- Cache query embeddings by language + normalized query.
- Use Postgres for scholarship metadata and FAISS/Chroma/Milvus for vector search.
- Make search async at the API boundary; keep CPU-heavy ranking in a worker pool if traffic grows.

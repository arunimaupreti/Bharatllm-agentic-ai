# BharatLLM

BharatLLM is an AI-powered multilingual Indian scholarship assistant. It combines agentic RAG, strict eligibility rules, weighted recommendation scoring, multilingual translation, citation-grounded answers, and a Streamlit dashboard for Indian students.

## What Improved

- Added planner, retrieval, ranking, reasoning, summarizer, and memory agents.
- Added strict eligibility filtering for education, income, marks, state, category, gender, age, nationality, course type, institute type, and deadline.
- Added weighted recommendation scoring:
  - Education: 35%
  - Income: 25%
  - Academic marks: 15%
  - State and category: 10%
  - Gender: 5%
  - Deadline/open status: 10%
- Added recommendation types: Highly Recommended, Eligible, Future Eligible, Partially Eligible, Not Eligible.
- Added card explanations for matched criteria, failed criteria, warnings, and eligibility confidence.
- Upgraded retrieval to hybrid semantic + keyword scoring over FAISS.
- Added session memory for preferred language, state, domains, and recent turn summaries.
- Expanded supported Indian language codes.
- Added evaluation metrics, production API notes, and database schema docs.

## Project Structure

```text
bharatllm/
├── app.py
├── requirements.txt
├── README.md
├── eligibility_checker.py
├── recommendation_engine.py
├── scholarship_schema.py
├── scoring_engine.py
├── vector_search.py
├── agents/
├── components/
├── data/
├── docs/
│   ├── API_ENDPOINTS.md
│   ├── ARCHITECTURE.md
│   ├── DATABASE_SCHEMA.sql
│   └── FASTAPI_TARGET.md
├── evaluation/
├── models/
├── rag/
├── tests/
├── ui/
├── utils/
└── vectorstore/
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Configure `.env`:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-flash
```

Run:

```bash
streamlit run app.py
```

If `GEMINI_API_KEY` is not set, BharatLLM uses a deterministic citation-aware fallback generator.

## Architecture Docs

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) covers the AI pipeline, Indian language strategy, evaluation plan, fine-tuning direction, and deployment roadmap.
- [docs/FASTAPI_TARGET.md](docs/FASTAPI_TARGET.md) shows the production backend shape using FastAPI.
- [docs/API_ENDPOINTS.md](docs/API_ENDPOINTS.md) sketches production recommendation endpoints.
- [docs/DATABASE_SCHEMA.sql](docs/DATABASE_SCHEMA.sql) defines the production scholarship table.

## Notes

Semantic/vector search finds relevant candidates, but final ranking is controlled by the strict rule engine. This prevents an education mismatch, such as Class 12 user versus Undergraduate-only scholarship, from receiving a high recommendation score.

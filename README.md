# BharatLLM 🇮🇳🤖
### AI-Powered Multilingual Indian Scholarship Recommendation System

BharatLLM is an intelligent multilingual scholarship recommendation platform designed for Indian students. It combines **Agentic Retrieval-Augmented Generation (RAG)**, **strict rule-based eligibility filtering**, **semantic retrieval**, **weighted recommendation scoring**, and **multilingual support** to provide accurate scholarship recommendations with transparent reasoning and citations.

The system ensures scholarships are recommended only when users satisfy eligibility constraints including education level, income, marks, category, gender, state, age, nationality, deadlines, and institution requirements.

---

# 🚀 Live Demo

🌐 Try BharatLLM here:

**https://hjr6tphckhzc8jzbvsdyzb.streamlit.app/**

---

# 📌 Key Features

### 🤖 Agentic AI Pipeline
Integrated multiple agents:

- Planner Agent
- Retrieval Agent
- Ranking Agent
- Reasoning Agent
- Summarizer Agent
- Memory Agent

These agents improve contextual understanding, recommendation quality, and response transparency.

---

### 🎯 Strict Eligibility Filtering

Scholarships are filtered using:

✅ Education Level  
✅ Annual Family Income  
✅ Academic Marks  
✅ State Eligibility  
✅ Gender  
✅ Category (SC/ST/OBC/General/EWS)  
✅ Age Constraints  
✅ Nationality  
✅ Course Type  
✅ Institute Type  
✅ Application Deadline

This prevents irrelevant scholarship recommendations.

---

### 📊 Weighted Recommendation Scoring

Recommendations use weighted scoring:

| Factor | Weight |
|--------|--------|
| Education Match | 35% |
| Income Match | 25% |
| Academic Marks | 15% |
| State & Category | 10% |
| Gender | 5% |
| Deadline/Open Status | 10% |

---

### 🏆 Recommendation Categories

Scholarships are classified as:

- Highly Recommended
- Eligible
- Future Eligible
- Partially Eligible
- Not Eligible

---

### 🔍 Hybrid Retrieval System

Uses:

- FAISS Vector Search
- Semantic Retrieval
- Keyword Matching
- Hybrid Ranking

Improves recommendation accuracy.

---

### 🌍 Multilingual Support

Supports multiple Indian languages.

Examples:

- Hindi
- Bengali
- Tamil
- Telugu
- Marathi
- Gujarati
- Kannada
- Punjabi
- Malayalam
- Urdu
- English

---

### 🧠 Session Memory

Stores:

- Preferred language
- Previous searches
- User state
- Domains
- Recent interactions

Improves personalization.

---

### 📖 Explainable AI

Every recommendation includes:

✔ Matched criteria  
✔ Failed criteria  
✔ Warnings  
✔ Confidence score  
✔ Eligibility reasoning

---

# 🏗 Architecture

AI Pipeline:

```text
User Query
    ↓
Planner Agent
    ↓
Retriever Agent
    ↓
FAISS + Semantic Search
    ↓
Eligibility Engine
    ↓
Weighted Scoring Engine
    ↓
Ranking Agent
    ↓
Reasoning Agent
    ↓
Summarizer Agent
    ↓
Final Recommendation
```

---

# 📂 Project Structure

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
│
├── agents/
├── rag/
├── ui/
├── components/
├── data/
├── models/
├── utils/
├── tests/
├── vectorstore/
│
├── docs/
│   ├── API_ENDPOINTS.md
│   ├── ARCHITECTURE.md
│   ├── DATABASE_SCHEMA.sql
│   └── FASTAPI_TARGET.md
│
└── evaluation/
```

---

# ⚙ Installation

Clone repository:

```bash
git clone https://github.com/yourusername/bharatllm.git

cd bharatllm
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate:

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create:

```env
.env
```

Add:

```env
GEMINI_API_KEY=your_key_here

GEMINI_MODEL=gemini-1.5-flash
```

If no API key is available:

BharatLLM automatically uses deterministic citation-aware fallback generation.

---

# ▶ Run Application

Start Streamlit:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# 📈 Evaluation Metrics

Evaluation includes:

- Recommendation accuracy
- Eligibility precision
- Retrieval relevance
- Ranking quality
- Response grounding
- Multilingual performance

---

# 📚 Documentation

Additional docs:

### Architecture

```text
docs/ARCHITECTURE.md
```

Covers:

- AI pipeline
- Retrieval strategy
- Fine-tuning roadmap
- Deployment architecture

---

### API Design

```text
docs/API_ENDPOINTS.md
```

Production endpoints:

- Recommendations
- Search
- Eligibility
- User preferences

---

### Database Schema

```text
docs/DATABASE_SCHEMA.sql
```

Contains scholarship database structure.

---

### FastAPI Production Backend

```text
docs/FASTAPI_TARGET.md
```

Shows migration toward scalable backend deployment.

---

# 💻 Tech Stack

Frontend:

- Streamlit

AI/ML:

- Gemini API
- RAG
- FAISS
- NLP
- Embeddings

Backend:

- Python
- Rule Engines

Database:

- SQL

Deployment:

- Streamlit Cloud / Render

---

# 🔮 Future Improvements

Planned:

- FastAPI backend
- Authentication
- User profiles
- Feedback loop learning
- Analytics dashboard
- Real-time scholarship updates
- Mobile support

---

# 📷 Screenshots

Add screenshots here:

```markdown
![Homepage](images/homepage.png)

![Recommendations](images/recommendations.png)
```

---

# 🌟 Impact

BharatLLM aims to improve scholarship accessibility for Indian students by reducing information barriers and improving recommendation accuracy using explainable AI.

---

# 🤝 Contributing

Contributions are welcome.

Fork → Create Branch → Commit → Push → Pull Request

---

# 📄 License

MIT License

---

# 👩‍💻 Author

**Arunima Upreti**

GitHub:

https://github.com/arunimaupreti

LinkedIn:

https://www.linkedin.com/in/arunima-upreti-a1941a26a/

---

from __future__ import annotations

from typing import Dict, List

from rag.retrieve import Retriever


class VectorSearch:
    """Thin adapter around the FAISS retriever.

    Keep vector search separate from eligibility rules so semantic similarity
    never overrides mandatory scholarship requirements.
    """

    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def search(self, query: str, profile: Dict, top_k: int = 30) -> List[Dict]:
        return self.retriever.search(query=query, profile=profile, top_k=top_k)

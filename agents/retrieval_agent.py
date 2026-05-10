from __future__ import annotations

from typing import Dict, List

from rag.retrieve import Retriever


class RetrievalAgent:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def run(self, query: str, profile: Dict, top_k: int = 20) -> List[Dict]:
        return self.retriever.search(query=query, profile=profile, top_k=top_k)

from __future__ import annotations

import re
from typing import Dict, List

from sentence_transformers import SentenceTransformer

from rag.embed import MODEL_NAME, embed_query


class Retriever:
    def __init__(self, index, store, model_name: str = MODEL_NAME):
        self.index = index
        self.store = store
        self.model = SentenceTransformer(model_name)

    @staticmethod
    def _keyword_score(query: str, text: str) -> float:
        query_terms = set(re.findall(r"[a-z0-9]+", query.lower()))
        text_terms = set(re.findall(r"[a-z0-9]+", text.lower()))
        if not query_terms or not text_terms:
            return 0.0
        return len(query_terms & text_terms) / len(query_terms)

    @staticmethod
    def _intent_boost(query: str, metadata: Dict) -> float:
        query_l = query.lower()
        haystack = " ".join(str(metadata.get(k, "")) for k in metadata).lower()
        boost = 0.0
        if any(term in query_l for term in ["deadline", "last date", "closing"]) and metadata.get("deadline"):
            boost += 0.05
        if any(term in query_l for term in ["girl", "girls", "female", "women"]) and any(
            term in haystack for term in ["girl", "girls", "female", "women"]
        ):
            boost += 0.08
        if any(term in query_l for term in ["highest", "amount", "benefit", "money"]) and metadata.get("benefits"):
            boost += 0.05
        return boost

    def search(self, query: str, profile: Dict, top_k: int = 20) -> List[Dict]:
        qvec = embed_query(query=query, model=self.model)
        scores, ids = self.index.search(qvec, top_k)

        results = []
        seen = set()
        for score, idx in zip(scores[0], ids[0]):
            if idx < 0:
                continue
            metadata = self.store["metadata"][idx]
            chunk_text = self.store.get("texts", [""])[idx]
            key = metadata.get("name", f"id-{idx}")
            if key in seen:
                continue
            seen.add(key)

            semantic_score = float(score)
            keyword_score = self._keyword_score(query, chunk_text)
            hybrid_score = (0.7 * semantic_score) + (0.25 * keyword_score) + self._intent_boost(query, metadata)
            results.append(
                {
                    **metadata,
                    "semantic_score": semantic_score,
                    "keyword_score": round(keyword_score, 4),
                    "hybrid_score": round(hybrid_score, 4),
                }
            )
        results.sort(key=lambda item: item.get("hybrid_score", item.get("semantic_score", 0.0)), reverse=True)
        return results

from __future__ import annotations

from typing import Dict, List


class SummarizerAgent:
    """Creates deterministic summaries for memory and fallback answers."""

    def summarize_turn(self, query: str, ranked: List[Dict]) -> Dict:
        return {
            "last_query": query,
            "last_recommendations": [item.get("name", "") for item in ranked[:5]],
            "last_top_score": ranked[0].get("match_score", 0) if ranked else 0,
        }

    def fallback_answer(self, ranked: List[Dict]) -> str:
        if not ranked:
            return (
                "I could not find a grounded match from the current scholarship data. "
                "Try broadening state, education level, or category filters."
            )

        top = ranked[:3]
        names = ", ".join(item.get("name", "a scholarship") for item in top)
        citations = ", ".join(
            f"{item.get('name')} ({item.get('link')})"
            for item in top
            if item.get("link")
        )
        citation_line = f" Sources: {citations}." if citations else ""
        return (
            f"Your strongest grounded matches are {names}. "
            "Review the cards for eligibility, income limits, deadlines, benefits, and application links."
            f"{citation_line}"
        )

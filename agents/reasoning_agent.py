from __future__ import annotations

from typing import Dict, List


class ReasoningAgent:
    """Builds a grounded answer brief before the LLM writes the final response."""

    def build_grounding_brief(self, plan: Dict, profile: Dict, scholarships: List[Dict]) -> Dict:
        sources = []
        warnings = []

        for item in scholarships:
            sources.append(
                {
                    "name": item.get("name", "Unknown scholarship"),
                    "link": item.get("link", ""),
                    "match_score": item.get("match_score", 0),
                    "evidence": {
                        "state": item.get("state", ""),
                        "category": item.get("category", ""),
                        "education_level": item.get("education_level", ""),
                        "income_limit": item.get("income_limit", ""),
                        "deadline": item.get("deadline", ""),
                        "benefits": item.get("benefits", ""),
                    },
                }
            )

        if not scholarships:
            warnings.append("No retrieved scholarship evidence is available.")

        if profile.get("state") == "All India":
            warnings.append("State is broad; include central and state-neutral options.")

        return {
            "plan": plan,
            "profile": profile,
            "sources": sources,
            "grounding_rules": [
                "Answer only from retrieved scholarship evidence.",
                "Cite links when naming schemes.",
                "Say when a criterion is unclear instead of guessing.",
            ],
            "warnings": warnings,
        }

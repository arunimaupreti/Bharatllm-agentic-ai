from __future__ import annotations

from typing import Dict, List

from recommendation_engine import RecommendationEngine


class RankingAgent:
    def __init__(self, include_not_eligible: bool = False):
        self.engine = RecommendationEngine(include_not_eligible=include_not_eligible)

    def rank(self, items: List[Dict], profile: Dict, top_n: int = 8) -> List[Dict]:
        return self.engine.recommend(items, profile=profile, top_n=top_n)

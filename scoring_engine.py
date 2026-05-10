from __future__ import annotations

from typing import Dict

from eligibility_checker import EligibilityResult


SCORING_WEIGHTS = {
    "education": 35,
    "income": 25,
    "academic": 15,
    "state_category": 10,
    "gender": 5,
    "deadline": 10,
}

STATUS_MULTIPLIERS = {
    "Highly Recommended": 1.0,
    "Eligible": 0.92,
    "Partially Eligible": 0.62,
    "Future Eligible": 0.48,
    "Not Eligible": 0.12,
}


class ScoringEngine:
    """Weighted eligibility-first scoring.

    Semantic/vector relevance is intentionally not allowed to rescue hard
    eligibility mismatches. It only breaks ties after the rule score is built.
    """

    def score(self, scholarship: Dict, eligibility: EligibilityResult) -> float:
        matched = set(eligibility.matched)

        score = 0.0
        score += SCORING_WEIGHTS["education"] if "education_match" in matched else 0
        score += SCORING_WEIGHTS["income"] if "income_match" in matched else 0
        score += SCORING_WEIGHTS["academic"] if "academic_marks_match" in matched else 0

        state_category = 0
        if "state_match" in matched:
            state_category += 5
        if "category_match" in matched:
            state_category += 5
        score += state_category

        score += SCORING_WEIGHTS["gender"] if "gender_match" in matched else 0
        score += SCORING_WEIGHTS["deadline"] if "deadline_open" in matched or "deadline_unknown" in matched else 0

        score *= STATUS_MULTIPLIERS.get(eligibility.status, 0.5)

        if "education_mismatch" in eligibility.failed:
            score = min(score, 49.0)
        if "deadline_closed" in eligibility.failed:
            score = min(score, 59.0)

        relevance_bonus = min(5.0, max(0.0, float(scholarship.get("hybrid_score", 0.0)) * 5))
        if eligibility.status in {"Highly Recommended", "Eligible"}:
            score += relevance_bonus

        return round(min(100.0, max(0.0, score)), 1)

    @staticmethod
    def recommendation_type(score: float, status: str) -> str:
        if status in {"Future Eligible", "Partially Eligible", "Not Eligible"}:
            return status
        if score >= 85:
            return "Highly Recommended"
        if score >= 65:
            return "Eligible"
        if score >= 40:
            return "Partially Eligible"
        return "Not Eligible"

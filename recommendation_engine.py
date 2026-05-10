from __future__ import annotations

from typing import Dict, List

from eligibility_checker import EligibilityChecker
from scoring_engine import ScoringEngine
from scholarship_schema import Scholarship


LABELS = {
    "education_match": "Education match",
    "income_match": "Income match",
    "academic_marks_match": "Academic marks match",
    "state_match": "State eligibility match",
    "category_match": "Category fit",
    "gender_match": "Gender criteria match",
    "nationality_match": "Nationality match",
    "age_match": "Age criteria match",
    "age_not_required": "No age restriction",
    "course_type_match": "Course type match",
    "institute_type_match": "Institute type match",
    "deadline_open": "Applications open",
    "deadline_unknown": "Deadline not verified",
    "education_mismatch": "Education mismatch",
    "income_below_minimum": "Income below required range",
    "income_above_limit": "Income above limit",
    "academic_marks_below_requirement": "Academic marks below requirement",
    "state_mismatch": "State mismatch",
    "category_mismatch": "Category mismatch",
    "gender_mismatch": "Gender mismatch",
    "nationality_mismatch": "Nationality mismatch",
    "age_below_limit": "Age below limit",
    "age_above_limit": "Age above limit",
    "course_type_mismatch": "Course type mismatch",
    "institute_type_mismatch": "Institute type mismatch",
    "deadline_closed": "Deadline closed",
}


class RecommendationEngine:
    def __init__(self, include_not_eligible: bool = False):
        self.eligibility_checker = EligibilityChecker()
        self.scoring_engine = ScoringEngine()
        self.include_not_eligible = include_not_eligible

    def recommend(self, candidates: List[Dict], profile: Dict, top_n: int = 10) -> List[Dict]:
        recommendations = []

        for candidate in candidates:
            scholarship = Scholarship.from_dict(candidate).to_legacy_dict()
            eligibility = self.eligibility_checker.check(scholarship, profile)

            if eligibility.is_excluded and not self.include_not_eligible:
                continue

            score = self.scoring_engine.score(scholarship, eligibility)
            recommendation_type = self.scoring_engine.recommendation_type(score, eligibility.status)

            recommendations.append(
                {
                    **scholarship,
                    "match_score": score,
                    "eligibility_confidence": eligibility.confidence,
                    "eligibility_status": recommendation_type,
                    "recommendation_type": recommendation_type,
                    "matched_criteria": [LABELS.get(item, item) for item in eligibility.matched],
                    "failed_criteria": [LABELS.get(item, item) for item in eligibility.failed],
                    "eligibility_warnings": eligibility.warnings,
                    "deadline_open": eligibility.deadline_open,
                    "days_to_deadline": eligibility.days_to_deadline,
                    "education_match": "education_match" in eligibility.matched,
                    "income_match": "income_match" in eligibility.matched,
                    "academic_marks_match": "academic_marks_match" in eligibility.matched,
                    "state_match": "state_match" in eligibility.matched,
                    "category_match": "category_match" in eligibility.matched,
                    "gender_match": "gender_match" in eligibility.matched,
                }
            )

        recommendations.sort(
            key=lambda item: (
                item.get("match_score", 0),
                item.get("deadline_open", False),
                item.get("hybrid_score", 0.0),
            ),
            reverse=True,
        )
        return recommendations[:top_n]

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from scholarship_schema import Scholarship


EDUCATION_ORDER = {
    "School": 1,
    "Class 10": 2,
    "Class 12": 3,
    "Diploma": 4,
    "Undergraduate": 5,
    "Postgraduate": 6,
    "PhD": 7,
    "Any": 0,
}


@dataclass
class EligibilityResult:
    status: str
    matched: List[str] = field(default_factory=list)
    failed: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    confidence: float = 0.0
    deadline_open: bool = True
    days_to_deadline: int | None = None

    @property
    def is_excluded(self) -> bool:
        return self.status == "Not Eligible"


def _norm(value: object) -> str:
    return str(value or "").strip().lower()


def _matches_any(value: str, allowed: List[str], wildcard: str = "any") -> bool:
    allowed_norm = {_norm(item) for item in allowed}
    return wildcard in allowed_norm or "all" in allowed_norm or _norm(value) in allowed_norm


class EligibilityChecker:
    """Rule-based mandatory eligibility checks before ranking."""

    def check(self, scholarship_data: Dict, profile: Dict) -> EligibilityResult:
        scholarship = Scholarship.from_dict(scholarship_data)
        result = EligibilityResult(status="Eligible")

        self._check_education(scholarship, profile, result)
        self._check_income(scholarship, profile, result)
        self._check_marks(scholarship, profile, result)
        self._check_state(scholarship, profile, result)
        self._check_category(scholarship, profile, result)
        self._check_gender(scholarship, profile, result)
        self._check_nationality(scholarship, profile, result)
        self._check_age(scholarship, profile, result)
        self._check_course_type(scholarship, profile, result)
        self._check_institute_type(scholarship, profile, result)
        self._check_deadline(scholarship, result)

        hard_failures = [item for item in result.failed if not item.startswith("deadline")]
        if hard_failures:
            if any("education" in item for item in hard_failures) and result.warnings:
                result.status = "Future Eligible"
            elif len(hard_failures) <= 2:
                result.status = "Partially Eligible"
            else:
                result.status = "Not Eligible"
        elif not result.deadline_open:
            result.status = "Partially Eligible"
        elif len(result.matched) >= 6:
            result.status = "Highly Recommended"

        total_checks = len(result.matched) + len(result.failed)
        result.confidence = round((len(result.matched) / total_checks) * 100, 1) if total_checks else 0.0
        return result

    def _check_education(self, scholarship: Scholarship, profile: Dict, result: EligibilityResult) -> None:
        user_education = profile.get("education_level", "Any")
        required = scholarship.required_education
        if required == "Any" or user_education == required:
            result.matched.append("education_match")
            return

        user_rank = EDUCATION_ORDER.get(user_education, 0)
        required_rank = EDUCATION_ORDER.get(required, 0)
        result.failed.append("education_mismatch")
        if user_rank and required_rank and user_rank < required_rank:
            result.warnings.append(f"Eligible after {required} admission")

    def _check_income(self, scholarship: Scholarship, profile: Dict, result: EligibilityResult) -> None:
        income = int(profile.get("income", 0) or 0)
        if scholarship.min_income and income < scholarship.min_income:
            result.failed.append("income_below_minimum")
        elif scholarship.max_income and income > scholarship.max_income:
            result.failed.append("income_above_limit")
        else:
            result.matched.append("income_match")

    def _check_marks(self, scholarship: Scholarship, profile: Dict, result: EligibilityResult) -> None:
        marks = int(profile.get("marks", 0) or 0)
        if scholarship.min_marks and marks < scholarship.min_marks:
            result.failed.append("academic_marks_below_requirement")
        else:
            result.matched.append("academic_marks_match")

    def _check_state(self, scholarship: Scholarship, profile: Dict, result: EligibilityResult) -> None:
        state = profile.get("state", "All India")
        if "All India" in scholarship.eligible_states or state == "All India" or state in scholarship.eligible_states:
            result.matched.append("state_match")
        else:
            result.failed.append("state_mismatch")

    def _check_category(self, scholarship: Scholarship, profile: Dict, result: EligibilityResult) -> None:
        category = profile.get("category", "All")
        if _matches_any(category, scholarship.categories, wildcard="all"):
            result.matched.append("category_match")
        else:
            result.failed.append("category_mismatch")

    def _check_gender(self, scholarship: Scholarship, profile: Dict, result: EligibilityResult) -> None:
        gender = profile.get("gender", "Not specified")
        required = scholarship.gender
        if _norm(required) in {"any", "all", "not specified"} or _norm(gender) in {"", "not specified"}:
            result.matched.append("gender_match")
        elif _norm(gender) == _norm(required):
            result.matched.append("gender_match")
        else:
            result.failed.append("gender_mismatch")

    def _check_nationality(self, scholarship: Scholarship, profile: Dict, result: EligibilityResult) -> None:
        nationality = profile.get("nationality", "Indian")
        if _norm(scholarship.nationality) in {"any", _norm(nationality)}:
            result.matched.append("nationality_match")
        else:
            result.failed.append("nationality_mismatch")

    def _check_age(self, scholarship: Scholarship, profile: Dict, result: EligibilityResult) -> None:
        age = int(profile.get("age", 0) or 0)
        if not age:
            result.matched.append("age_not_required")
            return
        if scholarship.min_age and age < scholarship.min_age:
            result.failed.append("age_below_limit")
        elif scholarship.max_age and age > scholarship.max_age:
            result.failed.append("age_above_limit")
        else:
            result.matched.append("age_match")

    def _check_course_type(self, scholarship: Scholarship, profile: Dict, result: EligibilityResult) -> None:
        course_type = profile.get("course_type", "Any")
        if _norm(scholarship.course_type) in {"any", _norm(course_type)} or _norm(course_type) == "any":
            result.matched.append("course_type_match")
        else:
            result.failed.append("course_type_mismatch")

    def _check_institute_type(self, scholarship: Scholarship, profile: Dict, result: EligibilityResult) -> None:
        institute_type = profile.get("institute_type", "Any")
        if _norm(scholarship.institute_type) in {"any", _norm(institute_type)} or _norm(institute_type) == "any":
            result.matched.append("institute_type_match")
        else:
            result.failed.append("institute_type_mismatch")

    def _check_deadline(self, scholarship: Scholarship, result: EligibilityResult) -> None:
        if not scholarship.deadline:
            result.matched.append("deadline_unknown")
            return
        try:
            deadline = datetime.strptime(scholarship.deadline, "%Y-%m-%d")
        except ValueError:
            result.matched.append("deadline_unknown")
            return

        days = (deadline - datetime.now()).days
        result.days_to_deadline = days
        if days < 0:
            result.deadline_open = False
            result.failed.append("deadline_closed")
        else:
            result.matched.append("deadline_open")
            if days <= 30:
                result.warnings.append("Deadline closing soon")

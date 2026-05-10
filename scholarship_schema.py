from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


def _as_list(value: Any, default: List[str] | None = None) -> List[str]:
    if value is None or value == "":
        return default or []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value or default)
    except (TypeError, ValueError):
        return default


@dataclass
class Scholarship:
    name: str
    required_education: str = "Any"
    min_income: int = 0
    max_income: int = 0
    min_marks: int = 0
    eligible_states: List[str] = field(default_factory=lambda: ["All India"])
    gender: str = "Any"
    categories: List[str] = field(default_factory=lambda: ["All"])
    deadline: str = ""
    course_type: str = "Any"
    institute_type: str = "Any"
    nationality: str = "Indian"
    min_age: int = 0
    max_age: int = 0
    benefits: str = ""
    official_link: str = ""
    description: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Scholarship":
        return cls(
            name=str(data.get("name", "Unknown scholarship")),
            required_education=str(data.get("required_education") or data.get("education_level") or "Any"),
            min_income=_as_int(data.get("min_income"), 0),
            max_income=_as_int(data.get("max_income") if data.get("max_income") is not None else data.get("income_limit"), 0),
            min_marks=_as_int(data.get("min_marks"), 0),
            eligible_states=_as_list(data.get("eligible_states") or data.get("state"), ["All India"]),
            gender=str(data.get("gender") or "Any"),
            categories=_as_list(data.get("categories") or data.get("category"), ["All"]),
            deadline=str(data.get("deadline", "")),
            course_type=str(data.get("course_type") or "Any"),
            institute_type=str(data.get("institute_type") or "Any"),
            nationality=str(data.get("nationality") or "Indian"),
            min_age=_as_int(data.get("min_age"), 0),
            max_age=_as_int(data.get("max_age") if data.get("max_age") is not None else data.get("age_limit"), 0),
            benefits=str(data.get("benefits", "")),
            official_link=str(data.get("official_link") or data.get("link") or ""),
            description=str(data.get("description", "")),
            raw=data,
        )

    def to_legacy_dict(self) -> Dict[str, Any]:
        merged = {
            **self.raw,
            "name": self.name,
            "required_education": self.required_education,
            "education_level": self.required_education,
            "min_income": self.min_income,
            "max_income": self.max_income,
            "income_limit": self.max_income,
            "min_marks": self.min_marks,
            "eligible_states": self.eligible_states,
            "state": ", ".join(self.eligible_states),
            "gender": self.gender,
            "categories": self.categories,
            "category": ", ".join(self.categories),
            "deadline": self.deadline,
            "course_type": self.course_type,
            "institute_type": self.institute_type,
            "nationality": self.nationality,
            "min_age": self.min_age,
            "max_age": self.max_age,
            "age_limit": self.max_age,
            "benefits": self.benefits,
            "official_link": self.official_link,
            "link": self.official_link,
            "description": self.description,
        }
        return merged

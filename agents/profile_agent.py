from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class StudentProfile:
    state: str
    category: str
    income: int
    education_level: str
    gender: str = "Not specified"
    marks: int = 0
    age: int = 0
    nationality: str = "Indian"
    course_type: str = "Any"
    institute_type: str = "Any"
    language: str = "English"

    def to_dict(self) -> Dict:
        return asdict(self)


class ProfileAgent:
    def normalize(self, raw: Dict) -> Dict:
        profile = StudentProfile(
            state=(raw.get("state") or "All India").strip(),
            category=(raw.get("category") or "All").strip(),
            income=int(raw.get("income") or 0),
            education_level=(raw.get("education_level") or "Any").strip(),
            gender=(raw.get("gender") or "Not specified").strip(),
            marks=int(raw.get("marks") or 0),
            age=int(raw.get("age") or 0),
            nationality=(raw.get("nationality") or "Indian").strip(),
            course_type=(raw.get("course_type") or "Any").strip(),
            institute_type=(raw.get("institute_type") or "Any").strip(),
            language=(raw.get("language") or "English").strip(),
        )
        return profile.to_dict()

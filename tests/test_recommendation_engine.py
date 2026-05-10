from __future__ import annotations

from recommendation_engine import RecommendationEngine


def test_class_12_user_is_future_eligible_for_undergraduate_scholarship():
    engine = RecommendationEngine(include_not_eligible=True)
    profile = {
        "education_level": "Class 12",
        "income": 200000,
        "marks": 85,
        "state": "All India",
        "category": "All",
        "gender": "Female",
        "nationality": "Indian",
        "age": 18,
        "course_type": "Any",
        "institute_type": "Any",
    }
    scholarships = [
        {
            "name": "UG Scholarship",
            "required_education": "Undergraduate",
            "max_income": 800000,
            "min_marks": 60,
            "eligible_states": ["All India"],
            "categories": ["All"],
            "gender": "Any",
            "deadline": "2026-12-31",
        }
    ]

    result = engine.recommend(scholarships, profile, top_n=1)[0]

    assert result["recommendation_type"] == "Future Eligible"
    assert result["match_score"] < 50
    assert "Education mismatch" in result["failed_criteria"]


def test_exact_match_ranks_high():
    engine = RecommendationEngine()
    profile = {
        "education_level": "Class 12",
        "income": 200000,
        "marks": 85,
        "state": "Delhi",
        "category": "EWS",
        "gender": "Female",
        "nationality": "Indian",
        "age": 18,
        "course_type": "Any",
        "institute_type": "Any",
    }
    scholarships = [
        {
            "name": "Delhi Class 12 EWS Scholarship",
            "required_education": "Class 12",
            "max_income": 800000,
            "min_marks": 75,
            "eligible_states": ["Delhi"],
            "categories": ["EWS"],
            "gender": "Any",
            "deadline": "2026-12-31",
        }
    ]

    result = engine.recommend(scholarships, profile, top_n=1)[0]

    assert result["match_score"] >= 85
    assert result["recommendation_type"] == "Highly Recommended"
    assert result["failed_criteria"] == []

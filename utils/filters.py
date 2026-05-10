from typing import Dict, List, Tuple


def metadata_match(doc: Dict, profile: Dict) -> bool:
    profile_state = profile.get("state", "All India")
    doc_state = doc.get("state", "All India")
    if profile_state == "All India":
        # When user selects All India, keep both central and state scholarships.
        state_ok = True
    else:
        state_ok = doc_state in ["All India", profile_state]
    category = doc.get("category", "All")
    category_ok = category in ["All", profile.get("category", "All")]
    # Education is treated as a ranking signal, not a hard retrieval filter.
    return state_ok and category_ok


def income_fit(income_limit: int, student_income: int) -> bool:
    if income_limit <= 0:
        return True
    return student_income <= income_limit


def get_no_result_suggestions(profile: Dict) -> List[str]:
    tips = [
        "Try central government schemes (state = All India).",
        "Try increasing the income range in your query.",
        "Try selecting education level as 'Any' for broader matching.",
    ]
    if profile.get("state") and profile.get("state") != "All India":
        tips.append("Try setting state to 'All India' to include national scholarships.")
    return tips


def shortlist_with_reasons(results: List[Dict]) -> List[Tuple[Dict, str]]:
    shortlist = []
    for item in results:
        reasons = []
        if item.get("state_match"):
            reasons.append("state match")
        if item.get("income_match"):
            reasons.append("income criteria fit")
        if item.get("education_match"):
            reasons.append("education level fit")
        if item.get("category_match"):
            reasons.append("category fit")
        shortlist.append((item, ", ".join(reasons) if reasons else "semantic relevance"))
    return shortlist

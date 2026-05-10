from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class EvaluationCase:
    query: str
    expected_terms: List[str]
    answer: str
    citations: List[str]


def rouge_lite(expected_terms: Iterable[str], answer: str) -> float:
    answer_l = answer.lower()
    terms = [term.lower() for term in expected_terms if term.strip()]
    if not terms:
        return 0.0
    hits = sum(1 for term in terms if term in answer_l)
    return round(hits / len(terms), 4)


def citation_coverage(citations: List[str], answer: str) -> float:
    if not citations:
        return 0.0
    answer_l = answer.lower()
    hits = sum(1 for citation in citations if citation.lower() in answer_l)
    return round(hits / len(citations), 4)


def hallucination_risk(expected_terms: Iterable[str], answer: str, citations: List[str]) -> float:
    grounding = rouge_lite(expected_terms, answer)
    citation = citation_coverage(citations, answer)
    return round(max(0.0, 1.0 - ((0.7 * grounding) + (0.3 * citation))), 4)


def evaluate_cases(cases: List[EvaluationCase]) -> List[dict]:
    return [
        {
            "query": case.query,
            "rouge_lite": rouge_lite(case.expected_terms, case.answer),
            "citation_coverage": citation_coverage(case.citations, case.answer),
            "hallucination_risk": hallucination_risk(case.expected_terms, case.answer, case.citations),
        }
        for case in cases
    ]


if __name__ == "__main__":
    demo = [
        EvaluationCase(
            query="Best scholarship for engineering girls",
            expected_terms=["engineering", "girls", "deadline", "benefits"],
            answer="The top option is a girls engineering scholarship. Check deadline and benefits in the card.",
            citations=[],
        )
    ]
    for row in evaluate_cases(demo):
        print(row)

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


def load_scholarships(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _make_text(doc: Dict) -> str:
    fields = [
        f"Name: {doc.get('name', '')}",
        f"State: {doc.get('eligible_states', doc.get('state', ''))}",
        f"Category: {doc.get('categories', doc.get('category', ''))}",
        f"Income Range: {doc.get('min_income', '')} to {doc.get('max_income', doc.get('income_limit', ''))}",
        f"Education Level: {doc.get('required_education', doc.get('education_level', ''))}",
        f"Minimum Marks: {doc.get('min_marks', '')}",
        f"Gender: {doc.get('gender', '')}",
        f"Course Type: {doc.get('course_type', '')}",
        f"Institute Type: {doc.get('institute_type', '')}",
        f"Nationality: {doc.get('nationality', '')}",
        f"Description: {doc.get('description', '')}",
        f"Benefits: {doc.get('benefits', '')}",
        f"Deadline: {doc.get('deadline', '')}",
        f"Link: {doc.get('official_link', doc.get('link', ''))}",
    ]
    return " | ".join(fields)


def chunk_documents(
    docs: List[Dict], chunk_size: int = 500, chunk_overlap: int = 80
) -> List[Dict]:
    chunks: List[Dict] = []
    for doc in docs:
        text = _make_text(doc)
        words = text.split()
        step = max(1, chunk_size - chunk_overlap)
        for start in range(0, len(words), step):
            part = words[start : start + chunk_size]
            if not part:
                continue
            chunks.append(
                {
                    "text": " ".join(part),
                    "metadata": doc,
                }
            )
            if start + chunk_size >= len(words):
                break
    return chunks


def save_processed_chunks(chunks: List[Dict], output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

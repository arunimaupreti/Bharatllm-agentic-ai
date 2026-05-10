from __future__ import annotations

import io
from datetime import datetime
from typing import Dict, List

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def scholarships_to_csv(items: List[Dict]) -> bytes:
    return pd.DataFrame(items).to_csv(index=False).encode("utf-8")


def scholarships_to_pdf(items: List[Dict]) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    y = 800
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "BharatLLM Scholarship Results")
    y -= 24
    c.setFont("Helvetica", 10)
    for idx, item in enumerate(items, start=1):
        line = (
            f"{idx}. {item.get('name')} | Score: {item.get('match_score')}% | "
            f"Deadline: {item.get('deadline')} | {item.get('link')}"
        )
        c.drawString(40, y, line[:120])
        y -= 16
        if y < 60:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = 800
    c.save()
    return buffer.getvalue()


def filter_results(items: List[Dict], mode: str) -> List[Dict]:
    if mode == "Only Central Schemes":
        return [x for x in items if x.get("state") == "All India"]
    if mode == "Highest Benefits":
        return sorted(items, key=lambda x: len(str(x.get("benefits", ""))), reverse=True)
    if mode == "Deadline Soon":
        def parse_dt(v: str) -> datetime:
            try:
                return datetime.strptime(v, "%Y-%m-%d")
            except Exception:
                return datetime.max
        return sorted(items, key=lambda x: parse_dt(str(x.get("deadline", ""))))
    if mode == "100% Match":
        exact = [x for x in items if float(x.get("match_score", 0)) >= 99.9]
        return exact if exact else items
    return items

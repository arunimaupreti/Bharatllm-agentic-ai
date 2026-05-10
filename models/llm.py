from __future__ import annotations

import os
from typing import Dict, List

import google.generativeai as genai


class ResponseGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None

    def _fallback_response(self, query: str, scholarships: List[Dict]) -> str:
        if not scholarships:
            return (
                "I could not find scholarships matching your exact profile. "
                "Try setting state to 'All India' or education level to 'Any' for broader results."
            )

        names = ", ".join(s.get("name", "") for s in scholarships[:3])
        citations = ", ".join(
            f"{s.get('name')} ({s.get('link')})"
            for s in scholarships[:3]
            if s.get("link")
        )
        citation_line = f" Sources: {citations}." if citations else ""
        return (
            f"Based on your profile, here are your top matches: {names} - and more below. "
            "Review the cards for scores, deadlines, benefits, and apply links. "
            "You can follow up with 'only central schemes', 'deadline soon', or 'highest benefit'."
            f"{citation_line}"
        )

    def generate(
        self,
        query: str,
        profile: Dict,
        scholarships: List[Dict],
        chat_history: List[Dict],
        plan: Dict | None = None,
        grounding_brief: Dict | None = None,
    ) -> str:
        if not self.model or not scholarships:
            return self._fallback_response(query, scholarships)

        scholarships_text = "\n".join(
            f"- {s.get('name')} | State: {s.get('state')} | Category: {s.get('category')} | "
            f"Income Limit: {s.get('income_limit')} | Education: {s.get('education_level')} | "
            f"Benefits: {s.get('benefits')} | Deadline: {s.get('deadline')} | "
            f"Link: {s.get('link')} | Match Score: {s.get('match_score')}% | "
            f"Hybrid Score: {s.get('hybrid_score')}"
            for s in scholarships
        )

        history_text = ""
        for item in chat_history[-4:]:
            role = "User" if item["role"] == "user" else "Assistant"
            history_text += f"{role}: {item['content']}\n"

        prompt = f"""You are BharatLLM, a multilingual scholarship assistant for Indian students.
You understand Indian languages, Hinglish, code-mixed requests, and Indian education contexts.
Use only the provided scholarship context and grounding brief. Do not hallucinate.
Always cite source links when naming scholarships. If evidence is missing, say so.

Student profile: {profile}
Recent conversation:
{history_text}
User query: {query}
Execution plan: {plan or {}}
Grounding brief: {grounding_brief or {}}

Scholarship context:
{scholarships_text}

Respond concisely and conversationally:
1. Overall suitability summary.
2. Best next action for the student.
3. Citations with application links for named scholarships.
4. A useful follow-up suggestion.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception:
            return self._fallback_response(query, scholarships)

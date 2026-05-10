from __future__ import annotations

from typing import Dict


class MemoryAgent:
    """Small preference memory wrapper for Streamlit session state."""

    KEY = "long_term_memory"

    def load(self, session_state) -> Dict:
        if self.KEY not in session_state:
            session_state[self.KEY] = {
                "preferred_language": "English",
                "preferred_state": "All India",
                "preferred_domains": [],
                "recent_turn_summaries": [],
            }
        return session_state[self.KEY]

    def update_preferences(self, session_state, profile: Dict) -> Dict:
        memory = self.load(session_state)
        memory["preferred_language"] = profile.get("language", memory["preferred_language"])
        memory["preferred_state"] = profile.get("state", memory["preferred_state"])
        session_state[self.KEY] = memory
        return memory

    def remember_turn(self, session_state, summary: Dict) -> None:
        memory = self.load(session_state)
        recent = memory.setdefault("recent_turn_summaries", [])
        recent.append(summary)
        memory["recent_turn_summaries"] = recent[-8:]
        session_state[self.KEY] = memory

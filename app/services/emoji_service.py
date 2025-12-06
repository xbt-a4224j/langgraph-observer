# app/services/emoji_service.py

from typing import Dict, Any, Optional
from app.adapters.openai_adapter import OpenAIAdapter


class EmojiService:
    """
    Handles:
    - Transforming the text to make it have more emojis (optional).
    - Scoring emojiness (always).
    """

    def __init__(self, adapter: Optional[OpenAIAdapter] = None):
        self.adapter = adapter or OpenAIAdapter()

    # ---------------------------------------------------------
    # 1) Make the text emojified ONLY if emoji_mode==True
    # ---------------------------------------------------------
    def make_emoji(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if not state.get("emoji_mode"):
            return state  # skip if not requested

        output = state.get("llm_output", "")
        if not output:
            return state

        prompt = f"""
Your job is to take the following output and emojify it.

Rules:
- DO NOT break meaning completely.
- Aim add two more emojis than the input.


Text:
\"\"\"{output}\"\"\"
"""

        resp = self.adapter.generate_text(prompt)
        new_text = resp["text"].strip()

        state["llm_output"] = new_text
        state["emoji_transformed"] = True

        return state

    # ---------------------------------------------------------
    # 2) Score emojiness for every output (0–1 float)
    # ---------------------------------------------------------
    def score_emoji(self, state: Dict[str, Any]) -> Dict[str, Any]:
        output = state.get("llm_output", "")

        if not output:
            state["emoji_score"] = 0.0
            return state

        prompt = f"""
Rate how emoji-ey the following text is. What percentage roughly of the input is Emoji?
Respond ONLY with a FLOAT from 0 to 1.

Text:
\"\"\"{output}\"\"\"
"""

        try:
            resp = self.adapter.generate_text(prompt)
            raw = resp["text"].strip()
            score = float(raw)
        except Exception:
            score = 0.0

        state["emoji_score"] = round(score, 3)
        return state
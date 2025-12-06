# app/services/silly_service.py

from typing import Dict, Any, Optional
from app.adapters.openai_adapter import OpenAIAdapter


class SillyService:
    """
    Handles:
    - Transforming the text to make it sillier (optional).
    - Scoring silliness (always).
    """

    def __init__(self, adapter: Optional[OpenAIAdapter] = None):
        self.adapter = adapter or OpenAIAdapter()

    # ---------------------------------------------------------
    # 1) Make the text sillier ONLY if silly_mode==True
    # ---------------------------------------------------------
    def make_silly(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if not state.get("silly_mode"):
            return state  # skip if not requested

        output = state.get("llm_output", "")
        if not output:
            return state

        prompt = f"""
Your job is to take the following output and make it sillier.

Rules:
- Add humor, absurdity, whimsy, or paradox.
- Use emojis, unicode, backwards, etc. 
- DO NOT break meaning completely.
- Aim for clearly, but only 20%, sillier than before.


Text:
\"\"\"{output}\"\"\"
"""

        resp = self.adapter.generate_text(prompt)
        new_text = resp["text"].strip()

        state["llm_output"] = new_text
        state["silly_transformed"] = True

        return state

    # ---------------------------------------------------------
    # 2) Score silliness for every output (0–1 float)
    # ---------------------------------------------------------
    def score_silly(self, state: Dict[str, Any]) -> Dict[str, Any]:
        output = state.get("llm_output", "")

        if not output:
            state["silly_score"] = 0.0
            return state

        prompt = f"""
Rate how silly / humorous / whimsical / absurd the following text is.
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

        state["silly_score"] = round(score, 3)
        return state
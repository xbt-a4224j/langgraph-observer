# app/services/hallucination_service.py

from typing import Dict, Any, Optional
from app.adapters.openai_adapter import OpenAIAdapter


class HallucinationService:
    """
    Computes a hallucination score (0–1) by prompting the LLM to evaluate
    whether its own answer is factual or unsupported.
    This replaces hallucination_score_node from the original code.
    """

    def __init__(self, adapter: Optional[OpenAIAdapter] = None):
        self.adapter = adapter or OpenAIAdapter()

    def score_hallucination(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assigns a hallucination score based on LLM self-critique.
        """

        output = state.get("llm_output", "")
        user = state.get("user_input", "")

        if not output:
            state["hallucination_score"] = 0.0
            return state

        prompt = f"""
Evaluate whether the model's response contains hallucinations.

Consider two types of hallucinations:
1. Factual inaccuracies or unsupported claims.
2. Treating fictional, impossible, or unanswerable premises as if real
   without stating they are fictional.

USER QUESTION:
\"\"\"{user}\"\"\"

MODEL RESPONSE:
\"\"\"{output}\"\"\"

Respond ONLY with a number 0–1:
  0 = fully factual / properly handled
  1 = strongly hallucinated
"""

        try:
            resp = self.adapter.generate_text(prompt)
            score_raw = resp["text"].strip()
            score = float(score_raw)
        except Exception:
            score = 0.5  # fallback if model responds strangely

        state["hallucination_score"] = round(score, 3)
        return state
# app/services/toxicity_service.py

from typing import Dict, Any, Optional

from app.adapters.openai_adapter import OpenAIAdapter


class ToxicityService:
    """
    Wraps the OpenAI moderation API and returns a numeric toxicity score
    (0.0–1.0), consistent with the original toxicity_score_node logic.
    """

    def __init__(self, adapter: Optional[OpenAIAdapter] = None):
        self.adapter = adapter or OpenAIAdapter()

    def score_toxicity(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Equivalent to the old toxicity_score_node, but using dict state and
        the new adapter.
        """

        text = state.get("llm_output", "")
        if not text:
            state["toxicity_score"] = 0.0
            return state

        response = self.adapter.moderate_text(text)
        raw = response.category_scores

        # Flatten possible Pydantic structure
        try:
            flat = raw.model_dump()
        except Exception:
            flat = raw.__dict__

        numeric_vals = []

        for k, v in flat.items():
            try:
                numeric_vals.append(float(v))
            except Exception:
                pass  # skip None or non-numerics

        toxicity = max(numeric_vals) if numeric_vals else 0.0

        state["toxicity_score"] = float(toxicity)
        return state
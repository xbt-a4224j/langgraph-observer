# app/services/explanation_service.py

from typing import Dict, Any, Optional

from app.adapters.openai_adapter import OpenAIAdapter


class ExplanationService:
    """
    Generates a clarity/explanation score for the model output.
    Mirrors the behavior of the old explanation_node.
    """

    def __init__(self, adapter: Optional[OpenAIAdapter] = None):
        self.adapter = adapter or OpenAIAdapter()

    def score_explanation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Equivalent to explanation_node: Requests a 0–100 clarity score.
        """

        llm_output = state.get("llm_output", "")
        if not llm_output:
            state["explanation"] = None
            state["score"] = None
            return state

        prompt = (
            "Give a score 0–100 for clarity of this text "
            "(just output a number): "
            f"{llm_output}"
        )

        resp = self.adapter.generate_text(prompt)
        text = resp["text"].strip()

        # Extract a numeric score from freeform text
        score = None
        for token in text.split():
            if token.isdigit():
                score = int(token)
                break

        state["explanation"] = text
        state["score"] = score
        return state

    def explain(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Alias required by workflow_graph: explanation node must expose `.explain`.
        Internally delegates to score_explanation.
        """
        return self.score_explanation(state)
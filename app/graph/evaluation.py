from typing import Dict
from .state import GraphState


def evaluate_output(state: GraphState) -> GraphState:
    """
    Basic evaluation (stub).
    Adds a simple score based on heuristics for now.
    """
    output = state.get("llm_output", "")

    score = 0
    if len(output) > 0:
        score += 1
    if '?' in output:
        score += 1
    if len(output) > 80:
        score += 1

    return {
        **state,
        "score": score
    }
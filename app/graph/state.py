from typing import Optional, TypedDict, Dict, Any

class GraphState(TypedDict, total=False):
    user_input: str
    llm_output: Optional[str]

    explanation: Optional[str]
    score: Optional[int]

    toxicity_score: Optional[float]
    hallucination_score: Optional[float]

    token_usage: Optional[Dict[str, Any]]
    cost: Optional[float]

    start_time: Optional[float]
    duration_seconds: Optional[float]
    artifact_path: Optional[str]
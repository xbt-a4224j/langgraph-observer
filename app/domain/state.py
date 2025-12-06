from typing import Optional, Dict, Any
from pydantic import BaseModel

class GraphState(BaseModel):
    user_input: str
    llm_output: Optional[str] = None

    explanation: Optional[str] = None
    score: Optional[int] = None

    toxicity_score: Optional[float] = None
    hallucination_score: Optional[float] = None

    token_usage: Optional[Dict[str, Any]] = None
    cost: Optional[float] = None

    start_time: Optional[float] = None
    duration_seconds: Optional[float] = None
    artifact_path: Optional[str] = None
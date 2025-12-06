from typing import Optional, Dict, Any
from pydantic import BaseModel

class GraphState(BaseModel):
    user_input: str
    llm_output: Optional[str] = None

    toxicity_score: Optional[float] = None
    hallucination_score: Optional[float] = None
    emoji_score: Optional[int] = None

    token_usage: Optional[Dict[str, Any]] = None
    cost: Optional[float] = None

    start_time: Optional[float] = None
    duration_seconds: Optional[float] = None
    artifact_path: Optional[str] = None
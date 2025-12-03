from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class RunGraphRequest(BaseModel):
    input: str

class RunGraphResponse(BaseModel):
    state: Dict[str, Any]
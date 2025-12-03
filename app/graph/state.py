from typing import TypedDict, Optional, List

class GraphState(TypedDict, total=False):
    user_input: str
    llm_output: Optional[str]
    explanation: Optional[str]
    artifacts: Optional[List[str]]  # paths to logs, stored artifacts, etc.
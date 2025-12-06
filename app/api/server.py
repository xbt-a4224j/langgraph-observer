from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.domain.workflow_graph import build_graph

# init fastApi and state graph
app = FastAPI(title="LangGraph Observer API (Refactored)")
graph = build_graph()


# like @controller in Spring Boot
class RunRequest(BaseModel):
    input: str
    emoji_mode: bool = False


@app.post("/run-graph", summary="Run the workflow", response_description="Final state")
def run_graph(payload: RunRequest):
    """
    Runs the LangGraph pipeline.

    - Generates model output
    - Computes toxicity, hallucination, emoji metrics
    - Saves artifact + history

    Returns the final state as a JSON object.
    """
    try:
        # Base state
        state = {
            "user_input": payload.input,
            "emoji_mode": payload.emoji_mode,
        }

        # Execute LangGraph
        result = graph.invoke(state)

        # Return final output state
        return {"state": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/health",
    summary="Health check",
    response_description="API status"
)
def health():
    """
    Returns basic API availability status.
    """
    return {"status": "ok"}
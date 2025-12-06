# app/api/server.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.domain.workflow_graph import build_graph


app = FastAPI(title="LangGraph Observer API (Refactored)")

# Build the compiled workflow once at startup
graph = build_graph()


# -----------------------------
# Request Model
# -----------------------------
class RunRequest(BaseModel):
    input: str


# -----------------------------
# POST /run-graph
# -----------------------------
@app.post("/run-graph")
def run_graph(payload: RunRequest):
    """
    Runs the full LangGraph workflow and returns final state.
    Identical to the old API structure.
    """
    try:
        state = {"user_input": payload.input}
        result = graph.invoke(state)
        return {"state": result}

    except Exception as e:
        # Preserve original FastAPI error formatting
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Optional: Basic health check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}
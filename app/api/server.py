# app/api/server.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.domain.workflow_graph import build_graph

app = FastAPI(title="LangGraph Observer API (Refactored)")

# Build LangGraph workflow once at startup
graph = build_graph()


# -----------------------------
# Request Model
# -----------------------------
class RunRequest(BaseModel):
    input: str
    emoji_mode: bool = False   # <-- NEW, optional


# -----------------------------
# POST /run-graph
# -----------------------------
@app.post("/run-graph")
def run_graph(payload: RunRequest):
    """
    Runs the full LangGraph workflow and returns final state.
    Adds emoji_mode to the backend state so the emoji-service can read it.
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


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}
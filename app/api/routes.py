# app/api/routes.py

from fastapi import APIRouter
from pydantic import BaseModel

from app.domain.workflow_graph import build_graph

router = APIRouter()
graph = build_graph()  # Precompiled workflow


class RunRequest(BaseModel):
    input: str


@router.post("/run-graph")
def run_graph(payload: RunRequest):
    """
    Executes the full LangGraph pipeline with the provided input text.
    """
    state = {"user_input": payload.input}
    result = graph.invoke(state)
    return {"state": result}
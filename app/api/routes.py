from fastapi import APIRouter
from app.graph.workflow import build_graph
from .models import RunGraphRequest, RunGraphResponse

router = APIRouter()

# Build the graph once at import time
graph = build_graph()

@router.post("/run-graph", response_model=RunGraphResponse)
async def run_graph(payload: RunGraphRequest):
    result = graph.invoke({"user_input": payload.input})
    return RunGraphResponse(state=result)


@router.get("/health")
async def health():
    return {"status": "ok"}
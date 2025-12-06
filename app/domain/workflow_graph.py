# app/domain/workflow_graph.py

from langgraph.graph import StateGraph, END

# Import services
from app.services.llm_service import LLMService
from app.services.explanation_service import ExplanationService
from app.services.toxicity_service import ToxicityService
from app.services.hallucination_service import HallucinationService
from app.services.artifact_service import ArtifactService


def build_graph():
    """
    Assembles the LangGraph workflow using the refactored services.
    All services operate on plain dict state.
    """

    # Instantiate services
    llm = LLMService()
    explain = ExplanationService()
    toxic = ToxicityService()
    halluc = HallucinationService()
    artifacts = ArtifactService()

    # Build workflow graph
    workflow = StateGraph(dict)

    workflow.add_node("generate", llm.generate)
    workflow.add_node("explain", explain.explain)  # alias to score_explanation
    workflow.add_node("toxicity", toxic.score_toxicity)
    workflow.add_node("hallucination", halluc.score_hallucination)
    workflow.add_node("artifact", artifacts.save_artifact)

    # Define flow order
    workflow.set_entry_point("generate")
    workflow.add_edge("generate", "explain")
    workflow.add_edge("explain", "toxicity")
    workflow.add_edge("toxicity", "hallucination")
    workflow.add_edge("hallucination", "artifact")
    workflow.add_edge("artifact", END)

    return workflow.compile()
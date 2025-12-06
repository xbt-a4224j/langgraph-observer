# app/domain/workflow_graph.py

from langgraph.graph import StateGraph, END

from app.services.llm_service import LLMService
from app.services.toxicity_service import ToxicityService
from app.services.hallucination_service import HallucinationService
from app.services.artifact_service import ArtifactService
from app.services.silly_service import SillyService

_llm = LLMService()
_tox = ToxicityService()
_hal = HallucinationService()
_art = ArtifactService()
_silly = SillyService()


def build_graph():
    workflow = StateGraph(dict)

    workflow.add_node("generate", _llm.generate)
    workflow.add_node("make_silly", _silly.make_silly)
    workflow.add_node("score_silly", _silly.score_silly)
    workflow.add_node("toxicity", _tox.score_toxicity)
    workflow.add_node("hallucination", _hal.score_hallucination)
    workflow.add_node("artifact", _art.save_artifact)

    workflow.set_entry_point("generate")

    # Main linear chain
    workflow.add_edge("generate", "make_silly")
    workflow.add_edge("make_silly", "score_silly")
    workflow.add_edge("score_silly", "toxicity")
    workflow.add_edge("toxicity", "hallucination")
    workflow.add_edge("hallucination", "artifact")
    workflow.add_edge("artifact", END)

    return workflow.compile()
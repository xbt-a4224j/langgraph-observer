# app/domain/workflow_graph.py

from langgraph.graph import StateGraph, END

from app.services.llm_service import LLMService
from app.services.toxicity_service import ToxicityService
from app.services.hallucination_service import HallucinationService
from app.services.artifact_service import ArtifactService
from app.services.emoji_service import EmojiService

_llm = LLMService()
_tox = ToxicityService()
_hal = HallucinationService()
_art = ArtifactService()
_emoji = EmojiService()


def build_graph():
    workflow = StateGraph(dict)

    #nodeset
    workflow.add_node("generate", _llm.generate)
    workflow.add_node("make_emoji", _emoji.make_emoji)
    workflow.add_node("score_emoji", _emoji.score_emoji)
    workflow.add_node("toxicity", _tox.score_toxicity)
    workflow.add_node("hallucination", _hal.score_hallucination)
    workflow.add_node("artifact", _art.save_artifact)

    workflow.set_entry_point("generate")

    # edgeset; Main linear chain
    workflow.add_edge("generate", "make_emoji")
    workflow.add_edge("make_emoji", "score_emoji")
    workflow.add_edge("score_emoji", "toxicity")
    workflow.add_edge("toxicity", "hallucination")
    workflow.add_edge("hallucination", "artifact")
    workflow.add_edge("artifact", END)

    return workflow.compile()
from langgraph.graph import StateGraph, END
from .state import GraphState
from .nodes import (
    llm_generate_node,
    explanation_node,
    toxicity_score_node,
    hallucination_score_node,
    artifact_node
)

def build_graph():
    workflow = StateGraph(GraphState)

    # Nodes
    workflow.add_node("generate", llm_generate_node)
    workflow.add_node("explain", explanation_node)
    workflow.add_node("toxicity", toxicity_score_node)
    workflow.add_node("hallucination", hallucination_score_node)
    workflow.add_node("artifact", artifact_node)

    # Flow
    workflow.set_entry_point("generate")
    workflow.add_edge("generate", "explain")
    workflow.add_edge("explain", "toxicity")
    workflow.add_edge("toxicity", "hallucination")
    workflow.add_edge("hallucination", "artifact")
    workflow.add_edge("artifact", END)


    return workflow.compile()
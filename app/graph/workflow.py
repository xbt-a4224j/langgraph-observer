from langgraph.graph import StateGraph, END
from .state import GraphState
from .nodes import llm_generate_node, explanation_node, artifact_node
from .evaluation import evaluate_output

def build_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("generate", llm_generate_node)
    workflow.add_node("evaluate", evaluate_output)
    workflow.add_node("explain", explanation_node)
    workflow.add_node("artifact", artifact_node)

    workflow.set_entry_point("generate")

    workflow.add_edge("generate", "evaluate")
    workflow.add_edge("evaluate", "explain")
    workflow.add_edge("explain", "artifact")
    workflow.add_edge("artifact", END)

    return workflow.compile()
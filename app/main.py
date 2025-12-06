# app/main.py

from pprint import pprint

from app.services.llm_service import LLMService
from app.domain.workflow_graph import build_graph

def run_example():
    """
    Quick entrypoint for local dev + debugging.

    Run this file directly from PyCharm:
        Right-click -> Run 'main'
    """

    # Build the graph
    graph = build_graph()
    print(graph.nodes)

    # Create initial dict-based state (required by LangGraph)
    state = {"user_input": "Hello from the refactor!"}

    # Execute the workflow
    result_state = graph.invoke(state)

    print("\n=== LangGraph Refactored Demo Output =====================")
    pprint(result_state)
    print("===========================================================\n")


if __name__ == "__main__":
    run_example()
from langgraph.graph import StateGraph, END
from typing import TypedDict


# ---- State Definition ----
class MyState(TypedDict):
    message: str


# ---- Node Definition ----
def add_exclamation(state: MyState):
    msg = state["message"] + "!"
    return {"message": msg}


# ---- Build Graph ----
def build_graph():
    graph = StateGraph(MyState)
    graph.add_node("exclaim", add_exclamation)
    graph.set_entry_point("exclaim")
    graph.add_edge("exclaim", END)
    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    output = app.invoke({"message": "Hello"})
    print(output)
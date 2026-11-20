# importing the lib
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

# State
class State(TypedDict):
    graph_str:str

# node
def greeting(state: State) -> State:
    """function takes a dict and return a dict with greeting"""
    return {"graph_str": state["graph_str"]+" welcome to AI Career Lab!"}

# edges

# putting our graph togther
builder = StateGraph(State)

builder.add_node("greeting", greeting)

builder.add_edge(START, "greeting")
builder.add_edge("greeting", END)

graph = builder.compile()

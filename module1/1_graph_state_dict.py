# importing the lib
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

# State
class State(TypedDict):
    graph_str:str

# node: make sure input and output following State type
def greeting(state: State) -> State:
    """function takes a dict and returns a dict with the greeting message"""
    return {"graph_str": state["graph_str"] + " welcome to AI Career Lab!"}

# edges

# putting our graph togther
builder = StateGraph(State)

builder.add_node("greeting", greeting)

builder.add_edge(START, "greeting")
builder.add_edge("greeting", END)

# Compile graph
graph = builder.compile()

# print(graph.invoke({"graph_str": "hey am new!"}))

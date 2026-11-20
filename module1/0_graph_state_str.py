# importing our lib
from langgraph.graph import END, START, StateGraph

# State


# nodes
def greeting(state: str) -> str:
    """this function greets people to ACL"""
    return state + " welcome to AI Career Lab!"


# edges

# langGraph putting our graph together
builder = StateGraph(str)

# add nodes to our graph
builder.add_node("greeting", greeting)

# add edges
builder.add_edge(START, "greeting")
builder.add_edge("greeting", END)

# Compile graph
graph = builder.compile()

# print(graph.invoke("hey am new!"))

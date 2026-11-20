from typing import Literal, NotRequired

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

load_dotenv()


# State: NotRequired indicates optional field
class State(TypedDict):
    graph_int: NotRequired[int]
    graph_str: str


model_llm = ChatOpenAI(model="gpt-4o", temperature=0.7, max_tokens=1000)


# nodes
def node1(state: State) -> State:
    """take a state and ask our model to pick a number between 1, 2, or 3"""
    model_response = model_llm.invoke(
        "choose between 1 or 3 or 2,  reply only with a number"
    )

    try:
        graph_int = int(model_response.content)
    except ValueError:
        graph_int = 0
    return {
        "graph_int": graph_int,
        "graph_str": state["graph_str"] + "passed by node 1",
    }


def node2(state: State) -> State:
    return {
        "graph_int": state["graph_int"],
        "graph_str": state["graph_str"] + "passed by node 2",
    }


def node3(state: State) -> State:
    return {
        "graph_int": state["graph_int"],
        "graph_str": state["graph_str"] + "passed by node 3",
    }


# create edges
def next_step(state: State) -> Literal["node2", "node3", END]:
    """check state and return which node to go"""
    number_state = state["graph_int"]
    if number_state == 2:
        return "node2"
    elif number_state == 3:
        return "node3"
    else:
        return END


# building graph
builder = StateGraph(State)

builder.add_node("node1", node1)
builder.add_node("node2", node2)
builder.add_node("node3", node3)

builder.add_edge(START, "node1")
builder.add_conditional_edges("node1", next_step)
builder.add_edge("node2", END)
builder.add_edge("node3", END)

# Compile graph
graph = builder.compile()

print(graph.invoke({"graph_str": "Hello, I am new!"}))
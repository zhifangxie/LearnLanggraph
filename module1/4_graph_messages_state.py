# check Mural for Messages state explenation

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph

"""
# state 
class MessagesState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
"""
model_llm = ChatOpenAI(model="gpt-4o")


# nodes
def chat(state: MessagesState) -> MessagesState:
    return {"messages": [model_llm.invoke(state["messages"])]}


# edges

# create our graph
builder = StateGraph(MessagesState)

builder.add_node("chat", chat)

builder.add_edge(START, "chat")
builder.add_edge("chat", END)

graph = builder.compile()

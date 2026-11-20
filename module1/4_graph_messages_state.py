# check Mural for Messages state explenation

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages

from typing import Annotated, List
from typing_extensions import TypedDict

from dotenv import load_dotenv
load_dotenv()

# state: add_messages merges current messages with new messages
class MessagesState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]

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

# Compile graph
graph = builder.compile()


messages = graph.invoke({"messages": [
    SystemMessage(content="You are a Python assistant."),
    HumanMessage(content="What is 2 + 2?")
    ]})
print(messages["messages"][-1].content)  # should print "4"
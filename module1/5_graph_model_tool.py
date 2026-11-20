from dotenv import load_dotenv
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

model_llm = ChatOpenAI(model="gpt-4o")


# Functional docstring: the tool's description that gets sent to the LLM so it knows when and how to call the tool.
@tool
def multiply(nb1: int, nb2: int) -> int:
    """This tool is used for multiplying 2 numbers and returning the product"""
    return nb1 * nb2

# Bind the tool to the LLM so that it can call the tool when needed. 
# The LLM will decide when to call the tool based on the input it receives and the tool's description.
model_llm_with_tool = model_llm.bind_tools([multiply])


# nodes
def chat_with_tool(state: MessagesState) -> MessagesState:
    return {"messages": [model_llm_with_tool.invoke(state["messages"])]}


builder = StateGraph(MessagesState)

builder.add_node("chat_with_tool", chat_with_tool)

builder.add_edge(START, "chat_with_tool")
builder.add_edge("chat_with_tool", END)

graph = builder.compile()

messages = graph.invoke({"messages": [
    SystemMessage(content="You are a Python assistant."),
    HumanMessage(content="What is 2 * 2?")
]})

# .tool_calls returns a list of tool_calls
# print tool_call details including the tool name, arguments, id and type.
print(messages["messages"][-1].tool_calls[0]) # print tool_call details in dict form: {'name': 'multiply', 'args': {'nb1': 2, 'nb2': 2}, 'id': 'call_sR0YRjlcy1tKKizD7aRPtudA', 'type': 'tool_call'}

print(messages["messages"][-1].content)  # Empty string
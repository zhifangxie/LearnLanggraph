from dotenv import load_dotenv
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, SystemMessage

from langgraph.prebuilt import ToolNode, tools_condition

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

# Tool node appends a ToolMessage with the tool's response (content) and tool's name, id and tool_call_id
builder.add_node("tools", ToolNode([multiply]))

builder.add_edge(START, "chat_with_tool")
# Conditional edges: if the LLM requests a tool, go to the tool node; otherwise, go to the end node.
builder.add_conditional_edges("chat_with_tool", tools_condition)
builder.add_edge("tools", END)

graph = builder.compile()

messages = graph.invoke({"messages": [
    SystemMessage(content="You are a Python assistant."),
    HumanMessage(content="What is 2 * 2?")
]})

print(messages["messages"][-1].content)  # should print "4"

"""
def tool_node(state: MessagesState) -> MessagesState:
    last_message = state["messages"][-1]
    tool_call = last_message.tool_calls[0]
    response = multiply.invoke(tool_call["args"])

    return {"messages": [ToolMessage(content=str(response),
                                      tool_call_id=tool_call["id"])]}


# creating conditional edges logic
def should_continue(state: MessagesState) -> Literal["tool_node", END]:

    last_message = state["messages"][-1]

    # Did the LLM request a tool?
    if last_message.tool_calls:
        return "tool_node"

    return END
"""

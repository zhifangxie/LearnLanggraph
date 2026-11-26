# check mural for explenation
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

model_llm = ChatOpenAI(model="gpt-4o")


@tool
def multiply(nb1: int, nb2: int) -> int:
    """this tool return the multiplication of 2 numbers"""
    return nb1 * nb2


@tool
def addition(nb1: int, nb2: int) -> int:
    """this tool return the sum of 2 numbers"""
    return nb1 + nb2


@tool
def subtraction(nb1: int, nb2: int) -> int:
    """this tool return the subtaction of 2 numbers"""
    return nb1 - nb2


model_llm_with_tools = model_llm.bind_tools([multiply, addition, subtraction])

system_message = SystemMessage(content="you are a helpful Math teach")


# nodes
def chat_with_tools(state: MessagesState) -> MessagesState:
    return {
        "messages": [model_llm_with_tools.invoke(state["messages"] + [system_message])]
    }


builder = StateGraph(MessagesState)
# In case of multiple tools, the LLM may generate an AI message with multiple tool calls 
builder.add_node("chat_with_tools", chat_with_tools)
# Each tool call generates a ToolMessage, and ToolMessages are appended in order of the tool calls
builder.add_node("tools", ToolNode([multiply, addition, subtraction]))

# START -> chat_with_tools -> (tools_condition) -> tools -> chat_with_tools -> ...
#                           => END
builder.add_edge(START, "chat_with_tools")
builder.add_conditional_edges("chat_with_tools", tools_condition)
builder.add_edge("tools", "chat_with_tools")

# graph = builder.compile()

# Initialize a memory saver to store the state of the graph
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Specify a thread
config = {"configurable": {"thread_id": "1"}}

# Specify an input
messages = [HumanMessage(content="Add 3 and 4.")]

# Run - NEED to provide the config to ensure the state is saved in the correct thread
response = graph.invoke({"messages": messages}, config)
print(response["messages"][-1].content)

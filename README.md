# LangGraph ACL Crash Course

> A small, beginner-friendly LangGraph learning repo from AI Career Lab. Each numbered file introduces one concept at a time, from the simplest possible graph to tool-calling agents with memory.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Learning%20Graphs-1C3C3C)](https://www.langchain.com/langgraph)
[![LangChain](https://img.shields.io/badge/LangChain-Tools%20%2B%20Models-1C3C3C)](https://www.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-ChatOpenAI-412991?logo=openai&logoColor=white)](https://platform.openai.com/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-DE5FE9)](https://docs.astral.sh/uv/)

---

## What Is This?

This repository is a hands-on crash course for refreshing the core ideas behind **LangGraph**:

- how state moves through a graph
- how nodes transform that state
- how edges and conditional routing control flow
- how to use `MessagesState` for chat-style applications
- how models request tools
- how `ToolNode` executes tool calls
- how to build a simple agent loop
- how checkpoint memory keeps conversation state by thread

The project is intentionally small. Instead of hiding concepts inside a large app, every file in `module1/` focuses on one idea so you can read, run, tweak, and compare the examples quickly.

---

## Learning Path

Work through the files in order:

| File | Concept | What It Demonstrates |
|---|---|---|
| `module1/0_graph_state_str.py` | Minimal graph | A graph whose state is just a plain string |
| `module1/1_graph_state_dict.py` | Typed state | A `TypedDict` state object with a single field |
| `module1/2_graph_conditional_edge.py` | Conditional edges | Routing to different nodes based on state |
| `module1/3_graph_introduction_model.py` | LLM-driven routing | Calling `ChatOpenAI` inside a node and routing from the result |
| `module1/4_graph_messages_state.py` | Message state | Using LangGraph's built-in `MessagesState` for chat messages |
| `module1/5_graph_model_tool.py` | Tool binding | Binding a Python tool to a chat model so the model can request it |
| `module1/6_graph_tool_call.py` | Tool execution | Running model-requested tools through `ToolNode` and `tools_condition` |
| `module1/8_graph_agent.py` | Agent loop | A math assistant that loops between model and tools until it can answer |
| `module1/9_graph_agent_memory.py` | Checkpoint memory | Adding `MemorySaver` so graph state can persist by `thread_id` |
| `main.py` | Scratch example | A compact weather-tool graph using `ToolNode` and conditional routing |

The configured LangGraph API graphs are listed in `langgraph.json`.

---

## Architecture

```text
User input
   |
   v
StateGraph
   |
   +-- node function
   |     transforms state or calls a model
   |
   +-- edge / conditional edge
   |     decides where the state goes next
   |
   +-- optional ToolNode
   |     executes tool calls requested by the model
   |
   v
Compiled graph
   |
   v
Final state
```

For the agent examples, the flow becomes:

```text
MessagesState
   -> chat model with bound tools
   -> tools_condition
      -> ToolNode
      -> chat model again
   -> final assistant message
```

---

## Project Structure

```text
LangGraph_ACL/
|
+-- module1/
|   +-- 0_graph_state_str.py
|   +-- 1_graph_state_dict.py
|   +-- 2_graph_conditional_edge.py
|   +-- 3_graph_introduction_model.py
|   +-- 4_graph_messages_state.py
|   +-- 5_graph_model_tool.py
|   +-- 6_graph_tool_call.py
|   +-- 8_graph_agent.py
|   `-- 9_graph_agent_memory.py
|
+-- main.py              # Additional graph scratchpad
+-- langgraph.json       # LangGraph API / Studio graph registry
+-- pyproject.toml       # Project metadata and dependencies
+-- uv.lock              # Locked dependency graph
+-- .python-version      # Python version hint
+-- .env.example         # Template for local environment variables
+-- .gitignore
`-- README.md
```

---

## Getting Started

### Prerequisites

| Requirement | Notes |
|---|---|
| Python 3.12+ | Required by `pyproject.toml` |
| `uv` | Used for dependency installation and command execution |
| OpenAI API key | Required for examples that call `ChatOpenAI` |

Check your local versions:

```bash
python --version
uv --version
```

If `uv` is not installed:

```bash
pip install uv
```

### 1. Clone The Repository

```bash
git clone https://github.com/<your-username>/LangGraph_ACL.git
cd LangGraph_ACL
```

### 2. Install Dependencies

```bash
uv sync
```

This creates a virtual environment and installs the dependencies pinned in `uv.lock`.

### 3. Configure Environment Variables

Create a local `.env` file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Keep `.env` private. It is ignored by Git and should never be committed.

---

## Running The Examples

### Run A No-API Example

The first examples do not need an API key because they do not call a model.

```bash
uv run python -c "import importlib; graph = importlib.import_module('module1.0_graph_state_str').graph; print(graph.invoke('hey, I am new! '))"
```

Expected shape:

```text
hey, I am new! welcome to AI Career Lab!
```

### Run A Typed State Example

```bash
uv run python -c "import importlib; graph = importlib.import_module('module1.1_graph_state_dict').graph; print(graph.invoke({'graph_str': 'hello'}))"
```

### Run With LangGraph Dev

The repo includes a `langgraph.json` file so you can inspect registered graphs with the LangGraph development server:

```bash
uv run langgraph dev
```

Then open the local URL printed by the CLI. The registered graphs are:

- `0_graph`
- `1_graph`
- `2_graph`
- `3_graph`
- `4_graph`
- `5_graph`
- `6_graph`
- `8_graph`

### Run Model And Tool Examples

Examples `3` and above use `ChatOpenAI`, so make sure `OPENAI_API_KEY` is set in `.env`.

The tool-calling examples are easiest to explore through LangGraph Dev, but you can also import a graph directly:

```bash
uv run python -c "import importlib; from langchain_core.messages import HumanMessage; graph = importlib.import_module('module1.8_graph_agent').graph; result = graph.invoke({'messages': [HumanMessage(content='What is 12 multiplied by 7?')]}); print(result['messages'][-1].content)"
```

---

## Key Concepts

### State

State is the data that moves through a graph. In the early examples, the state starts as a string and then becomes a `TypedDict`.

### Nodes

Nodes are normal Python functions. A node receives the current state and returns an update.

### Edges

Edges define the path between nodes. A standard edge always goes to the same next node; a conditional edge chooses the next node dynamically.

### MessagesState

`MessagesState` is a prebuilt state shape for chat applications. It stores a list of messages and automatically appends new messages through LangGraph's message reducer.

### Tools

Tools are Python functions decorated with `@tool`. A model can request a tool call after the tool is bound with `model.bind_tools(...)`.

### ToolNode

`ToolNode` executes tool calls from the latest AI message and appends the tool result back into the message state.

### Agent Loop

An agent loop lets the model call tools, receive results, and continue reasoning until it returns a final response.

### Memory

Checkpointing saves graph state across turns. `MemorySaver` is an in-memory checkpointer, useful for learning and local demos.

---

## Suggested Exercises

1. Change the greeting in `0_graph_state_str.py`.
2. Add another field to the `State` type in `1_graph_state_dict.py`.
3. Update the routing condition in `2_graph_conditional_edge.py`.
4. Make the model in `3_graph_introduction_model.py` choose from more branches.
5. Add a division tool to `8_graph_agent.py`.
6. Register `9_graph_agent_memory.py` in `langgraph.json`.
7. Replace `MemorySaver` with a persistent checkpointer.
8. Add tests that invoke each graph with a small input.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `OPENAI_API_KEY` is missing | Add it to `.env` or export it in your shell |
| `ModuleNotFoundError` | Run `uv sync` from the project root |
| `langgraph` command not found | Run commands through `uv run`, for example `uv run langgraph dev` |
| Model examples fail | Confirm your API key is valid and has access to the selected model |
| Tool examples stop after a tool result | Compare `5_graph_model_tool.py`, `6_graph_tool_call.py`, and `8_graph_agent.py` to see how the loop changes |

---

## Why This Repo Is Useful

LangGraph can feel abstract at first because agents, tools, routing, and memory often appear together in finished examples. This repo separates those ideas into small steps.

Use it as a reference when you need to remember:

- how to define state
- how to add nodes and edges
- how conditional routing works
- how messages accumulate
- how tool calls move through a graph
- how an agent keeps looping until it has enough information

---

## Security Notes

- Do not commit `.env` or real API keys.
- Rotate keys immediately if they are accidentally pushed to GitHub.
- Treat model outputs as generated suggestions, not guaranteed facts.

---

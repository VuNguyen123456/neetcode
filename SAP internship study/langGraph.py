### LangGraph
# my-agent-project/
# ├── .env
# ├── requirements.txt            # langgraph, langchain-openai, etc.
# ├── main.py                      # entry point
# ├── config.py                    # llm setup (same as before)
# ├── state.py                     # defines the shared State shape
# ├── nodes/
# │   ├── __init__.py
# │   ├── fetch_account.py         # one function = one node
# │   ├── search_transactions.py
# │   └── generate_answer.py
# ├── graph.py                     # builds and compiles the graph
# └── tools/
#     └── account_tools.py         # same @tool functions, reused here too

# How it connect

# state.py — the shape of data flowing through every node (a json)
# One object that every node reads from and writes back to as it moves through the graph

from typing import TypedDict

class AgentState(TypedDict):
    question: str
    account_id: str
    account_data: dict
    transactions: list
    answer: str

# nodes/fetch_account.py — one node, one job
from tools.account_tools import get_account_balance
from state import AgentState

def fetch_account(state: AgentState) -> AgentState:
    balance = get_account_balance.invoke({"account_id": state["account_id"]})
    state["account_data"] = {"balance": balance}
    return state

# nodes/generate_answer.py
from config import llm
from state import AgentState

def generate_answer(state: AgentState) -> AgentState:
    prompt = f"Account balance: {state['account_data']}. Answer: {state['question']}"
    response = llm.invoke(prompt)
    state["answer"] = response.content
    return state

# graph.py — where the actual graph gets assembled
from langgraph.graph import StateGraph, END
from state import AgentState
from nodes.fetch_account import fetch_account
from nodes.generate_answer import generate_answer

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("fetch_account", fetch_account)
    graph.add_node("generate_answer", generate_answer)

    graph.set_entry_point("fetch_account")
    graph.add_edge("fetch_account", "generate_answer")
    graph.add_edge("generate_answer", END)

    # in graph.py
    graph.add_conditional_edges(
        "fetch_account",
        route_after_fetch,
        {
            "flag_overdraft": "handle_overdraft",
            "generate_answer": "generate_answer",
        }
    )

    return graph.compile()

app_graph = build_graph()

# main.py — entry point, same role as before
from graph import app_graph

if __name__ == "__main__":
    result = app_graph.invoke({
        "question": "What's the account balance?",
        "account_id": "42",
        "account_data": {},
        "transactions": [],
        "answer": "",
    })
    print(result["answer"])

# Adding a branching node — where LangGraph actually earns its keep
# nodes/router.py
def route_after_fetch(state: AgentState) -> str:
    if state["account_data"]["balance"] < 0:
        return "flag_overdraft"
    return "generate_answer"

# A node in LangGraph have tools and prompt (all that stuff too)
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from config import llm

# this @tool is 100% LangChain — nothing LangGraph-specific about it
@tool
def get_account_balance(account_id: str) -> float:
    """Look up account balance."""
    return 5000.00

# this prompt template is also 100% LangChain
lookup_prompt = ChatPromptTemplate.from_messages([
    ("system", "Decide if you need to look up account info."),
    ("human", "{question}")
])

llm_with_tools = llm.bind_tools([get_account_balance])  # also LangChain

# NOW we wrap it in a node — this part is LangGraph
def smart_lookup_node(state: AgentState) -> AgentState:
    formatted_prompt = lookup_prompt.invoke({"question": state["question"]})
    response = llm_with_tools.invoke(formatted_prompt)
    state["tool_calls"] = response.tool_calls
    return state

# Differ from LangChain is:

# AgentExecutor: you don't write the loop, it's baked in
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": "..."})  # loop happens invisibly inside

# LangGraph: you write every step of the loop yourself
graph.add_node("search", search_node)
graph.add_conditional_edges(
    "search",
    lambda state: "search" if len(state["results"]) < 3 else "answer",
    {"search": "search", "answer": "generate_answer"}  # loop back to itself
)

@ Quiz
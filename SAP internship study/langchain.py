### LangChain:
# LangChain is the older, broader toolkit — 
# mostly for wiring together prompts, models, and tools in a mostly linear pipeline 
# (prompt → model → parse output → maybe call a tool → done). Good for simpler chains.

# This is just PROMPT IN -> TEXT OUT, no agentic reasoning or tool use.
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o")

response = llm.invoke([HumanMessage(content="What is revenue recognition?")])
print(response.content)

# The usual way to structure prompt
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that explains SQL queries."),
    ("human", "{question}")
])

chain = prompt | llm  # the "|" pipes prompt into model so it behave accordingly

response = chain.invoke({"question": "What does GROUP BY do?"}) # Asking what you want to know
print(response.content)

# Giving the model tools - this is where agentic start (not just prompt and agent anymore)
from langchain_core.tools import tool

# They are just function that do stuff and give your model the output after model call them for something
# The model decides which tool to call and with what arguments — it doesn't execute the function itself.
@tool
def get_account_balance(account_id: str) -> float:
    """Look up the balance for a given account ID."""
    # pretend database call
    return 5000.00

@tool
def search_transactions(account_id: str, keyword: str) -> list:
    """Search transactions for an account matching a keyword."""
    return ["Payment to Acme Corp - $500"]

tools = [get_account_balance, search_transactions]
llm_with_tools = llm.bind_tools(tools)

response = llm_with_tools.invoke("What's the balance for account 42?")
print(response.tool_calls)
# model decides to call get_account_balance, doesn't run it itself —
# you get back which tool it wants + what arguments to use

# Full agent loop:
from langchain.agents import create_tool_calling_agent, AgentExecutor

agent = create_tool_calling_agent(llm, tools, prompt) # Give the agent the model, the tools you have, prompt you made for it
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = executor.invoke({"input": "What's account 42's balance, then search its transactions for Acme"})
print(result["output"])

# Quick Quiz:
# 1.
chain = prompt | llm
response = chain.invoke({"question": "What is a foreign key?"})
# => This chain the llm model with prompt so that llm model consider the prompt before answering question
# 2.
@tool
def get_order_history(customer_id: str) -> list:
    """Get order history for a customer."""
    return db.query(...)

# 3. No you have to give the tools to the model
# 4. AgentExecutor runs the full loop automatically
# lets the model decide whether to call another tool or give a final answer, and repeats that cycle until the model says it's done.

# my-agent-project/
# ├── .env                      # API keys (OPENAI_API_KEY, etc.) — never committed to git
# ├── requirements.txt           # langchain, langchain-openai, python-dotenv, etc.
# ├── main.py                    # entry point — where you actually run things
# ├── config.py                  # loads env vars, model settings
# ├── prompts/
# │   └── templates.py           # ChatPromptTemplate definitions
# ├── tools/
# │   ├── __init__.py
# │   ├── account_tools.py       # @tool functions for account lookups
# │   └── transaction_tools.py   # @tool functions for transaction search
# ├── chains/
# │   └── qa_chain.py            # simple prompt|llm chains
# ├── agents/
# │   └── account_agent.py       # AgentExecutor setup, combines tools + prompt
# └── db/
#     └── connection.py          # actual database connection logic tools call into

### config.py — centralizes setup so you're not repeating it everywhere
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()  # reads .env file into environment variables

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

### tools/account_tools.py — the actual tool functions
from langchain_core.tools import tool
from db.connection import get_db_connection

@tool
def get_account_balance(account_id: str) -> float:
    """Look up the balance for a given account ID."""
    conn = get_db_connection()
    result = conn.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    return result.fetchone()[0]

### prompts/templates.py — prompt templates kept separate from logic
from langchain_core.prompts import ChatPromptTemplate

account_agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant for account inquiries."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),  # required for tool-calling agents
])

### agents/account_agent.py — wires tools + prompt + model together
from langchain.agents import create_tool_calling_agent, AgentExecutor
from config import llm
from prompts.templates import account_agent_prompt
from tools.account_tools import get_account_balance
from tools.transaction_tools import search_transactions

tools = [get_account_balance, search_transactions]

agent = create_tool_calling_agent(llm, tools, account_agent_prompt)
account_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

### main.py — the actual entry point, same role as React's index.js
from agents.account_agent import account_executor

if __name__ == "__main__":
    result = account_executor.invoke({
        "input": "What's the balance for account 42?"
    })
    print(result["output"])
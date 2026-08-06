# Normal LLM call: Only generate text. ( prompt in → text out )
# Agentic AI agent: Think, reason, use tools, and generate answers. (Prompt in → Plan → Search → Answer out)
# Framework like LangChain, LangGraph allow you to hand code this loop

# RAG: RAG (Retrieval-Augmented Generation) is about grounding answers in real data
# before the model answers, you retrieve relevant documents (via a vector database/embeddings search)
# and stuff them into the prompt, so the model isn't just guessing from training data.
# it's not necessarily "agentic" by itself unless the model is also deciding when and what to retrieve, 
# and looping based on results.

# Rough LangGraph shape — nodes and edges, not exact syntax
graph = StateGraph()
graph.add_node("plan", plan_step)
graph.add_node("search", search_tool)
graph.add_node("answer", generate_answer)

graph.add_edge("plan", "search")
graph.add_conditional_edges("search", should_continue, {"yes": "search", "no": "answer"})


### LangGraph:
# LangGraph is built for the harder case: when the agent's path isn't linear
# it might loop, backtrack, branch based on conditions, or run multiple steps 
# that depend on each other in a graph rather than a straight line.
# You model the whole thing as a state machine/graph of nodes (each node = a step) 
# and edges (what happens next based on the result).


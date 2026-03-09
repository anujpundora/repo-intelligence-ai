from app.indexing.vector_store import query_chunks
from app.llm.llm_router import LLMRouter

llm = LLMRouter()


def planner_agent(task: str):

    print("\nPlanner received task:", task)

    # Retrieve relevant code
    results = query_chunks(task)

    context_chunks = results["documents"][0]

    context = "\n\n".join(context_chunks[:3])

    prompt = f"""
You are a software analysis planner.

Task:
{task}

Relevant code context:
{context}

Based on the task and code context, decide which analysis agent should handle it.

Available agents:
- Bug Agent
- Security Agent
- Performance Agent

Return only the agent name.
"""

    decision = llm.generate(prompt)

    return decision
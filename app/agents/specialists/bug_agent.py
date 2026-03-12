from app.llm.llm_router import LLMRouter
from app.agents.tools import run_tool

llm = LLMRouter()


def bug_agent(code_chunks, max_steps=3):

    history = []
    observations = []

    for step in range(max_steps):

        code_preview = "\n\n".join(code_chunks[:3])

        prompt = f"""
You are a Specialized bug detection agent.

Previous actions:
{history}

Observations:
{observations}

Code:
{code_preview}

Tools:
- query_chunks
- analyze_bug
- finish

Return JSON:
{{"tool": "query_chunks"}}
{{"tool": "analyze_bug"}}
{{"tool": "finish"}}
"""

        response = llm.generate(prompt)

        if "query_chunks" in response:

            result = run_tool("query_chunks", ["logic bug code"])

            code_chunks.extend(result)

            observations.append("Retrieved additional code")

            history.append("query_chunks")

        elif "analyze_bug" in response:

            result = llm.generate(f"Find bugs in this code:\n{code_preview}")

            observations.append(result)

            history.append("analyze_bug")

        elif "finish" in response:

            return observations[-1]

    return observations[-1] if observations else "No bugs detected."
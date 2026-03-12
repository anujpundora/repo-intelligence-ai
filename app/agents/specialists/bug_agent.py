import json
from app.llm.llm_router import LLMRouter
from app.analysis.bug_patterns import check_syntax
from app.analysis.bug_patterns import detect_infinite_loops

llm = LLMRouter()


TOOLS = {
    "check_syntax": check_syntax,
    "detect_infinite_loops": detect_infinite_loops
}


def bug_agent(code_chunks, max_steps=3):

    history = []
    observations = []

    code_context = "\n\n".join(code_chunks[:3])

    for step in range(max_steps):

        prompt = f"""
You are a bug detection agent.

Goal:
Find logical bugs in the provided code.

Code:
{code_context}

Previous actions:
{history}

Observations:
{observations}

Available tools:
- check_syntax
- detect_infinite_loops
- finish

Return JSON:

{{"tool":"check_syntax"}}
{{"tool":"detect_infinite_loops"}}
{{"tool":"finish"}}
"""

        response = llm.generate(prompt)

        decision = json.loads(response)
        tool = decision["tool"]

        if tool == "finish":
            return observations[-1] if observations else "No bugs found"

        result = TOOLS[tool](code_context)

        observations.append(result)
        history.append(tool)

    return observations[-1] if observations else "No bugs found"
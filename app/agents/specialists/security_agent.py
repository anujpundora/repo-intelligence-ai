import json
from app.llm.llm_router import LLMRouter
from app.analysis.security_patterns import (
    detect_sql_injection,
    detect_hardcoded_secrets,
    detect_command_injection
)

llm = LLMRouter()


TOOLS = {
    "detect_sql_injection": detect_sql_injection,
    "detect_hardcoded_secrets": detect_hardcoded_secrets,
    "detect_command_injection": detect_command_injection
}


def security_agent(code_chunks, max_steps=3):

    history = []
    observations = []

    code_context = "\n\n".join(code_chunks[:3])

    for step in range(max_steps):

        prompt = f"""
You are a security analysis agent.

Goal:
Find security vulnerabilities in the code.

Code:
{code_context}

Previous actions:
{history}

Observations:
{observations}

Available tools:
- detect_sql_injection
- detect_hardcoded_secrets
- detect_command_injection
- finish

Return JSON:

{{"tool":"detect_sql_injection"}}
{{"tool":"detect_hardcoded_secrets"}}
{{"tool":"detect_command_injection"}}
{{"tool":"finish"}}
"""

        response = llm.generate(prompt)

        decision = json.loads(response)
        tool = decision["tool"]

        if tool == "finish":
            return observations[-1] if observations else "No vulnerabilities found"

        result = TOOLS[tool](code_context)

        observations.append(result)
        history.append(tool)

    return observations[-1] if observations else "No vulnerabilities found"
from app.llm.llm_router import LLMRouter
from app.agents.tools import run_tool
llm = LLMRouter()


def security_agent(code_chunks, max_steps=3):

    history = []
    observations = []

    for step in range(max_steps):

        context_preview = "\n\n".join(code_chunks[:3])

        prompt = f"""
You are a security analysis agent.

Your task is to find vulnerabilities in the code.

Previous actions:
{history}

Observations:
{observations}

Code context:
{context_preview}

Available tools:
- query_chunks
- analyze_security
- finish

Rules:
- Use query_chunks if you need more context
- Use analyze_security to evaluate the code
- Finish when you are confident

Return JSON:
{{"tool": "query_chunks"}}
{{"tool": "analyze_security"}}
{{"tool": "finish"}}
"""

        response = llm.generate(prompt)

        if "query_chunks" in response:

            result = run_tool("query_chunks", ["security vulnerability code"])

            code_chunks.extend(result)

            observations.append("Retrieved more code")

            history.append("query_chunks")

        elif "analyze_security" in response:

            analysis_prompt = f"""
Analyze the following code for security vulnerabilities:

{context_preview}
"""

            result = llm.generate(analysis_prompt)

            observations.append(result)

            history.append("analyze_security")

        elif "finish" in response:

            return observations[-1]

    return observations[-1] if observations else "No vulnerabilities found."
import json
import re
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

#Helper function

def clean_llm_json(response: str):

    if not response:
        return ""

    # remove markdown code blocks
    response = re.sub(r"```json|```", "", response).strip()

    return response

def parse_llm_json(response):

        if not response:
            return None

        # find first JSON object
        match = re.search(r"\{.*?\}", response)

        if not match:
            return None

        try:
            return json.loads(match.group())
        except:
            return None
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

Return ONLY valid JSON.
Do not include explanations.
Do not include markdown.

Return ONLY ONE JSON object.
Do NOT return multiple tool calls.
{{"tool":"detect_sql_injection"}}
{{"tool":"detect_hardcoded_secrets"}}
{{"tool":"detect_command_injection"}}
{{"tool":"finish"}}
"""

        response = llm.generate(prompt)
        response = clean_llm_json(response)

        print("\n------ RAW LLM RESPONSE ------")
        print(response)
        print("------ END RESPONSE ------\n")

        if not response:
            return "LLM returned empty response"

        decision = parse_llm_json(response)

        if not decision:
            return "Agent failed to parse response"

        tool = decision.get("tool")


        # Fallback detection if model output wasn't perfect
        if "check_syntax" in response:
            tool = "check_syntax"

        elif "detect_infinite_loops" in response:
            tool = "detect_infinite_loops"

        elif "finish" in response:
            tool = "finish"


        # HANDLE FINISH FIRST
        if tool == "finish":

            if not observations:
                return "Code is safe!"

            if all(
                "no" in obs.lower() or "not detected" in obs.lower()
                for obs in observations
            ):
                return "Code is safe!"

            return "\n".join(observations)


        # TOOL VALIDATION
        if tool not in TOOLS:
            return f"Unknown tool: {tool}"


        # EXECUTE TOOL
        result = TOOLS[tool](code_context)

        observations.append(result)
        history.append(tool)


        return observations[-1] if observations else "No vulnerabilities found"
import json
import re
from app.llm.llm_router import LLMRouter
from app.analysis.security_patterns import (
    detect_sql_injection,
    detect_hardcoded_secrets,
    detect_command_injection
)
#Helper funtion to Finish
def is_safe(observations):
    return all(
        any(word in obs.lower() for word in ["no", "not detected", "safe"])
        for obs in observations
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
Select next tool from Available tools and Only return it in this format:
{{"tool": "<tool_name>"}}
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

        if "detect_sql_injection" in response:
            tool = "detect_sql_injection"

        elif "detect_hardcoded_secrets" in response:
            tool = "detect_hardcoded_secrets"

        elif "detect_command_injection" in response:
            tool = "detect_command_injection"

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


        #Avoiding Repeated Tool Usage
        if tool in history:
            print("Skipping repeated tool")
            continue
        # TOOL VALIDATION
        if tool not in TOOLS:
            return f"Unknown tool: {tool}"


        # EXECUTE TOOL
        result = TOOLS[tool](code_chunks)

        observations.append(result)
        history.append(tool)

    if not observations or is_safe(observations):
        return "Code is safe!"

    return "\n".join(observations)

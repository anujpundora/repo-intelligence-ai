import json
import re
from app.llm.llm_router import LLMRouter
from app.analysis.bug_patterns import check_syntax
from app.analysis.bug_patterns import detect_infinite_loops

llm = LLMRouter()


TOOLS = {
    "check_syntax": check_syntax,
    "detect_infinite_loops": detect_infinite_loops
}

#Helper function

def clean_llm_json(response: str):

    if not response:
        return ""

    # remove markdown code blocks
    response = re.sub(r"```json|```", "", response).strip()

    return response

#Parsing function to extract JSON object from LLM response
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

Return ONLY valid JSON.
Do not include explanations.
Do not include markdown.

STRICTILY Return ONLY One JSON object in the format:
{{"tool":"check_syntax"}}
{{"tool":"detect_infinite_loops"}}
{{"tool":"finish"}}
"""

        response = llm.generate(prompt)
        response = clean_llm_json(response)

        print("\n------ RAW LLM RESPONSE ------")
        print(response)
        print("------ END RESPONSE ------\n")

        if not response:
            return "LLM returned empty response"

        decision = parse_llm_json(response) or {}
        tool = decision.get("tool")

        # fallback if parsing failed
        if not decision:
            if "check_syntax" in response:
                tool = "check_syntax"
            elif "detect_infinite_loops" in response:
                tool = "detect_infinite_loops"
            elif "finish" in response:
                tool = "finish"
            else:
                return observations[-1] if observations else "No issues detected"
            
        else:
            tool = decision["tool"]
        result = TOOLS[tool](code_context)

        if tool == "finish":
            if not observations:
                    return "Code is safe!"

            if all(
                "No" in obs or "not detected" in obs.lower()
                for obs in observations
            ):
                return "Code is safe!"

            return "\n".join(observations)


        if tool not in TOOLS:
            return f"Unknown tool: {tool}"

        result = TOOLS[tool](code_context)

        observations.append(result)
        history.append(tool)

        observations.append(result)
        history.append(tool)

        if history and tool == history[-1]:
            return observations[-1]
    return observations[-1] if observations else "No bugs found"
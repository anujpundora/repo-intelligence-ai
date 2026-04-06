import re
import json

from typer.cli import state
from app.llm.llm_router import LLMRouter
from app.agents.tools import run_tool
from app.agents.agent_state import AgentState
from app.agents.specialists.reflection_agent import reflection_agent
from app.agents.specialists.fix_agent import fix_agent

llm = LLMRouter()
#Helper function to extract JSON object from LLM response
def extract_json(text):
                match = re.search(r"\{.*?\}", text, re.DOTALL)
                if not match:
                    raise ValueError("No JSON found in LLM response")
                return json.loads(match.group())

#Helper function to extract first JSON object from text (for cases where LLM may return multiple JSON objects or text)
def extract_first_json(text):
    matches = re.findall(r'\{.*?\}', text)

    for m in matches:
        try:
            return json.loads(m)
        except:
            continue

    return None

#Helper function to clean LLM responses that may include """ formatting
def clean_llm_json(response: str):

    response = response.strip()

    if response.startswith("```"):
        response = response.split("```")[1]

    response = response.replace("json", "").strip()

    return response

def planner_agent(task):

    state = AgentState(task)

    max_steps = 25

    retrieved_preview = state.context["retrieved_chunks"][:3]
    for step in range(max_steps):

        print(f"\nStep {step+1}")

        prompt = f"""
You are an autonomous software repository analysis agent.

Your goal is to analyze the repository and detect:
- security vulnerabilities
- logical bugs

Task:
{state.task}

Previous actions:
{state.history}

Recent observations:
{state.observations[-2:]}

Retrieved code preview:
{retrieved_preview}


Available tools:
- query_chunks
- security_agent
- bug_agent
- reflection_agent
- fix_agent
- finish

STRICT WORKFLOW:

1. If no code retrieved → query_chunks
2. After retrieving code → security_agent
3. After security_agent → bug_agent
4. After bug_agent → reflection_agent
5. If issues exist → fix_agent
6. After fix_agent → finish

STATE:
Retrieved code count: {len(state.context["retrieved_chunks"])}
If this is greater than 0, DO NOT use query_chunks again.

CRITICAL OUTPUT RULES:

- You MUST return ONLY ONE JSON object
- DO NOT explain anything
- DO NOT return multiple JSON objects
- DO NOT include text before or after JSON
- DO NOT describe steps
- DO NOT return a list
- DO NOT simulate future steps

If you violate this, the system will fail.

Select next tool from Available tools and Only return it in this format:

{{"tool": "<tool_name>"}}
"""
        
        response = llm.generate(prompt)
        response = clean_llm_json(response)

        print("LLM response:", response)

        decision = extract_first_json(response)

        tool = decision.get("tool")
        tool_input = decision.get("input", "")
        valid_tools = [
            "query_chunks",
            "security_agent",
            "bug_agent",
            "reflection_agent",
            "fix_agent",
            "finish"
        ]

        if tool not in valid_tools:
            print("Invalid tool from LLM. Forcing fallback.")
            tool = "security_agent"
        # ---------- finish ----------
        if tool == "finish" and (
            state.context["security_findings"] or state.context["bug_findings"]
        ) and "fix_agent" not in state.history:
            
            print("Forcing fix step before finish")
            tool = "fix_agent"

        # ---------- prevent repeated retrieval ----------
        if tool == "query_chunks" and state.context["retrieved_chunks"]:
                print("Already have code. Forcing security analysis.")
                tool = "security_agent"
       # ---------- enforce workflow ----------
        if tool == "reflection_agent" and not (
            state.context["security_findings"] or state.context["bug_findings"]
        ):
            print("No issues found. Skipping fix.")
            tool = "finish"

        elif tool == "fix_agent" and not (
            state.context["security_findings"] or state.context["bug_findings"]
        ):
            print("No issues to fix. Skipping fix.")
            tool = "finish"
        # ---------- ensure code context ----------
        if tool in ["security_agent", "bug_agent"] and not state.context["retrieved_chunks"]:
            print("No code context available. Forcing retrieval.")
            tool = "query_chunks"

        # ---------- prepare arguments ----------
        if tool == "query_chunks":
            args = [state.task]

        elif tool in ["security_agent", "bug_agent"]:
            args = [state.context["retrieved_chunks"]]

        elif tool == "reflection_agent":
            args = [
                state.context["security_findings"],
                state.context["bug_findings"],
                state.context["retrieved_chunks"]
            ]
        elif tool == "fix_agent":
            result = fix_agent(
                state.context["security_findings"],
                state.context["bug_findings"],
                state.context["retrieved_chunks"]
            )

        else:
                result = run_tool(tool, args)


        # ---------- execute ----------
        if tool == "reflection_agent":
            result = reflection_agent(*args)

        elif tool == "fix_agent":
            state.context["fixes"] = result
     
        print("Observation:", str(result)[:200])

        if tool == "reflection_agent" and not (
            state.context["security_findings"] or state.context["bug_findings"]
        ):
            tool = "finish"
        elif tool == "fix_agent":

            result = fix_agent(
                state.context["security_findings"],
                state.context["bug_findings"],
                state.context["retrieved_chunks"]
            )
        # ---------- update memory ----------
        if tool == "query_chunks":
            state.context["retrieved_chunks"] = (
                state.context["retrieved_chunks"] + result
            )[:5]

        elif tool == "security_agent":
            state.context["security_findings"].append(result[:200])

        elif tool == "bug_agent":
            state.context["bug_findings"].append(result)

        state.history.append(tool)
        print("\n🔍 Final Report:\n")
        print(state.context.get("final_report", "No report"))

        print("\n🛠️ Suggested Fixes:\n")
        print(state.context.get("fixes", "No fixes"))
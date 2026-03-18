import re
import json
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
#Helper function to clean LLM responses that may include """ formatting
def clean_llm_json(response: str):

    response = response.strip()

    if response.startswith("```"):
        response = response.split("```")[1]

    response = response.replace("json", "").strip()

    return response

def planner_agent(task):

    state = AgentState(task)

    max_steps = 5

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
- finish

Workflow:

1. If no code retrieved → query_chunks
2. After retrieving code → security_agent
3. After security_agent → bug_agent
4. After bug_agent → reflection_agent
5. If issues exist → fix_agent
6. After fix_agent → finish

Rules:

- Never repeat the same tool twice.
- Use query_chunks only if no code has been retrieved.
- Security and bug agents automatically receive code context.
- Return exactly ONE JSON object.
- Do not include explanations.

Valid outputs:

{{"tool": "query_chunks"}}

{{"tool": "security_agent"}}

{{"tool": "bug_agent"}}

{{"tool": "finish"}}
"""
        
        response = llm.generate(prompt)
        response = clean_llm_json(response)

        print("LLM response:", response)

        decision = extract_json(response)

        tool = decision.get("tool")
        tool_input = decision.get("input", "")

        # ---------- finish ----------
        if tool == "finish":
            print("\nAgent finished")
            return "Analysis completed"

        # ---------- prevent repeated retrieval ----------
        if tool == "query_chunks" and state.history and state.history[-1] == "query_chunks":
            print("Code already retrieved. Switching to analysis.")
            tool = "security_agent"

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

        else:
            raise ValueError(f"Unknown tool: {tool}")

        # ---------- execute ----------
        if tool == "reflection_agent":
            result = reflection_agent(*args)

        else:
            result = run_tool(tool, args)

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
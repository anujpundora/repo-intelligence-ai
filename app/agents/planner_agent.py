import re
import json
from app.llm.llm_router import LLMRouter
from app.agents.tools import run_tool
from app.agents.agent_state import AgentState


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
- finish

Workflow rules:

1. If no code retrieved → use query_chunks
2. After retrieving code → you MUST run security_agent or bug_agent
3. Only finish AFTER at least one analysis tool has been executed
4. Never call query_chunks twice in a row

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
        tool = None
        tool_input = ""
        try:

            decision = extract_json(response)

            

            # finish action
            if tool == "finish":

                print("\nAgent finished:")
                print(decision["output"])
                return decision["output"]

            if tool in ["security_agent", "bug_agent"] and not state.context["retrieved_chunks"]:
                print("No code context available. Forcing retrieval.")
                tool = "query_chunks"
                args = ["authentication"]
                
            tool = decision.get("tool")

            if tool == "query_chunks":
                args = [state.task]

            elif tool in ["security_agent", "bug_agent"]:
                args = [state.context["retrieved_chunks"]]

            elif tool == "finish":
                return "Analysis completed"

            else:
                raise ValueError("Unknown tool")

            # prevent infinite loops
            if state.history and tool == state.history[-1]:
                print("Preventing repeated tool usage")
                if tool == "security_agent":
                    tool = "bug_agent"

                elif tool == "bug_agent":
                    tool = "finish"

                else:
                    break
            # prepare arguments
            if tool == "query_chunks" and state.context["retrieved_chunks"]:
                print("Code already retrieved. Switching to analysis.")
                tool = "security_agent"
            if tool == "query_chunks":
                args = [tool_input]

            elif tool in ["security_agent", "bug_agent"]:
                # ignore whatever the LLM sends
                args = [state.context["retrieved_chunks"]]

            else:
                args = []

            # execute tool
            result = run_tool(tool, args)

            # handle empty retrieval
            if tool == "query_chunks" and not result:
                print("No relevant chunks found.")
                continue

            # update shared memory
            if tool == "query_chunks":
                state.context["retrieved_chunks"] = (
                state.context["retrieved_chunks"] + result
                )[:5]

            if tool == "security_agent":
                #Will later add a summarizer instead of 200 cliping
                summary = result[:200]  # first 200 chars
                state.context["security_findings"].append(summary)

            if tool == "bug_agent":
                state.context["bug_findings"].append(result)

            #prevents direct finish without analysis
            if tool == "finish" and "security_agent" not in state.history and "bug_agent" not in state.history:
                print("Analysis not performed yet. Running security_agent.")
                tool = "security_agent"
            print("Observation:", str(result)[:200])

            state.add_step(tool, result)

        except Exception as e:

            print("Error:", e)
            break
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

    for step in range(max_steps):

        print(f"\nStep {step+1}")

        prompt = f"""
You are an autonomous software repository analysis agent.

Your job is to analyze a code repository and detect bugs or security vulnerabilities.

Task:
{state.task}

Previous actions:
{state.history}

Observations from tools:
{state.observations[-3:]}

Current retrieved code chunks:
{state.context["retrieved_chunks"][:2]}

Available tools:
- query_chunks
- security_agent
- bug_agent
- finish


TOOL DESCRIPTIONS:

query_chunks:
Retrieve relevant code snippets from the repository based on a query.

security_agent:
Analyze retrieved code for security vulnerabilities.

bug_agent:
Analyze retrieved code for logical errors or bugs.

Workflow rules:

1. If no code chunks exist → use query_chunks.
2. After retrieving code → analyze it with security_agent or bug_agent.
3. After security_agent finishes → run bug_agent.
4. After both analyses → use finish.
5. Do NOT call the same tool twice in a row.

STRICT JSON FORMAT

You MUST return exactly one JSON object.

Allowed outputs:

{{"tool": "query_chunks"}}
{{"tool": "security_agent"}}
{{"tool": "bug_agent"}}
{{"tool": "finish"}}

Do NOT include input.
Do NOT include code.
Do NOT include explanations.
Return only the JSON object.

1. If no code has been retrieved yet, you MUST call query_chunks first.
2. Never call security_agent or bug_agent if retrieved code chunks are empty.
3. After retrieving code, use security_agent or bug_agent to analyze it.
4. Do NOT call query_chunks repeatedly if relevant code has already been retrieved.
5. Do NOT call the same tool repeatedly.
6. Always choose the next logical step in the analysis process.
7. Return ONLY ONE JSON object.
8. Never include code snippets inside JSON output.
9. Specialist agents will receive code from the system context.


OUTPUT FORMAT (STRICT):

Tool usage:
{{
  "tool": "query_chunks",
  "input": "authentication login session"
}}

Security analysis:
{{
  "tool": "security_agent"
}}

Bug analysis:
{{
  "tool": "bug_agent"
}}

Finish task:
{{
  "tool": "finish",
  "output": "summary of findings"
}}

IMPORTANT:
- Return ONLY ONE JSON object.
- Do NOT include explanations.
- Do NOT return multiple tool calls.

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
                state.context["retrieved_chunks"].extend(result)

            if tool == "security_agent":
                state.context["security_findings"].append(result)

            if tool == "bug_agent":
                state.context["bug_findings"].append(result)

            print("Observation:", str(result)[:200])

            state.add_step(tool, result)

        except Exception as e:

            print("Error:", e)
            break
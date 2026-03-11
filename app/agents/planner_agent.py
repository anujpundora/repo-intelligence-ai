import json
from app.llm.llm_router import LLMRouter
from app.agents.tools import run_tool
from app.agents.agent_state import AgentState


llm = LLMRouter()

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
You are an autonomous software analysis agent.

Task:
{state.task}

Previous actions:
{state.history}

Observations:
{state.observations}

Available tools:
- query_chunks
- security_agent
- bug_agent
- finish

Tool descriptions:

query_chunks:
Retrieve relevant code chunks from the repository.

security_agent:
Analyze code for vulnerabilities.

bug_agent:
Analyze code for logical bugs.

Respond ONLY with raw JSON. Do not include markdown or backticks.

Tool usage format:
{{
  "tool": "query_chunks",
  "input": "authentication"
}}

Finish format:
{{
  "tool": "finish",
  "output": "final result"
}}
"""
        
        response = llm.generate(prompt)
        response = clean_llm_json(response)

        print("LLM response:", response)

        try:

            decision = json.loads(response)

            tool = decision["tool"]

            # finish action
            if tool == "finish":

                print("\nAgent finished:")
                print(decision["output"])

                return decision["output"]

            # get arguments safely
            args = decision.get("args", [])

            # inject shared context before execution
            if tool in ["security_agent", "bug_agent"]:

                args = [state.task, state.context["retrieved_chunks"]]

            # execute tool
            result = run_tool(tool, args)

            # update shared memory
            if tool == "query_chunks":

                documents = result.get("documents", [[]])[0]

                state.context["retrieved_chunks"].extend(documents)

            if tool == "security_agent":

                state.context["security_findings"].append(result)

            if tool == "bug_agent":

                state.context["bug_findings"].append(result)

            print("Observation:", str(result)[:200])

            state.add_step(tool, result)

        except Exception as e:

            print("Error:", e)
            break

    print("\nAgent stopped after max steps.")
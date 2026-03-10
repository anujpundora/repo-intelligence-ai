import json
from app.llm.llm_router import LLMRouter
from app.agents.tools import run_tool
from app.agents.agent_state import AgentState


llm = LLMRouter()


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
- finish

Respond ONLY in JSON format.

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

        print("LLM response:", response)

        try:

            decision = json.loads(response)

            tool = decision["tool"]

            if tool == "finish":

                print("\nAgent finished:")
                print(decision["output"])

                return decision["output"]

            tool_input = decision["input"]

            result = run_tool(tool, tool_input)

            print("Observation:", str(result)[:200])

            state.add_step(tool, result)

        except Exception as e:

            print("Error:", e)
            break

    print("\nAgent stopped after max steps.")
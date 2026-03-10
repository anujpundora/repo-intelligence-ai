from app.llm.llm_router import LLMRouter
from app.agents.tools import run_tool
from app.agents.agent_state import AgentState


llm = LLMRouter()


def planner_agent(task):

    state = AgentState(task)

    max_steps = 3

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

Use the tool to retrieve relevant code.

Return format:
tool_name | input
"""

        decision = llm.generate(prompt)

        print("Decision:", decision)

        try:

            tool_name, tool_input = decision.split("|")

            tool_name = tool_name.strip()
            tool_input = tool_input.strip()

            result = run_tool(tool_name, tool_input)

            print("Observation:", str(result)[:200])

            state.add_step(tool_name, result)

        except Exception as e:

            print("Error:", e)
            break

    return state
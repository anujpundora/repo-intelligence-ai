from app.agents.planner_agent import planner_agent


def main():

    task = "Check authentication code for security vulnerabilities"

    decision = planner_agent(task)

    print("\nPlanner Decision:\n")
    print(decision)


if __name__ == "__main__":
    main()
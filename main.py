from app.agents.planner_agent import planner_agent


def main():

    task = "Analyze authentication logic in the repository"

    planner_agent(task)


if __name__ == "__main__":
    main()
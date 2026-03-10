class AgentState:

    def __init__(self, task):

        self.task = task

        self.history = []
        self.observations = []

        # shared memory between agents
        self.context = {
            "retrieved_chunks": [],
            "security_findings": [],
            "bug_findings": [],
            "analysis_summary": []
        }

    def add_step(self, action, result):

        self.history.append(action)
        self.observations.append(str(result)[:500])
class AgentState:

    def __init__(self, task):

        self.task = task
        self.history = []
        self.observations = []

    def add_step(self, action, result):

        self.history.append(action)
        self.observations.append(str(result)[:500])
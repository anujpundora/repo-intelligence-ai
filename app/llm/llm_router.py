from app.llm import gemini_client, groq_client


class LLMRouter:

    def __init__(self, provider="gemini"):

        self.provider = provider

    def generate(self, prompt):

        if self.provider == "gemini":
            return gemini_client.generate(prompt)

        elif self.provider == "grok":
            return groq_client.generate(prompt)

        else:
            raise ValueError("Unsupported LLM provider")
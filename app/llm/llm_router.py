from app.llm import gemini_client, groq_client


class LLMRouter:

    def generate(self, prompt):

        try:
            print("Using Gemini")

            return gemini_client.generate(prompt)

        except Exception as e:

            print("Gemini failed, switching to Groq")

            return groq_client.generate(prompt)
from app.llm.llm_router import LLMRouter

if __name__ == "__main__":

    llm = LLMRouter(provider="grok")

    response = llm.generate("Explain SQL injection in simple terms")

    print(response)
from app.llm.llm_router import LLMRouter


def main():

    llm = LLMRouter()

    prompt = "Explain SQL injection in simple terms"

    response = llm.generate(prompt)

    print("\nLLM Response:\n")
    print(response)


if __name__ == "__main__":
    main()
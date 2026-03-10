from app.llm.llm_router import LLMRouter

llm = LLMRouter()


def bug_agent(code_chunk):

    prompt = f"""
You are a software debugging expert.

Analyze the following code for logical bugs or errors.

Code:
{code_chunk}

Return:
- bug description
- explanation
"""

    return llm.generate(prompt)
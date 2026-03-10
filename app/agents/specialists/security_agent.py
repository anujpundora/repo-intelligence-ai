from app.llm.llm_router import LLMRouter

llm = LLMRouter()


def security_agent(code_chunk):

    prompt = f"""
You are a security analysis agent.

Analyze the following code for security vulnerabilities.

Code:
{code_chunk}

Return:
- vulnerability
- explanation
- severity (low/medium/high)
"""

    return llm.generate(prompt)
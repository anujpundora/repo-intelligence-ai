from app.llm.llm_router import LLMRouter

llm = LLMRouter()


def security_agent(code_chunks):

    code_context = "\n\n---CODE CHUNK---\n\n".join(code_chunks[:3])

    prompt = f"""
You are a security analysis agent.

Analyze the following code for vulnerabilities.

Code:
{code_context}

Return:
- vulnerability
- explanation
- severity
"""

    return llm.generate(prompt)
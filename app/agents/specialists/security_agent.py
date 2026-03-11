from app.llm.llm_router import LLMRouter

llm = LLMRouter()


def security_agent(task, code_chunks):

    code_context = "\n\n".join(code_chunks[:5])

    prompt = f"""
You are a security analysis agent.

Task:
{task}

Code:
{code_context}

Find possible vulnerabilities.

Return:
- vulnerability
- explanation
- severity
"""

    return llm.generate(prompt)
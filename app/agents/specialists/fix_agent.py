from app.llm.llm_router import LLMRouter

llm = LLMRouter()

def fix_agent(security_findings, bug_findings, code_chunks):

    issues = "\n".join(security_findings + bug_findings)

    if not issues or "safe" in issues.lower():
        return "No fixes required. Code is safe."

    code_context = "\n\n".join(code_chunks[:2])

    prompt = f"""
You are a senior software engineer.

Issues detected:
{issues}

Code:
{code_context}

Your task:
Suggest minimal fixes for the issues.

Return in this format:

- Issue
- Fix suggestion (only the changed lines)
- Explanation

Do NOT rewrite full code.
Only suggest patches.
"""

    return llm.generate(prompt)
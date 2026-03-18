from app.llm.llm_router import LLMRouter

llm = LLMRouter()

def fix_agent(security_findings, bug_findings, code_chunks):

    issues = "\n".join(security_findings + bug_findings)

    if not issues or "safe" in issues.lower():
        return "No fixes required. Code is safe."

    code_context = "\n\n".join(code_chunks[:2])

    prompt = f"""
You are a senior software engineer.

The following issues were detected in the code:

Issues:
{issues}

Code:
{code_context}

Your task:
1. Fix the issues in the code.
2. Provide the corrected code.
3. Explain the fix briefly.

Return:
- Fixed code
- Explanation
"""

    return llm.generate(prompt)
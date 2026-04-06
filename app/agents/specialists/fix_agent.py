from app.llm.llm_router import LLMRouter

llm = LLMRouter()


def fix_agent(security_findings, bug_findings, code_chunks):

    issues_list = security_findings + bug_findings

    # ---------- early exit ----------
    if not issues_list:
        return "No fixes required. Code is safe."

    if all("safe" in i.lower() for i in issues_list):
        return "No fixes required. Code is safe."

    issues = "\n".join(issues_list)
    code_context = "\n\n".join(code_chunks[:2])

    prompt = f"""
You are a senior software engineer.

Your task:
Generate minimal and precise fixes for the given issues.

Issues:
{issues}

Code:
{code_context}

Instructions:
- DO NOT rewrite full code
- ONLY show changed lines
- Keep fixes minimal and precise
- Prefer secure and standard practices

Return in this format:

Issue:
<short issue name>

Fix:
<what to change>

Code Patch:
- old line
+ new line

Explanation:
<why this fix works>

If no real fix is needed, return:
Code is safe
"""

    response = llm.generate(prompt)

    if not response:
        return "No fixes generated."

    return response.strip()
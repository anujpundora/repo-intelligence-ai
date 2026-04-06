from app.llm.llm_router import LLMRouter

llm = LLMRouter()


def reflection_agent(security_findings, bug_findings, code_chunks):

    # ---------- early exit ----------
    if not security_findings and not bug_findings:
        return "Code is safe!"

    combined = security_findings + bug_findings

    if all("safe" in f.lower() for f in combined):
        return "Code is safe!"

    code_context = "\n\n".join(code_chunks[:2])

    security_report = "\n".join(security_findings)
    bug_report = "\n".join(bug_findings)

    prompt = f"""
You are a senior software auditor.

Your task:
Review and validate findings from automated code analysis agents.

Security Findings:
{security_report}

Bug Findings:
{bug_report}

Code:
{code_context}

Instructions:
- Remove false positives
- Deduplicate similar issues
- Keep only real and relevant problems
- Assign severity (High / Medium / Low)
- Be concise and structured

Return format:

Issue:
<Type of issue>

Category:
(Security / Bug)

Severity:
(High / Medium / Low)

Explanation:
<why this is a real issue>

If no valid issues exist, return:
Code is safe
"""

    response = llm.generate(prompt)

    if not response:
        return "Reflection failed."

    return response.strip()
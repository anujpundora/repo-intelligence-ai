from app.llm.llm_router import LLMRouter

llm = LLMRouter()


def reflection_agent(security_findings, bug_findings, code_chunks):

    if not security_findings and not bug_findings:
        return "Code is safe!"

    if all("safe" in f.lower() for f in security_findings + bug_findings):
        return "Code is safe!"
    
    code_context = "\n\n".join(code_chunks[:2])

    security_report = "\n".join(security_findings)
    bug_report = "\n".join(bug_findings)

    prompt = f"""
You are a senior software auditor.

Your task is to review findings from automated code analysis agents.

Security Findings:
{security_report}

Bug Findings:
{bug_report}

Relevant Code:
{code_context}

Tasks:
1. Validate whether the reported issues are real.
2. Remove false positives.
3. Combine findings into a final report.

Output:
- Verified issues
- Severity
- Explanation
"""

    return llm.generate(prompt)
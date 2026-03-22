from app.llm.llm_router import LLMRouter

llm = LLMRouter()
#Tool 1- Validate Security findings
def validate_security_issue(findings, code):
    return "Validated security issues" if findings else "No valid security issues"
#Tool 2- Validate Bug findings
def validate_bug_issue(findings, code):
    return "Validated bug issues" if findings else "No valid bug issues"
#Tool 3-Finds duplicate findings
def deduplicate_findings(findings):
    return list(set(findings))

TOOLS = {
    "validate_security": validate_security_issue,
    "validate_bug": validate_bug_issue,
    "deduplicate": deduplicate_findings
}

def reflection_agent(security_findings, bug_findings, code_chunks, max_steps=3):

    history = []
    observations = []

    if not security_findings and not bug_findings:
        return "Code is safe!"

    code_context = "\n\n".join(code_chunks[:2])

    for step in range(max_steps):

        prompt = f"""
You are a reflection agent.

Goal:
Validate and refine findings from other agents.

Security Findings:
{security_findings}

Bug Findings:
{bug_findings}

Code:
{code_context}

Previous actions:
{history}

Observations:
{observations}

Available tools:
- validate_security
- validate_bug
- deduplicate
- finish

Rules:
- Do not repeat tools
- Use at most 3 steps
- Return ONLY ONE JSON

Valid outputs:
{{"tool": "validate_security"}}
{{"tool": "validate_bug"}}
{{"tool": "deduplicate"}}
{{"tool": "finish"}}
"""

        response = llm.generate(prompt)
        response = clean_llm_json(response)

        decision = parse_llm_json(response) or {}
        tool = decision.get("tool")

        # fallback
        if not tool:
            if "validate_security" in response:
                tool = "validate_security"
            elif "validate_bug" in response:
                tool = "validate_bug"
            elif "deduplicate" in response:
                tool = "deduplicate"
            elif "finish" in response:
                tool = "finish"

        # finish
        if tool == "finish":
            break

        # prevent repetition
        if tool in history:
            continue

        if tool not in TOOLS:
            return "Reflection failed: unknown tool"

        # execute
        if tool == "deduplicate":
            combined = security_findings + bug_findings
            result = TOOLS[tool](combined)
        elif tool == "validate_security":
            result = TOOLS[tool](security_findings, code_context)
        elif tool == "validate_bug":
            result = TOOLS[tool](bug_findings, code_context)

        observations.append(str(result))
        history.append(tool)

    # FINAL OUTPUT
    if not observations:
        return "Code is safe!"

    return "\n".join(observations)
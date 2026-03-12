import re

def detect_hardcoded_secrets(code):

    patterns = [
        r"API_KEY\s*=",
        r"SECRET\s*=",
        r"password\s*="
    ]

    for p in patterns:
        if re.search(p, code):
            return "Hardcoded secret detected"

    return "No obvious secrets"

def detect_command_injection(code):

    if "os.system(" in code or "subprocess.call(" in code:
        return "Potential command injection risk"

    return "No command injection detected"

def detect_sql_injection(code):

    if "execute(" in code and "%" in code:
        return "Possible SQL injection via string formatting"

    return "No obvious SQL injection"
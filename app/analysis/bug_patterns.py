import ast

#For syntax Checking
def check_syntax(code):
    try:
        ast.parse(code)
        return "No syntax errors"
    except SyntaxError as e:
        return f"Syntax error: {e}"
    
#For simple Infinite loop detection
def detect_infinite_loops(code):

    if "while True" in code and "break" not in code:
        return "Potential infinite loop detected"
    return "No obvious infinite loop"

#For simple bare except detection
def check_bare_except(code):

    if "except:" in code:
        return "Bare except detected. Should specify exception type."

    return "No bare except blocks"

#For simple unused variable detection
def check_unused_variables(code):

    # simple heuristic example
    if "=" in code and "print(" not in code:
        return "Potential unused variable"

    return "No obvious unused variables"
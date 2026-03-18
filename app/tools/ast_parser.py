import ast


def parse_code(code: str):
    try:
        tree = ast.parse(code)
        return tree
    except Exception as e:
        return None


def extract_functions(tree):
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "lineno": node.lineno
            })

    return functions


def extract_imports(tree):
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for alias in node.names:
                imports.append(f"{module}.{alias.name}")

    return imports

def ast_analysis_tool(code_chunks):

    results = []

    for chunk in code_chunks[:3]:  # limit for performance

        tree = parse_code(chunk)

        if not tree:
            results.append("Syntax error detected")
            continue

        functions = extract_functions(tree)
        imports = extract_imports(tree)

        results.append({
            "functions": functions,
            "imports": imports
        })

    return results
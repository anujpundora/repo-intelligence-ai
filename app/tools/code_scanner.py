import os

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".c",
    ".go",
    ".rs"
}
IGNORED_DIRS = {
    "node_modules",
    ".git",
    "dist",
    "build",
    "venv",
    "__pycache__"
}

def scan_repository(repo_path: str):

    code_files = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for file in files:

            _, ext = os.path.splitext(file)

            if ext in SUPPORTED_EXTENSIONS:

                full_path = os.path.join(root, file)

                code_files.append(full_path)

    return code_files
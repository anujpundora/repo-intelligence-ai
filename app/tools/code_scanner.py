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

def scan_repository(repo_path: str):

    code_files = []

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            _, ext = os.path.splitext(file)

            if ext in SUPPORTED_EXTENSIONS:

                full_path = os.path.join(root, file)

                code_files.append(full_path)

    return code_files
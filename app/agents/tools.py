from app.tools.repo_cloner import clone_repo
from app.tools.code_scanner import scan_repository
from app.indexing.vector_store import query_chunks


TOOLS = {
    "clone_repo": clone_repo,
    "scan_repository": scan_repository,
    "query_chunks": query_chunks
}


def run_tool(tool_name, *args):

    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool = TOOLS[tool_name]

    return tool(*args)
from app.indexing.vector_store import query_chunks
from app.agents.specialists.security_agent import security_agent
from app.agents.specialists.bug_agent import bug_agent


TOOLS = {
    "query_chunks": query_chunks,
    "security_agent": security_agent,
    "bug_agent": bug_agent
}


def run_tool(tool_name, args):

    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool = TOOLS[tool_name]

    return tool(*args)
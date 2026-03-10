from app.indexing.vector_store import query_chunks


TOOLS = {
    "query_chunks": query_chunks
}


def run_tool(tool_name, *args):

    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")

    return TOOLS[tool_name](*args)
from app.agents.planner_agent import planner_agent
from app.tools.code_scanner import scan_repository
from app.tools.code_scanner import scan_repository
from app.indexing.code_loader import load_and_chunk_files
from app.indexing.vector_store import index_chunks
from app.agents.planner_agent import planner_agent

def main():

    repo_path = "./repos/flask"

    files = scan_repository(repo_path)

    chunks = load_and_chunk_files(files)

    print("Chunks created:", len(chunks))

    index_chunks(chunks)

    print("Chunks indexed")

    task = """
    Perform an automated code review of the repository.
    Identify:
    - security vulnerabilities
    - logical bugs
    - performance issues
    """

    planner_agent(task)


if __name__ == "__main__":
    main()
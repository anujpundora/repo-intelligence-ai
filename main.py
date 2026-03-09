from app.tools.repo_cloner import clone_repo
from app.tools.code_scanner import scan_repository
from app.indexing.code_loader import load_and_chunk_files
from app.indexing.vector_store import index_chunks, query_chunks


def main():

    repo_url = "https://github.com/pallets/flask"

    repo_path = clone_repo(repo_url)

    files = scan_repository(repo_path)

    chunks = load_and_chunk_files(files)

    print("Chunks created:", len(chunks))

    # Index chunks into Chroma
    index_chunks(chunks)

    print("Chunks indexed in Chroma")

    # Test retrieval
    results = query_chunks("authentication token")

    print("\nRetriever Results:\n")

    for doc in results["documents"][0][:3]:
        print(doc[:200])
        print("----")


if __name__ == "__main__":
    main()
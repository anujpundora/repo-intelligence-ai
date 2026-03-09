from app.tools.repo_cloner import clone_repo
from app.tools.code_scanner import scan_repository
from app.indexing.code_loader import load_and_chunk_files


def main():

    repo_url = "https://github.com/pallets/flask"

    repo_path = clone_repo(repo_url)

    files = scan_repository(repo_path)

    print("\nFiles found:", len(files))

    chunks = load_and_chunk_files(files)

    print("\nTotal chunks created:", len(chunks))

    print("\nExample chunk:\n")

    print(chunks[0]["content"][:300])


if __name__ == "__main__":
    main()
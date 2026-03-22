import os
import subprocess
from app.agents.planner_agent import planner_agent
from app.tools.code_scanner import scan_repository
from app.tools.code_scanner import scan_repository
from app.indexing.code_loader import load_and_chunk_files
from app.indexing.vector_store import index_chunks
from app.agents.planner_agent import planner_agent

def get_repo_name_from_url(url: str) -> str:
    """
    Extract repo name from GitHub URL
    Example: https://github.com/user/repo → repo
    """
    return url.rstrip("/").split("/")[-1].replace(".git", "")


def ensure_repo():
    base_path = "./repos"

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    # find valid repos (non-empty folders)
    existing_repos = [
        d for d in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, d)) and os.listdir(os.path.join(base_path, d))
    ]

    if existing_repos:
        print("\nAvailable repos:")
        for i, repo in enumerate(existing_repos):
            print(f"{i+1}. {repo}")

        choice = input("\nSelect repo (or press Enter to clone new): ").strip()

        if choice:
            try:
                index = int(choice) - 1
                if index < 0 or index >= len(existing_repos):
                    print("Invalid selection")
                    return None

                repo_name = existing_repos[index]
                repo_path = os.path.join(base_path, repo_name)

                print(f"Using existing repo: {repo_path}")
                return repo_path

            except ValueError:
                print("Invalid input")
                return None

        # default: use first repo
        repo_name = existing_repos[0]
        repo_path = os.path.join(base_path, repo_name)

        print(f"Using existing repo: {repo_path}")
        return repo_path

    # no repos → clone new
    repo_url = input("Enter GitHub repo URL: ").strip()

    if not repo_url.startswith("http"):
        print("Invalid URL")
        return None

    repo_name = get_repo_name_from_url(repo_url)
    repo_path = os.path.join(base_path, repo_name)

    try:
        subprocess.run(
            ["git", "clone", repo_url, repo_path],
            check=True
        )
        print(f"Repo '{repo_name}' cloned successfully!")

    except Exception as e:
        print("Failed to clone repo:", e)
        return None

    return repo_path


def main():

    repo_path = ensure_repo()

    if not repo_path:
        print("Exiting...")
        return

    print(f"\n🔍 Analyzing repository: {repo_path}\n")

    try:
        files = scan_repository(repo_path)

        chunks = load_and_chunk_files(files)

        print("Chunks created:", len(chunks))

        index_chunks(chunks)

        print("✅ Chunks indexed successfully")

        print("\n🚀 Starting AI analysis...\n")

        task = """
        Perform an automated code review of the repository.
        Identify:
        - security vulnerabilities
        - logical bugs
        - performance issues
        """

        planner_agent(task)

    except Exception as e:
        print("❌ Error during processing:", e)

if __name__ == "__main__":
    main()
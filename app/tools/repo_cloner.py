import os 
from git import Repo 

REPO_DIR = "repos"

def clone_repo(repo_url: str) -> str:
    """
    Clones a GitHub repository locally and returns the local path
    """
    if not os.path.exists(REPO_DIR):
        os.makedirs(REPO_DIR)

    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(REPO_DIR, repo_name)

    if os.path.exists(repo_path):
        return repo_path

    Repo.clone_from(repo_url, repo_path)

    return repo_path
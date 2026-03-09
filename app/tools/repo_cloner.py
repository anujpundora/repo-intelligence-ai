import os
from git import Repo

BASE_REPO_DIR = "repos"


def clone_repo(repo_url: str):
#Clones a github repository to a local directory and returns the path to the cloned repository.
    if not os.path.exists(BASE_REPO_DIR):
        os.makedirs(BASE_REPO_DIR)

    repo_name = repo_url.split("/")[-1].replace(".git", "")

    repo_path = os.path.join(BASE_REPO_DIR, repo_name)

    if os.path.exists(repo_path):
        print("Repository already exists locally.")
        return repo_path

    print("Cloning repository...")

    Repo.clone_from(repo_url, repo_path)

    return repo_path
from app.tools.repo_cloner import clone_repo

if __name__ == "__main__":

    repo_url = "https://github.com/pallets/flask"

    path = clone_repo(repo_url)

    print("Repo cloned to:", path)
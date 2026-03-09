from app.tools.repo_cloner import clone_repo
from app.tools.code_scanner import scan_repository


def main():

    repo_url = "https://github.com/pallets/flask"

    repo_path = clone_repo(repo_url)

    files = scan_repository(repo_path)

    print("\nFiles found:", len(files))

    for f in files[:10]:
        print(f)


if __name__ == "__main__":
    main()
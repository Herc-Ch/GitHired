# repo_loader.py
import os
from dotenv import load_dotenv
from github import Auth, Github
from langchain_community.document_loaders import GitLoader


def get_github_client() -> Github:
    """Authenticate with GitHub and return a Github client."""
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("❌ Missing GITHUB_TOKEN environment variable")
    auth = Auth.Token(token)
    return Github(auth=auth)


def load_readmes_from_repos(g: Github, base_dir: str = "./temp_repos"):
    """Load top-level README.md files from all user repositories."""
    os.makedirs(base_dir, exist_ok=True)
    all_docs = []

    for repo in g.get_user().get_repos():
        print(f"🔍 Checking repo: {repo.name}")
        try:
            loader = GitLoader(
                clone_url=repo.clone_url,
                repo_path=f"{base_dir}/{repo.name}",
                file_filter=lambda p: os.path.basename(p).lower() == "readme.md"
                and (
                    p.replace("\\", "/").lower().endswith(f"{repo.name.lower()}/readme.md")
                    or "/" not in p.replace("\\", "/").strip("./")
                ),
            )
            docs = loader.load()
            docs[0].metadata["source"] = repo.clone_url
            print(f"  ✅ Loaded {len(docs)} top-level README.md from {repo.name}")
            all_docs.extend(docs)
        except Exception as e:
            print(f"  ⚠️ Skipped {repo.name}: {e}")

    print(f"📦 Total READMEs collected: {len(all_docs)}")
    return all_docs


def close_github_client(g: Github):
    """Close the GitHub connection."""
    g.close()

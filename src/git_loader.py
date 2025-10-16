# repo_loader.py
import os
from pathlib import Path

from dotenv import load_dotenv
from github import Auth, Github
from langchain_community.document_loaders import GitLoader
from langchain_core.documents import Document


def get_github_client() -> Github:
    """Authenticate with GitHub and return a Github client."""
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("❌ Missing GITHUB_TOKEN environment variable")
    auth = Auth.Token(token)
    return Github(auth=auth)


def is_top_level_readme(path: str) -> bool:
    """Return True if file is README.md located at repo root."""
    normalized = path.replace("\\", "/").lower()
    filename = os.path.basename(normalized)
    depth = normalized.strip("./").count("/")
    return filename == "readme.md" and depth <= 1


def load_readmes_from_repos(g: Github, base_dir: str = "./repo_cache"):
    """
    Load top-level README.md files from all accessible repositories.
    Handles ignored READMEs and prevents index errors.
    """
    base_path = Path(base_dir)
    base_path.mkdir(parents=True, exist_ok=True)
    all_docs = []

    for repo in g.get_user().get_repos():
        print(f"🔍 Checking repo: {repo.name}")
        repo_path = base_path / repo.name
        try:
            loader = GitLoader(
                clone_url=repo.clone_url,
                repo_path=str(repo_path),
                file_filter=is_top_level_readme,
            )
            docs = loader.load()

            # Fallback for repos that ignore README.md in .gitignore
            if not docs:
                readme_path = repo_path / "README.md"
                if readme_path.exists():
                    print(f"  ⚙️ README ignored by .gitignore — loading manually.")
                    text = readme_path.read_text(encoding="utf-8", errors="ignore")
                    docs = [
                        Document(page_content=text, metadata={"source": repo.clone_url})
                    ]
                else:
                    print(f"  ⚠️ No README.md found in {repo.name}")
                    continue

            docs[0].metadata["source"] = repo.clone_url
            print(f"  ✅ Loaded {len(docs)} README.md from {repo.name}")
            all_docs.extend(docs)

        except Exception as e:
            print(f"  ⚠️ Skipped {repo.name}: {e}")

    print(f"📦 Total READMEs collected: {len(all_docs)}")
    return all_docs


def close_github_client(g: Github):
    """Close the GitHub connection."""
    g.close()

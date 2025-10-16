from pathlib import Path
from typing import List

from langchain_core.documents import Document

from src.cover_letter.web_scraper import crawler
from src.git_loader import get_github_client, load_readmes_from_repos
from utils.file_paths import COVER_LETTER_TEX


def load_as_doc(path: str) -> Document:
    """Load a local text or LaTeX file and wrap it as a LangChain Document."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    content = file_path.read_text(encoding="utf-8")
    return Document(page_content=content, metadata={"source": str(file_path.name)})


# --- COMBINED DOCUMENT COLLECTION ---
def get_combined_docs(cv_path: str) -> List[Document]:
    """Fetch GitHub READMEs and append CV document."""
    g = get_github_client()
    readmes = load_readmes_from_repos(g)
    cv_doc = load_as_doc(cv_path)
    return [cv_doc] + readmes


def get_coverletter_docs(cv_path: str, job_url: str) -> List[Document]:
    """Prepare context documents for a cover letter."""
    jobs_docs = crawler(f"{job_url}")
    cover_letter_template = load_as_doc(str(COVER_LETTER_TEX))
    cv_doc = load_as_doc(cv_path)
    return [cv_doc, cover_letter_template] + jobs_docs

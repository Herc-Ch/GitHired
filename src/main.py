# cv_builder.py
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_openai import ChatOpenAI

from src.cover_letter.cover_letter_templates import *
from src.cv_templates import *
from utils.file_paths import *
from utils.loaders import *

# from utils.pdf_compiler import generate_pdf_local

load_dotenv()


def summarize_documents(
    all_docs,
    template: str,
    *,
    model="gpt-5",
    **kwargs,
):
    """Generic document summarization or rewriting function."""

    prompt = PromptTemplate.from_template(template)
    llm = ChatOpenAI(model=model)

    def _fmt_docs(docs):
        return "\n\n".join(
            f"---\nSource: {d.metadata.get('source', '')}\n\n{d.page_content}\n"
            for d in docs
        )

    chain = (
        {
            "context": RunnableLambda(lambda _: all_docs) | RunnableLambda(_fmt_docs),
            **{k: RunnablePassthrough() for k in kwargs.keys()},
        }
        | prompt
        | llm
    )

    result = chain.invoke(kwargs)
    return getattr(result, "content", str(result))


def create_cv(force_update: bool = False) -> Path:
    """Generate an updated CV only if requested, otherwise reuse base CV."""

    if not force_update:
        print(f"🟢 Reusing existing base CV: {CV_TEX}")
        return CV_TEX

    print("⚙️ Regenerating updated CV from base template...")
    combined_docs_cv = get_combined_docs(str(CV_TEX))
    cv_output = summarize_documents(
        combined_docs_cv,
        TEMPLATE_REWRITE,
        fields="AI Engineer, RAG Engineer, Prompt Engineer",
        number_of_repos=4,
        extra_info="Begin",
    )

    OUTPUT_CV_TEX.write_text(cv_output, encoding="utf-8")
    print(f"💾 Saved updated CV: {OUTPUT_CV_TEX}")
    return OUTPUT_CV_TEX


def create_cover_letter(
    job_url: str,
    generate: bool = True,
    cv_path: Path = OUTPUT_CV_TEX,
    template_choice: str = TEMPLATE_COVER_REWRITE,
) -> Path | None:
    """Generate a cover letter based on an existing (updated or base) CV."""

    if not generate:
        print("⚪ Cover letter generation skipped.")
        return None

    # Always ensure we have a CV reference.
    if not cv_path.exists():
        print(f"⚙️ No updated CV found — using base CV in data/: {CV_TEX}")
        cv_path = CV_TEX  # always guaranteed to exist in data/

    print(f"📄 Using CV file: {cv_path}")

    # --- Generate cover letter ---
    combined_docs_cover_letter = get_coverletter_docs(str(cv_path), job_url)
    cover_output = summarize_documents(
        combined_docs_cover_letter,
        template_choice,
        fields="AI Engineer, RAG Engineer, Prompt Engineer",
        extra_info="the readme file and the position advertised. Keep it under one page.",
    )

    OUTPUT_COVER_TEX.write_text(cover_output, encoding="utf-8")
    print(f"💾 Saved LaTeX Cover Letter: {OUTPUT_COVER_TEX}")
    return OUTPUT_COVER_TEX


if __name__ == "__main__":
    JOB_URL = "https://eellak.ellak.gr/2025/10/02/software-engineer-python/?utm_medium=paid&utm_source=fb&utm_id=120234863720040414&utm_content=120234863721400414&utm_term=120234863720290414&utm_campaign=120234863720040414&fbclid=IwY2xjawNZYtxleHRuA2FlbQEwAGFkaWQBqyj4tioPvgEe7vNIRrbJxTR6h6_yvXwU165360dd2GkcAlXZsCYkjFsdaevoRuZ977Hue_8_aem_60_eIeNVUqENAlobqeXM4w"

    # 🟢 Default: not reuse existing CV
    cv_path = create_cv(force_update=True)

    # 🧩 If you want to explicitly not update the CV first:
    # cv_path = create_cv(force_update=False)

    create_cover_letter(JOB_URL, True, cv_path)

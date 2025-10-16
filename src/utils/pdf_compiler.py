from pathlib import Path

from pylatex import Document


def generate_pdf_local(tex_path: str, output_path: str | None = None) -> bool:
    """
    Compile a LaTeX .tex file into a PDF locally using PyLaTeX.
    Requires a LaTeX compiler installed (MiKTeX, TeX Live, or MacTeX).

    Args:
        tex_path: Path to the .tex file.
        output_path: Optional path for the resulting PDF (defaults to same base name).
    Returns:
        True if compilation succeeded, False otherwise.
    """
    tex_file = Path(tex_path)
    if not tex_file.exists():
        print(f"❌ File not found: {tex_file}")
        return False

    # Default output path: same basename as input
    if output_path is None:
        output_path = str(tex_file.with_suffix(".pdf"))

    try:
        tex_content = tex_file.read_text(encoding="utf-8")

        # Create a PyLaTeX Document and override its content
        doc = Document()
        doc.default_filepath = tex_file.stem  # sets base filename (without .tex)
        doc.dumps = lambda: tex_content  # inject our LaTeX content directly

        # Try compiling
        doc.generate_pdf(
            filepath=str(tex_file.with_suffix("")),
            clean=True,  # remove aux/log
            clean_tex=False,  # keep .tex
            compiler="xelatex",  # autodetect latexmk or pdflatex/xelatex
            compiler_args=["-interaction=nonstopmode"],
            silent=True,
        )

        built_pdf = tex_file.with_suffix(".pdf")
        if built_pdf.exists() and str(built_pdf) != output_path:
            Path(output_path).write_bytes(built_pdf.read_bytes())

        print(f"✅ PDF generated successfully: {output_path}")
        return True

    except FileNotFoundError:
        print(
            "❌ No LaTeX compiler found. Please install MiKTeX, TeX Live, or MacTeX and ensure it's in your PATH."
        )
        return False
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        return False

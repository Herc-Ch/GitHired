from pathlib import Path

# --- Base directories ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPOS_DIR = BASE_DIR / "temp_repos"

# --- Key files ---
CV_TEX = DATA_DIR / "cv_private.tex"
COVER_LETTER_TEX = DATA_DIR / "cover_letter_private.tex"

if not CV_TEX.exists():
    CV_TEX = DATA_DIR / "example_cv.tex"

if not COVER_LETTER_TEX.exists():
    COVER_LETTER_TEX = DATA_DIR / "example_cover_letter.tex"

# --- Outputs ---
OUTPUT_COVER_TEX = OUTPUTS_DIR / "cover_letter_updated.tex"
# UPDATED_COVER_PDF = OUTPUTS_DIR / "cover_letter_updated.pdf"
OUTPUT_CV_TEX = OUTPUTS_DIR / "cv_updated.tex"
# UPDATED_CV_PDF = OUTPUTS_DIR / "cv_updated.pdf"

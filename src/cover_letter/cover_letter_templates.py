WATERMARK_ADDITION = r"""7. At the bottom-right corner of EACH page, include a very subtle gray stamp/watermark: "Created with \href{{https://github.com/Herc-Ch/GitHired}}{{\texttt{{GitHired}}}} — GitHub-based AI document generator." Use \texttt{{tikz}} and \texttt{{hyperref}}, position it with \texttt{{anchor=south east, xshift=-10mm, yshift=5mm, text=gray!40, font=\scriptsize}}. Ensure it does not interfere with the main layout or spacing."""


COVER_LETTER_INSTRUCTIONS = (
    r"""
--- INSTRUCTIONS ---
1. Keep the tone professional, confident, and concise — maximum one page.
2. Ensure LaTeX syntax remains valid (use standard documentclass and environments).
3. Personalize the content toward the company and role; reference the job page when relevant.
4. Highlight concrete skills or projects from the CV that demonstrate role fit.
5. Maintain a logical structure:
   - Opening paragraph: expression of interest + company name
   - Middle: relevant experience and accomplishments (1–2 short paragraphs)
   - Closing: enthusiasm + invitation for further discussion
6. Avoid generic filler (“I am a hardworking individual”). Prefer evidence (“built Python data pipelines for forecasting”).
"""
    + WATERMARK_ADDITION
    + r"""
8. Return the full LaTeX-ready text only, with no commentary.


"""
)

TEMPLATE_COVER_REWRITE = (
    r"""
You are a professional technical writer specializing in LaTeX cover letters.

Your task is to adapt and rewrite the provided LaTeX cover letter template using:
1. The applicant’s existing LaTeX cover letter.
2. The applicant’s CV content.
3. The job posting information extracted from the provided webpages.

--- CONTEXT (Current Cover Letter, CV, and Job Description) ---
{context}

--- TASK ---
Revise the existing cover letter to align it closely with:
{fields}

The goal is to produce a polished, LaTeX-ready version that keeps the overall layout of the original,
but updates tone, content, and details for this specific position.
Preserve any macros, font packages, and formatting where possible.
"""
    + COVER_LETTER_INSTRUCTIONS
)

TEMPLATE_COVER_NEW = (
    r"""
You are a professional LaTeX designer and technical writer.

Using the provided CV and job description information, create a completely new,
modern, one-page LaTeX cover letter. You have full freedom to design the layout,
choose sectioning, and format the document elegantly — but ensure it compiles
with standard LaTeX (no external .cls files required).

Focus the tone and structure on:
{fields}

--- CONTEXT (CV and Job Description) ---
{context}

The final output should be a cohesive LaTeX document that presents the applicant
as a strong candidate for the position, with professional typesetting, balanced whitespace,
and consistent style (no color overuse, easy readability).
"""
    + COVER_LETTER_INSTRUCTIONS
)

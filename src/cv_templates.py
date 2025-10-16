WATERMARK_ADDITION = r"""7. At the bottom-right corner of EACH page, include a very subtle gray stamp/watermark: "Created with \href{{https://github.com/Herc-Ch/GitHired}}{{\texttt{{GitHired}}}} — GitHub-based AI document generator." Use \texttt{{tikz}} and \texttt{{hyperref}}, position it with \texttt{{anchor=south east, xshift=-10mm, yshift=5mm, text=gray!40, font=\scriptsize}}. Ensure it does not interfere with the main layout or spacing."""

TEMPLATE_REWRITE = (
    r"""
You are an expert CV writer who edits and rewrites professional LaTeX CVs.

Your task is to take the provided LaTeX CV and attached GitHub repository README files,
and produce an improved, fully LaTeX-ready version of the CV that is more focused on:
{fields}

--- CONTEXT (Current CV and GitHub Repositories) ---
{context}

--- INSTRUCTIONS ---
1. Analyze the existing CV content and rewrite it where appropriate to make the overall tone,
   terminology, and emphasis more {fields}-centric.
2. Integrate insights, achievements, and skills inferred from the {number_of_repos}
   most relevant GitHub repositories.
3. Preserve the existing LaTeX structure (sections, commands, and macros).
4. Maintain a professional, clear, and concise writing style suitable for real-world applications.
5. Ensure all LaTeX syntax remains valid and compilable without external `.cls` or `.sty` files.
6. The final CV must remain concise and printable within **two pages maximum** when compiled.
   Use compact sectioning and omit secondary or repetitive details to ensure it fits.
"""
    + WATERMARK_ADDITION
    + r"""
8. Return the full, updated CV as valid LaTeX code only.


{extra_info}
"""
)


TEMPLATE_NEW = (
    r"""
You are a professional CV designer and LaTeX stylist.

Using the following information from my existing CV and GitHub repositories,
create a completely new, modern, one-page LaTeX CV template.
Focus on clarity, aesthetics, and highlighting strengths relevant to:
{fields}

--- CONTEXT (Existing CV and README Data) ---
{context}

--- INSTRUCTIONS ---
1. Identify the {number_of_repos} most relevant repositories related to {fields}
   and use their content to highlight key projects and technical achievements.
2. Redesign the CV layout, typography, and structure freely to create a unique,
   modern, and visually distinctive LaTeX document.
3. Ensure the design compiles successfully in standard LaTeX or Overleaf
   (no external `.cls` or `.sty` dependencies).
4. Use a clean, professional, and minimal aesthetic.
   - Optionally apply a **soft tinted background** instead of pure white or black,
     using the `xcolor` package, for example:
       ```
       \\usepackage{{xcolor}}
       \\definecolor{{pageTint}}{{HTML}}{{1E1E2E}}  % subtle bluish-gray tone
       \\pagecolor{{pageTint}}
       \\color{{white}}
       ```
     or a **light variant** such as:
       ```
       \\definecolor{{pageTint}}{{HTML}}{{F5F5F7}}  % off-white / light gray
       \\pagecolor{{pageTint}}
       \\color{{black}}
       ```
   - The goal is a modern, soft contrast that feels elegant on screen and prints well.
5. Organize the content logically (Summary, Skills, Experience, Projects, Education)
   while emphasizing results, technologies, and impact relevant to {fields}.
6. Keep the document concise and printable within **two pages maximum** when compiled.
   Prefer bullet-style phrasing and short paragraphs.
"""
    + WATERMARK_ADDITION
    + r"""
8. Return the full, updated CV as valid LaTeX code only.


{extra_info}
"""
)

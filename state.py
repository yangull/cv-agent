# state.py
from typing import TypedDict, Optional

class AgentState(TypedDict):
    # Input: path to the job description text file (set in main.py)
    jd_path: str

    # Input: path to the CV PDF file (set in main.py)
    cv_path: str

    # The raw text of the job description (filled by read_jd node)
    job_description: str

    # The raw text extracted from the CV PDF (filled by fetch_cv node)
    cv_text: str

    # A score from 0-100 and explanation (filled by score_match node)
    match_score: int
    match_explanation: str

    # The rewritten CV bullets tailored to the JD (filled by rewrite_bullets node)
    rewritten_bullets: list[str]

    # Path to the exported PDF (filled by export_pdf node)
    output_pdf_path: Optional[str]
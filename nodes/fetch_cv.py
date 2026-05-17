# nodes/fetch_cv.py
from pypdf import PdfReader
from state import AgentState

def fetch_cv(state: AgentState) -> AgentState:
    # Get the CV PDF path from state (set in main.py before graph runs)
    cv_path = state["cv_path"]

    # Create a PdfReader object pointing at the file
    reader = PdfReader(cv_path)

    # Loop through every page and extract text, joining with newlines
    cv_text = "\n".join(
        page.extract_text() for page in reader.pages
    )

    print(f"✅ fetch_cv: extracted {len(cv_text)} characters from {cv_path}")

    # Return only what this node produced
    return {"cv_text": cv_text}
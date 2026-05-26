from pypdf import PdfReader
from state import AgentState

def fetch_cv(state: AgentState) -> AgentState:
    cv_path = state["cv_path"]
    reader = PdfReader(cv_path)

    cv_text = "\n".join(
        page.extract_text() or "" for page in reader.pages
    )

    print(f"fetch_cv: extracted {len(cv_text)} characters from {cv_path}")

    return {"cv_text": cv_text}

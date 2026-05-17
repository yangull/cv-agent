# nodes/read_jd.py
from state import AgentState

def read_jd(state: AgentState) -> AgentState:
    # We expect the JD file path to already be in state
    # It gets set in main.py before the graph runs
    jd_path = state["jd_path"]

    # Open the file and read the full text
    with open(jd_path, "r") as f:
        jd_text = f.read()

    # Print so we can see progress when running the pipeline
    print(f"✅ read_jd: loaded {len(jd_text)} characters from {jd_path}")

    # Return updated state — LangGraph merges this with existing state
    return {"job_description": jd_text}
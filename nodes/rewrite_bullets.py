import json
import anthropic
from state import AgentState
from nodes.utils import strip_code_fences

# Sonnet for rewriting — produces noticeably better output than Haiku for this task
client = anthropic.Anthropic()

def rewrite_bullets(state: AgentState) -> AgentState:
    jd = state["job_description"]
    cv = state["cv_text"]
    explanation = state["match_explanation"]

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        system="""You are an expert CV writer helping a backend/AI engineering candidate in Berlin.
You will receive a job description, the candidate's current CV, and a gap analysis.
Your job is to rewrite the candidate's experience bullets to better match the job description.

Rules:
- Keep bullets truthful — do not invent experience that isn't in the CV
- Use strong action verbs and quantify where possible
- Tailor language to match keywords in the job description
- Return ONLY a JSON array of strings, where each string is one rewritten bullet
- No markdown, no backticks, no extra text. Just the JSON array.""",
        messages=[
            {
                "role": "user",
                "content": f"JOB DESCRIPTION:\n{jd}\n\nCURRENT CV:\n{cv}\n\nGAP ANALYSIS:\n{explanation}"
            }
        ]
    )

    bullets = json.loads(strip_code_fences(response.content[0].text))

    print(f"rewrite_bullets: got {len(bullets)} bullets")

    return {"rewritten_bullets": bullets}

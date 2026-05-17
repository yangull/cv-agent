# nodes/rewrite_bullets.py
import os
import json
import anthropic
from state import AgentState

# Initialize client — reads ANTHROPIC_API_KEY from environment automatically
client = anthropic.Anthropic()

def rewrite_bullets(state: AgentState) -> AgentState:
    jd = state["job_description"]
    cv = state["cv_text"]
    explanation = state["match_explanation"]

    # We use claude-sonnet here because rewriting requires more nuance than scoring
    # Haiku is fast and cheap for scoring; Sonnet produces better rewritten content
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

    # Extract raw text from Claude's response
    raw = response.content[0].text

    # Strip markdown code fences if Claude wrapped the response in them
    clean = raw.strip()
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[1]
    if clean.endswith("```"):
        clean = clean.rsplit("```", 1)[0]
    clean = clean.strip()

    # Parse the cleaned string as a JSON array
    bullets = json.loads(clean)

    print(f"✅ rewrite_bullets: got {len(bullets)} rewritten bullets")

    # Print a preview of the first bullet so we can see it working
    if bullets:
        print(f"   Preview: {bullets[0][:80]}...")

    return {"rewritten_bullets": bullets}
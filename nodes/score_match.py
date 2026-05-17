# nodes/score_match.py
import os
import json
import anthropic
from state import AgentState

# Initialize the Anthropic client once at module level
# It automatically reads ANTHROPIC_API_KEY from your environment
client = anthropic.Anthropic()

def score_match(state: AgentState) -> AgentState:
    jd = state["job_description"]
    cv = state["cv_text"]

    # Ask Claude to compare the JD and CV and return structured JSON
    # We use claude-haiku for cost efficiency on this scoring step
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="""You are a technical recruiter scoring how well a CV matches a job description.
Return ONLY a JSON object with exactly these keys:
- score: integer from 0 to 100
- explanation: string summarizing strengths and gaps in 3-4 sentences
No markdown, no backticks, no extra text. Just the JSON object.""",
        messages=[
            {
                "role": "user",
                "content": f"JOB DESCRIPTION:\n{jd}\n\nCV:\n{cv}"
            }
        ]
    )

    # Extract the raw text response from Claude
    raw = response.content[0].text

    # Strip markdown code fences if Claude wrapped the response in them
    # e.g. ```json { ... } ``` -> { ... }
    clean = raw.strip()
    if clean.startswith("```"):
        # Remove opening fence (```json or ```)
        clean = clean.split("\n", 1)[1]
    if clean.endswith("```"):
        # Remove closing fence
        clean = clean.rsplit("```", 1)[0]
    clean = clean.strip()

    # Parse the cleaned string as JSON
    result = json.loads(clean)

    print(f"✅ score_match: score={result['score']}, explanation previewed")

    # Write both values into state
    return {
        "match_score": result["score"],
        "match_explanation": result["explanation"]
    }
import json
import anthropic
from state import AgentState
from nodes.utils import strip_code_fences

# Haiku for cost efficiency on this scoring step
client = anthropic.Anthropic()

def score_match(state: AgentState) -> AgentState:
    jd = state["job_description"]
    cv = state["cv_text"]

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

    result = json.loads(strip_code_fences(response.content[0].text))

    print(f"score_match: score={result['score']}")

    return {
        "match_score": result["score"],
        "match_explanation": result["explanation"]
    }

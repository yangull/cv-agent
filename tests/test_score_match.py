import json
import types
import nodes.score_match as sm


def _state(**kwargs):
    base = {"jd_path": "", "cv_path": "", "job_description": "Need Python",
            "cv_text": "5 years Python", "match_score": 0, "match_explanation": "",
            "rewritten_bullets": [], "output_pdf_path": None}
    base.update(kwargs)
    return base


def _mock_client(text):
    response = types.SimpleNamespace(content=[types.SimpleNamespace(text=text)])
    return types.SimpleNamespace(
        messages=types.SimpleNamespace(create=lambda **kw: response)
    )


def test_returns_score_and_explanation(monkeypatch):
    monkeypatch.setattr(sm, "client", _mock_client(
        json.dumps({"score": 75, "explanation": "Good match"})
    ))
    result = sm.score_match(_state())
    assert result["match_score"] == 75
    assert result["match_explanation"] == "Good match"


def test_strips_code_fences_from_response(monkeypatch):
    payload = "```json\n" + json.dumps({"score": 60, "explanation": "Partial"}) + "\n```"
    monkeypatch.setattr(sm, "client", _mock_client(payload))
    result = sm.score_match(_state())
    assert result["match_score"] == 60
    assert result["match_explanation"] == "Partial"


def test_uses_haiku_model(monkeypatch):
    captured = {}

    def fake_create(**kwargs):
        captured.update(kwargs)
        return types.SimpleNamespace(
            content=[types.SimpleNamespace(text=json.dumps({"score": 50, "explanation": "ok"}))]
        )

    monkeypatch.setattr(sm, "client",
        types.SimpleNamespace(messages=types.SimpleNamespace(create=fake_create)))
    sm.score_match(_state())
    assert "haiku" in captured.get("model", "")

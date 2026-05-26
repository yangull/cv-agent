import json
import types
import nodes.rewrite_bullets as rb


def _state(**kwargs):
    base = {"jd_path": "", "cv_path": "", "job_description": "Need Python",
            "cv_text": "5 years Python", "match_score": 80,
            "match_explanation": "Strong Python skills",
            "rewritten_bullets": [], "output_pdf_path": None}
    base.update(kwargs)
    return base


def _mock_client(text):
    response = types.SimpleNamespace(content=[types.SimpleNamespace(text=text)])
    return types.SimpleNamespace(
        messages=types.SimpleNamespace(create=lambda **kw: response)
    )


def test_returns_list_of_bullets(monkeypatch):
    bullets = ["Built REST API with FastAPI", "Deployed to AWS ECS"]
    monkeypatch.setattr(rb, "client", _mock_client(json.dumps(bullets)))
    result = rb.rewrite_bullets(_state())
    assert result["rewritten_bullets"] == bullets


def test_strips_code_fences(monkeypatch):
    bullets = ["Led backend architecture redesign"]
    payload = "```json\n" + json.dumps(bullets) + "\n```"
    monkeypatch.setattr(rb, "client", _mock_client(payload))
    result = rb.rewrite_bullets(_state())
    assert result["rewritten_bullets"] == bullets


def test_uses_sonnet_model(monkeypatch):
    captured = {}

    def fake_create(**kwargs):
        captured.update(kwargs)
        return types.SimpleNamespace(
            content=[types.SimpleNamespace(text=json.dumps(["bullet"]))]
        )

    monkeypatch.setattr(rb, "client",
        types.SimpleNamespace(messages=types.SimpleNamespace(create=fake_create)))
    rb.rewrite_bullets(_state())
    assert "sonnet" in captured.get("model", "")

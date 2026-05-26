import types
from nodes.fetch_cv import fetch_cv


def _state(**kwargs):
    base = {"jd_path": "", "cv_path": "test.pdf", "job_description": "",
            "cv_text": "", "match_score": 0, "match_explanation": "",
            "rewritten_bullets": [], "output_pdf_path": None}
    base.update(kwargs)
    return base


def _make_reader(page_texts):
    pages = [types.SimpleNamespace(extract_text=lambda t=t: t) for t in page_texts]
    return types.SimpleNamespace(pages=pages)


def test_joins_text_across_pages(monkeypatch):
    monkeypatch.setattr("nodes.fetch_cv.PdfReader", lambda _: _make_reader(["Page one", "Page two"]))
    result = fetch_cv(_state())
    assert result["cv_text"] == "Page one\nPage two"


def test_handles_page_returning_none(monkeypatch):
    monkeypatch.setattr("nodes.fetch_cv.PdfReader", lambda _: _make_reader(["Text", None]))
    result = fetch_cv(_state())
    assert result["cv_text"] == "Text\n"

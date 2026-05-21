# cv-agent

A LangGraph-powered agentic pipeline that reads a job description, scores it against a CV using Claude AI, rewrites experience bullets tailored to the role, and exports a PDF report.

## Pipeline
read_jd → fetch_cv → score_match → rewrite_bullets → export_pdf

## Stack

- **LangGraph** — stateful agent graph
- **Anthropic Claude API** — scoring (Haiku) and bullet rewriting (Sonnet)
- **pypdf** — CV text extraction from PDF
- **reportlab** — PDF generation
- **Python 3.12**

## How it works

Each node reads from and writes to a shared `AgentState` TypedDict. LangGraph manages the execution order and state passing between nodes.

1. `read_jd` — loads job description from a `.txt` file
2. `fetch_cv` — extracts text from a CV PDF using pypdf
3. `score_match` — Claude Haiku scores the match 0-100 with gap analysis
4. `rewrite_bullets` — Claude Sonnet rewrites CV bullets tailored to the JD
5. `export_pdf` — generates a PDF report with score, analysis, and bullets

## Usage

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Configuration

Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

Update `main.py` with your JD and CV paths:
```python
"jd_path": "sample_jd.txt",
"cv_path": "your_cv.pdf",
```

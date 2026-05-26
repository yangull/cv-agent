def strip_code_fences(text: str) -> str:
    """Remove markdown code fences that Claude sometimes wraps JSON responses in."""
    clean = text.strip()
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[1]
    if clean.endswith("```"):
        clean = clean.rsplit("```", 1)[0]
    return clean.strip()

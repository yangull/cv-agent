from nodes.utils import strip_code_fences


def test_strips_json_fence():
    assert strip_code_fences("```json\n{\"a\": 1}\n```") == '{"a": 1}'


def test_strips_bare_fence():
    assert strip_code_fences("```\n[1, 2]\n```") == "[1, 2]"


def test_passes_through_clean_json():
    text = '{"score": 80, "explanation": "Good match"}'
    assert strip_code_fences(text) == text


def test_strips_surrounding_whitespace():
    assert strip_code_fences("  ```json\n{}\n```  ") == "{}"

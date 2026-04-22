from modules.readability import get_readability

EASY_TEXT = "The cat sat on the mat. The dog ran fast."
HARD_TEXT = "The epistemological ramifications of poststructuralist philosophical discourse necessitate comprehensive reexamination."

def test_returns_score_and_grade():
    result = get_readability(EASY_TEXT)
    assert "score" in result
    assert "grade" in result

def test_easy_text_higher_score():
    easy = get_readability(EASY_TEXT)
    hard = get_readability(HARD_TEXT)
    assert easy["score"] > hard["score"]

def test_grade_label_exists():
    result = get_readability(EASY_TEXT)
    assert result["grade"] in ["Very Easy", "Easy", "Moderate", "Difficult", "Very Difficult"]

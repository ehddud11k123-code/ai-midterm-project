from modules.sentiment import get_sentiment

def test_positive_text():
    result = get_sentiment("I love this wonderful amazing product!")
    assert result["label"] == "Positive"
    assert result["polarity"] > 0.1

def test_negative_text():
    result = get_sentiment("This is terrible, awful, and disgusting.")
    assert result["label"] == "Negative"
    assert result["polarity"] < -0.1

def test_has_required_keys():
    result = get_sentiment("Hello world.")
    assert "polarity" in result
    assert "subjectivity" in result
    assert "label" in result

def test_polarity_range():
    result = get_sentiment("The sky is blue.")
    assert -1.0 <= result["polarity"] <= 1.0
    assert 0.0 <= result["subjectivity"] <= 1.0

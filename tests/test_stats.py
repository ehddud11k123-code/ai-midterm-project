from modules.stats import get_stats

SAMPLE = "Hello world.\n\nThis is a test."

def test_word_count():
    result = get_stats(SAMPLE)
    assert result["word_count"] > 0

def test_sentence_count():
    result = get_stats(SAMPLE)
    assert result["sentence_count"] == 2

def test_paragraph_count():
    result = get_stats(SAMPLE)
    assert result["paragraph_count"] == 2

def test_avg_sentence_length():
    result = get_stats(SAMPLE)
    assert result["avg_sentence_length"] > 0

def test_unique_word_count():
    result = get_stats(SAMPLE)
    assert result["unique_word_count"] > 0

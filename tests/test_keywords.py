from modules.keywords import get_keywords

SAMPLE = "The quick brown fox jumps over the lazy dog. The fox is quick and the dog is lazy."

def test_returns_list_of_tuples():
    result = get_keywords(SAMPLE)
    assert isinstance(result, list)
    assert isinstance(result[0], tuple)

def test_top_n_limit():
    result = get_keywords(SAMPLE, top_n=5)
    assert len(result) <= 5

def test_no_stopwords():
    result = get_keywords(SAMPLE)
    words = [w for w, _ in result]
    assert "the" not in words
    assert "is" not in words

def test_frequency_descending():
    result = get_keywords(SAMPLE, top_n=10)
    freqs = [f for _, f in result]
    assert freqs == sorted(freqs, reverse=True)

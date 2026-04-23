from kiwipiepy import Kiwi

_kiwi = None

def _get_kiwi() -> Kiwi:
    global _kiwi
    if _kiwi is None:
        _kiwi = Kiwi()
    return _kiwi

def korean_sentences(text: str) -> list[str]:
    kiwi = _get_kiwi()
    result = kiwi.split_into_sents(text)
    return [s.text for s in result]

def korean_nouns(text: str) -> list[str]:
    kiwi = _get_kiwi()
    tokens = kiwi.tokenize(text)
    return [t.form for t in tokens if t.tag.startswith("NN")]

def korean_pos(text: str) -> dict[str, int]:
    kiwi = _get_kiwi()
    tokens = kiwi.tokenize(text)
    tag_map = {
        "NNG": "명사", "NNP": "고유명사", "NNB": "의존명사",
        "VV": "동사", "VA": "형용사",
        "MAG": "부사", "MM": "관형사",
        "JKS": "조사", "JX": "보조사",
        "EF": "어미", "EC": "연결어미",
    }
    counts: dict[str, int] = {}
    for t in tokens:
        label = tag_map.get(t.tag, "기타")
        counts[label] = counts.get(label, 0) + 1
    return counts

def korean_entities(text: str) -> dict[str, list[str]]:
    kiwi = _get_kiwi()
    result = {}
    try:
        ner_result = kiwi.analyze(text, stopwords=None)
        # kiwipiepy doesn't have NER in all versions; return empty safely
    except Exception:
        pass
    return result

def korean_sentiment(text: str) -> dict:
    # Korean sentiment via simple heuristic (kiwipiepy has no built-in sentiment)
    # Return neutral as fallback
    return {"label": "Neutral", "polarity": 0.0, "subjectivity": 0.0}

def korean_readability(text: str, sentences: list[str]) -> dict:
    if not sentences:
        return {"score": 0.0, "grade": "N/A"}
    kiwi = _get_kiwi()
    tokens_per_sent = []
    for s in sentences:
        toks = kiwi.tokenize(s)
        tokens_per_sent.append(len(toks))
    avg = sum(tokens_per_sent) / len(tokens_per_sent) if tokens_per_sent else 0
    # Simple heuristic: fewer tokens per sentence = easier
    if avg < 8:
        grade = "Very Easy"
        score = 90.0
    elif avg < 12:
        grade = "Easy"
        score = 75.0
    elif avg < 16:
        grade = "Moderate"
        score = 55.0
    elif avg < 22:
        grade = "Difficult"
        score = 35.0
    else:
        grade = "Very Difficult"
        score = 15.0
    return {"score": round(score, 1), "grade": grade}

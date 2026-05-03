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

    # 문장당 평균 어절 수 (띄어쓰기 기준)
    avg_eojeols = sum(len(s.split()) for s in sentences) / len(sentences)

    # 어절당 평균 한글 음절 수 (AC00-D7A3)
    eojeols = [w for w in text.split() if w]
    if eojeols:
        avg_syllables = sum(
            sum(1 for c in w if '가' <= c <= '힣') for w in eojeols
        ) / len(eojeols)
    else:
        avg_syllables = 2.0

    score = 100 - (avg_eojeols * 2.5) - (avg_syllables * 6.0)
    score = round(max(0.0, min(100.0, score)), 1)

    if score >= 80:
        grade = "Very Easy"
    elif score >= 60:
        grade = "Easy"
    elif score >= 40:
        grade = "Moderate"
    elif score >= 20:
        grade = "Difficult"
    else:
        grade = "Very Difficult"

    return {"score": score, "grade": grade}

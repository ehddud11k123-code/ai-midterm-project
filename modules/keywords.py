from modules.lang_utils import detect_language


def get_keywords(text: str, top_n: int = 20) -> list[tuple[str, int]]:
    groq_result = _groq_keywords(text, top_n)
    if groq_result:
        return groq_result
    return _fallback_keywords(text, top_n)


def _groq_keywords(text: str, top_n: int) -> list[tuple[str, int]] | None:
    try:
        import streamlit as st
        from groq import Groq
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)
        prompt = f"""다음 텍스트에서 핵심 키워드 {top_n}개를 추출해주세요.
중요도 순서로, 한 줄에 하나씩, "키워드: 점수" 형식으로만 답하세요. (점수는 1~100 정수)

텍스트:
{text[:4000]}"""

        from modules.groq_client import groq_create
        _content = groq_create(client, [{"role": "user", "content": prompt}],
                              temperature=0.1, max_tokens=512)
        return _parse_keywords(_content, top_n)
    except Exception:
        return None


def _parse_keywords(text: str, top_n: int) -> list[tuple[str, int]] | None:
    import re
    results = []
    for line in text.strip().split('\n'):
        m = re.match(r'\s*[-*]?\s*(.+?):\s*(\d+)', line)
        if m:
            results.append((m.group(1).strip(), int(m.group(2))))
    return results[:top_n] if results else None


def _fallback_keywords(text: str, top_n: int) -> list[tuple[str, int]]:
    from collections import Counter
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    lang = detect_language(text)
    if lang == "ko":
        from modules.korean_nlp import korean_nouns
        nouns = [n for n in korean_nouns(text) if len(n) > 1]
        return Counter(nouns).most_common(top_n)
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text.lower())
    filtered = [w for w in tokens if w.isalpha() and w not in stop_words and len(w) > 2]
    return Counter(filtered).most_common(top_n)

from modules.lang_utils import detect_language


def _groq_summary(text: str, sentence_count: int, lang: str) -> list | None:
    try:
        import streamlit as st
        from groq import Groq
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)
        instruction = "한국어로" if lang == "ko" else "in English"
        prompt = f"""다음 텍스트를 {instruction} {sentence_count}문장으로 핵심만 요약해주세요. 번호 없이 문장만 출력하세요.

텍스트:
{text[:6000]}"""
        from modules.groq_client import groq_create
        raw = groq_create(client, [{"role": "user", "content": prompt}],
                          temperature=0.3, max_tokens=512)
        sentences = [s.strip() for s in raw.split('\n') if s.strip()]
        return sentences[:sentence_count] or None
    except Exception:
        return None


def _lexrank_summary(text: str, sentence_count: int) -> list:
    try:
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lex_rank import LexRankSummarizer
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        return [str(s) for s in summarizer(parser.document, sentence_count)]
    except Exception:
        return []


def _korean_summary(text: str, sentence_count: int) -> list:
    from modules.korean_nlp import korean_sentences, korean_nouns
    from collections import Counter
    sentences = korean_sentences(text)
    if len(sentences) <= sentence_count:
        return sentences
    nouns = korean_nouns(text)
    freq = Counter(nouns)
    def score(sent):
        return sum(freq.get(n, 0) for n in korean_nouns(sent))
    ranked = sorted(sentences, key=score, reverse=True)
    top = set(ranked[:sentence_count])
    return [s for s in sentences if s in top]


def get_summary(text: str, sentence_count: int = 3) -> list:
    lang = detect_language(text)
    groq_result = _groq_summary(text, sentence_count, lang)
    if groq_result:
        return groq_result
    if lang == "ko":
        return _korean_summary(text, sentence_count)
    return _lexrank_summary(text, sentence_count)

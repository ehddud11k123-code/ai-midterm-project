from nltk.tokenize import sent_tokenize, word_tokenize
from modules.lang_utils import detect_language


def _tokenize(text: str, lang: str) -> tuple[list, list]:
    if lang == "ko":
        from modules.korean_nlp import korean_sentences, get_morphemes
        return korean_sentences(text), get_morphemes(text)
    sentences = sent_tokenize(text)
    words = [w for w in word_tokenize(text) if w.isalpha()]
    return sentences, words


def get_stats(text: str) -> dict:
    lang = detect_language(text)
    sentences, words = _tokenize(text, lang)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    unique_words = set(w.lower() for w in words)
    avg_len = round(len(words) / len(sentences), 1) if sentences else 0
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs) or 1,
        "avg_sentence_length": avg_len,
        "unique_word_count": len(unique_words),
    }

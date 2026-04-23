from nltk.tokenize import sent_tokenize, word_tokenize
from modules.lang_utils import detect_language


def get_stats(text: str) -> dict:
    lang = detect_language(text)
    if lang == "ko":
        from modules.korean_nlp import korean_sentences, korean_nouns, _get_kiwi
        sentences = korean_sentences(text)
        kiwi = _get_kiwi()
        all_tokens = kiwi.tokenize(text)
        words = [t.form for t in all_tokens if t.tag not in ("SP", "SW", "SF", "SE", "SY", "SSO", "SSC", "SC", "SB")]
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
    else:
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        words = [w for w in words if w.isalpha()]
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

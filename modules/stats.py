from nltk.tokenize import word_tokenize, sent_tokenize


def get_stats(text: str) -> dict:
    sentences = sent_tokenize(text)
    words = [w for w in word_tokenize(text) if w.isalpha()]
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    word_count = len(words)
    sentence_count = len(sentences)
    paragraph_count = len(paragraphs)
    avg_sentence_length = round(word_count / sentence_count, 1) if sentence_count else 0
    unique_word_count = len(set(w.lower() for w in words))

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "avg_sentence_length": avg_sentence_length,
        "unique_word_count": unique_word_count,
    }

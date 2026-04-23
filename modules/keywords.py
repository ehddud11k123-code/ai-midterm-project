from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from modules.lang_utils import detect_language


def get_keywords(text: str, top_n: int = 20) -> list[tuple[str, int]]:
    lang = detect_language(text)
    if lang == "ko":
        from modules.korean_nlp import korean_nouns
        nouns = korean_nouns(text)
        # Filter single-char nouns
        nouns = [n for n in nouns if len(n) > 1]
        return Counter(nouns).most_common(top_n)
    else:
        stop_words = set(stopwords.words("english"))
        tokens = word_tokenize(text.lower())
        filtered = [w for w in tokens if w.isalpha() and w not in stop_words and len(w) > 2]
        return Counter(filtered).most_common(top_n)

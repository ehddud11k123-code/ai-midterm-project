from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def get_keywords(text: str, top_n: int = 20) -> list:
    stop_words = set(stopwords.words("english"))
    words = [
        w.lower()
        for w in word_tokenize(text)
        if w.isalpha() and w.lower() not in stop_words
    ]
    counter = Counter(words)
    return counter.most_common(top_n)

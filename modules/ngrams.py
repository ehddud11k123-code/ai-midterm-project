from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
from collections import Counter
import plotly.graph_objects as go
from modules.lang_utils import detect_language
from modules.korean_nlp import korean_nouns


def get_ngrams(text: str, n: int = 2, top_k: int = 15) -> list:
    lang = detect_language(text)
    if lang == "ko":
        nouns = korean_nouns(text)
        grams = list(ngrams(nouns, n))
        counter = Counter(grams)
        return [(" ".join(gram), count) for gram, count in counter.most_common(top_k)]
    else:
        stop_words = set(stopwords.words("english"))
        tokens = [
            w.lower()
            for w in word_tokenize(text)
            if w.isalpha() and w.lower() not in stop_words
        ]
        grams = ngrams(tokens, n)
        counter = Counter(grams)
        return [(" ".join(gram), count) for gram, count in counter.most_common(top_k)]


def plot_ngram_bar(ngram_list: list, title: str = "Top N-grams") -> go.Figure:
    if not ngram_list:
        return go.Figure()
    phrases = [p for p, _ in reversed(ngram_list)]
    counts = [c for _, c in reversed(ngram_list)]
    fig = go.Figure(go.Bar(
        x=counts,
        y=phrases,
        orientation="h",
        marker_color="#f28e2b",
    ))
    fig.update_layout(
        title=title,
        xaxis_title="빈도",
        height=max(300, len(ngram_list) * 28),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig

from nltk import word_tokenize, pos_tag
from collections import Counter
import plotly.graph_objects as go
from modules.lang_utils import detect_language
from modules.korean_nlp import korean_pos

_POS_MAP = {
    "NN": "Noun", "NNS": "Noun", "NNP": "Noun", "NNPS": "Noun",
    "VB": "Verb", "VBD": "Verb", "VBG": "Verb", "VBN": "Verb", "VBP": "Verb", "VBZ": "Verb",
    "JJ": "Adjective", "JJR": "Adjective", "JJS": "Adjective",
    "RB": "Adverb", "RBR": "Adverb", "RBS": "Adverb",
}


def get_pos_distribution(text: str) -> dict:
    lang = detect_language(text)
    if lang == "ko":
        return korean_pos(text)
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    counts: Counter = Counter()
    for _, tag in tagged:
        label = _POS_MAP.get(tag)
        if label:
            counts[label] += 1
    return dict(counts)


def plot_pos_pie(pos_dist: dict) -> go.Figure:
    labels = list(pos_dist.keys())
    values = list(pos_dist.values())
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"],
    ))
    fig.update_layout(
        title="품사 분포" if any(ord(c) > 127 for c in "".join(labels)) else "Part-of-Speech Distribution",
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig

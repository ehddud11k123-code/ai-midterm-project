from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from modules.lang_utils import detect_language
from modules.korean_nlp import korean_sentences, korean_nouns
from collections import Counter


def _korean_summary(text: str, sentence_count: int = 3) -> list:
    sentences = korean_sentences(text)
    if len(sentences) <= sentence_count:
        return sentences
    nouns = korean_nouns(text)
    freq = Counter(nouns)
    def score(sent):
        return sum(freq.get(n, 0) for n in korean_nouns(sent))
    ranked = sorted(sentences, key=score, reverse=True)
    top = ranked[:sentence_count]
    return [s for s in sentences if s in top]


def get_summary(text: str, sentence_count: int = 3) -> list:
    lang = detect_language(text)
    if lang == "ko":
        return _korean_summary(text, sentence_count)
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return [str(sentence) for sentence in summary]

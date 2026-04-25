import re
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

SECTION_PATTERNS = [
    "abstract", "introduction", "related work", "background",
    "methodology", "methods", "proposed method", "approach",
    "experiment", "experiments", "results", "evaluation",
    "discussion", "conclusion", "conclusions", "future work",
    "references",
]

_HEADER_RE = re.compile(
    r'(?:^|\n)(?:\d+\.?\s+)?(' +
    '|'.join(re.escape(s) for s in SECTION_PATTERNS) +
    r')s?\s*\n',
    re.IGNORECASE,
)

# Sections that are already summaries — take directly
_SUMMARY_SECTIONS = {"abstract", "conclusion", "conclusions", "future work"}


def detect_sections(text: str) -> dict[str, str]:
    matches = list(_HEADER_RE.finditer(text))
    if not matches:
        return {"전체 텍스트": text}
    sections: dict[str, str] = {}
    for i, m in enumerate(matches):
        name = m.group(1).strip().title()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if body:
            key = name if name not in sections else f"{name} ({i+1})"
            sections[key] = body
    return sections if sections else {"전체 텍스트": text}


def _score_sentences(sentences: list[str], section_text: str) -> list[tuple[float, str]]:
    stop_words = set(stopwords.words("english"))
    # TF of meaningful words in the section
    all_words = [w.lower() for w in word_tokenize(section_text) if w.isalpha() and w.lower() not in stop_words]
    tf = Counter(all_words)
    total = max(len(all_words), 1)

    scored = []
    paragraphs = [p.strip() for p in section_text.split("\n\n") if p.strip()]
    para_first = set()
    for p in paragraphs:
        sents = sent_tokenize(p)
        if sents:
            para_first.add(sents[0].strip())

    for idx, sent in enumerate(sentences):
        words = [w.lower() for w in word_tokenize(sent) if w.isalpha() and w.lower() not in stop_words]
        if len(words) < 4:
            continue
        tfidf_score = sum(tf.get(w, 0) / total for w in words) / max(len(words), 1)
        # Boost first sentence of document section and paragraph-opening sentences
        position_boost = 1.5 if idx == 0 else (1.3 if sent.strip() in para_first else 1.0)
        scored.append((tfidf_score * position_boost, sent))

    return sorted(scored, reverse=True)


def summarize_section(section_name: str, text: str, n: int = 2) -> list[str]:
    sentences = sent_tokenize(text)
    if len(sentences) <= n:
        return sentences

    # For abstract/conclusion: first n sentences are best
    if section_name.lower().rstrip("s") in _SUMMARY_SECTIONS:
        return sentences[:n]

    scored = _score_sentences(sentences, text)
    if not scored:
        return sentences[:n]

    # Pick top-n by score, restore original order
    top = set(s for _, s in scored[:n])
    return [s for s in sentences if s in top][:n]


def get_section_keywords(text: str, top_n: int = 5) -> list[tuple[str, int]]:
    from modules.keywords import get_keywords
    return get_keywords(text, top_n=top_n)


def analyze_paper(text: str) -> list[dict]:
    sections = detect_sections(text)
    results = []
    for name, body in sections.items():
        words = [w for w in body.split() if w.isalpha()]
        results.append({
            "name": name,
            "text": body,
            "word_count": len(words),
            "keywords": get_section_keywords(body),
            "summary": summarize_section(name, body, n=2),
        })
    return results

import re
from collections import Counter

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
            if name in sections:
                name = f"{name} ({i+1})"
            sections[name] = body

    return sections if sections else {"전체 텍스트": text}


def summarize_section(text: str, n: int = 2) -> list[str]:
    from modules.summarize import get_summary
    result = get_summary(text, sentence_count=n)
    return result if result else []


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
            "summary": summarize_section(body, n=2),
        })
    return results

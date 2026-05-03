from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree

LABEL_KO = {
    "PERSON": "인물",
    "ORGANIZATION": "기관/단체",
    "GPE": "국가/도시",
    "LOCATION": "장소",
    "FACILITY": "시설",
    "GSP": "지명",
}


def get_entities(text: str) -> dict[str, list[str]]:
    try:
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        chunks = ne_chunk(pos_tags)
        entities: dict[str, list[str]] = {}
        for chunk in chunks:
            if isinstance(chunk, Tree):
                label = chunk.label()
                name = " ".join(c[0] for c in chunk)
                ko_label = LABEL_KO.get(label, label)
                if ko_label not in entities:
                    entities[ko_label] = []
                if name not in entities[ko_label]:
                    entities[ko_label].append(name)
        return entities
    except Exception:
        return {}

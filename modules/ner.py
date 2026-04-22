import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree


def get_entities(text: str) -> dict:
    """Extract named entities grouped by type."""
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    chunked = ne_chunk(tagged)

    entities: dict[str, list[str]] = {}
    for subtree in chunked:
        if isinstance(subtree, Tree):
            entity_type = subtree.label()
            entity_name = " ".join(word for word, tag in subtree.leaves())
            entities.setdefault(entity_type, [])
            if entity_name not in entities[entity_type]:
                entities[entity_type].append(entity_name)
    return entities

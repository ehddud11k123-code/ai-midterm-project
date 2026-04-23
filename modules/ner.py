import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree
from modules.lang_utils import detect_language
from modules.korean_nlp import korean_entities


def get_entities(text: str) -> dict:
    lang = detect_language(text)
    if lang == "ko":
        return korean_entities(text)
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    chunked = ne_chunk(tagged)
    entities: dict = {}
    for subtree in chunked:
        if isinstance(subtree, Tree):
            entity_type = subtree.label()
            entity_name = " ".join(word for word, tag in subtree.leaves())
            entities.setdefault(entity_type, [])
            if entity_name not in entities[entity_type]:
                entities[entity_type].append(entity_name)
    return entities

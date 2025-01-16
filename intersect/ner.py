# https://www.wisecube.ai/blog/named-entity-recognition-ner-with-python/
# displacy
# https://spacy.io/models/en

# uv pip install pip
# uv uv run -- spacy download es_core_news_md

import spacy
from spacy.lang.en.examples import sentences
from collections import Counter


def get_ents(string: str):
    db = []
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(string)
    for ent in doc.ents:
        db.append(ent.text)
    return db


def ner_count(sentences: list[str]):
    c = Counter()
    for sentence in sentences:
        c.update(get_ents(sentence))
    return dict(c)

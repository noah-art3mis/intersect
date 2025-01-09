# https://www.wisecube.ai/blog/named-entity-recognition-ner-with-python/
# displacy
# https://spacy.io/models/en

# uv pip install pip
# uv uv run -- spacy download es_core_news_md

import spacy
from spacy.lang.en.examples import sentences

nlp = spacy.load("en_core_web_sm")
doc = nlp(sentences[0])
print(doc.text)
for token in doc:
    print(token.text, token.pos_, token.dep_)

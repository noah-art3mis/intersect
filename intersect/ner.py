import spacy
from collections import Counter
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

# https://www.wisecube.ai/blog/named-entity-recognition-ner-with-python/
# displacy
# https://spacy.io/models/en

# uv pip install pip
# uv uv run -- spacy download es_core_news_md


def get_ents(string: str) -> list[str]:
    ents = []
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(string)
    for ent in doc.ents:
        ents.append(ent.text)
    return ents


def ner_count(sentences: list[str]) -> dict:
    c = Counter()
    for sentence in sentences:
        c.update(get_ents(sentence))
    return dict(c)


def wordcloud_ner(frequencies) -> None:
    fig, ax = plt.subplots()
    wordcloud = WordCloud().generate_from_frequencies(frequencies)
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

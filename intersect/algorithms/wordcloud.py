from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

# https://scikit-learn.org/1.5/auto_examples/text/plot_hashing_vs_dict_vectorizer.html#sphx-glr-auto-examples-text-plot-hashing-vs-dict-vectorizer-py

# def count_words(documents: list[str]) -> dict[str, int]:
#     vectorizer = CountVectorizer(stop_words="english")
#     X = vectorizer.fit_transform(documents)
#     names = vectorizer.get_feature_names_out()
#     total_count = X.toarray().sum(axis=0)
#     word_freq = dict(zip(names, total_count))
#     return word_freq

def render_wordcloud(df: pd.DataFrame) -> None:
    """Render word cloud visualization"""
    with st.spinner("Generating word cloud..."):
        descriptions: list[str] = df["description"].tolist()  # type: ignore
        wordcloud_tfidf(tfidf_words(descriptions))

def wordcloud_tfidf(frequencies: dict) -> None:
    plt.figure(figsize=(24, 14), dpi=1200)
    fig, ax = plt.subplots()
    wordcloud = WordCloud().generate_from_frequencies(frequencies)
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)


def nb_wordcloud_tfidf(frequencies: dict) -> None:
    plt.figure(figsize=(24, 14), dpi=1200)
    fig, ax = plt.subplots()
    wordcloud = WordCloud().generate_from_frequencies(frequencies)
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")


def tfidf_words(documents: list[str]) -> dict[str, int]:
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(documents)
    names = vectorizer.get_feature_names_out()
    total_count = X.toarray().sum(axis=0) # type: ignore
    word_freq = dict(zip(names, total_count))
    return word_freq 
import pandas as pd
import bm25s
import Stemmer

# rank_bm25 is a somewhat popular python implementation of bm25. bm25s is a more performant alternative.

# https://github.com/dorianbrown/rank_bm25
# https://github.com/xhluca/bm25s

# - preprocessing
#     - [x] lowercasing
#     - [x] tokenizing
#     - [x] removing stop words
#     - [x] stemming
#     - [ ] lemmatizing
#     - [x] removing special characters
#     - [x] removing numbers

# as this is not the focus of the project, using the default configurations should suffice - (tokenizer, stemmer, stop words, lucene method). even though using a lemmatizer might give better results, since it is a real time application the stemmer will be used because of its lower latency.

# even though the point of tf-idf and bm25 is to deal with this, we find that the word clouds are dominated by words that are too generic to be useful.


def lexical_search(query: str, df: pd.DataFrame, corpus_col: str) -> pd.DataFrame:
    """Side effects:
        - adds "i_lexical": index (int),
        - adds "score_lexical": score (float),

    Returns:
        - df: pd.DataFrame with the added columns
    """

    corpus = df[corpus_col].tolist()

    preprocessed_query = preprocess_text(query)
    preprocessed_corpus = [preprocess_text(doc) for doc in corpus]

    stemmer = Stemmer.Stemmer("english")
    corpus_tokens = bm25s.tokenize(preprocessed_corpus, stopwords="en", stemmer=stemmer)

    retriever = bm25s.BM25()
    retriever.index(corpus_tokens)

    query_tokens = bm25s.tokenize(preprocessed_query, stopwords="en", stemmer=stemmer)
    results, scores = retriever.retrieve(query_tokens, corpus=preprocessed_corpus, k=len(corpus))

    # Add scores directly to the original DataFrame
    df = df.copy()
    df["score_lexical"] = scores[0]
    df["i_lexical"] = range(len(df))
    
    return df


def preprocess_text(text: str) -> str:
    text = text.lower()
    # text = re.sub(r'[^a-z\s]', '', text)
    return text 
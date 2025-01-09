import bm25s
from rich import print
import pandas as pd

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

# as this is not the focus of the project, using the default configurations should suffice - (tokenizer, stemmer, stop words, lucene method). example does not use lemmatizing and library does not have immediate integration. since it is a real time application the stemmer will be used even though using a lemmatizer might give better results.

import bm25s
import Stemmer

def lexical_search(query: str, corpus: list[str]) -> pd.DataFrame:
    preprocessed_query = preprocess_text(query)
    preprocessed_corpus = [preprocess_text(doc) for doc in corpus]

    stemmer = Stemmer.Stemmer("english")
    corpus_tokens = bm25s.tokenize(preprocessed_corpus, stopwords="en", stemmer=stemmer)
    retriever = bm25s.BM25()
    retriever.index(corpus_tokens)

    query_tokens = bm25s.tokenize(preprocessed_query, stopwords="en", stemmer=stemmer)
    results, scores = retriever.retrieve(query_tokens, corpus=corpus, k=len(corpus))

    formatted_results = []
    
    for i in range(results.shape[1]):
        doc, score = results[0, i], scores[0, i]
        formatted_results.append(
            {
                "Rank": i + 1,
                "Score": score,
                # "Title": ,
                # "Link": ,
                "Document": doc,
            }
        )
    
    return pd.DataFrame(formatted_results)

def preprocess_text(text: str) -> str:
    text = text.lower()
    # text = re.sub(r'[^a-z\s]', '', text)
    return text
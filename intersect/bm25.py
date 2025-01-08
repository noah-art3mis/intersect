import bm25s

# rank_bm25 is a somewhat popular python implementation of bm25. bm25s is a more performant alternative.

# https://github.com/dorianbrown/rank_bm25
# https://github.com/xhluca/bm25s

# tokenize
# remove special CHARACTERS
# remove stop words
# stemming

# Create your corpus here
corpus = [
    "a cat is a feline and likes to purr",
    "a dog is the human's best friend and loves to play",
    "a bird is a beautiful animal that can fly",
    "a fish is a creature that lives in water and swims",
]

# Create the BM25 model and index the corpus
retriever = bm25s.BM25(corpus=corpus)
retriever.index(bm25s.tokenize(corpus))

# Query the corpus and get top-k results
query = "does the fish purr like a cat?"
results, scores = retriever.retrieve(bm25s.tokenize(query), k=2)

# Let's see what we got!
doc, score = results[0, 0], scores[0, 0]
print(f"Rank {i+1} (score: {score:.2f}): {doc}")

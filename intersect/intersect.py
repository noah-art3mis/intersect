from openai import OpenAI
import pandas as pd
import numpy as np
from dotenv import load_dotenv

DB_FILEPATH = './data/jobs.csv'
TEXT = 'The food was delicious and the waiter...'


def get_embedding(client: OpenAI, text: str, model="text-embedding-3-small"):
    res = client.embeddings.create(
        model=model,
        input="The food was delicious and the waiter...",
        encoding_format="float")
    return res.data[0].embedding

def get_database(filepath) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df

def similarity_search(df, embedding):
    df['similarity'] = df['embedding'].apply(lambda x: np.dot(embedding, x))
    df.sort_values('similarity', ascending=False, inplace=True)
    return df

def main(client):
    v = get_embedding(client, TEXT)
    print(TEXT)
    print(v)

    # db = get_database(DB_FILEPATH)
    # result = similarity_search(db, v)
    # print(result.head(10))

if __name__ == "__main__":
    load_dotenv()
    client = OpenAI()
    main(client)

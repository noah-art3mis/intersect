from openai import OpenAI
import pandas as pd
import numpy as np
from dotenv import load_dotenv

DB_FILEPATH = './data/jobs.feather'
TEXT = 'The food was delicious and the waiter...'


def get_embedding(client: OpenAI, text: str, model="text-embedding-3-small"):
    
    # TODO check if exceeds token limit
    # TODO add support for list of strs
    # def num_tokens_from_string(string: str, encoding_name: str) -> int:
        # """Returns the number of tokens in a text string."""
        # encoding = tiktoken.get_encoding(encoding_name)
        # num_tokens = len(encoding.encode(string))
        # return num_tokens
    
    res = client.embeddings.create(
        model=model,
        input=text,
        encoding_format="float")
    return res.data[0].embedding

def get_database(filepath) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df

def similarity_search(df, embedding):
    df['similarity'] = df['embedding'].apply(lambda x: np.dot(embedding, x))
    df.sort_values('similarity', ascending=False, inplace=True)
    return df

def main():
    load_dotenv()
    client = OpenAI()

    v = get_embedding(client, TEXT)
    # db = get_database(DB_FILEPATH)
    # result = similarity_search(db, v)
    # print(result.head(10))

if __name__ == "__main__":
    main()

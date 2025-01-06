import pandas as pd
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken

DB_FILEPATH = 'intersect/data/jobs.feather'

def get_input_text() -> str:
    with open('intersect/data/raw/cvs/cv2.txt', 'r') as f:
        return f.read()

def get_embedding(client: OpenAI, text: str, model="text-embedding-3-small"):
    
    def num_tokens_from_string(string: str, model="text-embedding-3-small") -> int:
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    
    if num_tokens_from_string(text) > 8000:
        raise Exception("Text too long")
    
    res = client.embeddings.create(
        model=model,
        input=text,
        encoding_format="float")

    return res.data[0].embedding

def similarity_search(df: pd.DataFrame, embedding) -> pd.DataFrame:
    df['similarity'] = df['embedding'].apply(lambda x: np.dot(embedding, x))
    df.sort_values('similarity', ascending=False, inplace=True)
    return df

def main():
    load_dotenv()
    client = OpenAI()

    text = get_input_text()
    v = get_embedding(client, text)
    
    df = pd.read_feather(DB_FILEPATH)
    
    result = similarity_search(df, v)
    
    print(result)

if __name__ == "__main__":
    main()

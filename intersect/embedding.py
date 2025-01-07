from openai import OpenAI
import tiktoken


def get_embedding(client: OpenAI, text: str, model="text-embedding-3-small"):
    # you will probably need to call load_dotenv before calling this

    def num_tokens_from_string(string: str, model="text-embedding-3-small") -> int:
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    if num_tokens_from_string(text) > 8000:
        raise Exception("Text too long")

    res = client.embeddings.create(model=model, input=text, encoding_format="float")

    return res.data[0].embedding

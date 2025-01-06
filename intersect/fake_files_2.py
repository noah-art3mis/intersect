# import pandas as pd
# from intersect import get_embedding
# from openai import OpenAI
# import dotenv

# dotenv.load_dotenv()
# DB_FILEPATH = 'intersect/data/jobs.feather'
# db = pd.read_feather(DB_FILEPATH)

# # apply get_embedding to each row
# # db['embedding'] = db['text'].apply(lambda x: get_embedding(OpenAI(), x))

# print(db.head())

# # db.to_feather(DB_FILEPATH)
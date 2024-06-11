

# Import API keys (in a .gitignore'd file)
from keys import weaviate_key, weaviate_url, openai_key


# Weaviate packages
import weaviate
import weaviate.classes as wvc

# Regular web-based packages
import requests
import json

# Pandas for reading CSV
import pandas as pd

# TQDM for progress bar on data upload
from tqdm.auto import tqdm


def create_collection(client, collection_name="lyrics"):
    """
    Create collections (in place, online) for the Weaviate instance.
    """
    if not client.collections.exists(collection_name):
        client.collections.create(
            name=collection_name,
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
            generative_config=wvc.config.Configure.Generative.openai()  # Ensure the `generative-openai` module is used for generative queries
        )
        print(f"Collection {collection_name} created.")
    else:
        print(f"Collection {collection_name} already exists, continuing.")


def read_data(fname = "all_lyrics.csv"):
    """
    Use pandas to read the song lyrics CSV that is stored locally.
    Default dataset is from: https://www.kaggle.com/datasets/elizzyliu/song-lyrics
    """
    df = pd.read_csv(fname)
    return df

def limit_tokens(x, max_tokens = 8192):
    if isinstance(x, str):
        return x[:max_tokens]

def add_data_to_client(client, collection_name, df, columns = [], max_tokens = 8192):
    """
    Given a pandas dataframe, add data information to the collection in the Weaviate client so that it can be vectorised.
    """

    if len(columns) == 0:
        columns = df.columns
    elif any([col not in df.columns for col in columns]):
        raise ValueError("Columns not found in dataframe.")

    # Enumerate df and add to client
    data = []

    n = len(df)
    n = min(n, 100) # limit to 100 for now for testing

    print("Adding data to client...")
    for i in tqdm(range(n)):

        d = df.iloc[i]

        # only add what is in the columns argument
        to_add = {c: limit_tokens(d[c], max_tokens) for c in columns}
        data.append(to_add)

    # add data to given collection
    collection = client.collections.get(collection_name)
    collection.data.insert_many(data)

if __name__ == "__main__":


    # Connect to Weaviate client
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url = weaviate_url,
        auth_credentials=weaviate.auth.AuthApiKey(weaviate_key),
        headers={
            "X-OpenAI-Api-Key": openai_key  # Replace with your inference API key
        }
    )

    # Print if successful connection
    if client.is_ready():
        print("Client connected successfully.")


    try:
        # Create collection and add data to it 
        create_collection(client, collection_name="lyrics")
        df = read_data("all_lyrics.csv")
        add_data_to_client(client, collection_name="lyrics", df=df)
        

        # test query
        questions = client.collections.get("lyrics")
        
        prompt = "im in love with myself"
        response = questions.generate.near_text(
            query=prompt,
            limit=1,
            single_prompt="Give a description of {song}, including the artist {artist} and genre {type}, with a brief overview of the meaning of the lyrics, especially how it relates to the prompt" + prompt
        )

        print(response.objects[0].generated)
        print(response.objects[0].properties)


    # close client after everything (even if errors)
    finally:
        client.close()
        


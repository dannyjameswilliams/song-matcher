

from keys import weaviate_key, weaviate_url, openai_key, spotify_id, spotify_secret

# Weaviate packages
import weaviate

# Regular web-based packages
import requests
# import json
import urllib.parse
import urllib

# Pandas for reading CSV
# import pandas as pd

# TQDM for progress bar on data upload
# from tqdm.auto import tqdm


def get_spotify_url(song, artist):

    auth_response = requests.post('https://accounts.spotify.com/api/token', {
        'grant_type': 'client_credentials',
        'client_id': spotify_id,
        'client_secret': spotify_secret,
    })

    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']

    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }


    query = urllib.parse.quote(f'{song} {artist}')
    response = requests.get(f'https://api.spotify.com/v1/search?q={query}&type=track', headers=headers)

    # Parse the response to get the Spotify URL of the song
    response_data = response.json()
    spotify_url = response_data['tracks']['items'][0]['external_urls']['spotify']

    return spotify_url


def query(client, input_text, collection_name):
    
    collection = client.collections.get(collection_name)

    response = collection.generate.near_text(
        query=input_text,
        limit=1,
        single_prompt="Give a description of {song}, including the artist {artist} and genre {type}, with a brief overview of the meaning of the lyrics, and how it relates to the idea of '" + input_text + "' without specifically mentioning it."   
    )

    return response, get_spotify_url(response.objects[0].properties["song"], response.objects[0].properties["artist"])
    

def app():

    client = weaviate.connect_to_weaviate_cloud(
        cluster_url = weaviate_url,
        auth_credentials=weaviate.auth.AuthApiKey(weaviate_key),
        headers={
            "X-OpenAI-Api-Key": openai_key  # Replace with your inference API key
        }
    )

    try:

        query(client, "hello", "lyrics")

    # close client after everything (even if errors)
    finally:
        client.close()
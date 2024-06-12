

from keys import weaviate_key, weaviate_url, openai_key, spotify_id, spotify_secret

# Weaviate packages
import weaviate

# Regular web-based packages
import requests
# import json
import urllib.parse
import urllib
from io import BytesIO

# random library for randomising the song choice
import random


# Flask for the app
from flask import Flask, jsonify, request

app = Flask(__name__)

from flask_cors import CORS
CORS(app)

# for getting colour palette of image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def get_palette(image_path, n_colors):
    response = requests.get(image_path)

    with Image.open(BytesIO(response.content)) as img:

        img.thumbnail((100, 100))

        # Convert the image data to a 2D array
        data = np.array(img)
        data = data.reshape(-1, 3)

        # Perform k-means clustering to find the most dominant colors
        kmeans = KMeans(n_clusters=n_colors)
        kmeans.fit(data)

    return ['#%02x%02x%02x' % tuple(map(int, color)) for color in kmeans.cluster_centers_]

def get_spotify_info(song, artist):

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
    album_image_url = response_data['tracks']['items'][0]["album"]["images"][0]["url"]

    return spotify_url, album_image_url


def query(client, input_text, collection_name):
    
    collection = client.collections.get(collection_name)

    # return 5 objects and randomise the choice within those
    response = collection.generate.near_text(
        query=input_text,
        limit=5,
        single_prompt="Give a description of {song}, including the artist {artist} and genre {type}, with a brief overview of the meaning of the lyrics, and how it relates to the idea of '" + input_text + "' without specifically mentioning it. The description should be only a VERY short paragraph."   
    )

    song_choice = random.choice(response.objects)

    spotify_info = get_spotify_info(song_choice.properties["song"], song_choice.properties["artist"])
    return (song_choice.properties, 
            song_choice.generated,
            spotify_info[0],
            spotify_info[1]
        )
    


if __name__ == "__main__":

    client = weaviate.connect_to_weaviate_cloud(
        cluster_url = weaviate_url,
        auth_credentials=weaviate.auth.AuthApiKey(weaviate_key),
        headers={
            "X-OpenAI-Api-Key": openai_key  # Replace with your inference API key
        }
    )

    @app.route('/api/submit', methods=['POST'])
    def react_query():
        data = request.json
        user_input = data.get('input')
        props, generated_text, spotify_url, album_image_url = query(client, user_input, "lyrics")

        song = props["song"]
        artist = props["artist"]
        palette = get_palette(album_image_url, 2)
        output = {
            "song": song,
            "artist":  artist, 
            "generated_text": generated_text, 
            "spotify_url": spotify_url,
            "album_image_url": album_image_url,
            "palette": palette
        }
        print(album_image_url)

        return jsonify(output)
    
    @app.route('/api/data', methods=['GET'])
    def get_data():
        data = {'message': 'Song Recommender!'}
        return jsonify(data)

    # @app.route('/api/submit', methods=['POST'])
    # def submit_data():
    #     data = request.json
    #     user_input = data.get('input')
    #     response_message = f'You sent: {user_input}'
    #     return jsonify({'message': response_message})

    app.run(port=5000, debug=True)

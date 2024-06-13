# 🎶 AI MoodSync 🎶 (song matcher)

## Introduction

A small web-app that matches a song to your input mood based on lyrics, using [Weaviate](https://weaviate.io/) and a [kaggle dataset](https://www.kaggle.com/datasets/elizzyliu/song-lyrics) of song lyrics.



### 📋 TODO 📋:
 - Add previously recommended history list
 - Use a larger database of songs
 - Implement multiple search strategies using more embedding models.

## How it works

First, the input mood or text given by the user is embedded via [OpenAI's text2vec embedding model](https://platform.openai.com/docs/guides/embeddings) as a high-dimensional vector.

Then, this embedding is compared to all the equivalent vectors in the song database via using [Weaviate](https://weaviate.io/)'s `near_text` query function, which returns the song with the most similar vector to the target input. This song is returned (with an element of randomness, so that the same search can yield up to 5 different songs) and displayed.

The backend of this app is developed in Python, and the front-end is developed in React.

## Installation

Provided that you have installed [Node.js](https://nodejs.org/en/download/package-manager) and [Python](https://www.python.org/downloads/), you can clone the github repository via
```bash
git clone https://github.com/dannyjameswilliams/song-matcher.git 
```
then enter the directory
```bash
cd song-matcher
```

### (Optional) Virtual Environment
I would recommend using a virtual python environment such as [conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html), and creating one with
```bash
conda create -n song-matcher
conda install pip
```

### Setting up Python
You can use `pip` to install the required python packages
```bash
pip install -r requirements.txt
```

### Setting up React
Navigate to the app directory via
```bash
cd app
```
and install the required packages with `npm`
```bash
npm install react
npm install axios
npm install react-spotify-embed
```




## Usage

## Credits


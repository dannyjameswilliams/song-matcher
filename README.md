# 🎶 AI MoodSync 🎶 (song matcher)

## ℹ Introduction

A small web-app that matches a song to your input mood based on lyrics, using [Weaviate](https://weaviate.io/) and a [kaggle dataset](https://www.kaggle.com/datasets/elizzyliu/song-lyrics) of song lyrics.

![til](https://raw.githubusercontent.com/dannyjameswilliams/song-matcher/main/example.gif)


### 📋 TODO 📋:
 - Add previously recommended history list
 - Use a larger database of songs
 - Implement multiple search strategies using more embedding models.

## 🛠 How it works

First, the input mood or text given by the user is embedded via [OpenAI's text2vec embedding model](https://platform.openai.com/docs/guides/embeddings) as a high-dimensional vector.

Then, this embedding is compared to all the equivalent vectors in the song database via using [Weaviate](https://weaviate.io/)'s `near_text` query function, which returns the song with the most similar vector to the target input. This song is returned (with an element of randomness, so that the same search can yield up to 5 different songs) and displayed.

The backend of this app is developed in Python, and the front-end is developed in React.

## 🚀 Installation

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
npm install 
```


## 🔦 Usage

We need to set up the front-end and the back-end separately. Ensure you are in the root directory (i.e. `.../song-finder` and not `.../song-finder/app`). The back-end is managed by Python and is located entirely within the home directory, and thus can be started via
```bash
python backend.py
```
This will run on port 5000, so make sure there is nothing else running on that port. If you would like to modify the port number, simply change `5000` in the line `app.run(port=5000, debug=False)` at the bottom of `backend.py` to a different value. Additionally, change any instances of `localhost:5000` inside of `app/App.js` to the new port number.

The front-end is entirely via React and you must first change to the `app` directory via
```bash
cd app
```
and then
```
npm start
```
This will run on port 3000, if you would like to change it, you can instead use 
```
PORT=XXXX npm start
```
which will change it to whatever number you replace `XXXX` with.

## 🪛 Modifications

If you would like to modify the code or app in any way, it should be relatively straightforward to figure out as the code should be fully commented and easy to understand.

Some ideas for modifications would be to change how the search works, or to change the embedding model of the songs/queries.


## Credits

- [Weaviate](https://weaviate.io/) for the Python library.
- OpenAI for the embedding model and generative model.
- 'Lizzie' for the [kaggle dataset](https://www.kaggle.com/datasets/elizzyliu/song-lyrics).




// obviously needed
import React, { useEffect, useState } from 'react';

// for fetching python stuff
import axios from 'axios';

// css
import './App.css';

// image 
import stars from './starssmall.png';


// invert a hex color (written by copilot) for text on background
function invertColor(hex) {
  if (hex.indexOf('#') === 0) {
    hex = hex.slice(1);
  }
  // convert 3-digit hex to 6-digits.
  if (hex.length === 3) {
    hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
  }
  if (hex.length !== 6) {
    throw new Error('Invalid HEX color.');
  }
  // invert color components
  var r = (255 - parseInt(hex.slice(0, 2), 16)).toString(16),
      g = (255 - parseInt(hex.slice(2, 4), 16)).toString(16),
      b = (255 - parseInt(hex.slice(4, 6), 16)).toString(16);
  // pad each with zeros and return
  return '#' + padZero(r) + padZero(g) + padZero(b);
}

// pad zeros (written by copilot) for invertColor
function padZero(str, len) {
  len = len || 2;
  var zeros = new Array(len).join('0');
  return (zeros + str).slice(-len);
}

// lighten a hex color (written by copilot) for background to be nicer
function lightenColor(color, percent) {
  var num = parseInt(color.replace("#",""), 16),
  amt = Math.round(2.55 * percent),
  R = (num >> 16) + amt,
  G = (num >> 8 & 0x00FF) + amt,
  B = (num & 0x0000FF) + amt;
  return "#" + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (G<255?G<1?0:G:255)*0x100 + (B<255?B<1?0:B:255)).toString(16).slice(1);
};

// JavaScript
function showLoader() {
  document.getElementById('loader').style.display = 'block';
}

function hideLoader() {
  document.getElementById('loader').style.display = 'none';
}

// main app function
function App() {
  const [input, setInput] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const [url, setUrl] = useState('');
  const [song, setSong] = useState('');
  const [artist, setArtist] = useState('');
  const [albumUrl, setAlbumUrl] = useState('');
  const [palette, setPalette] = useState([]);
  const [isLoading, setIsLoading] = useState(false);


  // form input
  const handleSubmit = (event) => {
    event.preventDefault();
    
    setIsLoading(true);

    axios.post('http://localhost:5000/api/submit', { input })
      .then(response => {

        setIsLoading(false);
        
        setResponseMessage(response.data.generated_text);
        setUrl(response.data.spotify_url);
        setSong(response.data.song);
        setArtist(response.data.artist);

        setAlbumUrl(response.data.album_image_url);

        setPalette(response.data.palette);
      })
      .catch(error => {
        setIsLoading(false);
        console.error('There was an error fetching the data!', error);
      });
  };

  let parts = url.split("/");
  let lastPart = parts[parts.length - 1];

  return (
        <div >
          <header className="App-header">
          <h1>AI Song Recommender</h1>
          <form onSubmit={handleSubmit}>
            <textarea
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter your mood..."
            />
            <button type="submit">🎶 Recommend</button>
            {isLoading && <div className="loader" id="loader"></div>}
          </form>
        </header>

        {/* Boxes for album art, song title, artist name, and recommendation */}
        {albumUrl &&
          <div className="center-box">

            <div className="imagebox" style={{ backgroundColor: lightenColor(palette[0], 5) }}>
              <div className="image-container">
                <img src={albumUrl} alt="Album art" />
                {song && <h1 style={{color: invertColor(palette[0]) }}> {song} </h1> }
                {artist && <h2 style={{color: invertColor(palette[1]) }}> {artist} </h2>}
              </div>
              <div className="text-right">
              </div>
            </div>

            <div className="textbox">
              <div className="image-container">
                <img src={stars} alt="AI generation symbol" />
              </div>
              
              {responseMessage && <p > {responseMessage} </p>}
            </div>
          </div>
        }

        {albumUrl &&
          <iframe src={`https://open.spotify.com/embed/track/${lastPart}`} width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        }

    </div>
  );
}

export default App;
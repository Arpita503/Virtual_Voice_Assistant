import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pyttsx3

# Initialize Spotify API credentials
SPOTIFY_CLIENT_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
SPOTIFY_CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
)

engine = pyttsx3.init()

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def search_and_play_song(song_name):
    """Search Spotify for a song and play it."""
    results = spotify.search(q=song_name, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        song_url = track['external_urls']['spotify']
        song_name = track['name']
        artist_name = ", ".join(artist['name'] for artist in track['artists'])

        # Play the song
        webbrowser.open(song_url)
        speak(f"Playing {song_name} by {artist_name} on Spotify.")
    else:
        speak(f"Sorry, I couldn't find the song {song_name} on Spotify.")


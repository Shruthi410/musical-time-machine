import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_secret=SPOTIFY_CLIENT_SECRET,
        client_id=SPOTIFY_CLIENT_ID,
        redirect_uri="http://example.com",
        cache_path="token.txt",
        show_dialog=True
    )
)

user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

all_songs = soup.find_all(name="span", class_="chart-element__information__song")

song_list = [song.getText() for song in all_songs]
print(song_list)

year = date.split("-")[0]

song_uris = []

for song in song_list:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

playlist_id = playlist["id"]

sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)

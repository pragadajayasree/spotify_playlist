import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pprint

inp = input("what year you would like to travel to in YYY-MM-DD format")
url = f"https://www.billboard.com/charts/hot-100/{inp}"
response = requests.get(url)
result = response.text

soup = BeautifulSoup(result, "html.parser")
p = soup.select("li ul li h3")

songs = []
for i in p:
    l = i.getText()
    songs.append(l.strip())

auth_manager = SpotifyOAuth(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    redirect_uri="http://example.com",
    scope="playlist-modify-private",
    username="songs",
    cache_path="token.txt",
    show_dialog=True,
)
sp = spotipy.Spotify(auth_manager=auth_manager)
user_id = sp.current_user()["id"]
year = inp.split("-")[0]
uri = []
for i in songs:
    result = sp.search(q=f"track:{i} year:{year}", type="track")
    try:
        uri_ = result["tracks"]["items"][0]["uri"]
        uri.append(uri_)
    except IndexError:
        print("not found")
playlist = sp.user_playlist_create(user=user_id, name=f"{inp} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=uri)
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

########VARIABLES######
SPOTIFY_ID = os.environ.get("SPOTIFY_ID")
SPOTIFY_SECRET = os.environ.get("SPOTIFY_SECRET")
SPOTIFY_USERNAME = os.environ.get("SPOTIFY_USERNAME")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

def generate_playlist(df):
    '''This function will access Spotify API and add playlist to your account.
    The playlist will be chosen randomly from the df.'''
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-public",
            redirect_uri=REDIRECT_URI,
            client_id=SPOTIFY_ID,
            client_secret=SPOTIFY_SECRET,
            show_dialog=True,
            cache_path="token.txt",
            username=SPOTIFY_USERNAME,
        )
    )
    user_id = sp.current_user()["id"]

    new_playlist = sp.user_playlist_create(user=user_id, name="Test_Playlist", public=True,
                                      description=None)
    new_playlist_id = new_playlist["id"]

    # Select some music from df.

    title_list_sample = list(df.sample(20)['track_name'])

    uri_list = []
    for value in range(20):
        spotify_result = sp.search(q=f"track:{title_list_sample[value]}",type="track", market="US")
        try:
            result_uri = spotify_result["tracks"]["items"][0]["uri"]
        except IndexError:
            pass
        else:
            uri_list.append(result_uri)

    sp.user_playlist_add_tracks(user=user_id, playlist_id=new_playlist_id, tracks=uri_list)

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Music_Selector_Project.params import *

def generate_playlist(df):
    '''This function will access Spotify API and add playlist to your account.
    The songs will be chosen randomly from the provided df.'''

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-public",
            redirect_uri=REDIRECT_URI,
            client_id=SPOTIFY_CLIENT_ID,
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

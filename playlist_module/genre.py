import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
from playlist_module.params import *

def get_genre():
    '''This function accesses Spotify user data and collect
    which genres the user like'''

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='user-library-read',
                                               username=SPOTIFY_USERNAME))

    #Collect liked tracks in your Spotify account
    saved_tracks = sp.current_user_saved_tracks()['items']

    track_titles1 = []
    for track in saved_tracks:
        track_titles1.append(track['track']['name'])

    #Collect track information from all the playlists
    playlists = sp.current_user_playlists()
    all_tracks = []
    for playlist in playlists['items']:
        playlist_tracks = sp.playlist_tracks(playlist['id'])
        all_tracks.append(playlist_tracks['items'])
    track_titles2 = []
    for track in all_tracks:
        track_titles2.append(track['track']['name'])

    all_titles = track_titles1+track_titles2
    print(all_tracks)

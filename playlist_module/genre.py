import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
from playlist_module.params import *

def get_genre():
    '''This function accesses Spotify user data and collect
    which genres the user liked'''

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='user-library-read',
                                               username=SPOTIFY_USERNAME))

    #Collect saved tracks in your Spotify account
    saved_tracks = sp.current_user_saved_tracks()['items']

    track_titles1 = []
    for track in saved_tracks:
        track_titles1.append(track['track']['name'])

    #Collect track information from all the saved playlists
    playlists = sp.current_user_playlists()
    all_playlists_info = []
    for playlist in playlists['items']:
        playlist_tracks = sp.playlist_tracks(playlist['id'])
        all_playlists_info.extend(playlist_tracks['items'])
    tracks_titles2 = [value['track']['name'] for value in all_playlists_info]

    #Get all the titles of tracks in user account.
    all_titles = track_titles1 + tracks_titles2

    #Extract genres of each tracks
    df = pd.read_csv('raw_data/spotify_dataset.csv')
    list_genre = []
    for title in all_titles:
        list_genre.extend(df.loc[df['track_name']==title]['track_genre'].to_list())

    user_genre = set(list_genre)

    return user_genre

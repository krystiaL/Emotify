import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
from playlist_module.params import *
#from functools import reduce

def get_genre():
    '''This function accesses Spotify user data and collect
    which genres the user liked
    -the returned variable will be fed to generate_playlist.tailor_df function'''

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
    df = pd.read_csv('raw_data/new_df_labeled.csv')

    list_genre = []
    for title in all_titles:
        list_genre.extend(df[df['name']==title]['track_genre_split'])

    user_genre = set([item.strip(" '[]") for sublist in list_genre for item in sublist.split(', ')])
    print(user_genre)
    print(len(user_genre))

    return user_genre

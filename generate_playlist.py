import spotipy
from spotipy.oauth2 import SpotifyOAuth
from params import *
from preprocess_df import kaggle_preprocess
from neuro_model import create_model

def tailor_df(emotion:str):
    '''This function takes emotion input from facial recognition
    and outputs a dataframe tailored for that emotion'''
    df = kaggle_preprocess(model=create_model()[0],scaler=create_model()[1])
    if emotion == 'anger' or 'disgust' or 'fear':
        mood_df = df.sort_values('mood_Calm',ascending=False).head(200)
        mood_df = mood_df.sort_values('mood_Energetic',ascending=True).head(100).sample(10)

    elif emotion == 'enthusiasm':
        mood_df = df.sort_values('mood_Energetic',ascending=False).head(200)
        mood_df = mood_df.sort_values('mood_Calm',ascending=True).head(100).sample(10)

    elif emotion == 'happiness' or 'neutral':
        mood_df = df.sort_values('mood_Happy',ascending=False).head(200)
        mood_df = mood_df.sort_values('mood_Sad',ascending=True).head(100).sample(10)

    else:
        mood_df = df.sort_values('mood_Sad',ascending=False).head(200)
        mood_df = mood_df.sort_values('mood_Happy',ascending=True).head(100).sample(10)

    return mood_df

def generate_playlist(emotion:str,account_name):
    '''This function will access Spotify API and add playlist to the developer's account.
    -The songs will be chosen randomly from the provided df.
    -ID of the playlist will be fed to send_playlist_id function'''

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
    title = f"{emotion.capitalize()} playlist for you, {account_name}!"

    new_playlist = sp.user_playlist_create(user=user_id, name=title, public=True,
                                      description=None)
    new_playlist_id = new_playlist["id"]

    # Select some music from df.
    title_list_sample = list(tailor_df(emotion=emotion).sample(10)['name'])

    uri_list = []
    for value in range(10):
        spotify_result = sp.search(q=f"track:{title_list_sample[value]}",type="track", market="US")
        try:
            result_uri = spotify_result["tracks"]["items"][0]["uri"]
        except IndexError:
            pass
        else:
            uri_list.append(result_uri)

    sp.user_playlist_add_tracks(user=user_id, playlist_id=new_playlist_id, tracks=uri_list)
    return title

def send_playlist_id(emotion:str,account_name):

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-read-private",
            redirect_uri=REDIRECT_URI,
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_SECRET,
            show_dialog=True,
            cache_path="token.txt",
            username=SPOTIFY_USERNAME,
        )
    )

    # Replace 'your_playlist_name' with the name of your playlist
    playlist_name = generate_playlist(emotion=emotion,account_name=account_name)

    # Get the user's playlists
    playlists = sp.current_user_playlists()

    # Search for the playlist by name
    playlist_id = None
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            break

    playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
    # Print the playlist ID
    if playlist_id:
        print(f"The ID of the playlist '{playlist_name}' is: {playlist_id}n\
            The url is {playlist_url}")
    else:
        print(f"Playlist '{playlist_name}' not found in your account.")

    return playlist_url

send_playlist_id(emotion='Happy',account_name='Test')

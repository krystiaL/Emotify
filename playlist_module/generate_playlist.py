import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
from playlist_module.params import *
from playlist_module.genre import get_genre
from sklearn.metrics import mean_squared_error
#from face_detect_module.read_video_file_ok import *

def process_emotion():
    '''This function imports emotion_weights from face_detect_module and outputs
    which emotion was dominant in the video clip.'''
    import_emotion = {'Anger': [0.2, 0.2, 0.2, 0.2, 0.21, 0.21, 0.21, 0.21, 0.2, 0.2, 0.21, 0.2, 0.2, 0.18, 0.18, 0.18],
                    'Sadness': [0.19, 0.2, 0.21, 0.21, 0.2, 0.21, 0.24, 0.23, 0.24, 0.24, 0.24, 0.25, 0.24, 0.22, 0.2,\
                        0.24, 0.26, 0.29, 0.27, 0.27, 0.27, 0.25, 0.28, 0.32, 0.36, 0.4, 0.43, 0.44, 0.45, 0.43, 0.42, 0.38, 0.34, 0.31, 0.27, 0.24, 0.23, 0.23],
                    'Happiness': [0.22, 0.23, 0.24, 0.24, 0.23, 0.22, 0.22, 0.2, 0.19, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.3, 0.28, 0.27, 0.24, 0.29, 0.29, 0.29, 0.28, 0.27],
                    'Neutral': [0.19, 0.18]}
    imported_emotion = {key:len(value) for key,value in import_emotion.items()}
    imported_emotion = {key:value/sum(imported_emotion.values()) for key,value in imported_emotion.items()}

    emotion_variation = ['Neutral','Happiness','Sadness','Surprise','Fear','Disgust','Anger']
    for element in emotion_variation:
        if element not in imported_emotion.keys():
            imported_emotion[element] = 0

    user_emotion = {
        'mood_Calm':imported_emotion['Fear']+imported_emotion['Disgust']+imported_emotion['Anger'],
        'mood_Energetic':imported_emotion['Surprise'],
        'mood_Happy':imported_emotion['Happiness']+imported_emotion['Neutral'],
        'mood_Sad':imported_emotion['Sadness']
    }

    dominant_emotion = [key for key,val in user_emotion.items() if val==max(user_emotion.values())]

    return dominant_emotion,user_emotion

def tailor_df():
    '''This function takes emotion input from facial recognition
    and outputs a dataframe tailored for that emotion'''

    df = pd.read_csv('raw_data/new_df_labeled.csv')
    emotion_target = process_emotion()[1].values()

    df['target_distance'] = 0
    for x in range(df.shape[0]):
        df['target_distance'].iloc[x] = mean_squared_error(df[['mood_Calm', 'mood_Energetic', 'mood_Happy', 'mood_Sad']].iloc[x],list(emotion_target))

    mood_df = df.sort_values('target_distance').head(200)
    print(mood_df.head())

    #Select genres that user likes
    # user_genre = get_genre()

    # def check_genre(list,set=user_genre):
    #     boolean_list=[]
    #     for element in list:
    #         if not element:
    #             boolean_list.append(element in set)
    #     if sum(boolean_list) >= 1:
    #         return True

    # df = df[df['track_genre_split'].apply(check_genre)]

    # print(df.shape)

    return mood_df

def generate_playlist(emotion,account_name):
    '''This function will access Spotify API and add playlist to the developer's account.
    -The songs will be chosen randomly from the provided df.
    -ID of the playlist will be fed to send_playlist_id function
    -title_list will be fed to UX module.'''

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
    title = f"{emotion[0].capitalize()} playlist for you, {account_name}!"

    new_playlist = sp.user_playlist_create(user=user_id, name=title, public=True,
                                      description=None)
    new_playlist_id = new_playlist["id"]

    # Randomly select music from tailored df.
    title_list = list(tailor_df().sample(10)['name'])

    uri_list = []
    for value in range(10):
        spotify_result = sp.search(q=f"track:{title_list[value]}",type="track", market="US")
        try:
            result_uri = spotify_result["tracks"]["items"][0]["uri"]
        except IndexError:
            pass
        else:
            uri_list.append(result_uri)

    sp.user_playlist_add_tracks(user=user_id, playlist_id=new_playlist_id, tracks=uri_list)
    return title,sp,title_list

def send_playlist_id(account_name):
    '''This function returns the url of the generated playlist on Spotify webpage.
    -The url will be fed to UX module.'''

    playlist_object = generate_playlist(emotion=process_emotion()[0],account_name=account_name)
    playlist_name = playlist_object[0]
    sp = playlist_object[1]

    # Get the user's playlists
    playlists = sp.current_user_playlists()

    # Search for the playlist by name
    playlist_id = None
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            break
    playlist_url = f"https://open.spotify.com/embed/playlist/{playlist_id}?utm_source=generator"

    # Print the playlist ID
    if playlist_id:
        print(f"{playlist_name} Here is the link:{playlist_url}")
    else:
        print(f"Playlist '{playlist_name}' not found in your account.")

    return playlist_url

if __name__=="__main__":
    # Account_name will be fed from UX module.
    # Emotion will be fed from Facial Recognition module.
    send_playlist_id(account_name='Test_Name')

import spotipy
import pandas as pd
import random
import streamlit as st
from spotipy.oauth2 import SpotifyOAuth
from playlist_module.params import *
from sklearn.metrics import mean_squared_error

def process_emotion(emotion):
    '''This function imports emotion_weights from face_detect_module and outputs
    which emotion was dominant in the video clip.'''

    import_emotion = emotion
    imported_emotion = {}
    for dictionary in import_emotion:
        for key, value in dictionary.items():
            if isinstance(value, list):
                imported_emotion[key] = len(value)
            else:
                imported_emotion[key] = value

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

def tailor_df(process_emo_out):
    '''This function takes emotion input from facial recognition
    and outputs a dataframe tailored for that emotion'''

    df = pd.read_csv('raw_data/new_df_labeled.csv')
    user_emotion = process_emo_out[1]
    dominant_emotion = process_emo_out[0]
    emotion_target = user_emotion.values()

    df['target_distance'] = 0.00
    for x in range(df.shape[0]):
        df.loc[x,'target_distance'] = float(mean_squared_error(df[['mood_Calm', 'mood_Energetic', 'mood_Happy', 'mood_Sad']].iloc[x],list(emotion_target)))

    if dominant_emotion=='mood_Calm' or 'mood_Sad':
        df = df[df['valence']<=0.5]
    elif dominant_emotion=='mood_Energetic' or 'mood_Happy':
        df = df[df['valence']>0.5]

    mood_df = df.sort_values('target_distance').head(50)
    print(mood_df['name'].head())

    return mood_df,user_emotion

def generate_playlist(emotion_df, account_name):
    '''This function will access Spotify API and add playlist to the developer's account.
    -The songs will be chosen randomly from the provided df.
    -ID of the playlist will be fed to send_playlist_id function
    -title_list will be fed to UX module.'''

    if 'code' not in st.session_state:
        sp_oauth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                client_secret=SPOTIFY_SECRET,
                                redirect_uri=REDIRECT_URI,
                                username=SPOTIFY_USERNAME,
                                scope='playlist-modify-public')
        st.session_state["sp_oauth"] = sp_oauth
        st.markdown("""<h1 style="font-size: 20px; text-align: center; color: #faaa0b">
        'Spotify Authentication'
        </h1>""",unsafe_allow_html=True)

        auth_url = sp_oauth.get_authorize_url()
        st.write(f"[Click here to authenticate with Spotify]({auth_url})")

        auth_code = st.text_input("Please enter the code below:")

        # Retrieve access token using the authorization code
        token_info = sp_oauth.get_access_token(auth_code)
        access_token = token_info['access_token']

        # Use the access token to create a Spotify object
        sp = spotipy.Spotify(auth=access_token)
        st.success("Successfully authenticated with Spotify!")

    user_id = sp.current_user()["id"]
    tailor_object = emotion_df
    user_emotion = tailor_object[1]

    dominant_emotion = max(user_emotion, key=user_emotion.get)

    #Give playlist a title
    if dominant_emotion == 'mood_Calm':
        playlist_title = random.choice(['Sooth Your Mind',"Serenity Soundscape",
                                        "Calm Canvas Collection","Peaceful Playlist",
                                        "Calm the Storm Within","Melodies of Peace",
                                        "Embrace Serenity","Soothing Soundwaves",
                                        "Harmony Haven","Tranquility Tunes"])

    elif dominant_emotion == 'mood_Energetic':
        playlist_title = random.choice(["High Voltage Hits","Energetic Explosion",
                                        "Powerhouse Playlist","Adrenaline Anthem Asylum",
                                        "Vibrant Vitality Vibes","Dynamic Drive",
                                        "Pulsating Power Tracks","Fired Up Frenzy",
                                        "Epic Energy Ensemble","Revved-Up Rhythms"])

    elif dominant_emotion == 'mood_Happy':
        playlist_title = random.choice(["Joyful Jams","Sunshine Serenade",
                                        "Smile Sessions","Dance of Delight",
                                        "Cheerful Melodies Mix","Positive Vibes Playlist",
                                        "Uplifting Utopia","Ecstatic Euphony",
                                        "Radiant Rhythms","Blissful Beats"])
    elif dominant_emotion == 'mood_Sad':
        playlist_title = random.choice(["Melancholy Melodies","Heartache Harmony",
                                        "Sorrowful Symphony","Gloomy Groove Gallery",
                                        "Tearful Tunes","Somber Serenade",
                                        "Emotional Echoes","Lonely Lamentations",
                                        "Pensive Playlist","Wistful Waters"])

    dominant_percentage = int(user_emotion[dominant_emotion] * 100)
    title = f"TuneOut: {playlist_title}"

    new_playlist = sp.user_playlist_create(user=user_id, name=title, public=True,
                                    description=None)
    new_playlist_id = new_playlist["id"]

    # Randomly select music from tailored df.
    title_list = list(tailor_object[0].sample(10)['name'])

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
    return [title, sp, title_list, dominant_emotion]

# generate_playlist = generate_playlist(emotion_df=emotion_df, account_name=account_name)

def send_playlist_id(generated_playlist, account_name):
    '''This function returns the url of the generated playlist on Spotify webpage.
    -The url will be fed to UX module.'''

    playlist_object = generated_playlist
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

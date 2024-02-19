import pandas as pd
from playlist_module.neuro_model import create_model
from playlist_module.genre import get_genre

def kaggle_preprocess():
    '''This function takes neuro network model and preprocess kaggle df.
    Returns a dataframe that feeds generate_playlist.py'''
    model_object = create_model()

    model = model_object[0]
    scaler = model_object[1]

    kaggle_df = pd.read_csv('raw_data/spotify_dataset.csv')
    kaggle_df = kaggle_df.rename(columns={'track_id':'id','artists':'artist','album_name':'album',
                          'track_name':'name','duration_ms':'length'})

    #Drop unnecessary columns (These columns are not included in 686_df)
    kaggle_df = kaggle_df.drop(columns={'explicit','mode','Unnamed: 0'})

    #Reorder the columns in kaggle database to match 686_df columns
    column_list = ['name','album','artist','id','popularity','length',
                'danceability','acousticness','energy','instrumentalness',
                'liveness','valence','loudness','speechiness','tempo',
                'key','time_signature','track_genre']
    kaggle_df = kaggle_df[column_list]

    #Drop duplicated rows from kaggle_df
    kaggle_df = kaggle_df.drop_duplicates(subset='name')

    #Drop tracks which have outlier features.
    kaggle_df = kaggle_df[kaggle_df['length']<400000]
    kaggle_df = kaggle_df[kaggle_df['liveness']<0.3]
    kaggle_df = kaggle_df[kaggle_df['loudness']>-30]
    kaggle_df = kaggle_df[kaggle_df['speechiness']<0.1]

    #Select genres that user likes
    user_genre = get_genre()

    genre_to_exclude = {'grunge','guitar','gospel','anime','children','brazil','german',
                         'kids','malay','opera','mandopop','iranian','comedy','cantopop'
                        'pagode','piano','salsa','samba','sertanejo','sleep','tango','turkish',
                        'world-music','folk','classical','indian','study','forro','j-idol','pop-film'}

    kaggle_df = kaggle_df[kaggle_df['track_genre'].isin(user_genre)]
    kaggle_df = kaggle_df[~kaggle_df['track_genre'].isin(genre_to_exclude)]

    #Scale the dataframe
    kaggle_df_scaled = scaler.transform(kaggle_df[['length', 'danceability',
       'acousticness', 'energy', 'instrumentalness', 'liveness', 'valence',
       'loudness', 'speechiness', 'tempo', 'key', 'time_signature']])

    kaggle_mood = model.predict(kaggle_df_scaled)
    kaggle_df[['mood_Calm', 'mood_Energetic', 'mood_Happy', 'mood_Sad']] = kaggle_mood

    print(kaggle_df.shape)
    kaggle_df.to_csv('raw_data/kaggle_df_labeled.csv')

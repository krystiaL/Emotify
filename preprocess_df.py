import pandas as pd

def kaggle_preprocess(model,scaler):
    '''This function takes neuro network model and preprocess kaggle df.
    Returns a dataframe that feeds generate_playlist.py'''

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

    #Drop songs that don't match the goal of this project
    kaggle_df = kaggle_df[(kaggle_df['speechiness']>0.33) & (kaggle_df['speechiness']<0.50)]
    kaggle_df = kaggle_df[kaggle_df['liveness']<0.8]
    kaggle_df = kaggle_df[kaggle_df['instrumentalness']<0.9]

    genres_to_exclude = {'grunge','guitar','gospel','anime','children','brazil','german',
                         'kids','malay','opera','mandopop','iranian','comedy','cantopop'
                        'pagode','piano','salsa','samba','sertanejo','sleep','tango','turkish',
                        'world-music','folk','classical','indian','study','forro','j-idol','pop-film'}

    kaggle_df = kaggle_df[~kaggle_df['track_genre'].isin(genres_to_exclude)]

    #Scale the dataframe
    kaggle_df_scaled = scaler.transform(kaggle_df[['length', 'danceability',
       'acousticness', 'energy', 'instrumentalness', 'liveness', 'valence',
       'loudness', 'speechiness', 'tempo', 'key', 'time_signature']])

    kaggle_mood = model.predict(kaggle_df_scaled)
    kaggle_df[['mood_Calm', 'mood_Energetic', 'mood_Happy', 'mood_Sad']] = kaggle_mood

    return kaggle_df

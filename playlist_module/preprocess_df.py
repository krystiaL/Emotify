import pandas as pd
from playlist_module.neuro_model import create_model

def df_preprocess():
    '''This function takes neuro network model and preprocess kaggle df.
    Returns a dataframe that feeds generate_playlist.py'''
    model_object = create_model()

    model = model_object[0]
    scaler = model_object[1]

    new_df = pd.read_csv('raw_data/top_5340_2000-now.csv')

    #Drop unnecessary columns and clean up(These columns are not included in new_df)
    new_df = new_df.drop(columns={'Artist URI(s)','Album URI', 'Album Artist URI(s)','Album Artist Name(s)',
                      'Album Image URL','Disc Number', 'Track Number',
                      'Track Preview URL', 'Explicit', 'ISRC', 'Added By','Added At',
                      'Album Genres','Label', 'Copyrights','Mode'})
    new_df = new_df.drop_duplicates()
    new_df = new_df[new_df['Danceability'].isna()==False]
    new_df = new_df[new_df['Track Name'].isna()==False]

    #Rename each columns to match those of new_df
    new_df = new_df.rename(columns={'Track Name':'name','Album Name':'album','Artist Name(s)':'artist',
                                    'Track URI':'id','Album Release Date':'release_date','Popularity':'popularity',
                                    'Track Duration (ms)':'length','Danceability':'danceability','Acousticness':'acousticness',
                                    'Energy':'energy','Instrumentalness':'instrumentalness','Liveness':'liveness',
                                    'Valence':'valence','Tempo':'tempo','Key':'key','Time Signature':'time_signature',
                                    'Loudness':'loudness','Speechiness':'speechiness','Artist Genres':'track_genre'})

    #Reorder the columns in kaggle database to match new_df columns
    column_list = ['name','album','artist','id','popularity','length',
                'danceability','acousticness','energy','instrumentalness',
                'liveness','valence','loudness','speechiness','tempo',
                'key','time_signature','track_genre']
    new_df = new_df[column_list]

    #Split the track_genre
    new_df['track_genre_split'] = new_df['track_genre'].apply(lambda x:x.split(',') if pd.notna(x) else [])
    new_df = new_df.drop(columns={'track_genre'})

    #Drop tracks which have outlier features.
    new_df = new_df[new_df['length']<400000]
    new_df = new_df[new_df['liveness']<0.3]
    new_df = new_df[new_df['loudness']>-30]

    #Scale the dataframe
    new_df_scaled = scaler.transform(new_df[['length', 'danceability',
       'acousticness', 'energy', 'instrumentalness', 'liveness', 'valence',
       'loudness', 'speechiness', 'tempo', 'key', 'time_signature']])

    new_df_mood = model.predict(new_df_scaled)
    new_df[['mood_Calm', 'mood_Energetic', 'mood_Happy', 'mood_Sad']] = new_df_mood

    print(new_df.shape)
    new_df.to_csv('raw_data/new_df_labeled.csv')

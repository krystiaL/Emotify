import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from scikeras.wrappers import KerasClassifier
from tensorflow.keras import utils
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score, KFold

def base_model():
    model = Sequential()
    model.add(Dense(8, input_dim=10, activation='relu'))
    model.add(Dense(4, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def predict_mood(preds, pip, target):
    preds_features = np.array(preds).reshape(1, -1)
    results = pip.predict(preds_features)
    mood_index = np.argmax(results)
    mood = np.array(target['mood'][target['encode'] == mood_index])
    return str(mood[0])

def main():
    # Load and preprocess the Spotify data
    spotify_df = pd.read_csv('dataset.csv')
    spotify_df.dropna(inplace=True)

    mood_prep = spotify_df[['duration_ms', 'danceability', 'acousticness', 'energy', 'instrumentalness',
                            'liveness', 'valence', 'loudness', 'speechiness', 'tempo']]
    col_features = mood_prep.columns[:]

    # Normalize the features
    scaler = MinMaxScaler()
    mood_trans = scaler.fit_transform(mood_prep[col_features])
    mood_trans_np = np.array(mood_prep[col_features])

    # Load the mood data
    df = pd.read_csv('data_moods.csv')
    cl_features = df.columns[6:-3]
    X = MinMaxScaler().fit_transform(df[cl_features])
    X2 = np.array(df[cl_features])
    Y = df['mood']

    # Encode the mood labels
    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_y = encoder.transform(Y)
    dummy_y = utils.to_categorical(encoded_y)

    # Split the data
    X_train, X_test, Y_train, Y_test = train_test_split(X, encoded_y, test_size=0.2, random_state=15)

    # Create target dataframe
    target = pd.DataFrame({'mood': df['mood'].tolist(), 'encode': encoded_y}).drop_duplicates().sort_values(['encode'], ascending=True)

    # Configure the model
    estimator = KerasClassifier(build_fn=base_model, epochs=300, batch_size=200, verbose=0)

    # Evaluate the model using KFold cross-validation
    kfold = KFold(n_splits=10, shuffle=True)
    results = cross_val_score(estimator, X, dummy_y, cv=kfold)
    print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

    # Fit the model and scaler in a Pipeline
    pip = Pipeline([('minmaxscaler', MinMaxScaler()), ('keras', KerasClassifier(build_fn=base_model, epochs=300, batch_size=200, verbose=0))])
    pip.fit(X2, dummy_y)

    # Make predictions and update the original dataframe
    res = [predict_mood(mood_trans_np[i], pip, target) for i in range(len(mood_trans_np))]

    spotify_df['Mood'] = np.resize(res, len(spotify_df))

    # Save the updated dataframe to a CSV file
    spotify_df.to_csv('MusicMoodFinal.csv')

if __name__ == "__main__":
    main()

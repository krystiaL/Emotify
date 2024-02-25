import pandas as pd
from sklearn.preprocessing import OneHotEncoder,RobustScaler
from sklearn.model_selection import train_test_split
from tensorflow import keras


def create_model():
    '''This function returns a neuro network model trained on a labeled dataset
    Returns a model.'''
    #Import dataset which already has emotion label.

    train_df = pd.read_csv('raw_data/trainset_new.csv')

    #Create a Deep Learning model based on this df.
    #Encode the target column.
    oh_encoder = OneHotEncoder(sparse_output=False)
    oh_encoder.fit(train_df[['mood']])
    train_df[oh_encoder.get_feature_names_out()] = oh_encoder.transform(train_df[['mood']])
    train_df.drop(columns=['mood'],inplace=True)

    #Split the dataframe
    y = train_df[['mood_Calm','mood_Energetic','mood_Happy','mood_Sad']]
    X = train_df[['length','danceability','acousticness','energy',
                'instrumentalness','liveness','valence','loudness',
                'speechiness','tempo','key','time_signature']]
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=42)

    #Robust scaling
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    #Deep Learning model
    model = keras.models.Sequential()

    # Neuronet for df_686
    # model.add(keras.layers.Dense(20,activation='relu',input_dim=12))
    # model.add(keras.layers.Dropout(rate=0.2))

    # model.add(keras.layers.Dense(10,activation='relu'))
    # model.add(keras.layers.Dropout(rate=0.2))

    # model.add(keras.layers.Dense(4,activation='softmax'))

    model.add(keras.layers.Dense(30,activation='relu',input_dim=12))
    model.add(keras.layers.Dropout(rate=0.3))

    model.add(keras.layers.Dense(10,activation='relu'))
    model.add(keras.layers.Dropout(rate=0.2))

    model.add(keras.layers.Dense(4,activation='softmax'))

    model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

    es = keras.callbacks.EarlyStopping(patience=30)

    model.fit(X_train_scaled,y_train,
                validation_split=0.3,
                batch_size=16,
                epochs=300,
                callbacks=[es])
    result = model.evaluate(X_test_scaled,y_test)
    print(f'Loss:{result[0]},Accuracy:{result[1]}')

    return model,scaler

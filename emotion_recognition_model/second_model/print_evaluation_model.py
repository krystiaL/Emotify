import tensorflow as tf
import keras
from keras import backend as K
import numpy as np
from keras.preprocessing.image import img_to_array, load_img

# Define custom f1_score function
def f1_score(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val

# Load the model
model = keras.models.load_model("emotion_recognition_model/my_h5_model_epoch50.h5", custom_objects={'BatchNormalization': tf.keras.layers.BatchNormalization, 'f1_score': f1_score})

# Load the test dataset
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

test_datagen = ImageDataGenerator(rescale=1./255)
test_dataset = test_datagen.flow_from_directory(directory=os.path.join(os.getcwd(), "emotion_recognition_model/input/fer2013/test/"),
                                                target_size=(48, 48),
                                                class_mode='categorical',
                                                batch_size=64)

# Define metrics including custom f1_score
METRICS = [
      tf.keras.metrics.BinaryAccuracy(name='accuracy'),
      tf.keras.metrics.Precision(name='precision'),
      tf.keras.metrics.Recall(name='recall'),
      tf.keras.metrics.AUC(name='auc'),
      f1_score,
]

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=METRICS)

# Evaluate the model
evaluation_result = model.evaluate(test_dataset, verbose=0)

# Print the name and value of each metric
for metric_name, metric_value in zip(model.metrics_names, evaluation_result):
    print(f"{metric_name}: {metric_value}")

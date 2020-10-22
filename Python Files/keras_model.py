from tensorflow import keras
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras import layers
import h5py
import re
import string
import tensorflow as tf

PATH = "assets/weights_text.h5"
h5 = h5py.File(PATH, 'r')

PATH_2 = "assets/xtreme_lite_weights_text.h5"
h5 = h5py.File(PATH_2, 'r')

def create_end_to_end_model(weights_path = PATH):
  '''
  Creates a model that accepts text as input and outputs a prediction from 0 to 1
  classifying success as a kickstarter

  weights_path is the path to the weight set for the inner function: create_model

  returns an instantiated tensorflow Model class
  '''

  max_features = 20000
  embedding_dim = 128
  sequence_length = 1000
  
  def create_model(max_features = max_features, embedding_dim = embedding_dim):
    '''
    Creates a model which was trained on a vectorized list of text and a 
    corresponding list of numbers as input. Each text line is a 'blurb' from a 
    kickstarter project describing the purpose of the project and each label is
    a 0 or 1, where 0 signifies that the funding goal was not met, and 
    1 signifies that the goal was met

    returns an instantiated tensorflow model class
    '''
    # A integer input for vocab indices.
    inputs = tf.keras.Input(shape=(None,), dtype="int64")

    # Next, we add a layer to map those vocab indices into a space of dimensionality
    # 'embedding_dim'.
    x = layers.Embedding(max_features, embedding_dim)(inputs)
    x = layers.Dropout(0.5)(x)

    # Conv1D + global max pooling
    x = layers.Conv1D(128, 7, padding="same", activation="relu", strides=3)(x)
    x = layers.Conv1D(128, 7, padding="same", activation="relu", strides=3)(x)
    x = layers.GlobalMaxPooling1D()(x)

    # We add a vanilla hidden layer:
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.5)(x)

    # We project onto a single unit output layer, and squash it with a sigmoid:
    predictions = layers.Dense(1, activation="sigmoid", name="predictions")(x)

    model = tf.keras.Model(inputs, predictions)

    # Compile the model with binary crossentropy loss and an adam optimizer.
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model

  def custom_standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    return tf.strings.regex_replace(
        lowercase, "[%s]" % re.escape(string.punctuation), ""
    )

  model = create_model()
  model.load_weights(weights_path)

  inputs = tf.keras.Input(shape=(1,), dtype="string")
  # Turn strings into vocab indices
  vectorize_layer = TextVectorization(
    standardize=custom_standardization,
    max_tokens=max_features,
    output_mode="int",
    output_sequence_length=sequence_length,
  )
  indices = vectorize_layer(inputs)
  # Turn vocab indices into predictions
  outputs = model(indices)

  # Our end to end model
  end_to_end_model = tf.keras.Model(inputs, outputs)
  end_to_end_model.compile(
      loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"]
  )
  return end_to_end_model
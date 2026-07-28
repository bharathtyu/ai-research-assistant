import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense, Dropout

from src.ml.dataset_prep import load_dataset


MAX_WORDS = 5000
MAX_LEN = 100


def train_model():
    # Load dataset
    texts, labels, label_encoder = load_dataset()

    # Create tokenizer
    tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)

    sequences = tokenizer.texts_to_sequences(texts)
    padded = pad_sequences(
        sequences,
        maxlen=MAX_LEN,
        padding="post",
        truncating="post"
    )

    # Build model
    model = Sequential([
        Embedding(MAX_WORDS, 64, input_length=MAX_LEN),
        GlobalAveragePooling1D(),
        Dense(64, activation="relu"),
        Dropout(0.3),
        Dense(len(label_encoder.classes_), activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    print("Training model...\n")

    model.fit(
        padded,
        labels,
        epochs=20,
        batch_size=4,
        verbose=1
    )

    # Save model
    model.save("models/tf_classifier.h5")

    # Save tokenizer
    with open("models/tokenizer.pickle", "wb") as f:
        pickle.dump(tokenizer, f)

    print("\nModel saved successfully!")
    print("Saved: models/tf_classifier.h5")
    print("Saved: models/tokenizer.pickle")


if __name__ == "__main__":
    train_model()
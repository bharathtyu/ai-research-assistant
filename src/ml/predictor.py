import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences


MAX_LEN = 100


class DocumentClassifier:

    def __init__(self):
        self.model = tf.keras.models.load_model("models/tf_classifier.h5")

        with open("models/tokenizer.pickle", "rb") as f:
            self.tokenizer = pickle.load(f)

        with open("models/label_encoder.pkl", "rb") as f:
            self.label_encoder = pickle.load(f)

    def predict(self, text):

        sequence = self.tokenizer.texts_to_sequences([text])

        padded = pad_sequences(
            sequence,
            maxlen=MAX_LEN,
            padding="post",
            truncating="post"
        )

        prediction = self.model.predict(padded, verbose=0)

        index = np.argmax(prediction)

        category = category = str(self.label_encoder.inverse_transform([index])[0])

        confidence = float(np.max(prediction))

        return {
            "category": category,
            "confidence": round(confidence, 4)
        }


if __name__ == "__main__":

    classifier = DocumentClassifier()

    sample = """
    TensorFlow is a deep learning framework used to build
    neural networks for AI applications.
    """

    result = classifier.predict(sample)

    print(result)
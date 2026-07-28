import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle


def load_dataset(csv_path="data/dataset/training_data.csv"):
    # Read CSV file
    df = pd.read_csv(csv_path)

    # Get text and category columns
    texts = df["text"].astype(str).tolist()
    labels = df["category"].astype(str).tolist()

    # Convert category names to numbers
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)

    # Save the label encoder
    with open("models/label_encoder.pkl", "wb") as f:
        pickle.dump(label_encoder, f)

    print("Dataset loaded successfully.")
    print(f"Total Samples: {len(texts)}")
    print(f"Categories: {list(label_encoder.classes_)}")

    return texts, encoded_labels, label_encoder


if __name__ == "__main__":
    load_dataset()
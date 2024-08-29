import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os
import joblib
import logging
import pprint as pp


class TfidfHelper:
    def __init__(self, data_path):
        if not os.path.exists(data_path):
            raise FileNotFoundError
        self.data = pd.read_csv(data_path)
        self.tfidf = None
        self.documents_vector = None

    def train(self) -> None:
        # Load data

        # Train model
        self.tfidf = TfidfVectorizer()
        self.documents_vector = self.tfidf.fit_transform(self.data["content"])

        # Save model
        joblib.dump(self.tfidf, "./models/tfidf.pkl")
        joblib.dump(self.documents_vector, "./models/documents_vector.pkl")

        logging.info("Data shape: " + str(self.data.shape))
        logging.info("Document vector shape:" + str(self.documents_vector.shape))

        return

    def load_model(self, tfidf_path: str, documents_vector_path: str):
        if os.path.exists(tfidf_path) and os.path.exists(documents_vector_path):
            self.tfidf = joblib.load(tfidf_path)
            self.documents_vector = joblib.load(documents_vector_path)
        else:
            raise FileNotFoundError

    def query(self, query: str):
        if self.tfidf is None or self.documents_vector is None:
            raise ValueError("The TF-IDF model is not trained or loaded.")

        query_vector = self.tfidf.transform([query])
        multiplied = self.documents_vector * query_vector.transpose()

        indexes = np.argpartition(multiplied.toarray(), -10, axis=None)[-10:]

        results = []
        for order, i in enumerate(indexes):
            row = self.data.iloc[i]
            results.append(
                {
                    "title": row["title"],
                    "content": row["content"][:500],
                    "relevance": (order + 1) / 10,
                }
            )

        for result in results:
            print(result)

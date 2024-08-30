import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import os
import joblib
import logging
import pprint as pp


class TfidfHelper:
    def __init__(self, df: pd.DataFrame, threshold=0.1):
        self.data = df
        self.threshold = threshold
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

    def query(self, query: str, max_results=10):
        if self.tfidf is None or self.documents_vector is None:
            raise ValueError("The TF-IDF model is not trained or loaded.")

        query_vector = self.tfidf.transform([query])

        relevance_scores = linear_kernel(query_vector, self.documents_vector).flatten()

        top_results = [
            (i, relevance_scores[i])
            for i in relevance_scores.argsort()[::-1]
            if relevance_scores[i] > self.threshold
        ][:max_results]

        if not top_results:
            logging.info("No results found")
            return []

        results = []
        for index, relevance in top_results:
            print(index, relevance)
            row = self.data.iloc[index]
            results.append(
                {
                    "title": row["title"],
                    "content": " ".join(
                        row["content"].split()[:50]
                    ),  # Only get first 500 words
                    "relevance": float(relevance),  # VERIFICAR COM VINI
                }
            )
        for result in results:
            print()
            print(result)

        return results

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import os
import joblib
import logging
import pprint as pp


class TfidfUtility:
    def __init__(
        self,
        df: pd.DataFrame,
        tfidf_vectorizer: TfidfVectorizer,
        documents_vector,
        threshold=0.1,
    ):
        self.df = df
        self.threshold = threshold
        self.vectorizer = tfidf_vectorizer
        self.documents_vector = documents_vector

    @classmethod
    def load(
        cls, data_path: str, tfidf_path: str, documents_vector_path: str, threshold=0.1
    ):
        try:
            if not os.path.exists(data_path):
                raise FileNotFoundError(f"Data file not found: {data_path}")
            if not os.path.exists(tfidf_path):
                raise FileNotFoundError(
                    f"TF-IDF vectorizer file not found: {tfidf_path}"
                )
            if not os.path.exists(documents_vector_path):
                raise FileNotFoundError(
                    f"Documents vector file not found: {documents_vector_path}"
                )

            data = pd.read_csv(data_path)
            vectorizer = joblib.load(tfidf_path)
            documents_vector = joblib.load(documents_vector_path)
        except FileNotFoundError as e:
            print(e)
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

        return cls(data, vectorizer, documents_vector, threshold)

    def query(self, query: str, max_results=10):
        if self.vectorizer is None or self.documents_vector is None:
            raise ValueError("The TF-IDF model is not trained or loaded.")

        query_vector = self.vectorizer.transform([query])

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
            row = self.df.iloc[index]
            results.append(
                {
                    "title": row["title"],
                    "content": " ".join(
                        row["content"].split()[:500]
                    ),  # Only get first 500 words
                    "relevance": float(relevance),
                }
            )
        # for result in results:
        #     print()
        #     print(result)

        return results

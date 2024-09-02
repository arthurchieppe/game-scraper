import pandas as pd
import joblib
import logging
from sklearn.exceptions import NotFittedError
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfTrainer:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def train(self) -> None:
        try:
            # Train model
            vectorizer = TfidfVectorizer()
            documents_vector = vectorizer.fit_transform(self.data["content"])

            # Save model
            joblib.dump(vectorizer, "./models/tfidf.pkl")
            joblib.dump(documents_vector, "./models/documents_vector.pkl")

            logging.info("Data shape: " + str(self.data.shape))
            logging.info("Document vector shape:" + str(documents_vector.shape))

        except KeyError as e:
            logging.error(
                f"KeyError: {e}. Ensure the 'content' column exists in the DataFrame."
            )
        except NotFittedError as e:
            logging.error(f"NotFittedError: {e}. The vectorizer could not be fitted.")
        except FileNotFoundError as e:
            logging.error(
                f"FileNotFoundError: {e}. Ensure the directory './models/' exists."
            )
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

        return

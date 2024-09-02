from tfidf_utility import TfidfUtility
import logging
import pandas as pd

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df = pd.read_csv("./data/reviews_content_20240828_052643.csv")
    tfidf = TfidfUtility.load(
        data_path="./data/reviews_content_20240828_052643.csv",
        tfidf_path="./models/tfidf.pkl",
        documents_vector_path="./models/documents_vector.pkl",
    )
    tfidf.query("Arcade racing game that has multiplayer and formula 1")

from models.train_tfidf import TfidfHelper
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tfidf = TfidfHelper("./data/reviews_content_20240828_052643.csv")
    # tfidf.train()
    tfidf_path = "./models/tfidf.pkl"
    documents_vector_path = "./models/documents_vector.pkl"
    tfidf.load_model(tfidf_path=tfidf_path, documents_vector_path=documents_vector_path)
    tfidf.query("Arcade racing game that has multiplayer and formula 1")

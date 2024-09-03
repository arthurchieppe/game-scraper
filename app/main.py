from fastapi import FastAPI, Query, HTTPException
import os
import uvicorn

from app.tfidf_utility import TfidfUtility


class DummyModel:
    def predict(self, X):
        return "dummy prediction"


def load_model():
    predictor = DummyModel()
    return predictor


app = FastAPI()
app.predictor = load_model()

tfidf = TfidfUtility.load(
    data_path="./data/reviews_content_20240828_052643.csv",
    tfidf_path="./models/tfidf.pkl",
    documents_vector_path="./models/documents_vector.pkl",
)


@app.get("/query")
def query_route(query: str = Query(..., description="Search query")):
    if len(query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Empty query")
    try:
        results = tfidf.query(query)
        # TODO: write your code here, keeping the return format
        return {
            "results": results,
            "message": "OK",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()

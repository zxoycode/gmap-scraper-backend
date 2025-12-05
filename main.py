from fastapi import FastAPI, Query, HTTPException
from scraper import fetch_reviews

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Google Maps Review Scraper API is running"}


@app.get("/scrape")
def scrape(
    url: str = Query(..., description="Google Maps URL（支援短網址 maps.app.goo.gl）"),
    limit: int = Query(150, description="評論數量（預設 150）")
):
    try:
        result = fetch_reviews(url, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

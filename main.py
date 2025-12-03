from fastapi import FastAPI, HTTPException
from scraper import fetch_reviews

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Serper Google Maps Scraper Ready"}

@app.get("/scrape")
def scrape(query: str, limit: int = 150):
    try:
        reviews = fetch_reviews(query, limit)
        return {
            "count": len(reviews),
            "reviews": reviews
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

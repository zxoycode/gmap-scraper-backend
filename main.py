from fastapi import FastAPI, HTTPException
from scraper import fetch_reviews

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Serper Google Maps Reviews API Ready"}

@app.get("/scrape")
def scrape(query: str, limit: int = 150):
    """
    query：可輸入餐廳名稱或 Google Maps 完整網址
    limit：最多評論數
    """

    if not query:
        raise HTTPException(status_code=400, detail="請提供 query（餐廳名稱或Google Maps網址）")

    try:
        reviews = fetch_reviews(query, limit)

        return {
            "query": query,
            "count": len(reviews),
            "reviews": reviews
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

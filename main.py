# main.py
from fastapi import FastAPI, Query
from scraper import get_reviews_from_input

app = FastAPI()

@app.get("/scrape")
def scrape(query: str = Query(...), limit: int = 150):
    result = get_reviews_from_input(query, limit)
    return result

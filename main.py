# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import asyncio
from scraper import scrape_reviews

app = FastAPI()

# 讓 Streamlit Cloud 或其他前端可以呼叫
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 若之後想限制來源可以改
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "Google Maps Scraper API Ready"}

@app.get("/scrape")
async def scrape(url: str, limit: Optional[int] = 150):
    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="請傳入正確的 Google Maps 連結")
    if limit is None or limit <= 0:
        limit = 150
    if limit > 300:
        limit = 300  # 安全上限

    reviews = await scrape_reviews(url, limit)
    return {
        "count": len(reviews),
        "reviews": reviews
    }

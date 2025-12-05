from fastapi import FastAPI, HTTPException, Query
import requests
import json
import re

app = FastAPI()

OX_USERNAME = "sylvia_X9skB"      # ← 放你的 username
OX_PASSWORD = "=E201316a123"      # ← 放你的 password

ENDPOINT = "https://realtime.oxylabs.io/v1/queries"


# -----------------------------
# 🔧 1. 展開 Google Maps 短網址
# -----------------------------
def expand_short_url(url: str) -> str:
    try:
        resp = requests.head(url, allow_redirects=True, timeout=10)
        return resp.url
    except:
        return url


# -----------------------------
# 🔧 2. 從 Google Maps URL 抽取 Place ID
# -----------------------------
def extract_place_id(url: str) -> str:
    match = re.search(r"/place/([^/]+)", url)
    if match:
        return match.group(1)
    return None


# -----------------------------
# 🔧 3. 從 Oxylabs 抓取 Google Maps Review（翻頁）
# -----------------------------
def fetch_reviews(place_url: str, limit: int = 150):

    place_url = expand_short_url(place_url)

    payload = {
        "source": "google_maps_reviews",
        "query": place_url,
        "parse": True,
        "context": {
            "reviews_limit": limit
        }
    }

    response = requests.post(
        ENDPOINT,
        auth=(OX_USERNAME, OX_PASSWORD),
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    data = response.json()
    reviews = data.get("results", [{}])[0].get("reviews", [])

    return {
        "count": len(reviews),
        "reviews": reviews
    }


# -----------------------------
# 🔧 4. API Route 入口
# -----------------------------
@app.get("/scrape")
def scrape(
    url: str = Query(..., description="Google Maps URL（支援短網址）"),
    limit: int = Query(150, description="評論數量（預設 150）")
):
    result = fetch_reviews(url, limit)
    return result

from fastapi import FastAPI, Query
import requests
import os
from urllib.parse import urlparse, unquote

app = FastAPI()

SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

# -------------------------
# 工具：從 Google Maps URL 中提取地點名稱
# -------------------------
def extract_place_from_url(url: str) -> str | None:
    try:
        parsed = urlparse(url)

        # 短網址 maps.app.goo.gl -> 自動展開
        if "maps.app.goo.gl" in parsed.netloc:
            expanded = requests.get(url, allow_redirects=True).url
            return extract_place_from_url(expanded)

        # 長網址格式：/maps/place/<名稱>/
        if "google.com" in parsed.netloc and "/maps/place/" in parsed.path:
            part = parsed.path.split("/maps/place/")[1]
            name = part.split("/")[0]
            name = unquote(name.replace("+", " "))
            return name

        return None
    except:
        return None


# -------------------------
# 主要 API：抓評論
# -------------------------
@app.get("/scrape")
def scrape_reviews(query: str = Query(...), limit: int = 20):
    """
    query = 餐廳名稱 或 Google Maps 連結（短/長）
    limit = 要抓的評論數（最多 ~150）
    """

    # 1. 如果 query 是網址 → 先解析地點名稱
    if query.startswith("http"):
        extracted = extract_place_from_url(query)
        if extracted:
            place = extracted
        else:
            return {"error": "無法解析網址，請確認是否為有效的 Google Maps 連結"}
    else:
        place = query  # 使用者直接輸入店名

    # 2. Serper.dev 查詢
    url = "https://google.serper.dev/localReviews"

    payload = {
        "q": place,
        "num": min(limit, 150)  # Serper 最佳效果範圍
    }

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    res = requests.post(url, json=payload, headers=headers)

    if res.status_code != 200:
        return {"error": "Serper API 發生錯誤", "detail": res.text}

    data = res.json()

    # 如果沒有評論
    if "reviews" not in data:
        return {"query": place, "count": 0, "reviews": []}

    reviews_raw = data["reviews"]

    # 整理成你前端好用的格式
    reviews = []
    for r in reviews_raw:
        reviews.append({
            "rating": r.get("rating"),
            "text": r.get("snippet", ""),
            "date": r.get("date"),
            "author": r.get("author")
        })

    return {
        "query": place,
        "count": len(reviews),
        "reviews": reviews
    }


@app.get("/")
def root():
    return {"status": "ok", "message": "Google Maps Review Scraper backend is running"}

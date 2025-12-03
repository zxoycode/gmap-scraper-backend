import os
import requests

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def fetch_reviews(query: str, limit: int = 150):
    """
    使用 Serper.dev Places Reviews API 取得 Google Maps 評論。
    query 可以是：餐廳名稱 或完整 Google Maps 連結
    """

    url = "https://google.serper.dev/places/reviews"

    payload = {
        "q": query,
        "num": limit   # Serper.dev 可直接指定評論數
    }

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    res = requests.post(url, json=payload, headers=headers)
    data = res.json()

    # 沒有 reviews
    if "reviews" not in data:
        return []

    reviews = data["reviews"]

    # 轉成統一格式
    parsed = [
        {"rating": r.get("rating"), "text": r.get("snippet", "")}
        for r in reviews
    ]

    return parsed[:limit]


import os
import requests

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def fetch_reviews(query: str, limit: int = 150):
    """
    使用 Serper.dev 搜尋 Google Maps，並回傳評論。
    query 可以是：店名 or Google Maps 網址
    """

    url = "https://google.serper.dev/places"

    payload = {
        "q": query
    }

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    res = requests.post(url, json=payload, headers=headers)
    data = res.json()

    # Serper 回傳格式：
    # "reviews": [
    #   {"rating": 5, "snippet": "...", "source": "Google Reviews"},
    #   ...
    # ]

    if "reviews" not in data:
        return []

    reviews = data["reviews"][:limit]

    # 轉成統一格式
    parsed = [{"rating": r.get("rating"), "text": r.get("snippet", "")} for r in reviews]

    return parsed

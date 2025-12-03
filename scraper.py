import os
import requests

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def find_place_id(query: str):
    """
    用 Serper Places API 找 placeId
    query = 餐廳名稱 or Google Maps URL
    """
    url = "https://google.serper.dev/places"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query
    }

    res = requests.post(url, headers=headers, json=payload)
    data = res.json()

    # places API 回傳格式：
    # {
    #    "places": [
    #        {"title": "...", "placeId": "..."}
    #    ]
    # }

    if "places" not in data or len(data["places"]) == 0:
        return None

    # 取第一個最相關的地點
    return data["places"][0].get("placeId")


def fetch_reviews(query: str, limit: int = 150):
    """
    使用 placeId 呼叫 Reviews API
    """

    place_id = find_place_id(query)

    if not place_id:
        return []

    url = "https://google.serper.dev/places/reviews"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "placeId": place_id,
        "num": limit
    }

    res = requests.post(url, headers=headers, json=payload)
    data = res.json()

    if "reviews" not in data:
        return []

    reviews = data["reviews"]

    # 整理格式
    parsed = [
        {"rating": r.get("rating"), "text": r.get("snippet", "")}
        for r in reviews
    ]

    return parsed[:limit]

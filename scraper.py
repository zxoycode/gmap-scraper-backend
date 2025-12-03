import os
import requests
import re

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def expand_short_url(url: str) -> str:
    """
    將 maps.app.goo.gl 短網址展開成完整 Google Maps 網址
    """
    try:
        resp = requests.get(url, allow_redirects=True, timeout=10)
        final_url = resp.url
        return final_url
    except:
        return url   # 展開失敗也先回傳原網址


def extract_text_from_url(url: str) -> str:
    """
    從完整 Google Maps 網址中取出地點名稱（Serper.dev 能用）
    EX: https://www.google.com/maps/place/鼎泰豐101店 → 鼎泰豐101店
    """

    # /maps/place/<name>
    m = re.search(r'/maps/place/([^/]+)', url)
    if m:
        name = m.group(1)
        # URL decode: 將 %E9%… 轉中文
        return requests.utils.unquote(name)

    return url


def find_place_id(query: str):
    """
    用 Serper Places API 找 placeId
    query = 餐廳名稱 或 完整 Google Maps URL
    """
    url = "https://google.serper.dev/places"

    headers = {"X-API-KEY": SERPER_API_KEY}
    payload = {"q": query}

    res = requests.post(url, json=payload, headers=headers)
    data = res.json()

    if "places" not in data or len(data["places"]) == 0:
        return None

    return data["places"][0].get("placeId")


def fetch_reviews(query: str, limit: int = 150):
    """
    完整流程：
    1. 若是短網址 → 展開成完整網址
    2. 從完整網址取出地點名稱
    3. places API 取得 placeId
    4. reviews API 取得評論
    """

    original_query = query

    # 如果是短網址 → 展開
    if "maps.app.goo.gl" in query:
        query = expand_short_url(query)

    # 若是 google maps 網址 → 抽取地點名稱
    if "google.com/maps" in query:
        query = extract_text_from_url(query)

    # Step 3: 找到 placeId
    place_id = find_place_id(query)

    if not place_id:
        return []

    # Step 4: 用 placeId 抓評論
    url = "https://google.serper.dev/places/reviews"
    headers = {"X-API-KEY": SERPER_API_KEY}
    payload = {"placeId": place_id, "num": limit}

    res = requests.post(url, json=payload, headers=headers)
    data = res.json()

    if "reviews" not in data:
        return []

    reviews = data["reviews"]

    parsed = [
        {"rating": r.get("rating"), "text": r.get("snippet", "")}
        for r in reviews
    ]

    return parsed[:limit]

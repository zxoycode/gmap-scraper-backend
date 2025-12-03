# scraper.py
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# ---------------------------------------
# STEP 1：解析短網址，不用跳轉，只讀 HTML
# ---------------------------------------
def extract_info_from_short_url(url):
    try:
        res = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0"
        })

        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.find("meta", property="og:title")
        desc = soup.find("meta", property="og:description")

        title = title["content"] if title else None
        desc = desc["content"] if desc else None

        return title, desc

    except Exception as e:
        print("短網址解析失敗:", e)
        return None, None


# ---------------------------------------
# STEP 2：Serper Places API（找 placeId）
# ---------------------------------------
def find_place_id(query):
    url = "https://google.serper.dev/places"
    payload = {"q": query}
    headers = {"X-API-KEY": SERPER_API_KEY}

    res = requests.post(url, json=payload, headers=headers)
    data = res.json()

    if "places" in data and len(data["places"]) > 0:
        return data["places"][0]["placeId"]

    return None


# ---------------------------------------
# STEP 3：Serper Reviews API（抓評論）
# ---------------------------------------
def fetch_reviews(place_id, limit=150):
    url = "https://google.serper.dev/reviews"
    payload = {"placeId": place_id}
    headers = {"X-API-KEY": SERPER_API_KEY}

    res = requests.post(url, json=payload, headers=headers)
    data = res.json()

    reviews = data.get("reviews", [])
    return reviews[:limit]


# ---------------------------------------
# STEP 4：對外提供的主要函式
# ---------------------------------------
def get_reviews_from_input(user_input, limit=150):
    # 判斷是否為短網址
    if "maps.app.goo.gl" in user_input:
        title, desc = extract_info_from_short_url(user_input)

        if not title:
            return {"error": "無法解析短網址"}

        # 用「店名 + 地址」搜尋成功率最高
        search_query = f"{title} {desc}" if desc else title  

        place_id = find_place_id(search_query)

        if not place_id:
            return {"error": "找不到店家 placeId"}

        reviews = fetch_reviews(place_id, limit)
        return {
            "query": search_query,
            "place_id": place_id,
            "count": len(reviews),
            "reviews": reviews
        }

    else:
        # 字串搜尋餐廳名稱
        place_id = find_place_id(user_input)

        if not place_id:
            return {"error": "找不到店家 placeId"}

        reviews = fetch_reviews(place_id, limit)
        return {
            "query": user_input,
            "place_id": place_id,
            "count": len(reviews),
            "reviews": reviews
        }

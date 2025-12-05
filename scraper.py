import requests
import os
import re

OX_USERNAME = os.getenv("OX_USERNAME")
OX_PASSWORD = os.getenv("OX_PASSWORD")

ENDPOINT = "https://realtime.oxylabs.io/v1/queries"


def expand_short_url(url: str) -> str:
    """支援 Google Maps 短網址展開"""
    try:
        resp = requests.head(url, allow_redirects=True, timeout=10)
        return resp.url
    except:
        return url


def fetch_reviews(place_url: str, limit: int = 150):
    """向 Oxylabs 請求 Google Maps 評論"""

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
        raise Exception(f"Oxylabs Error: {response.text}")

    data = response.json()
    reviews = data.get("results", [{}])[0].get("reviews", [])

    return {
        "count": len(reviews),
        "reviews": reviews
    }

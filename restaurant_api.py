#restaurant_api.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # ✅ This loads .env variables

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def fetch_restaurants(location, cuisine=None):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query = f"{cuisine} restaurants in {location}"
    params = {
        "query": query,
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    print("📡 URL:", response.url)
    print("📦 Raw response:", data)

    if "results" not in data or len(data["results"]) == 0:
        return []

    results = []
    for r in data["results"][:5]:
        results.append({
            "id": r["place_id"],
            "name": r["name"],
            "category": cuisine or "Unknown",
            "location": location,
            "rating": r.get("rating", 0)
        })
    return results

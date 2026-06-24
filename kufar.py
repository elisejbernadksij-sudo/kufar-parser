import requests
import os

# Параметры поиска
PRICE_MAX = 20000      # в копейках (200 рублей = 20000 копеек)
REGION_ID = 4          # Гомель
CATEGORY_ID = 37       # Мобильные телефоны
OS_FILTER = "android"  # Операционная система

def get_listings():
    url = "https://api.kufar.by/search-api/v2/search/rendered-paginated"

    params = {
        "lang": "ru",
        "cat": f"{CATEGORY_ID}",
        "rgn": f"{REGION_ID}",
        "cur": "BYR",
        "prc": f"r:0,{PRICE_MAX}",
        "sos": "android",   # фильтр по Android
        "size": 30,
        "sort": "lst.d",    # сортировка по дате (новые первые)
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/91.0",
        "Accept": "application/json",
    }

    response = requests.get(url, params=params, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()

    ads = data.get("ads", [])
    results = []

    for ad in ads:
        try:
            ad_id = ad.get("ad_id") or ad.get("id")
            title = ad.get("subject", "Без названия")
            price_raw = ad.get("price_byn") or ad.get("price", 0)
            price = int(price_raw) / 100 if price_raw else 0
            link = f"https://www.kufar.by/item/{ad_id}"

            # Картинка
            images = ad.get("images", [])
            photo_url = images[0].get("id", "") if images else ""
            if photo_url:
                photo_url = f"https://yams.kufar.by/api/v1/kufar-ads/images/{photo_url[:2]}/{photo_url}.jpg?rule=gallery"

            results.append({
                "ad_id": ad_id,
                "title": title,
                "price": price,
                "link": link,
                "photo_url": photo_url,
            })
        except Exception:
            continue

    return results

import requests
import re

PRICE_MAX = 20000      # в копейках (200 рублей = 20000 копеек)
REGION_ID = 4          # Гомель
CATEGORY_ID = 37       # Мобильные телефоны
MIN_STORAGE_GB = 32

def extract_storage(text):
    match = re.search(r'(\d+)\s*[гГgG][бБbB]', text or "")
    if match:
        return int(match.group(1))
    match = re.search(r'\b(16|32|64|128|256|512)\b', text or "")
    if match:
        return int(match.group(1))
    return None

def extract_brand(title):
    brands = [
        "Samsung", "Xiaomi", "Redmi", "POCO", "Huawei", "Honor",
        "Realme", "OPPO", "Vivo", "Nokia", "Motorola", "Sony",
        "LG", "OnePlus", "Meizu", "Lenovo", "Asus", "Tecno"
    ]
    title_lower = title.lower()
    for brand in brands:
        if brand.lower() in title_lower:
            return brand
    return "Другое"

def get_all_listings():
    """Получает все объявления (несколько страниц)"""
    all_ads = []
    cursor = None

    for page in range(5):  # до 5 страниц = ~250 объявлений
        url = "https://api.kufar.by/search-api/v2/search/rendered-paginated"
        params = {
            "lang": "ru",
            "cat": f"{CATEGORY_ID}",
            "rgn": f"{REGION_ID}",
            "cur": "BYR",
            "prc": f"r:0,{PRICE_MAX}",
            "sos": "android",
            "size": 50,
            "sort": "lst.d",
        }
        if cursor:
            params["cursor"] = cursor

        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/91.0",
            "Accept": "application/json",
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            ads = data.get("ads", [])
            if not ads:
                break
            all_ads.extend(ads)
            cursor = data.get("pagination", {}).get("after")
            if not cursor:
                break
        except Exception:
            break

    return all_ads

def get_listings():
    ads = get_all_listings()
    results = []

    for ad in ads:
        try:
            ad_id = ad.get("ad_id") or ad.get("id")
            title = ad.get("subject", "Без названия")
            body = ad.get("body", "")
            price_raw = ad.get("price_byn") or ad.get("price", 0)
            price = int(price_raw) / 100 if price_raw else 0
            link = f"https://www.kufar.by/item/{ad_id}"

            brand = extract_brand(title)
            storage = extract_storage(title) or extract_storage(body)

            if storage and storage < MIN_STORAGE_GB:
                continue

            images = ad.get("images", [])
            photo_url = images[0].get("id", "") if images else ""
            if photo_url:
                photo_url = f"https://yams.kufar.by/api/v1/kufar-ads/images/{photo_url[:2]}/{photo_url}.jpg?rule=gallery"

            results.append({
                "ad_id": ad_id,
                "title": title,
                "brand": brand,
                "storage": storage,
                "price": price,
                "link": link,
                "photo_url": photo_url,
            })
        except Exception:
            continue

    return results

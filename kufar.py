import requests
import re

MIN_STORAGE_GB = 64
MIN_PRICE = 80

STOP_WORDS = [
    "сим-карт", "симкарт", "sim card", "сим карт", "продам номер",
    "кнопочн", "кнопк", "бабушкофон",
    "запчаст", "на разбор", "разборов", "не работает", "разбит",
    "планшет", "tablet", "часы", "watch",
    "аксессуар", "чехол", "наушник", "зарядк", "кабель", "power bank",
    "нокиа 1", "нокиа 2", "нокиа 3", "нокиа 5", "нокиа 100", "нокиа 105",
    "nokia 1", "nokia 2", "nokia 3", "nokia 5130", "nokia 100", "nokia 105",
    "iphone", "apple",
]

BAD_MODELS = [
    "redmi 6", "redmi 6a", "redmi 7a", "redmi 5", "redmi 5a", "redmi 4",
    "redmi note 5", "redmi note 6", "redmi note 7",
    "samsung a10", "samsung a10s", "samsung a20", "samsung a20s",
    "samsung a02", "samsung a03", "samsung a04",
    "samsung j", "galaxy j",
    "honor 7", "honor 8", "honor 8a", "honor 9s",
    "huawei y5", "huawei y6", "huawei y7",
    "iphone 5", "iphone 6", "iphone 7",
]

def is_valid_phone(title, body=""):
    text = (title + " " + (body or "")).lower()
    for word in STOP_WORDS:
        if word in text:
            return False
    for model in BAD_MODELS:
        if model in text:
            return False
    return True

def extract_storage(text):
    match = re.search(r'(\d+)\s*[гГgG][бБbB]', text or "")
    if match:
        return int(match.group(1))
    match = re.search(r'\b(64|128|256|512)\b', text or "")
    if match:
        return int(match.group(1))
    return None

def extract_brand(title):
    brands = [
        "Samsung", "Xiaomi", "Redmi", "POCO", "Huawei", "Honor",
        "Realme", "OPPO", "Vivo", "Nokia", "Motorola", "Sony",
        "LG", "OnePlus", "Meizu", "Lenovo", "Asus", "Tecno",
        "Infinix", "iPhone", "Apple", "TCL", "ZTE"
    ]
    title_lower = title.lower()
    for brand in brands:
        if brand.lower() in title_lower:
            return brand
    return "Другое"

def get_all_listings():
    all_ads = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0",
        "Accept": "application/json",
        "Referer": "https://www.kufar.by/",
    }

    # Все районы Гомеля из URL который ты скинул
    GOMEL_AR = "v.or:162,62,128,6,164,65,8,66,39,165,166,167,131,163,129,63,58,149,59,130,152,5,7,132,68,67,64,32,60,61"

    cursor = None
    for page in range(6):
        url = "https://api.kufar.by/search-api/v2/search/rendered-paginated"
        params = {
            "lang": "ru",
            "cat": "17010",
            "ar": GOMEL_AR,
            "cur": "BYR",
            "prc": "r:4000,20000",
            "size": 50,
            "sort": "lst.d",
        }
        if cursor:
            params["cursor"] = cursor

        try:
            response = requests.get(url, params=params, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                ads = data.get("ads", [])
                print(f"Страница {page+1}: {len(ads)} объявлений")
                if not ads:
                    break
                all_ads.extend(ads)
                cursor = data.get("pagination", {}).get("after")
                if not cursor:
                    break
        except Exception as e:
            print(f"Ошибка: {e}")
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

            if not is_valid_phone(title, body):
                continue
            if price < MIN_PRICE:
                continue

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
                "body": body,
            })
        except Exception:
            continue

    return results

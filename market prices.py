# Примерные рыночные цены в Беларуси (б/у, рублей)
MARKET_PRICES = {
    # Samsung
    "samsung galaxy a02s": 80,
    "samsung galaxy a03": 85,
    "samsung galaxy a03s": 90,
    "samsung galaxy a04": 90,
    "samsung galaxy a04s": 100,
    "samsung galaxy a05": 110,
    "samsung galaxy a05s": 120,
    "samsung galaxy a10": 80,
    "samsung galaxy a10s": 85,
    "samsung galaxy a12": 110,
    "samsung galaxy a13": 130,
    "samsung galaxy a14": 145,
    "samsung galaxy a20": 90,
    "samsung galaxy a20s": 95,
    "samsung galaxy a21s": 110,
    "samsung galaxy a22": 140,
    "samsung galaxy a23": 150,
    "samsung galaxy a30": 100,
    "samsung galaxy a30s": 105,
    "samsung galaxy a31": 120,
    "samsung galaxy a32": 160,
    "samsung galaxy a33": 180,
    "samsung galaxy a50": 110,
    "samsung galaxy a50s": 115,
    "samsung galaxy a51": 130,
    "samsung galaxy a52": 170,
    "samsung galaxy a53": 190,
    "samsung galaxy a72": 180,
    "samsung galaxy a73": 200,
    "samsung galaxy m12": 100,
    "samsung galaxy m13": 110,
    "samsung galaxy m14": 120,
    "samsung galaxy m21": 105,
    "samsung galaxy m22": 120,
    "samsung galaxy m31": 120,
    "samsung galaxy m32": 140,
    "samsung galaxy m33": 155,
    "samsung galaxy s20 fe": 190,
    "samsung galaxy s21 fe": 210,

    # Xiaomi / Redmi / POCO
    "redmi 9": 85,
    "redmi 9a": 75,
    "redmi 9c": 80,
    "redmi 9t": 100,
    "redmi 10": 110,
    "redmi 10a": 90,
    "redmi 10c": 100,
    "redmi 12": 140,
    "redmi 12c": 110,
    "redmi note 9": 105,
    "redmi note 9s": 115,
    "redmi note 9 pro": 120,
    "redmi note 10": 130,
    "redmi note 10s": 145,
    "redmi note 10 pro": 160,
    "redmi note 11": 140,
    "redmi note 11s": 155,
    "redmi note 11 pro": 175,
    "redmi note 12": 160,
    "redmi note 12s": 170,
    "poco m3": 100,
    "poco m4": 120,
    "poco m5": 130,
    "poco x3": 130,
    "poco x4": 155,
    "xiaomi 11 lite": 170,
    "xiaomi 12 lite": 195,

    # Honor / Huawei
    "honor 10 lite": 85,
    "honor 20 lite": 90,
    "honor 8a": 75,
    "honor 8x": 90,
    "honor 9a": 85,
    "honor 9c": 90,
    "honor 9s": 75,
    "honor 10x lite": 100,
    "honor x6": 100,
    "honor x7": 115,
    "honor x8": 130,
    "huawei p30 lite": 110,
    "huawei p40 lite": 130,
    "huawei y6": 75,
    "huawei y7": 85,
    "huawei y8": 90,
    "huawei y9": 100,

    # Realme / OPPO
    "realme c11": 80,
    "realme c21": 90,
    "realme c25": 100,
    "realme c31": 100,
    "realme c33": 110,
    "realme 8": 140,
    "realme 9": 155,
    "realme 9i": 130,

    # Nokia / Motorola
    "nokia g10": 85,
    "nokia g20": 95,
    "motorola moto g10": 90,
    "motorola moto g20": 95,
    "motorola moto g30": 105,
    "motorola moto g31": 115,
    "motorola moto g32": 125,
    "motorola moto g42": 135,
    "motorola moto g52": 145,
}

def get_market_price(title):
    """Находит рыночную цену по названию объявления"""
    title_lower = title.lower()
    best_match = None
    best_len = 0

    for model, price in MARKET_PRICES.items():
        if model in title_lower and len(model) > best_len:
            best_match = price
            best_len = len(model)

    return best_match

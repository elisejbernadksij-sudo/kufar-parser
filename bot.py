import requests
import os
import logging

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_text(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    }, timeout=10)

def send_message(item):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return

    storage_str = f"{item['storage']} GB" if item.get('storage') else "?"
    rank_str = f"🏆 #{item['rank']}  " if item.get('rank') else "🆕 "

    # Выгода vs рынок б/у
    if item.get("market_price") and item.get("discount") is not None:
        if item["discount"] > 0:
            deal_str = f"\n📊 Рынок б/у: ~{item['market_price']}р. | Выгода: *{item['discount']}%* 🔥"
        else:
            deal_str = f"\n📊 Рынок б/у: ~{item['market_price']}р."
    else:
        deal_str = ""

    # Цена нового в магазине
    if item.get("new_price"):
        new_str = f"\n🏪 Новый в магазине: ~{item['new_price']}р."
    else:
        new_str = ""

    # Состояние
    condition_str = f"\n🔍 Состояние: {item.get('condition_label', '❓ Не указано')}"

    text = (
        f"{rank_str}*{item['title']}*\n"
        f"🏷 Марка: *{item['brand']}*\n"
        f"💾 Память: *{storage_str}*\n"
        f"💰 Цена: *{item['price']:.0f}р.*"
        f"{deal_str}"
        f"{new_str}"
        f"{condition_str}\n"
        f"🔗 [Открыть объявление]({item['link']})"
    )

    if item.get("photo_url"):
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
            r = requests.post(url, json={
                "chat_id": CHAT_ID,
                "photo": item["photo_url"],
                "caption": text,
                "parse_mode": "Markdown",
            }, timeout=10)
            if r.status_code == 200:
                return
        except Exception:
            pass

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    }, timeout=10)
    logging.info(f"📨 #{item.get('rank','-')} {item['title']} — {item['price']:.0f}р.")

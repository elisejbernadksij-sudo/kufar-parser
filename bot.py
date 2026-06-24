import requests
import os
import logging

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_message(item):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        logging.error("❌ Не заданы TELEGRAM_TOKEN или CHAT_ID")
        return

    text = (
        f"📱 *{item['title']}*\n"
        f"💰 Цена: *{item['price']:.2f} р.*\n"
        f"🔗 [Открыть объявление]({item['link']})"
    )

    # Пробуем отправить с фото
    if item.get("photo_url"):
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
            payload = {
                "chat_id": CHAT_ID,
                "photo": item["photo_url"],
                "caption": text,
                "parse_mode": "Markdown",
            }
            r = requests.post(url, json=payload, timeout=10)
            if r.status_code == 200:
                return
        except Exception:
            pass  # если фото не вышло — отправим без него

    # Отправить без фото
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    requests.post(url, json=payload, timeout=10)
    logging.info(f"📨 Отправлено: {item['title']} — {item['price']:.2f}р.")

import time
import json
import logging
from kufar import get_listings
from bot import send_message
from storage import load_seen, save_seen

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

CHECK_INTERVAL = 300  # каждые 5 минут

def main():
    logging.info("🚀 Куфар-парсер запущен")
    seen = load_seen()

    while True:
        try:
            logging.info("🔍 Проверяем новые объявления...")
            listings = get_listings()

            new_count = 0
            for item in listings:
                ad_id = str(item["ad_id"])
                if ad_id not in seen:
                    seen.add(ad_id)
                    send_message(item)
                    new_count += 1
                    time.sleep(1)  # небольшая пауза между сообщениями

            save_seen(seen)

            if new_count > 0:
                logging.info(f"✅ Найдено новых: {new_count}")
            else:
                logging.info("😴 Новых объявлений нет")

        except Exception as e:
            logging.error(f"❌ Ошибка: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

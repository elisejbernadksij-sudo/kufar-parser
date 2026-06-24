import time
import logging
import os
from kufar import get_listings
from bot import send_message, send_text
from storage import load_seen, save_seen
from market_prices import get_market_price

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

CHECK_INTERVAL = 300
FIRST_RUN_FILE = "first_run_done.txt"
TOP_COUNT = 50

def is_first_run():
    return not os.path.exists(FIRST_RUN_FILE)

def mark_first_run_done():
    with open(FIRST_RUN_FILE, "w") as f:
        f.write("done")

def score_listing(item):
    price = item["price"]
    market = get_market_price(item["title"])

    if market and price > 0:
        discount = (market - price) / market * 100
        item["market_price"] = market
        item["discount"] = round(discount, 1)
        storage_bonus = (item.get("storage") or 32) / 32 * 5
        return discount + storage_bonus
    else:
        item["market_price"] = None
        item["discount"] = None
        storage_bonus = (item.get("storage") or 32) / 32 * 5
        price_score = max(0, 200 - price)
        return price_score / 10 + storage_bonus

def main():
    logging.info("🚀 Куфар-парсер запущен")
    seen = load_seen()

    if is_first_run():
        logging.info("🔍 Первый запуск — собираю все объявления...")
        listings = get_listings()
        logging.info(f"📦 Получено объявлений: {len(listings)}")

        if not listings:
            send_text("⚠️ Не удалось получить объявления с Куфара. Проверяю каждые 5 минут...")
            mark_first_run_done()
        else:
            scored = []
            for item in listings:
                s = score_listing(item)
                scored.append((s, item))
                seen.add(str(item["ad_id"]))

            scored.sort(key=lambda x: x[0], reverse=True)
            top = scored[:TOP_COUNT]

            send_text(f"🏆 Топ-{len(top)} лучших телефонов до 200р в Гомеле:")
            time.sleep(1)

            for rank, (score, item) in enumerate(top, 1):
                item["rank"] = rank
                send_message(item)
                time.sleep(1.5)

            save_seen(seen)
            mark_first_run_done()
            logging.info(f"✅ Отправлено топ-{len(top)} объявлений")

    while True:
        try:
            time.sleep(CHECK_INTERVAL)
            logging.info("🔍 Проверяем новые объявления...")
            listings = get_listings()

            new_items = []
            for item in listings:
                ad_id = str(item["ad_id"])
                if ad_id not in seen:
                    seen.add(ad_id)
                    score_listing(item)
                    new_items.append(item)

            if new_items:
                send_text(f"🆕 Новых объявлений: {len(new_items)}")
                for item in new_items:
                    send_message(item)
                    time.sleep(1)
                save_seen(seen)
                logging.info(f"✅ Отправлено новых: {len(new_items)}")
            else:
                logging.info("😴 Новых нет")

        except Exception as e:
            logging.error(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()

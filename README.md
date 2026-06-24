# Куфар Парсер — Мобильные телефоны

Бот мониторит объявления на Куфаре и присылает новые в Telegram.

## Параметры поиска
- 📍 Гомель, Гомельский район
- 📱 Мобильные телефоны (Android)
- 💰 До 200 рублей

---

## Деплой на Railway.app

### 1. Создать Telegram-бота
1. Написать @BotFather в Telegram
2. Команда `/newbot`
3. Дать имя → получить **TOKEN**
4. Написать боту `/start`
5. Открыть в браузере:
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
6. Найти `"chat":{"id": XXXXXXX}` — это твой **CHAT_ID**

### 2. Загрузить на GitHub
```bash
git init
git add .
git commit -m "init"
git remote add origin https://github.com/ТВОЙлогин/kufar-parser.git
git push -u origin main
```

### 3. Railway.app
1. Зайти на railway.app
2. **New Project** → **Deploy from GitHub repo**
3. Выбрать репозиторий `kufar-parser`
4. Перейти в **Variables** и добавить:
   - `TELEGRAM_TOKEN` = токен от BotFather
   - `CHAT_ID` = твой chat id
5. Deploy! ✅

---

## Как работает
- Каждые **5 минут** проверяет новые объявления
- Сохраняет уже виденные в `seen_ads.json`
- Отправляет только **новые** объявления с фото и ценой

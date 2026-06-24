# Оценка состояния телефона по описанию

GOOD_WORDS = [
    "как новый", "отличное", "идеальн", "идеал", "10/10", "9/10", "9.5/10",
    "мало пользовал", "мало польз", "почти новый", "не пользовал",
    "без царапин", "без сколов", "без трещин", "состояние хорошее",
    "хорошее состояние", "хорош", "бережно", "аккуратно",
    "полный комплект", "коробка", "все работает",
]

BAD_WORDS = [
    "трещин", "скол", "царапин", "разбит", "не работает",
    "на запчаст", "на разбор", "восстановлен", "после ремонт",
    "проблем", "дефект", "потёртост", "потертост",
    "разбитый", "разбитое", "сломан",
]

def get_condition(title, body):
    text = (title + " " + (body or "")).lower()
    
    good_count = sum(1 for w in GOOD_WORDS if w in text)
    bad_count = sum(1 for w in BAD_WORDS if w in text)
    
    if bad_count > 0:
        return "bad", "⚠️ Есть дефекты"
    elif good_count >= 2:
        return "excellent", "✨ Отличное"
    elif good_count == 1:
        return "good", "👍 Хорошее"
    else:
        return "unknown", "❓ Не указано"

def condition_score(condition_grade):
    scores = {
        "excellent": 30,
        "good": 15,
        "unknown": 0,
        "bad": -50,
    }
    return scores.get(condition_grade, 0)

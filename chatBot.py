import json
import os
import random

memory_file = "memory.json"
knowledge = {}

# Загрузка памяти из файла
if os.path.exists(memory_file):
    with open(memory_file, "r", encoding="utf-8") as file:
        knowledge = json.load(file)

# Словарь синонимов
synonyms = {
    "привет": ["здравствуй", "приветик", "хай", "здорово"],
    "пока": ["до встречи", "до свидания", "увидимся"],
    "как дела": ["как ты", "как поживаешь"],
    "грустно": ["печально", "тоска", "уныло"],
    "весело": ["радостно", "кайф", "круто", "классно"]
}

def get_bot_reply(user_input):
    user_input = user_input.lower().strip()

    # Команда обучения: обучи фраза = ответ
    if user_input.startswith("обучи "):
        parts = user_input[7:].split("=")
        if len(parts) == 2:
            phrase = parts[0].strip()
            answer = parts[1].strip()
            if phrase and answer:
                # Если уже есть, добавим в список
                if phrase in knowledge:
                    if isinstance(knowledge[phrase], list):
                        knowledge[phrase].append(answer)
                    else:
                        knowledge[phrase] = [knowledge[phrase], answer]
                else:
                    knowledge[phrase] = [answer]

                with open(memory_file, "w", encoding="utf-8") as file:
                    json.dump(knowledge, file, ensure_ascii=False, indent=2)

                return "Спасибо! Я запомнил новую информацию."
            else:
                return "Фраза или ответ не могут быть пустыми."
        else:
            return "Формат команды должен быть: обучи фраза = ответ"

    # Распознавание синонимов
    matched = None
    for key_phrase, variants in synonyms.items():
        for variant in variants:
            if variant in user_input:
                matched = key_phrase
                break
        if matched:
            break

    # Ответ из базы знаний
    if matched and matched in knowledge:
        response = knowledge[matched]
    elif user_input in knowledge:
        response = knowledge[user_input]
    else:
        return "Я не знаю, как ответить на это. Напиши: обучи фраза = ответ"

    # Возвращаем случайный ответ, если их несколько
    if isinstance(response, list):
        return random.choice(response)
    else:
        return response
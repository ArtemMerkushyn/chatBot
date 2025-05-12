import os
import json
import random

memory_file = "memory.json"
knowledge = {}
synonyms = {}

if os.path.exists(memory_file):
    with open(memory_file, "r", encoding="utf-8") as file:
        knowledge = json.load(file)

def save_knowledge():
    with open(memory_file, "w", encoding="utf-8") as file:
        json.dump(knowledge, file, ensure_ascii=False, indent=2)

def get_bot_reply(user_input):
    user_input = user_input.lower().strip()

    if user_input == "покажи что ты знаешь":
        if knowledge:
            return "Я знаю следующие фразы:\n" + "\n".join(f"- {q}" for q in knowledge)
        else:
            return "Пока я ничего не знаю."

    elif user_input.startswith("забудь "):
        phrase = user_input.replace("забудь ", "", 1).strip()
        if phrase in knowledge:
            del knowledge[phrase]
            save_knowledge()
            return f"Хорошо, я забыл, как отвечать на: {phrase}"
        else:
            return "Я и так не знаю, как отвечать на это."

    elif user_input.startswith("обучи заново"):
        phrase = user_input.replace("обучи заново", "", 1).strip()
        if not phrase:
            return "Ты не указал фразу. Пример: 'обучи заново привет'"
        elif phrase in knowledge:
            return f"Какой новый ответ ты хочешь задать на '{phrase}'?"
        else:
            return "Я пока не знаю этой фразы. Сначала меня нужно научить ей."

    elif user_input.startswith("обучи вариативно"):
        phrase = user_input.replace("обучи вариативно", "", 1).strip()
        if not phrase:
            return "Пример: 'обучи вариативно привет'"
        return f"Введи варианты ответа на '{phrase}' через запятую:"

    elif user_input.startswith("добавь варианты"):
        phrase = user_input.replace("добавь варианты", "", 1).strip()
        if not phrase:
            return "Пример: 'добавь варианты привет'"
        return f"Введи новые варианты ответа на '{phrase}' через запятую:"

    matched = None
    for key_phrase, variants in synonyms.items():
        for variant in variants:
            if variant in user_input:
                matched = key_phrase
                break
        if matched:
            break

    if matched and matched in knowledge:
        response = knowledge[matched]
    elif user_input in knowledge:
        response = knowledge[user_input]
    else:
        return f"Я не знаю, как ответить на '{user_input}'. Напиши новый ответ, чтобы я запомнил его."

    if isinstance(response, list):
        return random.choice(response)
    return response

def retrain_phrase(phrase, answer):
    knowledge[phrase] = answer
    save_knowledge()
    return "Отлично! Я запомнил новый ответ."

def train_variants(phrase, variants):
    if len(variants) < 2:
        return "Нужно хотя бы два варианта."
    knowledge[phrase] = variants
    save_knowledge()
    return f"Запомнил несколько вариантов ответа для '{phrase}'"

def add_variants(phrase, new_variants):
    existing = knowledge.get(phrase, [])
    if isinstance(existing, str):
        existing = [existing]
    all_variants = list(set(existing + new_variants))
    knowledge[phrase] = all_variants
    save_knowledge()
    return f"Добавил варианты ответа для '{phrase}'"
from flask import Flask, render_template, request, jsonify
import os
import json
import random

app = Flask(__name__)

memory_file = "memory.json"
synonyms_file = "synonyms.json"
knowledge = {}
synonyms = {}

# === Загрузка знаний ===
if os.path.exists(memory_file):
    with open(memory_file, "r", encoding="utf-8") as file:
        knowledge = json.load(file)

# === Загрузка синонимов ===
if os.path.exists(synonyms_file):
    with open(synonyms_file, "r", encoding="utf-8") as file:
        synonyms = json.load(file)
else:
    with open(synonyms_file, "w", encoding="utf-8") as file:
        json.dump({}, file, ensure_ascii=False, indent=2)
    synonyms = {}

def save_knowledge():
    with open(memory_file, "w", encoding="utf-8") as file:
        json.dump(knowledge, file, ensure_ascii=False, indent=2)

def save_synonyms():
    with open(synonyms_file, "w", encoding="utf-8") as file:
        json.dump(synonyms, file, ensure_ascii=False, indent=2)

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
            return {"action": "retrain", "phrase": phrase}
        else:
            return "Я пока не знаю этой фразы. Сначала меня нужно научить ей."

    elif user_input.startswith("обучи вариативно"):
        phrase = user_input.replace("обучи вариативно", "", 1).strip()
        if not phrase:
            return "Пример: 'обучи вариативно привет'"
        return {"action": "train_variants", "phrase": phrase}

    elif user_input.startswith("добавь варианты"):
        phrase = user_input.replace("добавь варианты", "", 1).strip()
        if not phrase:
            return "Пример: 'добавь варианты привет'"
        return {"action": "add_variants", "phrase": phrase}

    elif user_input.startswith("добавь синонимы"):
        try:
            phrase_part = user_input.replace("добавь синонимы", "", 1).strip()
            phrase, synonyms_text = phrase_part.split(":", 1)
            phrase = phrase.strip()
            new_syns = [s.strip() for s in synonyms_text.split(",") if s.strip()]
            existing = synonyms.get(phrase, [])
            all_synonyms = list(set(existing + new_syns))
            synonyms[phrase] = all_synonyms
            save_synonyms()
            return f"Синонимы для '{phrase}' обновлены: {', '.join(all_synonyms)}"
        except ValueError:
            return "Формат: 'добавь синонимы фраза: синоним1, синоним2'"

    else:
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
            return {"action": "learn", "phrase": user_input}

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

# ===== Flask routes =====
session_state = {
    "pending_action": None,
    "pending_phrase": None
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    response = ""

    if session_state.get("pending_action"):
        action = session_state.pop("pending_action")
        phrase = session_state.pop("pending_phrase")

        if action == "learn" or action == "retrain":
            response = retrain_phrase(phrase, user_input)
        elif action == "train_variants":
            variants = [v.strip() for v in user_input.split(",") if v.strip()]
            response = train_variants(phrase, variants)
        elif action == "add_variants":
            variants = [v.strip() for v in user_input.split(",") if v.strip()]
            response = add_variants(phrase, variants)
    else:
        result = get_bot_reply(user_input)
        if isinstance(result, dict):
            session_state["pending_action"] = result["action"]
            session_state["pending_phrase"] = result["phrase"]

            if result["action"] == "learn":
                response = f"Я не знаю, как ответить на '{result['phrase']}'. Напиши новый ответ, чтобы я запомнил его."
            elif result["action"] == "retrain":
                response = f"Какой новый ответ ты хочешь задать на '{result['phrase']}'?"
            elif result["action"] == "train_variants":
                response = f"Введи варианты ответа на '{result['phrase']}' через запятую:"
            elif result["action"] == "add_variants":
                response = f"Введи дополнительные варианты для '{result['phrase']}' через запятую:"
        else:
            response = result

    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)
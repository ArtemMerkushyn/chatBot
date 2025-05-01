import os
import json
import random

print("Привет! Я ИИ-бот с памятью. Давай познакомимся.")
user_name = input("Как тебя зовут? ")
print("Приятно познакомиться, " + user_name + "!")

memory_file = "memory.json"
knowledge = {}

# Загрузка памяти
if os.path.exists(memory_file):
    with open(memory_file, "r", encoding="utf-8") as file:
        knowledge = json.load(file)

# Добавляем имя пользователя в память (обновляется каждый раз)
knowledge["как меня зовут"] = "Тебя зовут " + user_name + "!"

# Таблица синонимов
synonyms = {
    "привет": ["привет", "приветик", "здравствуй", "здорово", "добрый день"],
    "как дела": ["как дела", "как ты", "как поживаешь", "как у тебя дела"]
    # Добавляй свои синонимы по желанию
}

print("Можешь поговорить со мной. Команды: обучи заново, забудь, покажи что ты знаешь, пока.")

while True:
    user_input = input("Я: ").lower().strip()

    if user_input == "пока":
        print("ИИ: До встречи, " + user_name + "!")
        break

    elif user_input.startswith("забудь "):
        phrase_to_forget = user_input.replace("забудь ", "", 1).strip()
        if phrase_to_forget in knowledge:
            del knowledge[phrase_to_forget]
            with open(memory_file, "w", encoding="utf-8") as file:
                json.dump(knowledge, file, ensure_ascii=False, indent=2)
            print("ИИ: Хорошо, я забыл, как отвечать на:", phrase_to_forget)
        else:
            print("ИИ: Я и так не знаю, как отвечать на это.")

    elif user_input == "покажи что ты знаешь":
        if knowledge:
            print("ИИ: Вот что я знаю:")
            for question in knowledge:
                print("-", question)
        else:
            print("ИИ: Пока я ничего не знаю.")

    elif user_input.startswith("обучи заново"):
        phrase_to_relearn = user_input.replace("обучи заново", "", 1).strip()
        if not phrase_to_relearn:
            print("ИИ: Ты не указал фразу. Пример: 'обучи заново привет'")
        elif phrase_to_relearn in knowledge:
            print("ИИ: Какой новый ответ ты хочешь задать на '" + phrase_to_relearn + "'?")
            new_answer = input("Я: ").strip()
            if new_answer:
                knowledge[phrase_to_relearn] = new_answer
                with open(memory_file, "w", encoding="utf-8") as file:
                    json.dump(knowledge, file, ensure_ascii=False, indent=2)
                print("ИИ: Отлично! Я запомнил новый ответ.")
            else:
                print("ИИ: Ты ничего не написал. Переобучение отменено.")
        else:
            print("ИИ: Я пока не знаю этой фразы. Сначала меня нужно научить ей.")


    elif user_input.startswith("обучи вариативно"):
        phrase = user_input.replace("обучи вариативно", "", 1).strip()
        if not phrase:
           print("ИИ: Пример: 'обучи вариативно привет'") 
        else:
            print(f"ИИ: Введи варианты ответа на '{phrase}' через запятую:")
            line = input("Я: ").strip()
            variants = [v.strip() for v in line.split(",") if v.strip()]
            if len(variants) < 2:
                print("ИИ: Нужно хотя бы два варианта.")
            else:
                knowledge[phrase] = variants
                with open(memory_file, "w", encoding="utf-8") as file:
                    json.dump(knowledge, file, ensure_ascii=False, indent=2)
                print("ИИ: Запомнил несколько вариантов!")


    elif user_input.startswith("добавь варианты"):
        phrase = user_input.replace("добавь варианты", "", 1).strip()
        if not phrase:
            print("ИИ: Пример: 'добавь варианты привет'")
        else:
            print(f"Введи новые варианты ответа на '{phrase}' через запятую:")
            line = input("Ты:").strip()
            new_variants = [v.strip() for v in line.split(",") if v.strip()]
            if not new_variants:
                print("ИИ: Пустой список. Отмена.")
            else:
                existing = knowledge.get(phrase, [])
                if isinstance(existing, str):
                    existing = [existing]
                all_variants = list(set(existing + new_variants))
                knowledge[phrase] = all_variants
                with open(memory_file, 'w', encoding="utf-8") as file:
                    json.dump(knowledge, file, ensure_ascii=False, indent=2)
                print(f"ИИ: Добавил варианты для '{phrase}'.")

    else:
         # 🎭 Эмоции
        emotion_triggers = {
            "груст": "Не грусти! Всё обязательно наладится 💪",
            "печаль": "Скоро станет лучше. Я с тобой 🤍",
            "рад": "Рад за тебя! 😊",
            "счастл": "Здорово! Счастье — это круто!",
            "один": "Ты не один — я рядом 🤗",
            "шок": "Понимаю... Это бывает. Держись.",
            "устал": "Попробуй отдохнуть. Ты заслуживаешь этого 🌙",
            "ненавижу": "Сложно бывает... Но держи себя в руках 🙏"
        }

        for trigger, emo_response in emotion_triggers.items():
            if trigger in user_input:
                print("ИИ:", emo_response)
                break


        else:
            # Распознавание похожих фраз через синонимы
            matched = None
            for key_phrase, variants in synonyms.items():
                for variant in variants:
                    if variant in user_input:
                        matched = key_phrase
                        break
                if matched:
                    break

            if matched and matched in knowledge:
                responce = knowledge[matched]
                if isinstance(responce, list):
                    print("ИИ:", random.choice(responce))
                else:
                    print("ИИ:", responce)

            elif user_input in knowledge:
                responce = knowledge[user_input]
                if isinstance(responce, list):
                    print("ИИ:", random.choice(responce))
                else:
                    print("ИИ", responce)

            else:
                print("ИИ: Я не знаю, как ответить на это. Научи меня!")
                new_answer = input("Как мне нужно отвечать на это? ").strip()
                if new_answer:
                    knowledge[user_input] = new_answer
                    with open(memory_file, "w", encoding="utf-8") as file:
                        json.dump(knowledge, file, ensure_ascii=False, indent=2)
                    print("ИИ: Спасибо! Теперь я это запомнил.")
                else:
                    print("ИИ: Ты ничего не написал. Обучение отменено.")
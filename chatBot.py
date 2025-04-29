import os # библиотека для работы с файлами
import json


print("Привет, Я chatBot! Давай познакомимся!")
user_name = input("ИИ: Как тебя зовут? ")
print("ИИ: Приятно познакомиться, " + user_name + "!")


memory_file  = "memory.json"
knowledge = {}


# Загрузка памяти
if os.path.exists(memory_file):
    with open(memory_file, "r", encoding="utf-8") as file:
        knowledge = json.load(file)


# Добавляем имя в память (перезаписываем каждый раз)
knowledge["как меня зовут"] = "Тебя зовут, " + user_name + "."


print("Можешь поговорить со мной, если надоест, напиши 'пока' что бы выйти.")


while True:
    user_input = input("Я: ").lower()


    if user_input == "пока":
        print("ИИ: До встречи, " + user_name + "!")
        break


    elif user_input == "покажи что ты знаешь":
        if knowledge:
            print("ИИ: Вот что я знаю:")
            for question in knowledge:
                print("-", question )
        

        else:
            print("ИИ: Пока я ничего не знаю.")
    

    elif user_input.startswith("обучи заново "):
        phrase_to_relearn = user_input.replace("обучи заново ", "", 1).strip()

        if not phrase_to_relearn:
            print("ИИ: Ты не указал фразу, которую нужно переобучить. Пожалуйста, напиши так: 'обучи заново привет'")
        if phrase_to_relearn in knowledge:
            print("ИИ: Какой новый ответ ты хочешь задать на '" + phrase_to_relearn + "'?")
            new_answer = input("Я: ")
            knowledge[phrase_to_relearn] = new_answer
        

            # Обновляем JSON-файл
            with open(memory_file, "w", encoding="utf-8") as file:
                json.dump(knowledge, file, ensure_ascii=False, indent=2)

        
            print("ИИ: Отлично! Я запомнил новый ответ.")
        else:
            print("ИИ: Я не знаю этой фразы, так что не могу переобучиться. Можешь сначала меня научить.")


    elif user_input.startswith("забудь "):
        phrase_to_forget = user_input.replace("забудь ", "", 1).strip()


        if phrase_to_forget in knowledge:
            del knowledge[phrase_to_forget]
            print("ИИ: Хорошо, я забыл, как отвечать на:", phrase_to_forget)


             # Обновляем JSON-файл
            with open(memory_file, "w", encoding="utf-8") as file:
                json.dump(knowledge, file, ensure_ascii=False, indent=2)
        else:
            print("ИИ: Я и так не знаю, как отвечать на это.")


    elif user_input in knowledge:
        print("ИИ: " + knowledge[user_input])

    
    else:
        print("ИИ: Я не знаю, как ответить на это. Научи меня!")
        new_answer = input("Как мне нужно отвечать на это? ")
        knowledge[user_input] = new_answer


        # Сохраняем память в JSON-файл
        with open(memory_file, "w", encoding="utf-8") as file:
            json.dump(knowledge, file, ensure_ascii=False, indent=2)


        print("ИИ: Спасибо! Теперь я это запомнил.")
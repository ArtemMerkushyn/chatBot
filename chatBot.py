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
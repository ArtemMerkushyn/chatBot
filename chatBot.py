print("Привет, Я chatBot! Давай познакомимся!")
# Бот спрашивает имя и запоминает его
user_name = input("ИИ: Как тебя зовут? ")
print("ИИ: Приятно познакомиться, " + user_name + "!")


knowledge = {
    "привет": "Привет, " + user_name + "! Рад тебя видеть.",
    "как дела": "У меня всё отлично! А у тебя?",
    "как ты": "Я хорошо себя чувствую!",
    "как меня зовут": "Тебя зовут " + user_name + "!"
}


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
        print("ИИ: Спасибо! Теперь я это запомнил.")
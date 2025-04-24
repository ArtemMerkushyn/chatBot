print("Привет, Я chatBot! Давай поговорим!")
print("Ты можешь написать: привет, как дела, пока")


# Бот спрашивает имя и запоминает его
user_name = input("ИИ: Как тебя зовут? ")
print("ИИ: Приятно познакомиться, " + user_name + "!")


while True:
    user_input = input("Я: ").lower()


    if user_input == "пока":
        print("ИИ: До встречи, " + user_name + "!")
        break


    elif "привет" in user_input:
        print("ИИ: Привет, " + user_name + "! Рад тебя видеть.")

    
    elif "как дела" in user_input or "как ты" in user_input:
        print("ИИ: У меня всё отлично! А у тебя, " + user_name + "?")

    
    elif "как меня зовут" in user_input:
        print("Тебя зовут " + user_name + ".")

    
    else:
        print("Извини, пока не понимаю эту фразу.")
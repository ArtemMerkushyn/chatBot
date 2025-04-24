print("Привет, Я chatBot! Давай поговорим!")
print("Ты можешь написать: привет, как дела, пока")


while True:
    user_input = input("Я: ").lower()


    if user_input == "пока":
        print("ИИ: До встречи!")
        break


    elif "привет" in user_input:
        print("ИИ: Привет! Рад тебя видеть.")

    
    elif "как дела" in user_input or "как ты" in user_input:
        print("ИИ: У меня всё отлично! Спасибо что спросил.")

    
    else:
        print("Извини, пока не понимаю эту фразу.")
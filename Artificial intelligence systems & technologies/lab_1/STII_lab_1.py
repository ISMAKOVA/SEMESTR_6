print("Форма листа ланцентная? да|нет")
q1 = input().lower()
if q1 == "да":
    print("Поверхность обычная? да|нет")
    q2 = input().lower()
    if q2 == "да":
        print("Окраска листа зеленая? да|нет")
        q3 = input().lower()
        if q3 == "да":
            print("Это Хамеропс!")
        else:
            print("Это Лахеналия!")
    else:
        print("Окраска листа пестрая? да|нет")
        q3 = input().lower()
        if q3 == "да":
            print("Это Птерис!")
        else:
            print("Это Эухарис!")
else:
    print("Поверхность обычная? да|нет")
    q2 = input().lower()
    if q2 == "да":
        print("Размер листа 10-15? да|нет")
        q3 = input().lower()
        if q3 == "да":
            print("Это Криптантус!")
        else:
            print("Это Сансеверия!")
    else:
        print("Форма листа линейная? да|нет")
        q3 = input().lower()
        if q3 == "да":
            print("Это Гемантус!")
        else:
            print("Это Марранта!")
def convert_to_rub(number):
    cur_number = number
    while cur_number > 100:
        cur_number = cur_number % 100
    if cur_number < 10 or 20 < cur_number < 100:
        if cur_number % 10 == 0 or cur_number % 10 >= 5:
            return str(number) + " рублей"
        elif 2 <= cur_number % 10 <= 4:
            return str(number) + " рубля"
        else:
            return str(number) + " рубль"
    else:
        return str(number) + " рублей"


while True:
    print("Введите число")
    number = int(input())
    print(convert_to_rub(number))



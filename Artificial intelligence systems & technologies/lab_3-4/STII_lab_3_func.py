import csv


def write_read_csv(brightness, category):
    csv_file = csv.reader(open('results2.csv', "r"), delimiter=",")
    file_text = []
    for row in csv_file:
        if row[0].isdigit():
            if int(row[0]) == brightness:
                row[category] = int(row[category]) + 1
                row[4] = int(row[4]) + 1
            file_text.append(row)

    with open("results2.csv", 'w', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        columns = ["brightness", "dark", "middle", "light", "number_ppl"]
        a_pen.writerow(columns)
        for line in file_text:
            a_pen.writerow([line[0], line[1], line[2], line[3], line[4]])


def get_brightness_from(r, g, b):
    r = int(r)/2.55
    g = int(g)/2.55
    b = int(b) / 2.55
    brightness = 0.2126*r+0.7152*g+0.0722*b
    print(round(brightness))
    with open("results2.csv", "a") as file:
        a_pen = csv.writer(file)
        for i in range(100):
            a_pen.writerow([str(i), 0, 0, 0, 0])

    return ""


# get_brightness_from(230, 10, 255)

write_read_csv(3, 2)

#category: brightness = 0,dark = 1,middle = 2,light = 3,number_ppl = 4
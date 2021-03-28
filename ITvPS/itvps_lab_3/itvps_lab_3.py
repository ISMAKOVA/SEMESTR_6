import re
import csv
from nltk.tag import pos_tag
from langdetect import detect_langs


def parse_text_from(file_name):
    file = open(file_name, 'r')
    file_text = []
    for line in file:
        file_text.append(line)

    file_text = [re.sub(r'\n+', '', i) for i in file_text if i]
    file_text = [i for i in file_text if i != '']
    print(file_text)
    title = file_text[0]
    lid = file_text[1]
    text = ""
    url = ""
    date = ""
    ner = 0
    for part in file_text:
        if re.match(r'.*https.*', part):
            url += part
            date_reg = re.findall(r'20\d{2}', part)
            if len(date_reg) > 0:
                date += date_reg[0]
        else:
            text += part
            for i, j in pos_tag(part.split()):
                if j == 'NNP':
                    ner = 1
    if len(lid.split()) > 50:
        text += lid

    lang_dict = detect_langs(text)
    lang = ""
    for i in lang_dict:
        lang += i.lang

    return title, lid, text, ner, lang, url, date


def add_to_csv(file_name, csv_file):
    values = parse_text_from(file_name)
    with open(csv_file, 'a', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(values)


add_to_csv("/Users/daana/Projects/SEMESTR_6/ITvPS/itvps_lab_3/news/news02.txt",
           "/Users/daana/Projects/SEMESTR_6/ITvPS/itvps_lab_3/itvps_lab_3_db")
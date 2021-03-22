from prettytable import PrettyTable


def count_p_eh_flu(answers):
    flu = {
        'p_h': 0.01,
        'p_eh': [0.9, 0.01, 0.9, 0.05, 0.8],
        'p_e-h': [0.05, 0.8, 0.1, 0.8, 0.1]
    }
    pe1 = 0
    pe = 0
    pe_result = []
    for i in range(len(answers)):
        if answers[i] == "да":
            if i == 0:
                pe1 = flu['p_eh'][i] * flu['p_h']/(flu['p_eh'][i]*flu['p_h'] + flu['p_e-h'][i] * (1-flu['p_h']))
                pe_result.append(pe1)
            else:
                pe = flu['p_eh'][i] * pe1/(flu['p_eh'][i]*pe1 + flu['p_e-h'][i] * (1-pe1))
                #print(pe)
                pe1 = pe
                pe_result.append(pe1)
        elif answers[i] == "нет":
            if i == 0:
                pe1 = flu['p_eh'][i] * flu['p_h']/(flu['p_eh'][i]*flu['p_h'] + flu['p_e-h'][i] * (1-flu['p_h']))
                pe_result.append(pe1)
            else:
                pe = (1 - flu['p_eh'][i]) * pe1/((1 - flu['p_eh'][i])*pe1 + (1 - flu['p_e-h'][i]) * (1-pe1))
                #print(pe)
                pe1 = pe
                pe_result.append(pe1)
    # print(pe_result)
    return pe_result


def count_p_eh_poisoning(answers):
    poisoning = {
        'p_h': 0.01,
        'p_eh': [0.05, 0.8, 0.1, 0.8, 0.1],
        'p_e-h': [0.9, 0.01, 0.9, 0.05, 0.8]
    }
    pe1 = 0
    pe = 0
    pe_result = []
    for i in range(len(answers)):
        if answers[i] == "да":
            if i == 0:
                pe1 = poisoning['p_eh'][i] * poisoning['p_h']/(poisoning['p_eh'][i]*poisoning['p_h'] + poisoning['p_e-h'][i] * (1-poisoning['p_h']))
                pe_result.append(pe1)
            else:
                pe = poisoning['p_eh'][i] * pe1/(poisoning['p_eh'][i]*pe1 + poisoning['p_e-h'][i] * (1-pe1))
                #print(pe)
                pe1 = pe
                pe_result.append(pe1)
        elif answers[i] == "нет":
            if i == 0:
                pe1 = poisoning['p_eh'][i] * poisoning['p_h']/(poisoning['p_eh'][i]*poisoning['p_h'] + poisoning['p_e-h'][i] * (1-poisoning['p_h']))
                pe_result.append(pe1)
            else:
                pe = (1 - poisoning['p_eh'][i]) * pe1/((1 - poisoning['p_eh'][i])*pe1 + (1 - poisoning['p_e-h'][i]) * (1-pe1))
                #print(pe)
                pe1 = pe
                pe_result.append(pe1)
    # print(pe_result)
    return pe_result


questions = ['Высокая температура?', 'Боль в животе?', 'Кашель?', 'Тошнота?', 'Головная боль?']
th = ['Симптом', 'Ответ', 'P(Грипп)', 'P(Отравление)']
answers = []
for i in questions:
    print(i)
    answer = input().lower()
    answers.append(answer)

pe_flu = count_p_eh_flu(answers)
pe_poison = count_p_eh_poisoning(answers)

print("|                   Симптом| Ответ|                 P(Грипп)|            P(Отравление)")
for i in range(len(questions)):
    print(f"|{questions[i].rjust(26)}|{answers[i].rjust(6)}|{str(pe_flu[i]).rjust(25)}|{str(pe_poison[i]).rjust(25)}")
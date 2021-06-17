import nltk
from pymorphy2 import MorphAnalyzer
import re
from prettytable import PrettyTable
import random


def make_tags(sentence):
    morph = MorphAnalyzer()
    tags = {'NOUN': 'N', 'NPRO': 'N', 'ADJF': 'A', 'ADJS': 'A', 'PRTF': 'A', 'PRTS': 'V', 'NUMR': 'A', 'VERB': 'V',
            'INFN': 'V', 'GRND': 'V', 'ADVB': 'D', 'PREP': 'P', 'PRCL': 'P', 'CONJ': 'P'}
    tokens = [token for token in nltk.word_tokenize(sentence)]
    tokens_tags = [tags[morph.parse(token)[0].tag.POS] for token in nltk.word_tokenize(sentence)]
    return [tokens, tokens_tags]


def not_empty(arr, index):
    for i in range(len(arr[index:])):
        if arr[i] != '-':
            return i
        else:
            return None


def apply_rules(tagged_sentences):
    rules = {'N': 'NP', 'PP': 'NP', 'NP NP': 'NP', 'A NP': 'NP', 'P NP': 'PP',
             'V V': 'VP', 'V NP': 'VP', 'D VP': 'VP', 'D V': 'VP', 'V D': 'VP', 'VP NP': 'VP', 'NP VP': 'S', 'VP': 'S'}

    iteration = 0
    while 'S' != tagged_sentences[-1][-1]:
        # while 5 != iteration:
        current_arr = tagged_sentences[-1]
        iteration = iteration + 1
        join_arr = ' '.join(current_arr)
        new_arr = []
        for i, j in rules.items():
            pattern = '\s' + i + '\s'
            replacing = re.sub(pattern, ' ' + j + ' ', ' ' + join_arr + ' ').strip()
            # print(iteration, replacing, ' --------', j, '-------', pattern, join_arr)
            if replacing != join_arr:
                new_arr.append(replacing)

        # print(iteration, new_arr)
        if len(new_arr) != 0:
            new_arr = new_arr[0].split()
            tagged_sentences.append(new_arr)
            # print(new_arr)

    return tagged_sentences


if __name__ == '__main__':
    table = PrettyTable()
    text1 = 'Этот алгоритм показан на конкретном примере. Эта информация	представлена на	естественном языке. '
    text2 = 'Понимание	смысла	трактуется как	переход	от текста к формализованному представлению его смысла.'
    text3 = 'Проблема	синтеза	речи трактуется	как	переход	от	формализованного представления	смысла	к текстам	на	естественном языке.'
    text4 = 'Эти	проблемы	возникают	при	решении	ряда	прикладных	задач	с	использованием	текста.'
    text5 = 'К	декларативной	части	относятся	словари	единиц	языка	и	различного	рода	грамматические	таблицы.'
    patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
    symb = ['*', '~', '^', '`']
    sentences = nltk.tokenize.sent_tokenize(text4)
    sentences = [re.sub(patterns, ' ', sentence, flags=re.MULTILINE) for sentence in sentences]
    for sentence in sentences:
        tagged_sentences = make_tags(sentence)
        field_names = [i + symb[random.randint(0, 3)] for i in tagged_sentences[0]]
        table.field_names = field_names

        applied_rules = apply_rules(tagged_sentences)
        for i in applied_rules[1:]:
            table.add_row(i + ['-'] * (len(tagged_sentences[0]) - len(i)))

        print(table)

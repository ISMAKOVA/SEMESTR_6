import pandas as pd
import re
from pyprover import *
from termcolor import colored

# data = [{str:'', needOnEnd:bool, res: [0-false;1-true;2-mayBe], func: def func(me, nextObj), innerNode:[obj, obj], nextObj:obj},{}]
statements_conclusions = {
    "P": ['Если идет дождь, то нежарко. Если светит солнце, то жарко. Идет дождь.',
          'Экзамен сдан вовремя или сессия продлена. Если сессия ' +
          'продлена, то курсовая работа не сдана или не зачтены лабораторные работы. ' +
          'Курсовая работа сдана. Экзамен не сдан вовремя. ',
          'Если имеет место денежная эмиссия, то растет курс ' +
          'доллара. Если не имеет место денежная эмиссия и не растет инфляция, то не растет курс доллара. ' +
          'не растет инфляция.', 'или Джон переутомился или Джон болен. Если  Джон переутомился ,' +
          ' то Джон раздражается. Джон не раздражается.',
          'Если налоги в бюджет не собраны, то либо бюджет секвестируется, либо правительство уходит в отставку. Если бюджет секвестируется, то уровень жизни падает. Налоги в бюджет не собраны'],
    "Z": ['Нежарко и не светит солнце.', 'неверно, если курсовая работа сдана , то зачтены лабораторные работы.',
          'Имеет место денежная эмиссия и растет курс доллара или не имеет место денежная эмиссия и не растет курс доллара.',
          'Джон болен.',
          'Либо уровень жизни падает, либо уровень жизни не падает и правительство уходит в отставку.']
}

data = [{}]
alphabet = 'ABCDEFGHIJKLMNOP'
last_index = 0
blocks = {}
nodes = []
hypot = {}

regex_expressions = {
    "if": [r"(?:если([\w\sА-яЁё,]+), то([\w\sА-яЁё,]+))", '->'],
    'or': [r"(?:либо|или|)(?:([\w\sА-яЁё,]+)(?: или|\, либо)([\w\sА-яЁё,]+))", '|'],
    'and': [r"(?:([\w\sА-яЁё,]+) и ([\w\sА-яЁё,]+))", '&'],
}


def is_not(obj):
    if ' не' in " " + obj:
        obj = (" " + obj).replace(' не', '').strip()
        return [obj, 0]
    return [obj, 1]


def reverse(obj):
    if 'неверно' in obj['txt']:
        obj['nodeStr'] = "~(" + obj['nodeStr'] + ")"


def get_symbol(string):
    global last_index
    global alphabet
    if string == '':
        return -1
    for key in blocks:
        if blocks[key][0] == string.strip():
            return key
    sym = alphabet[last_index]
    blocks[sym] = [string.strip(), False]
    last_index += 1
    return sym


def refactor(string, cycle=False, absolute=False, view=True):
    br = False
    node = None
    for reg in regex_expressions:
        matches = re.findall(regex_expressions[reg][0], string)
        if len(matches) > 0 and len(matches[0]) > 1:
            part1 = is_not(matches[0][0])  # проверка на [не] для узла 1
            node1 = refactor(matches[0][0], True, absolute, view)
            is_1_simple = True
            if 'do' in node1.keys():
                nodes.append(node1)
                is_1_simple = False
            part2 = is_not(matches[0][1])  # проверка на [не] для узла 2
            node2 = refactor(matches[0][1], True, absolute, view)
            is_2_simple = True
            if 'do' in node2.keys():
                nodes.append(node2)
                is_2_simple = False
            symbol1 = get_symbol(part1[0])  # получение символа для узла 1
            symbol2 = get_symbol(part2[0])  # получение символа для узла 2
            is_no1 = part1[1]
            is_no2 = part2[1]
            if not is_1_simple:
                symbol1 = node1['nodeStr']
                is_no1 = 1
            if not is_2_simple:
                symbol2 = node2['nodeStr']
                is_no2 = 1
            node = {'txt': string.strip(), 'notf': is_no1, 'symf': symbol1, 'nott': is_no2, 'symt': symbol2,
                    'do': regex_expressions[reg][1], 'nodeStr': None}
            node['nodeStr'] = create_node_string(node)
            if absolute:
                node['absolute'] = True
            if view:
                node['n'] = 1
            reverse(node)
            nodes.append(node)
            br = True
            break
    if br:
        return node
    part1 = is_not(string)
    symbol1 = get_symbol(part1[0])
    node = {'txt': string.strip(), 'notf': part1[1], 'symf': symbol1}
    node['nodeStr'] = create_node_string(node)
    if not cycle or absolute:
        node['absolute'] = True
    if view:
        node['n'] = 1
    reverse(node)
    nodes.append(node)
    return node


def split_text(text):
    sentences = list(filter(None, text.lower().split('.')))
    for sentence in sentences:
        if sentence == '':
            sentences.remove(sentence)
    for stInd in range(0, len(sentences)):
        if stInd == len(sentences) - 1:
            refactor(sentences[stInd], False, True)
        else:
            refactor(sentences[stInd])
    return nodes


def set_hypothesis(string):
    return refactor(' ' + string.lower().replace('.', ' '), view=False)


def create_node_string(node):
    n1 = '~'
    n2 = '~'
    if node['notf'] == 1:
        n1 = ''
    if 'do' in node.keys():
        if node['nott'] == 1:
            n2 = ''
        return (f'({n1}{node["symf"]} {node["do"]} {n2}{node["symt"]})')
    else:
        return (f'{n1}{node["symf"]}')


def removeDubl(nodes):
    forDel = []
    for nodeSr in nodes:
        for ao in nodes:
            if ao['nodeStr'] in nodeSr['nodeStr'] and ao != nodeSr and 'absolute' not in ao.keys():
                forDel.append(ao)
    for dele in forDel:
        try:
            nodes.remove(dele)
        except:
            nothing = True
    return nodes


def getBooleanDataOf(sym):
    for key in blocks:
        if blocks[key][0] == sym:
            return blocks[key][1]


def get_result(statement, conclusion):
    global nodes
    global blocks
    global last_index
    last_index = 0
    nodes = []
    blocks = {}
    print('----------------------Начало-----------------------------')
    reformat_statement = removeDubl(split_text(statement))
    hypothesis = set_hypothesis(conclusion)
    for b in blocks:
        print(b, blocks[b])
    print(colored('-----------Утверждения--------------', 'green'))
    result_str = ''
    for c in reformat_statement:
        if c == hypothesis:
            continue
        if ('absolute' in c.keys() or len(c['nodeStr']) > 2) and 'n' in c.keys() and len(c['txt']) > 0:
            print(c)
            result_str += c['nodeStr'] + " & "
    result_str = result_str.strip(" & ")
    print(colored('------------Что-имеем---------------', 'magenta'))
    print(result_str)
    print(simplify(expr(result_str)))
    print(colored('----------Что-доказать--------------', 'magenta'))
    print(expr(hypothesis['nodeStr']))
    print(simplify(expr(hypothesis['nodeStr'])))
    result = str(proves(simplify(expr(result_str)), simplify(expr(hypothesis['nodeStr']))))

    if result == 'True':
        print("Заключение: " + colored(result, 'green'))
    else:
        print("Заключение: " + colored(result, 'red'))
    print('----------------------Конец------------------------------')

    result_dict = {"Утверждение": result_str, "Упрощенное утверждение": simplify(expr(result_str)),
                   "Гипотеза": expr(hypothesis['nodeStr']),
                   "Упрощенная гипотеза": simplify(expr(hypothesis['nodeStr'])),
                   "Результат": result}
    return result_dict

# dK =int(input())

def printer(dK):
    global nodes
    global blocks
    global last_index
    last_index = 0
    nodes = []
    blocks = {}
    print('----------------------Начало-----------------------------')
    df = removeDubl(split_text(statements_conclusions['P'][dK]))
    print(df)
    co = set_hypothesis(statements_conclusions['Z'][dK])
    for b in blocks:
        print(b, blocks[b])
    print(colored('------------Гипотеза----------------', 'cyan'))
    print(co)
    print(colored('-----------Утверждения--------------', 'green'))
    resultStr = ''
    for c in df:
        if c == co:
            continue
        if ('absolute' in c.keys() or len(c['nodeStr']) > 2) and 'n' in c.keys() and len(c['txt']) > 0:
            print(c)
            resultStr += c['nodeStr'] + " & "
    resultStr = resultStr.strip(" & ")
    print(colored('------------Что-имеем---------------', 'magenta'))
    print(resultStr)
    print(simplify(expr(resultStr)))
    print(colored('----------Что-доказать--------------', 'magenta'))
    print(expr(co['nodeStr']))
    print(simplify(expr(co['nodeStr'])))
    result = str(proves(simplify(expr(resultStr)), simplify(expr(co['nodeStr']))))
    if result == 'True':
        print("Заключение: " + colored(result, 'green'))
    else:
        print("Заключение: " + colored(result, 'red'))
    print('----------------------Конец------------------------------')


for i in range(0, len(statements_conclusions['P'])):
    printer(i)


# print('---------------------')
# print(stacking(parseP(prefs['P'][1])))


def get_result(statement, conclusion):
    global nodes
    global blocks
    global last_index
    last_index = 0
    nodes = []
    blocks = {}
    print('----------------------Начало-----------------------------')
    reformat_statement = removeDubl(split_text(statement))
    printer(reformat_statement)
    hypothesis = set_hypothesis(conclusion)
    for b in blocks:
        print(b, blocks[b])
    print(colored('-----------Утверждения--------------', 'green'))
    result_str = ''
    for c in reformat_statement:
        if c == hypothesis:
            continue
        if ('absolute' in c.keys() or len(c['nodeStr']) > 2) and 'n' in c.keys() and len(c['txt']) > 0:
            print(c)
            result_str += c['nodeStr'] + " & "
    result_str = result_str.strip(" & ")
    print(colored('------------Что-имеем---------------', 'magenta'))
    print(result_str)
    print(simplify(expr(result_str)))
    print(colored('----------Что-доказать--------------', 'magenta'))
    print(expr(hypothesis['nodeStr']))
    print(simplify(expr(hypothesis['nodeStr'])))
    result = str(proves(simplify(expr(result_str)), simplify(expr(hypothesis['nodeStr']))))

    if result == 'True':
        print("Заключение: " + colored(result, 'green'))
    else:
        print("Заключение: " + colored(result, 'red'))
    print('----------------------Конец------------------------------')

    result_dict = {"Утверждение": result_str, "Упрощенное утверждение": simplify(expr(result_str)),
                   "Гипотеза": expr(hypothesis['nodeStr']),
                   "Упрощенная гипотеза": simplify(expr(hypothesis['nodeStr'])),
                   "Результат": result}
    return result_dict

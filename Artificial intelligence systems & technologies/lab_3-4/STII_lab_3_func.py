import math
import pandas as pd


def get_result(r, g, b):
    brightness = get_brightness_from(r, g, b)
    dictionary = {get_dark(brightness): "Темный", get_middle(brightness): "Средний", get_light(brightness): "Светлый"}
    res = {}
    # for i in sorted(dictionary.keys()):
    #     res[i] = dictionary[i]
    #     print(res[i], dictionary[i])
    return dictionary[sorted(dictionary.keys())[-1]], sorted(dictionary.keys())[-1]


def get_light(x):
    df = pd.read_csv('results2.csv', sep=',')
    a = param_a(df, 'light')
    k = param_k(df, 'light')
    return 1 / (1 + math.pow(math.e, (-k * (x - a))))


def get_dark(x):
    df = pd.read_csv('results2.csv', sep=',')
    a = param_a(df, 'dark')
    k = param_k(df, 'dark')
    return 1 / (1 + math.pow(math.e, (-k * (x - a))))


def get_middle(x):
    df = pd.read_csv('results2.csv', sep=',')
    a = param_a(df, 'middle')
    k = param_k(df, 'middle')
    return math.pow(math.e, (-k * abs(x - a)))


def param_a(df, column):
    a_min = 101
    a_max = -1
    i = 0
    for aVar in df[column]:
        count = df.iloc[i, df.columns.get_loc("dark")]+df.iloc[i, df.columns.get_loc("middle")]+df.iloc[i, df.columns.get_loc("light")]
        if round(aVar / count, 1) == 0.5:
            if i > a_max:
                a_max = i
            if i < a_min:
                a_min = i
        i += 1
    return round((a_max + a_min) / 2)


def param_k(df, column):
    a = param_a(df, column)
    var = get_check_var(df, column)
    count = df.iloc[var, df.columns.get_loc("dark")]+df.iloc[var, df.columns.get_loc("middle")] + \
            df.iloc[var, df.columns.get_loc("light")]
    v = df.iloc[var, df.columns.get_loc(column)]
    return ((-math.log(v / count, math.e)) / abs(var - a)) if column == 'middle' else \
        (-math.log(1 / (v / count) - 1, math.e)) / (var - a)


def get_check_var(df, column):
    i = 0
    a = param_a(df, column)
    for a_var in df[column]:
        if (a_var != 0 and a_var != 1 and i != a
                and a_var != df.iloc[i, df.columns.get_loc("dark")]+df.iloc[i, df.columns.get_loc("middle")] +
                df.iloc[i, df.columns.get_loc("light")]):
            return i
        i += 1


def set_result(r, g, b, category):
    df = pd.read_csv('results2.csv', sep=',')
    brightness = get_brightness_from(r, g, b)
    df.iloc[brightness, df.columns.get_loc(category)] += 1
    df.iloc[brightness, df.columns.get_loc("number_ppl")] += 1
    df.to_csv('results2.csv', index=False, header=True)


def get_brightness_from(r, g, b):
    r = int(r)/2.55
    g = int(g)/2.55
    b = int(b) / 2.55
    brightness = 0.2126*r+0.7152*g+0.0722*b
    return round(brightness)


dfd = pd.read_csv('results2.csv', sep=',')
# print(param_k(dfd, "light"))
print(get_result(25, 25, 20))
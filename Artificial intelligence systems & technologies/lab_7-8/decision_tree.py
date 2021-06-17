from functools import reduce
import pandas as pd
import math
from termcolor import colored


def entropy(s):
    return -reduce(lambda x, y: x + y,
                   map(lambda x: (x / len(s)) * math.log2(x / len(s)), s.value_counts()))


def make_key_value(s):
    return [k + ":" + str(v) for k, v in sorted(s.value_counts().items())]


def id3(data_frame):
    tree = {
        "name": "decision tree " + data_frame.columns[-1] + " " + str(make_key_value(data_frame.iloc[:, -1])),
        "df": data_frame,
        "ends": [],
    }
    current_tree = [tree]

    while len(current_tree) != 0:
        n = current_tree.pop(0)
        df_n = n["df"]

        if 0 == entropy(df_n.iloc[:, -1]):
            continue
        attrs = {}
        for attr in df_n.columns[:-1]:
            attrs[attr] = {"entropy": 0, "dfs": [], "values": []}
            for value in sorted(set(df_n[attr])):
                df_m = df_n.query(attr + "=='" + value + "'")
                attrs[attr]["entropy"] += entropy(df_m.iloc[:, -1]) * df_m.shape[0] / df_n.shape[0]
                attrs[attr]["dfs"] += [df_m]
                attrs[attr]["values"] += [value]
                pass
            pass

        if len(attrs) == 0:
            continue

        attr = min(attrs, key=lambda x: attrs[x]["entropy"])
        for d, v in zip(attrs[attr]["dfs"], attrs[attr]["values"]):
            m = {"name": attr + " - " + v, "ends": [], "df": d.drop(columns=attr)}
            n["ends"].append(m)
            current_tree.append(m)
        pass

    def to_str(tree, indent=""):
        s = indent + tree["name"] + str(make_key_value(tree["df"].iloc[:, -1]) if len(tree["ends"]) == 0 else "") + "\n"
        for e in tree["ends"]:
            s += to_str(e, indent + "  ")
            pass
        return s

    # print(tree)
    print(to_str(tree))
    return tree


def make_questions(tree):
    for i in range(len(tree["ends"])):
        e = tree["ends"][i]
        if i != len(tree["ends"]) - 1:
            y = colored('y', 'green')
            n = colored('n', 'red')
            ans = input(e["name"] + "? " + y + "/" + n)
            if ans == "y":
                if len(e["ends"]) != 0:
                    make_questions(e)
                else:
                    print(str(make_key_value(e["df"].iloc[:, -1])[0]))
                    return str(make_key_value(e["df"].iloc[:, -1]))
            else:
                continue
        else:
            if len(e["ends"]) != 0:
                make_questions(e)
            else:
                print(str(make_key_value(e["df"].iloc[:, -1])[0]))
                return str(make_key_value(e["df"].iloc[:, -1]))


if __name__ == '__main__':
    data = pd.read_excel('растения.xls',
        engine='xlrd')
    d = data.to_dict()
    p = {}
    for key in d.keys():
        p[str(key).replace(" ", "")] = [str(val) for val in d[key].values()]
    df = pd.DataFrame(p)
    make_questions(id3(df))

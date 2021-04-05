import sys
import qdarkgraystyle
from PyQt5.QtGui import QIntValidator, QColor, QPainter
from PyQt5.QtWidgets import *
import math
import pandas as pd


def get_result(r, g, b):
    brightness = get_brightness_from(r, g, b)
    dictionary = {get_dark(brightness): "Темный", get_middle(brightness): "Средний", get_light(brightness): "Светлый"}
    for i in sorted(dictionary.keys()):
        print(i, dictionary[i])
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


class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(AppWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Система нечеткой логики")

        self.Width = 1200
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        self.tabs = Tabs(self)
        self.setCentralWidget(self.tabs)
        self.show()


class Tabs(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.Width = 1200
        self.height = int(0.618 * self.Width)
        self.tabs.resize(self.Width, self.height)

        self.tab_expert = TabForExpert()
        self.tab_analysis = TabForAnalysis()
        # Add tabs
        self.tabs.addTab(self.tab_expert, "Режим эксперта")
        self.tabs.addTab(self.tab_analysis, "Режим анализа")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class TabForExpert(QWidget):
    def __init__(self):
        super().__init__()

        self.Width = 1200
        self.onlyInt = QIntValidator(0, 255)
        self.R = QLineEdit(self)
        self.R.setPlaceholderText("Значение для красного цвета от 0 до 255")
        self.R.setValidator(self.onlyInt)

        self.G = QLineEdit(self)
        self.G.setPlaceholderText("Значение для зеленого цвета от 0 до 255")
        self.G.setValidator(self.onlyInt)

        self.B = QLineEdit(self)
        self.B.setPlaceholderText("Значение для синего цвета от 0 до 255")
        self.B.setValidator(self.onlyInt)

        self.button = QPushButton('Задать цвет', self)
        self.button_save = QPushButton('Сохранить', self)
        self.combo = QComboBox(self)
        self.combo.addItems(["dark", "middle", "light"])
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.R, 0, 0)
        self.layout.addWidget(self.G, 0, 1)
        self.layout.addWidget(self.B, 0, 2)
        self.layout.addWidget(self.button, 0, 3)

        self.s = QGraphicsScene()
        self.s.setBackgroundBrush(QColor(0, 0, 0))
        self.g = QGraphicsView(self.s)
        self.g.render(QPainter())
        self.label = QLabel(self)
        self.layout.addWidget(self.g, 1, 0, 1, 4)
        self.layout.addWidget(self.combo, 2, 0)
        self.layout.addWidget(self.button_save, 2, 1)
        self.layout.addWidget(self.label, 2, 2)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.btn_clicked)
        self.button_save.clicked.connect(self.write_dataset)

    def btn_clicked(self):
        self.s.setBackgroundBrush(QColor(int(self.R.text()), int(self.G.text()), int(self.B.text())))
        self.g.render(QPainter())

    def write_dataset(self):
        brightness = get_brightness_from(int(self.R.text()), int(self.G.text()), int(self.B.text()))
        self.label.setText("Яркость: "+str(brightness))
        category = self.combo.currentText()
        set_result(int(self.R.text()), int(self.G.text()), int(self.B.text()), category)


class TabForAnalysis(QWidget):
    def __init__(self):
        super().__init__()

        self.Width = 1200
        self.onlyInt = QIntValidator(0, 255)
        self.R = QLineEdit(self)
        self.R.setPlaceholderText("Значение для красного цвета от 0 до 255")
        self.R.setValidator(self.onlyInt)

        self.G = QLineEdit(self)
        self.G.setPlaceholderText("Значение для зеленого цвета от 0 до 255")
        self.G.setValidator(self.onlyInt)

        self.B = QLineEdit(self)
        self.B.setPlaceholderText("Значение для синего цвета от 0 до 255")
        self.B.setValidator(self.onlyInt)

        self.button = QPushButton('Определить цвет', self)
        self.label = QLabel(self)

        self.s = QGraphicsScene()
        self.s.setBackgroundBrush(QColor(0, 0, 0))
        self.g = QGraphicsView(self.s)
        self.g.render(QPainter())

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.R, 0, 0)
        self.layout.addWidget(self.G, 0, 1)
        self.layout.addWidget(self.B, 0, 2)
        self.layout.addWidget(self.button, 0, 3)
        self.layout.addWidget(self.g, 1, 0, 1, 4)
        self.layout.addWidget(self.label, 2, 0)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.get_result)


    def get_result(self):
        category, count = get_result(int(self.R.text()), int(self.G.text()), int(self.B.text()))
        self.s.setBackgroundBrush(QColor(int(self.R.text()), int(self.G.text()), int(self.B.text())))
        self.g.render(QPainter())
        self.label.setText("Результат: {0} ({1})".format(category, count))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    window = AppWindow()

    sys.exit(app.exec_())

# 10139,2364,6216,6286

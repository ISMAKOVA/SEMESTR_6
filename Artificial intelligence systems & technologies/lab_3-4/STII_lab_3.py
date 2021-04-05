import sys
import qdarkgraystyle
from PyQt5.QtGui import QIntValidator, QColor, QPainter
from PyQt5.QtWidgets import *


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
        self.combo.addItems(["Темный", "Средний", "Светлый"])
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.R, 0, 0)
        self.layout.addWidget(self.G, 0, 1)
        self.layout.addWidget(self.B, 0, 2)
        self.layout.addWidget(self.button, 0, 3)

        self.s = QGraphicsScene()
        self.s.setBackgroundBrush(QColor(0, 0, 0))
        self.g = QGraphicsView(self.s)
        self.g.render(QPainter())

        self.layout.addWidget(self.g, 1, 0, 1, 4)
        self.layout.addWidget(self.combo, 2, 0)
        self.layout.addWidget(self.button_save, 2, 1)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        self.s.setBackgroundBrush(QColor(int(self.R.text()), int(self.G.text()), int(self.B.text())))
        self.g.render(QPainter())
        # text = self.comboBox.currentText()

    def write_dataset(self):

        return ""


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
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.R, 0, 0)
        self.layout.addWidget(self.G, 0, 1)
        self.layout.addWidget(self.B, 0, 2)
        self.layout.addWidget(self.button, 0, 3)
        self.layout.addWidget(self.label, 1, 0)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    window = AppWindow()

    sys.exit(app.exec_())

# 10139,2364,6216,6286

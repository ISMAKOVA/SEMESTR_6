import sys
import qdarkgraystyle
from PyQt5.QtGui import QIntValidator, QColor, QPainter
from PyQt5.QtWidgets import *


class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(AppWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Метод резолюций в логике высказываний")

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
        # Add tabs
        self.tabs.addTab(self.tab_expert, "Метод резолюций в логике высказываний")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class TabForExpert(QWidget):
    def __init__(self):
        super().__init__()

        self.Width = 1200
        self.linebox1 = QPlainTextEdit(self)
        self.linebox1.setPlaceholderText("Утверждения")
        self.linebox1.setMinimumHeight(150)

        self.linebox2 = QPlainTextEdit(self)
        self.linebox2.setPlaceholderText("Заключения")
        self.linebox2.setMinimumHeight(150)
        self.button = QPushButton('Установить истинность', self)

        self.result = QLabel(self)
        self.result.setText("Результат")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.linebox1)
        self.layout.addWidget(self.linebox2)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.result)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        text1 = self.linebox1.toPlainText()
        text2 = self.linebox2.toPlainText()
        self.result.setText(text1+text2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    window = AppWindow()

    sys.exit(app.exec_())



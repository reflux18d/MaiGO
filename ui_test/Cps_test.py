import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt




class CpsWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Cps")
        self.setWindowIcon(QIcon('F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/bear.png'))
        self.resize(500, 500)
        self.more_widget()
        
    def more_widget(self):
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        count_bar = QGroupBox("点击次数")
        who_are_you = QGroupBox("你是谁？")
        maimai = QGroupBox("迫真洗衣机")
        layout.addWidget(count_bar)
        layout.addWidget(who_are_you)
        layout.addWidget(maimai)

        count = QHBoxLayout()
        count_bar.setLayout(count)
        i_am = QVBoxLayout()
        who_are_you.setLayout(i_am)
        buttons = QGridLayout()
        maimai.setLayout(buttons)

        self.total = 0
        self.total_label = QLabel(f"点击次数: {self.total}")
        count.addWidget(self.total_label)

        self.text = QTextEdit("我是")
        i_am.addWidget(self.text)

        button_list = [QPushButton(f"{i}") for i in range(1, 9)]
        pos_list = [(0, 2), (1, 3), (2, 3), (3, 2), (3, 1), (2, 0), (1, 0), (0, 1)]
        for button, pos in zip(button_list, pos_list):
            row, col = pos
            buttons.addWidget(button, row, col)
            button.clicked.connect(lambda state, b = button:
                                   self.hit(b))     

    def hit(self, button: QPushButton):
        self.total += 1
        self.total_label.setText(f"点击次数: {self.total}")
        history = self.text.toPlainText()
        self.text.setPlainText(history + button.text())


if __name__ == "__main__":
    app = QApplication([])

    window = CpsWindow()

    window.show()

    app.exec()
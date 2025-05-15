import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MaiWindow(QWidget):
    def __init__(self, parent = None, flags = Qt.WindowFlags()):
        super().__init__(parent, flags)

        self.setWindowTitle("MaiGO!!!!!")
        self.resize(500, 300)

        whole = QVBoxLayout()
        top = QHBoxLayout()
        layout = QVBoxLayout()
        
        icon = QIcon('offline.png')
        label = QLabel("可以和我玩一辈子舞萌吗", alignment=Qt.AlignCenter)
        button = QPushButton("账号")
        button1 = QPushButton("出发!")
        button2 = QPushButton("记录")
        button3 = QPushButton("设置")

        button.setIcon(icon)
        top.addWidget(button)
        top.addStretch(1)
        top.addWidget(button3)

        layout.addStretch(1)
        layout.addWidget(button1)
        layout.addStretch(1)
        layout.addWidget(button2)
        layout.addStretch(1)


        whole.addLayout(top)
        whole.addStretch(1)
        whole.addLayout(layout)
        whole.addStretch(1)
        whole.addWidget(label)

        self.setLayout(whole)

#文件名是Layout时不能运行

if __name__ == "__main__":
    app = QApplication([])

    window = MaiWindow()

    window.show()

    app.exec()
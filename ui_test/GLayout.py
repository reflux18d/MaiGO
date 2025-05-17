import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt




class MapWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moreWidget()
        
    def moreWidget(self):
        self.setWindowTitle("Map")
        self.setWindowIcon(QIcon('F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/bear.png'))
        self.resize(500, 300)

        Glayout = QGridLayout()

        Glayout.addWidget(QPushButton('上地'), 0, 3)
        Glayout.addWidget(QPushButton('北大'), 8, 0, 6, 4)
        Glayout.addWidget(QPushButton('清华'), 6, 4, 8, 6)

        self.setLayout(Glayout)


if __name__ == "__main__":
    app = QApplication([])

    window = MapWindow()

    window.show()

    app.exec()
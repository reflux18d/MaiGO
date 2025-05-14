import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

if __name__ == "__main__":
    app = QApplication(sys.argv) #necessary
    #or app = QApplication([])

    w = QWidget(parent = None, flags = Qt.Widget)

    w.setWindowTitle("MaiGO!!!!!")

    l = QLabel("A program for wmc", w)

    b = QPushButton("GO!", w)

    w.show()

    app.exec()
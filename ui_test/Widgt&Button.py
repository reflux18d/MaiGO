import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt

if __name__ == "__main__":
    app = QApplication(sys.argv) #necessary
    #or app = QApplication([])

    w = QWidget(parent = None, flags = Qt.Widget)

    w.setWindowTitle("My first qt")

    b = QPushButton("Press")

    b.setParent(w)

    w.show()

    v = QWidget(parent = w, flags = Qt.Window)

    b.setParent(v)

    v.show()

    app.exec()
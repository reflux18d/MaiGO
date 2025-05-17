import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == "__main__":
    app = QApplication(sys.argv) #necessary
    #or app = QApplication([])

    w = QWidget()

    w.setWindowTitle("My first qt")

    w.show()

    app.exec()
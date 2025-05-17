import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

if __name__ == "__main__":
    app = QApplication(sys.argv) #necessary
    #or app = QApplication([])

    center = QDesktopWidget().availableGeometry().center()
#    print(center)

    w = QWidget(parent = None, flags = Qt.Widget)
    w.setWindowTitle("MaiGO!!!!!")
    w.resize(960, 480)
    w.move(center)
    icon = QIcon('offline.png')
    print(icon.isNull())
    w.setWindowIcon(icon) #暂不能显示

    label = QLabel("A program for wmc", w)
    label.setGeometry(240, 120, 480, 30) # x, y, width, height

    line = QLineEdit("where to go", w) # 直接帮你输入一部分，可以删除
    line.setPlaceholderText("where to go")
    line.setGeometry(240, 240, 240, 30)

    b = QPushButton("GO!", w)
#    b.resize(b.sizeHint())
    b.setGeometry(240, 360, 60, 30)

    w.show()
    app.exec()
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

class MaiWindow(QWidget):
    def __init__(self, parent = None, flags = Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.ui_init()
        
    def ui_init(self):
        self.setWindowTitle("")
        self.setWindowIcon(QIcon('F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/bear.png'))
        self.resize(500, 300)

        bar = QGroupBox("MaiGO!!")
        option = QGroupBox("options")

        whole = QVBoxLayout()
        top = QHBoxLayout()
        content = QVBoxLayout()
        

        label = QLabel("可以和我玩一辈子舞萌吗", alignment=Qt.AlignCenter)
        button = QPushButton("账号")
        button1 = QPushButton("出发!")
        button2 = QPushButton("记录")
        button3 = QPushButton("设置")

        top.addWidget(button)
        top.addStretch(1)
        top.addWidget(button3)
        bar.setLayout(top)
        button.setIcon(QIcon('F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/bear.png'))

        content.addWidget(button1)
        content.addStretch(1)
        content.addWidget(button2)
        option.setLayout(content)

        whole.addWidget(bar)
#        whole.addStretch(1)
        whole.addWidget(option)
#        whole.addStretch(1)
        whole.addWidget(label)

        self.setLayout(whole)

        #button -> layout -> box -> layout -> window
        #       addw      setl    addw      setl
        #如果不用GroupBox直接对BoxLayout进行addlayout会不能伸缩？
        #效果仍不理想。整体stretch优于局部GroupBox的stretch


#文件名是Layout时不能运行

if __name__ == "__main__":
    app = QApplication([])

    window = MaiWindow()

    window.show()

    app.exec()
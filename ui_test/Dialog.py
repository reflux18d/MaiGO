import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTextEdit, QInputDialog

# GPT:
class DiaryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("日记")
        self.setWindowIcon(QIcon('F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/bear.png'))
        self.resize(500, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.text_display = QTextEdit(self)
        self.text_display.setPlaceholderText("今天出勤干了啥呢...")
        self.layout.addWidget(self.text_display)

        self.input_button = QPushButton("输入", self)
        self.input_button.clicked.connect(self.get_user_input)
        self.layout.addWidget(self.input_button)

    def get_user_input(self):
        text, ok = QInputDialog.getText(self, "输入内容", "请输入内容：")
        if ok and text:
            current = self.text_display.toPlainText()
            self.text_display.setPlainText(current + text)
        
        # 为什么有TextEdit还要弹出输入框啊

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiaryWindow()
    window.show()
    sys.exit(app.exec())
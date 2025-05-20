import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QStackedWidget, QMainWindow
)

class MainPage(QWidget):
    def __init__(self, switch_to_other):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("这是主页面")
        button = QPushButton("出发！")  # 点击切换到其他页面
        button.clicked.connect(switch_to_other)

        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)

class OtherPage(QWidget):
    def __init__(self, switch_to_main):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("你已经到达另一个页面！")
        button = QPushButton("返回")  # 点击切换回主页面
        button.clicked.connect(switch_to_main)

        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("界面切换示例")
        self.resize(400, 200)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # 创建页面
        self.main_page = MainPage(self.show_other_page)
        self.other_page = OtherPage(self.show_main_page)

        self.stack.addWidget(self.main_page)  # index 0
        self.stack.addWidget(self.other_page) # index 1

        self.stack.setCurrentIndex(0)  # 显示主页面

    def show_other_page(self):
        self.stack.setCurrentIndex(1)

    def show_main_page(self):
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
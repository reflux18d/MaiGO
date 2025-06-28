import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject, pyqtSlot, QUrl


class JsBridge(QObject):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    @pyqtSlot(str, str)
    def showInfo(self, name, address):
        self.text_edit.setPlainText(f"【机厅名称】\n{name}\n\n【地址】\n{address}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("舞萌机厅地图")
        self.resize(1000, 600)

        # 主部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # WebEngineView 加载地图
        self.view = QWebEngineView()
        self.view.setUrl(QUrl("http://localhost:8000/arcades2.html"))  # 放置在当前目录
        layout.addWidget(self.view, 2)  # 左边占2份空间

        # 右侧信息展示框
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        layout.addWidget(self.info_display, 1)

        # 设置 JS ↔ Py 通信
        self.channel = QWebChannel()
        self.js_bridge = JsBridge(self.info_display)
        self.channel.registerObject("pyBridge", self.js_bridge)
        self.view.page().setWebChannel(self.channel)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

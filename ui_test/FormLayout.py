import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QPushButton, QCheckBox, QToolButton, QRadioButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtWidgets import QGridLayout, QStackedLayout, QFormLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class RecordWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.more_widget()
        
    def more_widget(self):
        self.setWindowTitle("我的记录")
        self.setWindowIcon(QIcon('F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/bear.png'))
        self.resize(500, 300)
        self.form = QFormLayout()
        self.form.addRow(QLabel("日期"), QLabel("目的地"))
        self.setLayout(self.form)

    def add_record(self, records = []):
        for record in records:
            date, arcade = record
            self.form.addRow(QLabel(date), QLabel(arcade))

class SettingsWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.more_widget()
        
    def more_widget(self):
        self.setWindowTitle("设置")
        self.setWindowIcon(QIcon('F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/bear.png'))
        self.resize(500, 300)

        settings = QVBoxLayout()
        data = QGroupBox("数据")
        outfit = QGroupBox("出装")
        self.data_form = QFormLayout()
        self.outfit_form = QFormLayout()

        data.setLayout(self.data_form)
        outfit.setLayout(self.outfit_form)
        settings.addWidget(data)
        settings.addWidget(outfit)
        self.setLayout(settings)

    def add_data(self, options = []):
        for option in options:
            name, state = option
            off, on = state
            button, text = QCheckBox(name), QLabel(off)
            button.setStyleSheet("background-color: #66ccff; color: white;")
#            text.setStyleSheet("background-color: #66ccff; color: white;")
            self.data_form.addRow(button, text)
            button.stateChanged.connect(
                lambda state, b = button, t = text, on = on, off = off:
                t.setText(on if b.isChecked() else off)
                ) # 闭包 


    def add_outfit(self, options = []):
        for option in options:
            name = option # only name
            self.outfit_form.addRow(QCheckBox(name))


if __name__ == "__main__":

    app = QApplication([])

    window = RecordWindow()

    window.add_record([("5.1", "上地"), ("5.2", "上地")]) # No float for Qlabel

    window.show()

    settings = SettingsWindow()

    settings.add_data([("日记", ("不记录", "记录")), ("通勤", ("无通勤", "有通勤")), ("退勤", ("不退勤", "退勤"))])
    
    settings.add_outfit(["饮料", "手套", "谷子", "板子"])

    settings.show()

    app.exec()
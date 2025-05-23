import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtWidgets import QGridLayout, QFormLayout
from PyQt5.QtWidgets import QStackedWidget, QScrollArea
from PyQt5.QtWidgets import QTextEdit, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt

bear_path = 'F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/bear.png'
online_path = 'F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/offline.png'
map_path = 'F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/map.png'

class StartWindow(QWidget):
    def __init__(self, signal: pyqtSignal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("开始")
#        self.setWindowIcon(QIcon(bear_path))
#        self.resize(800, 400)
        self.signal = signal
        self.set_buttons()
        self.more_widgets()

    def set_buttons(self):
        self.go_button = QPushButton("出发!")
        self.go_button.clicked.connect(lambda: self.signal.emit(1))
        self.record_button = QPushButton("记录")
        self.record_button.clicked.connect(lambda: self.signal.emit(3))
        self.settings_button = QPushButton("设置")
        self.settings_button.clicked.connect(lambda: self.signal.emit(4))
        self.go_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                padding: 10px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            """)
        
        self.go_button.setMaximumWidth(100)
        self.record_button.setMaximumWidth(100)

    def more_widgets(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        top = QHBoxLayout()
        layout.addLayout(top)
        layout.addStretch(1)
        
        top.addWidget(QLabel("用户:"))
        top.addStretch(1)
        top.addWidget(self.settings_button)

        layout.addWidget(self.go_button)
        layout.addStretch(1)
        layout.addWidget(self.record_button)
        layout.addStretch(2)



class MapWindow(QWidget):
    def __init__(self, signal, arcades = ["上地", "五道口", "万柳", "新奥"], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("地图")
#        self.setWindowIcon(QIcon(bear_path))
#        self.resize(800, 400)
        self.signal = signal
        self.arcades = arcades
        self.arcade_buttons = []
        self.set_buttons(arcades)
        self.more_widgets()

    def set_buttons(self, arcades):
        for index, arcade in enumerate(arcades):
            button = QPushButton(arcade)
            button.clicked.connect(lambda: self.signal.emit(2))
            self.arcade_buttons.append(button)

    def more_widgets(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        map_label = QLabel()
        scroll = QScrollArea()
        scroll.setWidget(map_label)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        bottom = QGroupBox()
        layout.addWidget(bottom)

        pixmap = QPixmap(map_path)
        map_label.setPixmap(pixmap)
        
        bottom_layout = QHBoxLayout()
        bottom.setLayout(bottom_layout)
        
        for button in self.arcade_buttons:
            bottom_layout.addWidget(button)

class GoWindow(QWidget):
    def __init__(self, signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal = signal
        self.state = 0  # 0: preparing 1: marching 2: playing 
        self.set_buttons()
        self.more_widgets()
        self.state_update()

    def set_buttons(self):
        self.main_button = QPushButton()
        self.main_button.clicked.connect(lambda: self.state_change(self.state + 1))
        self.main_button.setMaximumWidth(200)

    def more_widgets(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.state_text = QLabel()
        layout.addWidget(self.state_text)
        self.state_text.setAlignment(Qt.AlignCenter)
        
        layout.addStretch(1)
        layout.addWidget(self.main_button)

    def state_change(self, n):
        self.state = n
        self.state_update()

    def state_update(self):
        if self.state == 0:
            self.setWindowTitle("准备中")
            self.main_button.setText("GO!")
            self.state_text.setText("准备好了就开始了哦")

        elif self.state == 1:
            self.setWindowTitle("通勤中")
            self.main_button.setText("到达!")
            self.state_text.setText("GOGOGO!")

        elif self.state == 2:
            self.setWindowTitle("游玩中")
            self.main_button.setText("退勤")
            self.state_text.setText("要继续游玩吗")

        else:
            self.state = 0
            self.state_update()
            self.signal.emit(0)


class RecordWindow(QWidget):
    def __init__(self, signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("记录")
        self.signal = signal
        self.set_buttons()
        self.more_widgets()

    def set_buttons(self):
        self.return_button = QPushButton("返回")
        self.return_button.clicked.connect(lambda: self.signal.emit(0))

    def more_widgets(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        top = QHBoxLayout()
        layout.addLayout(top)
        layout.addStretch(1)

        top.addWidget(self.return_button)
        top.addStretch(1)
                
        self.record_text = QLabel("空空如也")
        layout.addWidget(self.record_text)
        
        
class SettingsWindow(QWidget):
    def __init__(self, signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("设置")
#        self.setWindowIcon(QIcon(bear_path))
#        self.resize(800, 400)
        self.signal = signal
        self.set_buttons()
        self.more_widgets()
        self.add_data([("日记", ("不记录", "记录")), ("通勤", ("无通勤", "有通勤")), ("退勤", ("不退勤", "退勤"))])
        self.add_outfit(["饮料", "手套", "谷子", "板子"])
    
    def set_buttons(self):
        self.return_button = QPushButton("返回")
        self.return_button.clicked.connect(lambda: self.signal.emit(0))

    def more_widgets(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        top = QHBoxLayout()
        data = QGroupBox("数据")
        outfit = QGroupBox("出装")

        layout.addLayout(top)
        layout.addWidget(data)
        layout.addWidget(outfit)

        top.addWidget(self.return_button)
        top.addStretch(1)

        self.data_form = QFormLayout()
        self.outfit_form = QFormLayout()
        data.setLayout(self.data_form)
        outfit.setLayout(self.outfit_form)
        
        

    def add_data(self, options = []):
        for option in options:
            name, state = option
            off, on = state
            button, text = QCheckBox(name), QLabel(off)
#            button.setStyleSheet("background-color: #66ccff; color: white;")
#            text.setStyleSheet("background-color: #66ccff; color: white;")
            self.data_form.addRow(button, text)
            button.stateChanged.connect(
                lambda state, b = button, t = text, on = on, off = off:
                t.setText(on if b.isChecked() else off)
                )
            
    def add_outfit(self, options = []):
        for option in options:
            name = option # only name
            self.outfit_form.addRow(QCheckBox(name))

class MainWindow(QWidget):
    switch_signal = pyqtSignal(int)
    # 0: StartWindow 1: MapWindow 2: GoWindow 
    # 3: RecordWindow 4: SettingsWindow
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("MaiGO!!!!!")
        self.setWindowIcon(QIcon(bear_path))
        self.resize(800, 400)

        self.stack = QStackedWidget()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.stack)

        self.add_windows()
        self.switch_signal.connect(self.switch_to)

    def add_windows(self):
        self.windows = [StartWindow(self.switch_signal),
                        MapWindow(self.switch_signal),
                        GoWindow(self.switch_signal),
                        RecordWindow(self.switch_signal),
                        SettingsWindow(self.switch_signal)]
        for window in self.windows:
            self.stack.addWidget(window)

    def switch_to(self, index):
        self.stack.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()

    window.show()

    app.exec()
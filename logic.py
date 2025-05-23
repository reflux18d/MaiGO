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

from ui_class import Ui_start_window, Ui_record_window, Ui_settings_window
from ui_class import Ui_record_single, Ui_settings_single
from utils import *

bear_path = 'F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/bear.png'
online_path = 'F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/offline.png'
map_path = 'F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/map.png'

class Place:
    def __init__(self, name):
        self.name = name
        self.latitude, self.longitude = 0, 0
        self.visits = 0

    def set_pos(self, lati, longi):
        self.latitude, self.longitude = lati, longi

class Arcade(Place):
    def __init__(self, name):
        super.__init__("Arcade")

class Tour:
    states = ["preparing", "marching", "playing", "ended"]
    def __init__(self):
        self.start_time, self.arrival_time, self.end_time = None, None, None #time
        self.home, self.goal = None, None
        self.transport = None
        self.diary = ""
        self.state = 0

    def here_we_go(self, home: Place = None, st = None):
        self.home = home
        self.start_time = st
        self.state = 1

    def arrived(self, goal: Place = None, at = None):
        self.goal = goal
        self.play_time = at
        self.state = 2

    def end(self, et = None):
        self.end_time = et
        self.state = 3

class User:
    def __init__(self, name):
        self.name = name
        self.data = None
        self.history = [] #list of Tour
        self.achivement = []

class RecordSingle(MethodWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_record_single.Ui_RecordSingle() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        self.time_label = self.ui.time_label
        self.goal_label = self.ui.goal_label

class SettingsSingle(MethodWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_settings_single.Ui_SettingsSingle() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        self.single_layout = self.ui.single_layout

        self.set_widgets()
        self.add_data([("日记", ("不记录", "记录")), ("通勤", ("无通勤", "有通勤")), ("退勤", ("不退勤", "退勤"))])
        self.add_outfit(["饮料", "手套", "谷子", "板子"])

    def set_widgets(self):
        layout = self.single_layout

        top = QHBoxLayout()
        layout.addLayout(top)
        data = QGroupBox("数据")
        outfit = QGroupBox("出装")

        layout.addWidget(data)
        layout.addWidget(outfit)

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
        
        

    def add_data(self, options = []):
        for option in options:
            name, state = option
            off, on = state
            button, text = QCheckBox(name), QLabel(off)
            self.data_form.addRow(button, text)
            button.stateChanged.connect(
                lambda state, b = button, t = text, on = on, off = off:
                t.setText(on if b.isChecked() else off)
                )
            
    def add_outfit(self, options = []):
        for option in options:
            name = option # only name
            self.outfit_form.addRow(QCheckBox(name))



class StartWindow(MethodWidget):
    def __init__(self, signal: pyqtSignal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_start_window.Ui_StartWidget() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局

        self.signal = signal
        self.set_buttons()

    def set_buttons(self):
        self.go_button = self.ui.go_button
        self.record_button = self.ui.record_button
        self.settings_button = self.ui.settings_button
        self.account_button = self.ui.account_button

        self.go_button.clicked.connect(lambda: self.signal.emit(1))
        self.record_button.clicked.connect(lambda: self.signal.emit(3))
        self.settings_button.clicked.connect(lambda: self.signal.emit(4))
        self.account_button.clicked.connect(lambda: None) # TODO

class MapWindow(MethodWidget):
    def __init__(self, signal, arcades = ["上地", "五道口", "万柳", "新奥"], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal = signal
        self.arcades = arcades #机厅列表
        self.arcade_buttons = []
        self.set_buttons(arcades) #动态添加机厅按钮
        self.set_widgets()

    def set_buttons(self, arcades):
        for index, arcade in enumerate(arcades):
            button = QPushButton(arcade)
            button.clicked.connect(lambda: self.signal.emit(2))
            self.arcade_buttons.append(button)

    def set_widgets(self):
        #两个MethodWidget方法
        self.create_layout(QVBoxLayout)
        scroll, bottom = self.more_widgets(QScrollArea(), MGroupBox())

        map_label = QLabel()
        scroll.setWidget(map_label)
        scroll.setWidgetResizable(True)

        pixmap = QPixmap(map_path)
        map_label.setPixmap(pixmap)
        
        bottom_layout = bottom.create_layout(QHBoxLayout)
        
        for button in self.arcade_buttons:
            bottom_layout.addWidget(button)

class GoWindow(MethodWidget):
    def __init__(self, signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal = signal
        self.state = 0  # 0: preparing 1: marching 2: playing 
        self.set_buttons()
        self.set_widgets()
        self.state_update()

    def set_buttons(self):
        self.main_button = QPushButton()
        self.main_button.clicked.connect(lambda: self.state_change(self.state + 1))
        self.main_button.setMaximumWidth(200)

    def set_widgets(self):
        layout = self.create_layout(QVBoxLayout)

        #下面仍然是旧的添加控件方法
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

class RecordWindow(MethodWidget):
    def __init__(self, signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_record_window.Ui_RecordWidget() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        
        record_widget = MethodWidget()
        self.record_layout = record_widget.create_layout(QVBoxLayout)
        self.ui.record_scroll.setWidget(record_widget)
        #record_layout为添加记录的layout

        self.signal = signal
        self.set_buttons()
        self.add_record(RecordSingle(), RecordSingle())

    def set_buttons(self):
        self.return_button = self.ui.return_button
        self.return_button.clicked.connect(lambda: self.signal.emit(0))
        
    def add_record(self, *widgets):
        for widget in widgets:
            self.record_layout.addWidget(widget)

class SettingsWindow(MethodWidget):
    def __init__(self, signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_settings_window.Ui_SettingsWidget() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        
        settings_widget = MethodWidget()
        self.settings_layout = settings_widget.create_layout(QVBoxLayout)
        self.ui.settings_scroll.setWidget(settings_widget)
        # record_layout为添加记录的layout

        self.signal = signal
        self.set_buttons()
        self.add_settings(SettingsSingle(), SettingsSingle())
    """
        self.add_data([("日记", ("不记录", "记录")), ("通勤", ("无通勤", "有通勤")), ("退勤", ("不退勤", "退勤"))])
        self.add_outfit(["饮料", "手套", "谷子", "板子"])"""
    
    def set_buttons(self):
        self.return_button = self.ui.return_button
        self.return_button.clicked.connect(lambda: self.signal.emit(0))

    def add_settings(self, *widgets):
        for widget in widgets:
            self.settings_layout.addWidget(widget)
        
    

class MainWindow(QWidget):
    switch_signal = pyqtSignal(int)
    # 传给每个窗口的切换信号
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
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtWidgets import QGridLayout, QFormLayout
from PyQt5.QtWidgets import QStackedWidget, QScrollArea
from PyQt5.QtWidgets import QTextEdit, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt,QTimer
from datetime import datetime

from ui_class.start_window import Ui_StartWidget
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

    def here_we_go(self, home: Place = None, goal:Arcade=None):
        self.home = home
        self.start_time = datetime.now()
        self.goal=goal
        self.state = 1

    def arrived(self):
        
        self.play_time = datetime.now()
        self.state = 2

    def end(self):
        self.end_time = datetime.now()
        self.state = 3
        return self.calculate_stats()
    
    def calculate_stats(self):
        if not all([self.start_time,self.play_time,self.end_time]):
            return None
        return {
            "travel_time": (self.play_time - self.start_time).total_seconds() / 60,  # 分钟
            "play_duration": (self.end_time - self.play_time).total_seconds() / 60,  # 分钟
             "from_to": f"{self.home.name} → {self.goal.name}"
        }

class User:
    def __init__(self, name):
        self.name = name
        self.data = None
        self.history = [] #list of Tour
        self.achivement = []

class StartWindow(MethodWidget):
    def __init__(self, signal: pyqtSignal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_StartWidget() # 创建 UI 类实例
        self.ui.setupUi(self) # 从基类获取所有已有布局

        self.signal = signal
        self.set_buttons()

    def set_buttons(self):
        self.ui.go_button.clicked.connect(lambda: self.signal.emit(1))
        self.ui.record_button.clicked.connect(lambda: self.signal.emit(3))
        self.ui.settings_button.clicked.connect(lambda: self.signal.emit(4))
        self.ui.account_button.clicked.connect(lambda: None) # TODO

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
            button.clicked.connect(self.select_arcade)
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
    #关于记录终点
    def select_arcade(self,arcade):
        go_window=self.parent().findChild(GoWindow)
        if go_window:
            go_window.selected_arcade=arcade
        self.signal.emit(2)

class GoWindow(MethodWidget):
    def __init__(self, signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal = signal
        self.state = 0  # 0: preparing 1: marching 2: playing 
        self.set_buttons()
        self.set_widgets()
        self.state_update()

        #关于实现tour的新增代码
        self.current_tour=None
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_timer_display)
        self.time_elapsed=0

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

         #新增了计时器
        self.timer_label=QLabel("00:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer_label)

    #新增了计时的相关实现
    def start_timer(self):
        self.time_elapsed=0
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def update_timer_display(self):
        self.time_elapsed+=1
        minutes=self.time_elapsed//60
        seconds=self.time_elapsed%60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
    def state_change(self, n):
        self.state = n
        self.state_update()

    def state_update(self):
        if self.state == 0:
            self.setWindowTitle("准备中")
            self.main_button.setText("GO!")
            self.state_text.setText("准备好了就开始了哦")
            #新增的计时相关代码
            

        elif self.state == 1:
            self.setWindowTitle("通勤中")
            self.main_button.setText("到达!")
            self.state_text.setText("GOGOGO!")
            if hasattr(self,'selected_arcade'):
                self.current_tour=Tour()
                self.current_tour.here_we_go(Place("pku"),Place(self.selected_arcade))
                print(self.current_tour.start_time)
                print(self.current_tour.goal.name)
                self.start_timer()
            

        elif self.state == 2:
            self.setWindowTitle("游玩中")
            self.main_button.setText("退勤")
            self.state_text.setText("要继续游玩吗")
            if self.current_tour:
                self.current_tour.arrived()
                print(self.current_tour.play_time)
               

        else:
            #self.state = 0
            #self.state_update()
            if self.current_tour:
                stats=self.current_tour.end()
                self.stop_timer()
                print(self.current_tour.end_time)
                print(stats)
            self.signal.emit(0)

class RecordWindow(MethodWidget):
    def __init__(self, signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("记录")
        self.signal = signal
        self.set_buttons()
        self.set_widgets()

    def set_buttons(self):
        self.return_button = QPushButton("返回")
        self.return_button.clicked.connect(lambda: self.signal.emit(0))

    def set_widgets(self):
        layout = self.create_layout(QVBoxLayout)

        top = QHBoxLayout()
        layout.addLayout(top)
        layout.addStretch(1)

        top.addWidget(self.return_button)
        top.addStretch(1)
                
        self.record_text = QLabel("空空如也")
        layout.addWidget(self.record_text)

class SettingsWindow(MethodWidget):
    def __init__(self, signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("设置")
        self.signal = signal
        self.set_buttons()
        self.more_widgets()
        self.add_data([("日记", ("不记录", "记录")), ("通勤", ("无通勤", "有通勤")), ("退勤", ("不退勤", "退勤"))])
        self.add_outfit(["饮料", "手套", "谷子", "板子"])
    
    def set_buttons(self):
        self.return_button = QPushButton("返回")
        self.return_button.clicked.connect(lambda: self.signal.emit(0))

    def more_widgets(self):
        layout = self.create_layout(QVBoxLayout)

        top = QHBoxLayout()
        layout.addLayout(top)
        data = QGroupBox("数据")
        outfit = QGroupBox("出装")

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
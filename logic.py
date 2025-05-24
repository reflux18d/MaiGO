import sys
# 调用PyQt5相关组件
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtWidgets import QGridLayout, QFormLayout
from PyQt5.QtWidgets import QStackedWidget, QScrollArea
from PyQt5.QtWidgets import QTextEdit, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtCore import Qt

# 调用ui_class文件夹中使用QTdesigner写好的窗口类文件
from ui_class import Ui_start_window, Ui_record_window, Ui_settings_window, Ui_go_window, Ui_map_window
from ui_class import Ui_record_single, Ui_settings_single

# 调用utils中自定义的Method基类
from utils import *

from datetime import datetime
import os

bear_path = 'F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/bear.png'
online_path = 'F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/offline.png'
map_path = 'F:/cjdl/vsc/homework/ChSh/MaiGO/ui_test/map.png'

# MainWindow中main_signal:pyqtSignal(str)的绑定函数字典
# 现有val函数输入均为MainWindow的self, 均在MainWindow中定义
CMD_DICT = {
        "start_window": lambda self: MainWindow.switch_to(self, 0),
        "map_window": lambda self: MainWindow.switch_to(self, 1),
        "go_window": lambda self: MainWindow.switch_to(self, 2),
        "record_window": lambda self: MainWindow.switch_to(self, 3),
        "settings_window": lambda self: MainWindow.switch_to(self, 4),
        "save_record": lambda self: MainWindow.save_record(self)
    }


class Place:
    def __init__(self, name = "Peking University"):
        self.name = name
        self.latitude, self.longitude = 0, 0
        self.visits = 0

    def __str__(self):
        return self.name

    def set_pos(self, lati, longi):
        self.latitude, self.longitude = lati, longi


class Arcade(Place):
    def __init__(self, name, info_text = ""):
        super().__init__(name)
        self.info_text = info_text
    
    def description(self) -> str:
        return self.info_text


class Tour:
    def __init__(self, home, goal):
        self.start_time = None
        self.arrival_time = None
        self.end_time = None
        self.home = home  # 起点(Place对象)
        self.goal = goal  # 终点(Arcade对象)
        self.state = 0  # 0:准备 1:通勤 2:游玩 3:结束
        self.info = {} # 其他记录数据种类 key: str  val: varible
    
    def start_tour(self):
        """开始出勤"""
        self.start_time = datetime.now()
        self.state = 1
    
    def arrived(self):
        """到达目的地"""
        self.arrival_time = datetime.now()
        self.state = 2
    
    def end_tour(self):
        """结束出勤"""
        self.end_time = datetime.now()
        self.state = 3
        self._calculate_stats()
    
    def _calculate_stats(self):
        """计算统计数据"""
        # 函数名前加下划线，ok不在类外使用
        assert all([self.start_time, self.arrival_time, self.end_time]), "Uncomplete Tour"
        # 暂不返回
        self.info["travel_time"] = (self.arrival_time - self.start_time).total_seconds() / 60  # 分钟 
        self.info["play_duration"] = (self.end_time - self.arrival_time).total_seconds() / 60
        self.info["from_to"] = f"{str(self.home)} → {str(self.goal)}" # 使用Place的str形式

    def description(self):
        """返回对于本次出勤的详情文本"""
        result = ""
        for item in self.info.items():
            key, val = item
            result = result + key + ": " + str(val) + "\n"
        return result
        
        
class User:
    def __init__(self, name):
        self.name = name
        self.history = []  # 存储所有Tour记录
        self.current_tour = None  # 当前出勤
        self.home = Place()

    def __str__(self):
        return self.name
    
    def start_new_tour(self, home, goal):
        """开始新的出勤记录"""
        self.current_tour = Tour(home, goal)
    
    def save_tour(self):
        """保存当前出勤记录"""
        assert self.current_tour, "No Tour to save"
        if self.current_tour.state >= 3:
            self.history.append(self.current_tour)
            self.current_tour = None
    
    def _save_to_file(self, stats):
        """将记录保存到txt文件"""
        # 也许改一下还可以用？
        os.makedirs("records", exist_ok=True)
        filename = f"records/{self.name}_records.txt"
        
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"\n=== 出勤记录 {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")
            f.write(f"用户: {self.name}\n")
            f.write(f"路线: {stats['from_to']}\n")
            f.write(f"通勤时间: {stats['travel_time']:.1f} 分钟\n")
            f.write(f"游玩时长: {stats['play_duration']:.1f} 分钟\n")
            f.write("="*30 + "\n")

class RecordSingle(MethodWidget):
    def __init__(self, record: Tour = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_record_single.Ui_RecordSingle() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        self.time_label = self.ui.time_label
        self.goal_label = self.ui.goal_label
        self.tour = record
        if self.tour:
            self.set_tour_info()

    def set_tour_info(self):
        self.time_label.setText(f"时间:{self.tour.start_time.date()}")
        self.goal_label.setText(f"地点:{str(self.tour.goal)}")


class SettingsSingle(MethodWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_settings_single.Ui_SettingsSingle() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        self.single_layout = self.ui.single_layout

        self.set_widgets()
        self.add_data([("日记", ("不记录", "记录")), ("通勤", ("无通勤", "有通勤")), ("退勤", ("不退勤", "退勤"))])
        self.add_outfit(["饮料", "手套", "谷子", "板子"])

    """
    下面的函数仅做scroll测试
    从ui_test中的FormLayout复制而来
    以后会将该类写为更通用的设置部件
    """
    def set_widgets(self):
        layout = self.single_layout

        data = QGroupBox("数据")
        outfit = QGroupBox("出装")

        layout.addWidget(data)
        layout.addWidget(outfit)

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
        

class StartWindow(MethodWidget):
    def __init__(self, signal: pyqtSignal, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 创建ui类实例
        self.ui = Ui_start_window.Ui_StartWidget() 
        self.ui.setupUi(self) # 从ui对象获取所有已有布局

        self.user = user # 绑定用户
        self.signal = signal # 绑定切换界面信号
        self.trigger_widgets()

    def trigger_widgets(self):
        # 绑定所有QTdesigner中的控件并定义逻辑行为
        self.go_button = self.ui.go_button
        self.record_button = self.ui.record_button
        self.settings_button = self.ui.settings_button
        self.account_button = self.ui.account_button

        self.go_button.clicked.connect(lambda: self.signal.emit("map_window"))
        self.record_button.clicked.connect(lambda: self.signal.emit("record_window"))
        self.settings_button.clicked.connect(lambda: self.signal.emit("settings_window"))
        self.account_button.clicked.connect(lambda: None) # TODO

class MapWindow(MethodWidget):
    def __init__(self, signal, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 创建ui类实例
        self.ui = Ui_map_window.Ui_MapWidget() 
        self.ui.setupUi(self) # 从ui对象获取所有已有布局

        self.user = user # 绑定用户
        self.signal = signal # 绑定切换界面信号

        self.arcades = [Arcade("上地"), Arcade("五道口"), Arcade("万柳"), Arcade("新奥")] # 机厅列表
        self.trigger_widgets() # 动态添加机厅按钮

    def trigger_widgets(self):
        self.return_button = self.ui.return_button
        self.bottom_layout = self.ui.arcade_layout
        self.return_button.clicked.connect(lambda: self.signal.emit("start_window"))
        for index, arcade in enumerate(self.arcades):
            button = QPushButton(str(arcade))
            # 绑定selected函数, 点击记住机厅
            # 好阴间的占位符
            button.clicked.connect(lambda _, n = index: self.selected(n))
            self.bottom_layout.addWidget(button)

    def selected(self, index):
        self.user.start_new_tour(self.user.home, self.arcades[index])
        self.signal.emit("go_window")

class GoWindow(MethodWidget):
    def __init__(self, signal, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 创建ui类实例
        self.ui = Ui_go_window.Ui_GoWidget() 
        self.ui.setupUi(self) # 从ui对象获取所有已有布局

        self.user = user # 绑定用户
        self.signal = signal # 绑定切换界面信号

        self.state = 0  # 0: preparing 1: marching 2: playing

        self.trigger_widgets()        
        self.state_update() # 初始化为状态0

        # 计时功能
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_elapsed = -1 # 也许有其他归零时间的办法？
        self.update_timer()

    def trigger_widgets(self):
        # 绑定所有QTdesigner中的控件并定义逻辑行为
        self.main_button = self.ui.main_button
        self.state_label = self.ui.state_label
        self.timer_label = self.ui.time_label
        self.option_button = self.ui.option_button
        # 点击主按钮切换到下一阶段
        self.main_button.clicked.connect(lambda: self.state_change(self.state + 1))
        # TODO: 点击选项按钮可以进行记录

    def start_timer(self):
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()
        self.time_elapsed = -1
        self.update_timer()

    def update_timer(self):
        """更新计时器显示"""
        self.time_elapsed += 1
        mins = self.time_elapsed // 60
        secs = self.time_elapsed % 60
        self.timer_label.setText(f"{mins:02d}:{secs:02d}") # 可以显示在UI上

    def state_change(self, n):
        self.state = n
        self.state_update()

    def state_update(self):
        """根据self.state变化调用对应函数"""
        if self.state == 0:
            self.preparing()
        elif self.state == 1:
            self.marching()
        elif self.state == 2:
            self.playing()
        else:
            self.ending()
            
    def preparing(self):
        self.setWindowTitle("准备中")
        self.main_button.setText("GO!")
        self.state_label.setText("准备好了就开始了哦")

    def marching(self):
        # 启动user的current_tour
        self.user.current_tour.start_tour()
        self.start_timer()
        self.setWindowTitle("通勤中")
        self.main_button.setText("到达!")
        self.state_label.setText("GOGOGO!")

    def playing(self):
        # current_tour到达
        self.user.current_tour.arrived()
        self.setWindowTitle("游玩中")
        self.main_button.setText("退勤")
        self.state_label.setText("要继续游玩吗")

    def ending(self):
        # current_tour到达
        self.user.current_tour.end_tour()
        self.stop_timer()

        # 更新为状态0
        self.state = 0
        self.state_update()

        # 保存记录
        self.signal.emit("save_record")
        self.user.save_tour()
        self.signal.emit("start_window")

class RecordWindow(MethodWidget):
    def __init__(self, signal, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_record_window.Ui_RecordWidget() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        
        record_widget = MethodWidget()
        #添加记录的layout
        self.record_layout = record_widget.create_layout(QVBoxLayout)
        self.ui.record_scroll.setWidget(record_widget)

        self.signal = signal
        self.trigger_widgets()

    def trigger_widgets(self):
        self.return_button = self.ui.return_button
        self.return_button.clicked.connect(lambda: self.signal.emit("start_window"))
        
    def add_record(self, *widgets):
        for widget in widgets:
            self.record_layout.addWidget(widget)

class SettingsWindow(MethodWidget):
    def __init__(self, signal, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_settings_window.Ui_SettingsWidget() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        
        settings_widget = MethodWidget()
        # 添加设置选项的layout
        self.settings_layout = settings_widget.create_layout(QVBoxLayout)
        self.ui.settings_scroll.setWidget(settings_widget)

        self.signal = signal
        self.trigger_widgets()
        self.add_settings(SettingsSingle(), SettingsSingle())
    
    def trigger_widgets(self):
        self.return_button = self.ui.return_button
        self.return_button.clicked.connect(lambda: self.signal.emit("start_window"))

    def add_settings(self, *widgets):
        for widget in widgets:
            self.settings_layout.addWidget(widget)
        
    

class MainWindow(MethodWidget):
    main_signal = pyqtSignal(str)
    # 传给每个窗口的切换信号
    # 0: StartWindow 1: MapWindow 2: GoWindow 
    # 3: RecordWindow 4: SettingsWindow
    def __init__(self, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("MaiGO!!!!!")
        self.setWindowIcon(QIcon(bear_path))
        self.resize(800, 400)

        self.user = user # 设置用户
        self.stack = QStackedWidget()
        layout = self.create_layout(QVBoxLayout)
        layout.addWidget(self.stack) # 加入窗口栈

        self.start_window, self.map_window, self.go_window = None, None, None
        self.record_window, self.settings_window = None, None
        self.windows = []

        self.add_windows()
        self.main_signal.connect(self.signal_trigger)
        
    def add_windows(self):
        self.start_window = StartWindow(self.main_signal, self.user)
        self.windows.append(self.start_window)
        self.map_window = MapWindow(self.main_signal, self.user)
        self.windows.append(self.map_window)
        self.go_window = GoWindow(self.main_signal, self.user)
        self.windows.append(self.go_window)
        self.record_window = RecordWindow(self.main_signal, self.user)
        self.windows.append(self.record_window)
        self.settings_window = SettingsWindow(self.main_signal, self.user)
        self.windows.append(self.settings_window)

        for window in self.windows:
            self.stack.addWidget(window)

    # 切换界面的指令
    def switch_to(self, index):
        self.stack.setCurrentIndex(index)

    def save_record(self):
        # 加载用户的current_tour为RecordWindow的Widget
        self.record_window.add_record(RecordSingle(self.user.current_tour))

    # 所有指令
    def signal_trigger(self, command: str):
        func = CMD_DICT.get(command)
        assert func, "Undefined command"
        func(self)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow(User("Bo"))

    window.show()

    app.exec()
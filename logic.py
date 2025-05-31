"""存放主要窗口类和运行逻辑的文件"""
import sys
# 调用PyQt5相关组件
from PyQt5.QtWidgets import (
QApplication, QWidget,
QPushButton, QLabel,
QVBoxLayout, QHBoxLayout, QGroupBox,
QStackedWidget, QScrollArea, QTextEdit, QCheckBox,
QGraphicsEllipseItem, QGraphicsScene, QGraphicsPixmapItem,QSizePolicy
)
from PyQt5.QtGui import (
QPixmap, QColor, QFont, QBrush, QPen,
QIcon, QPixmap
)
from PyQt5.QtCore import (
pyqtSignal, QTimer, Qt
)
# 调用暂时不知道有没有用的资源文件
import resources_rc

# 调用ui_class文件夹中使用QTdesigner写好的窗口类文件
from ui_class import (
Ui_start_window, Ui_record_window, Ui_settings_window, 
Ui_go_window, Ui_map_window,
Ui_account_window, Ui_option_window
)
# 调用utils中自定义的Method基类
from utils import *

# 调用logicbase的数据类
from logicbase import (
User, Tour, Place, Arcade,
Data, NumData, StrData, DictData
)
# 调用subwindow中的子窗口类
from subwindow import (
SettingsSingle, RecordStack, RecordInterface,
DataSingle, OptionInput, OptionSelect,
)

# 调用datainfo中的sample
from datainfo import data_samples

bear_path = ":/image/bear.png"
map_path = ":/image/map.png"
salt_path = ":/image/salt.png"
acid_path = ":/image/acid.png"

# MainWindow中main_signal:pyqtSignal(str)的绑定函数字典
# 现有val函数输入均为MainWindow的self, 均在MainWindow中定义
CMD_DICT = {
        "start_window": lambda self: MainWindow.switch_to(self, 0),
        "map_window": lambda self: MainWindow.switch_to(self, 1),
        "go_window": lambda self: MainWindow.switch_to_go(self),
        "record_window": lambda self: MainWindow.switch_to_record(self),
        "settings_window": lambda self: MainWindow.switch_to(self, 4),
        "option_window": lambda self: MainWindow.switch_to_option(self),
        "account_window": lambda self: MainWindow.switch_to_account(self),
        "record_stack": lambda self: MainWindow.switch_to_record_stack(self),
        "save_record": lambda self: MainWindow.save_record(self),
    }  

class StartWindow(MethodWidget):
    def __init__(self, signal: pyqtSignal, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 创建ui类实例
        self.ui = Ui_start_window.Ui_StartWidget() 
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        #self.ui.label_2.setVisible(False)
        self.ui.label_2.setText("")
        self.original_pixmap=None
        self.user = user # 绑定用户
        self.signal = signal # 绑定切换界面信号
        self.trigger_widgets()
        self.set_figure(salt_path)
        

    def trigger_widgets(self):
        """
        绑定所有QTdesigner中定义的控件
        并定义逻辑行为
        """
        self.go_button = self.ui.go_button
        self.record_button = self.ui.record_button
        self.settings_button = self.ui.settings_button
        self.account_button = self.ui.account_button
        self.figure_label = self.ui.figure_label
        self.figure_label.setCursor(Qt.PointingHandCursor)  # 鼠标悬停时显示手型
        self.figure_label.mousePressEvent = self.on_image_click  # 绑定点击事件
        self.go_button.clicked.connect(lambda: self.signal.emit("map_window"))
        self.record_button.clicked.connect(lambda: self.signal.emit("record_window"))
        self.settings_button.clicked.connect(lambda: self.signal.emit("settings_window"))
        self.account_button.clicked.connect(lambda: self.signal.emit("account_window"))
    def on_image_click(self, event):
        from PyQt5.QtWidgets import QToolTip,QMessageBox
        from PyQt5.QtCore import QRect
        #self.ui.label_2.setVisible(True)
        
        self.ui.label_2.setText("喵喵~咕噜咕噜")
        QTimer.singleShot(2000, lambda:self.ui.label_2.setText(""))
        from PyQt5.QtMultimedia import QSound
        try:
            QSound.play("咕噜咕噜.wav")  # 需要准备WAV格式音频文件
        except:
            print("音频播放失败，请检查click.wav文件是否存在")
    def set_figure(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Failed to load image: {image_path}")
            return
        # 获取 QLabel 的尺寸
        label_size = self.figure_label.size()
        # 根据 QLabel 尺寸缩放 pixmap，保持原比例（AspectRatio）
        self.original_pixmap=pixmap
        scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.figure_label.setPixmap(scaled_pixmap)

class MapWindow(MethodWidget):
    def __init__(self, signal, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 创建ui类实例
        self.ui = Ui_map_window.Ui_MapWidget() 
        self.ui.setupUi(self) # 从ui对象获取所有已有布局

        self.user = user # 绑定用户
        self.signal = signal # 绑定切换界面信号

        # Arcade samples
        self.arcades = [Arcade("上地"), Arcade("五道口"), Arcade("万柳"), Arcade("学清")] # 机厅列表
        positions = [(584, 71), (892, 600), (403, 864), (1048, 357)]
        for arcade, pos in zip(self.arcades, positions):
            arcade.set_pos(*pos)

        self.trigger_widgets() # 动态添加机厅按钮

    def trigger_widgets(self):
        """
        绑定所有QTdesigner中定义的控件
        并定义逻辑行为
        """
        # QTdesigner只有GraphicView
        # 所以还要自己添加Graphic的其他控件
        self.scene = QGraphicsScene()
        self.view = self.ui.view
        self.view.setScene(self.scene)
        pixmap = QPixmap(map_path)
        self.background = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.background)

        self.return_button = self.ui.return_button
        self.return_button.clicked.connect(lambda: self.signal.emit("start_window"))
        for arcade in self.arcades:
            # 在ArcadeMarker中定义点击行为
            marker = ArcadeMarker(self, arcade)
            self.scene.addItem(marker)


    def selected(self, arcade):
        self.user.start_new_tour(self.user.home, arcade)
        self.signal.emit("go_window")

class ArcadeMarker(QGraphicsEllipseItem):
    """自定义商场标记图形项"""
    def __init__(self, map: MapWindow = None, arcade: Arcade = None, *args):
        super().__init__(0, 0, 30, 30, *args)
        self.map_parent = map
        self.arcade = arcade
        self.setPos(arcade.latitude, arcade.longitude)
        self.setBrush(QBrush(QColor(255, 0, 0, 150)))
        self.setPen(QPen(Qt.black))
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        
    def mousePressEvent(self, event):
        """点击标记时触发"""
        if event.button() == Qt.LeftButton:
            self.setSelected(True)
            self.map_parent.selected(self.arcade)
        super().mousePressEvent(event)


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
        """
        绑定所有QTdesigner中定义的控件
        并定义逻辑行为
        """
        self.main_button = self.ui.main_button
        self.state_label = self.ui.state_label
        self.timer_label = self.ui.time_label
        self.goal_label = self.ui.goal_label
        self.label=self.ui.label
        gif_path1="run.gif"
        gif_path2="play.gif"
        self.option_button = self.ui.option_button
        # 点击主按钮切换到下一阶段
        self.main_button.clicked.connect(lambda: self.state_change(self.state + 1))
        self.option_button.clicked.connect(lambda: self.signal.emit("option_window"))
    
    def set_gif(self,gif_path):
        from PyQt5.QtGui import QMovie
        
        try:
            self.movie = QMovie(gif_path)
            
            # 连接帧变化信号到缩放函数
            self.movie.frameChanged.connect(self._scale_gif_frame)
            
            # 设置标签大小策略和对齐方式
            self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.label.setAlignment(Qt.AlignCenter)
            
            self.label.setMovie(self.movie)
            self.movie.start()
            
            # 初始缩放
            self._scale_gif_frame()
            
        except Exception as e:
            print(f"加载GIF出错：{str(e)}")
            
    def _scale_gif_frame(self):
        if not self.movie:
            return
            
        # 获取当前帧
        pixmap = self.movie.currentPixmap()
        
        # 按标签大小缩放
        label_size = self.label.size()
        scaled_pixmap = pixmap.scaled(
            label_size, 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        
        # 应用缩放后的图像
        self.label.setPixmap(scaled_pixmap)

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
        self.main_button.setText("出发")
        self.state_label.setText("准备好了就开始了哦")
        
        
    def marching(self):
        """启动user的current_tour"""
        self.user.current_tour.start_tour()
        self.start_timer()
        self.setWindowTitle("通勤中")
        self.main_button.setText("到达")
        self.state_label.setText("GOGOGO!")
        self.set_gif("run.gif")
        from PyQt5.QtMultimedia import QSound
        try:
            QSound.play("出发咯.wav")  # 需要准备WAV格式音频文件
        except:
            print("音频播放失败，请检查click.wav文件是否存在")

    def playing(self):
        """current_tour到达"""

        self.set_gif("play.gif")
        self.user.current_tour.arrived()
        self.setWindowTitle("游玩中")
        self.main_button.setText("退勤")
        self.state_label.setText("要继续游玩吗")
        from PyQt5.QtMultimedia import QSound
        try:
            QSound.play("欢迎回来.wav")  # 需要准备WAV格式音频文件
        except:
            print("音频播放失败，请检查click.wav文件是否存在")

    def ending(self):
        """current_tour结束"""
        self.user.current_tour.end_tour()
        self.stop_timer()

        # 更新为状态0
        self.state = 0
        self.state_update()

        # 保存记录
        self.signal.emit("save_record")
        self.user.save_tour()
        self.signal.emit("start_window")

class OptionWindow(MethodWidget):
    def __init__(self, signal, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_option_window.Ui_OptionWidget() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        
        self.user = user
        self.signal = signal
        self.option_list = [] # 另外存放所有OptionSingle
        self.trigger_widgets()

    def trigger_widgets(self):
        """
        绑定所有QTdesigner中定义的控件
        并定义逻辑行为
        """
        option_widget = MethodWidget()

        #添加记录的layout
        self.option_layout = option_widget.create_layout(QVBoxLayout)
        self.ui.options_scroll.setWidget(option_widget)

        self.return_button = self.ui.return_button
        self.return_button.clicked.connect(self.cancel_and_quit)
        self.fixed_button = self.ui.Fixed_button
        self.fixed_button.clicked.connect(self.save_and_quit)        

        
    def add_option(self, *widgets):
        for widget in widgets:
            assert isinstance(widget, (OptionInput, OptionSelect)), "Invalid option type"
            self.option_layout.addWidget(widget)
            self.option_list.append(widget)

    def update(self):
        """将所有OptionInput或OptionSelect更新数据"""
        for option in self.option_list:
            assert isinstance(option, (OptionInput, OptionSelect)) and isinstance(option.data, Data), "Invalid option or data"
            option.update()
        
    def trigger_tour(self):
        """在开始出勤时绑定self.current_tour作为本界面Options"""
        assert isinstance(self.user, User), "No user for option"
        assert isinstance(self.user.current_tour, Tour), "No tour for option"
        tour = self.user.current_tour
        for data in tour.data.values():
            if bool(data):
                option = None
                if isinstance(data, DictData):
                    option = OptionSelect(data)
                elif isinstance(data, Data):
                    option = OptionInput(data)
                assert data is not None, "Invalid option type"
                self.add_option(option)


    def clear_scroll(self):
        """清空所有Option控件"""
        clear_layout(self.option_layout)


    def save_all(self):
        """按确定键保存所有编辑到相应的data"""
        for option in self.option_list:
            assert isinstance(option, (OptionInput, OptionSelect)), "Invalid option type"
            option.save()
    
    def reset_all(self):
        """按取消键取消所有编辑"""
        for option in self.option_list:
            assert isinstance(option, (OptionInput, OptionSelect)), "Invalid option type"
            option.reset()

    def save_and_quit(self):
        self.save_all()
        self.signal.emit("go_window")

    def cancel_and_quit(self):
        self.reset_all()
        self.signal.emit("go_window")
        


class RecordWindow(MethodWidget): 
    def __init__(self, signal, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_record_window.Ui_RecordWidget() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        
        self.user = user
        self.signal = signal
        self.trigger_widgets()

    def trigger_widgets(self):
        """
        绑定所有QTdesigner中定义的控件
        并定义逻辑行为
        """
        record_widget = MethodWidget()

        #添加记录的layout
        self.record_layout = record_widget.create_layout(QVBoxLayout)
        self.ui.record_scroll.setWidget(record_widget)

        self.return_button = self.ui.return_button
        self.return_button.clicked.connect(lambda: self.signal.emit("start_window"))
        
    def save_record(self, tour):
        assert isinstance(tour, Tour), "No tour to save"
        interface = RecordInterface(self.signal, self.user, tour)
        self.add_record(interface)
    
    def add_record(self, *widgets):
        for widget in widgets:
            assert isinstance(widget, RecordInterface), "Has to be interface"
            self.record_layout.addWidget(widget)


class SettingsWindow(MethodWidget):
    def __init__(self, signal, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_settings_window.Ui_SettingsWidget() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局

        self.user = user
        self.signal = signal
        self.settings_list = []
        self.trigger_widgets()
    
    def trigger_widgets(self):
        """
        绑定所有QTdesigner中定义的控件
        并定义逻辑行为
        """
        self.return_button = self.ui.return_button
        self.return_button.clicked.connect(lambda: self.signal.emit("start_window"))
        # 添加设置选项的layout
        settings_widget = MethodWidget()
        self.settings_layout = settings_widget.create_layout(QVBoxLayout)
        self.ui.settings_scroll.setWidget(settings_widget)
        # 将用户设置中所有editdable的data转化为SettingsSingle
        for data in self.user.data.values():
            assert isinstance(data, Data), "Invalid data type"
            if data.editable:
                settings_single = SettingsSingle(data)
                self.add_settings(settings_single)           

    def add_settings(self, *widgets):
        for widget in widgets:
            assert isinstance(widget, SettingsSingle), "Incorrect setting class"
            self.settings_layout.addWidget(widget)
            self.settings_list.append(widget)

    def update_settings(self):
        for setting in self.settings_list:
            assert isinstance(setting, SettingsSingle), "Incorrect setting class"
            setting.update()
        
class AccountWindow(MethodWidget):
    def __init__(self, signal, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_account_window.Ui_AccountWidget() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        
        self.user = user
        self.signal = signal
        self.data_list = [] # 另外存放所有DataSingle
        self.trigger_widgets()

    def trigger_widgets(self):
        """
        绑定所有QTdesigner中定义的控件
        并定义逻辑行为
        """
        #添加记录的layout
        self.return_button = self.ui.return_button
        self.return_button.clicked.connect(lambda: self.signal.emit("start_window"))

        data_widget = MethodWidget()
        self.data_layout = data_widget.create_layout(QVBoxLayout)
        self.ui.account_scroll.setWidget(data_widget)

        # 将用户设置中所有data转化为settingsSingle
        for data in self.user.data.values():
            assert isinstance(data, Data), "Invalid data type"
            if data.accumulable:
                data_single = DataSingle(data)
                self.add_data(data_single)    
        
    def add_data(self, *widgets):
        for widget in widgets:
            assert isinstance(widget, DataSingle), "Incorrect data class"
            self.data_layout.addWidget(widget)
            self.data_list.append(widget)

    def update_data(self):
        """将所有DataSingle更新数据"""
        for data_single in self.data_list:
            assert isinstance(data_single, DataSingle), "Incorrect data class"
            data_single.update()  

#class transWindow(MethodWidget):

class MainWindow(MethodWidget):
    main_signal = pyqtSignal(str)
    # 传给每个窗口的切换信号
    # 0: StartWindow 1: MapWindow 2: GoWindow 
    # 3: RecordWindow 4: SettingsWindow
    def __init__(self, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("MaiGO!!!!!")
        self.setWindowIcon(QIcon(bear_path))
        self.resize(600, 1000)

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
        self.option_window = OptionWindow(self.main_signal, self.user)
        self.windows.append(self.option_window)
        self.account_window = AccountWindow(self.main_signal, self.user)
        self.windows.append(self.account_window)
        self.record_stack = RecordStack(self.main_signal, self.user)
        self.windows.append(self.record_stack)       

        for window in self.windows:
            self.stack.addWidget(window)

    # 切换界面的指令
    def switch_to(self, index):
        self.stack.setCurrentIndex(index)

    def switch_to_go(self):
        assert isinstance(self.user.current_tour, Tour), "No current Tour"
        self.go_window.goal_label.setText(f"目的地:{str(self.user.current_tour.goal)}")
        self.option_window.clear_scroll()
        self.option_window.trigger_tour()
        from PyQt5.QtMultimedia import QSound
        try:
            QSound.play("要开始了哟.wav")  # 需要准备WAV格式音频文件
        except:
            print("音频播放失败，请检查click.wav文件是否存在")
        self.switch_to(2)

    def switch_to_record(self):
        self.switch_to(3)

    def switch_to_option(self):
        self.option_window.update()
        self.switch_to(5)

    def switch_to_account(self):
        self.account_window.update_data()
        self.switch_to(6)

    def switch_to_record_stack(self):
        self.record_stack.switch_to(self.user.record_index)
        self.switch_to(7)

    def save_record(self):
        """加载用户的current_tour为RecordWindow和RecordStack的Widget"""
        self.record_window.save_record(self.user.current_tour)
        self.record_stack.save_record(self.user.current_tour)

    # 所有指令经过此处
    def signal_trigger(self, command: str):
        func = CMD_DICT.get(command)
        assert func, "Undefined command"
        func(self)

if __name__ == "__main__":
    #QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])

    user = User("Bo")

    user.add_datatype(*data_samples)

    window = MainWindow(user)

    window.show()

    app.exec()
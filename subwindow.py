"""存放子窗口类的文件，比如单条记录的弹窗"""

# 调用logicbase中的数据类
from logicbase import User, Tour, Place, Arcade

# PyQt组件
from PyQt5.QtWidgets import (
    QGridLayout, QFormLayout,
    QLabel, QPushButton, QCheckBox, QGroupBox,
    QStackedWidget, QVBoxLayout
    )
from PyQt5.QtCore import (
    pyqtSignal
)

# subwindow的.ui文件
from ui_class import (
    Ui_record_info, Ui_record_interface,
    Ui_settings_single
)

# 调用utils中自定义的Method基类
from utils import MethodWidget, MGroupBox

class RecordSingle(MethodWidget):
    switch_signal = pyqtSignal(int)
    def __init__(self, record: Tour = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stack = QStackedWidget()
        self.tour = record
        self.switch_signal.connect(self.switch_to)
        # 创建两个窗口放入stack中
        self.interface = RecordInterface(self.tour, self.switch_signal)
        self.info = RecordInfo(self.tour, self.switch_signal)
        self.stack.addWidget(self.interface)
        self.stack.addWidget(self.info)
        # 将stack加入layout布局
        layout = self.create_layout(QVBoxLayout)
        layout.addWidget(self.stack)

    def switch_to(self, index):
        self.stack.setCurrentIndex(index)
        self.adjustSize() # 调整高度
        self.parentWidget().adjustSize()

    def reset(self):
        self.switch_to(0)


class RecordInterface(MethodWidget):
    """
    默认展示的简单信息窗口 只标明时间地点
    有切换到详情的按钮
    """
    def __init__(self, record: Tour = None, signal = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_record_interface.Ui_RecordInterface() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        self.signal = signal
        self.tour = record
        self.trigger_widgets()
        if self.tour:
            self.set_tour_interface()

    def trigger_widgets(self):
        """
        绑定所有QTdesigner中定义的控件
        并定义逻辑行为
        """
        self.time_label = self.ui.time_label
        self.goal_label = self.ui.goal_label
        self.info_button = self.ui.info_button
        self.info_button.clicked.connect(lambda: self.signal.emit(1))

    def set_tour_interface(self):
        self.time_label.setText(f"时间:{self.tour.start_time.date()}")
        self.goal_label.setText(f"地点:{str(self.tour.goal)}")

class RecordInfo(MethodWidget):
    """
    详细信息窗口，有返回按钮
    """
    def __init__(self, record: Tour = None, signal = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_record_info.Ui_RecordInfo() # 创建ui类逻辑
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        self.signal = signal
        self.tour = record
        self.trigger_widgets()
        if self.tour:
            self.set_tour_info()

    def trigger_widgets(self):
        """
        绑定所有QTdesigner中定义的控件
        并定义逻辑行为
        """
        self.info_label = self.ui.info_label
        self.return_button = self.ui.return_button
        self.return_button.clicked.connect(lambda: self.signal.emit(0))

    def set_tour_info(self):
        """展示详细信息"""
        pass


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
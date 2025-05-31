"""存放子窗口类的文件，比如单项记录的选择"""

# 调用logicbase中的数据类
from logicbase import (
User, Tour,
Data, NumData, StrData, DictData
)
# PyQt组件
from PyQt5.QtWidgets import (
QApplication,
QGridLayout, QFormLayout,
QLabel, QPushButton, QCheckBox, QGroupBox,
QStackedWidget, QVBoxLayout,
QButtonGroup, QRadioButton
)
from PyQt5.QtCore import (
pyqtSignal
)

# subwindow的.ui文件
from ui_class import (
Ui_record_info, Ui_record_interface,
Ui_settings_single, Ui_data_single,
Ui_option_input, Ui_option_select,
Ui_select_single
)

# 调用utils中自定义的Method基类
from utils import MethodWidget, MGroupBox

class RecordStack(MethodWidget):
    """展示RecordInfo的stack"""
    
    def __init__(self, signal = None, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stack = QStackedWidget()
        self.user = user
        self.signal = signal
        # 将stack加入layout布局
        layout = self.create_layout(QVBoxLayout)
        layout.addWidget(self.stack)

    def save_record(self, tour):
        assert isinstance(tour, Tour), "No tour to save"
        info = RecordInfo(self.signal, self.user, tour)
        self.add_record(info)
  
    def add_record(self, *widgets):
        for widget in widgets:
            assert isinstance(widget, RecordInfo), "Has to be info"
            self.stack.addWidget(widget)

    def switch_to(self, index):
        self.stack.setCurrentIndex(index)



class RecordInterface(MethodWidget):
    """
    默认展示的简单信息窗口 只标明时间地点
    有切换到详情的按钮
    """
    def __init__(self, signal = None, user = None, record: Tour = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_record_interface.Ui_RecordInterface() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        self.signal = signal
        assert isinstance(user, User) and isinstance(record, Tour), "Invalid user or tour"
        self.user = user
        self.tour = record
        self.trigger_widgets()
        self.set_tour_interface() # 设定时间地点

    def trigger_widgets(self):
        """
        绑定所有QTdesigner中定义的控件
        并定义逻辑行为
        """
        self.time_label = self.ui.time_label
        self.goal_label = self.ui.goal_label
        self.info_button = self.ui.info_button
        self.info_button.clicked.connect(self.switch_to_info)
   
    def switch_to_info(self):
        assert isinstance(self.user, User), "No User"
        index = self.tour.index
        self.user.record_index = index
        self.signal.emit("record_stack")
    
    def set_tour_interface(self):
        self.time_label.setText(f"{self.tour.start_time.date()}")
        self.goal_label.setText(f"{str(self.tour.goal)}")

class RecordInfo(MethodWidget):
    """
    详细信息窗口，有返回按钮
    """
    def __init__(self, signal = None, user = None, record: Tour = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_record_info.Ui_RecordInfo() # 创建ui类逻辑
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        self.tour = record
        self.user = user
        self.signal = signal
        self.trigger_widgets()

    def trigger_widgets(self):
        """
        绑定所有QTdesigner中定义的控件
        并定义逻辑行为
        """
        #添加记录的layout
        self.return_button = self.ui.return_button
        self.return_button.clicked.connect(lambda: self.signal.emit("record_window"))

        info_widget = MethodWidget()
        self.info_layout = info_widget.create_layout(QVBoxLayout)
        self.ui.info_scroll.setWidget(info_widget)

        # 将用户设置中所有data转化为settingsSingle
        for data in self.tour.data.values():
            assert isinstance(data, Data), "Invalid data type"
            if data.name != "出勤次数":
                data_single = DataSingle(data)
                self.add_data(data_single)    
        
    def add_data(self, *widgets):
        for widget in widgets:
            assert isinstance(widget, DataSingle), "Incorrect data class"
            self.info_layout.addWidget(widget)



class DataSingle(MethodWidget):
    """
    展示信息的窗口
    """
    def __init__(self, data = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_data_single.Ui_DataSingle() # 创建ui类逻辑
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        self.data = data
        self.trigger_widgets()
        self.update()
    
    def trigger_widgets(self):
        self.data_label = self.ui.data_label

    def update(self):
        """更新label展示的数据 可扩展"""
        assert isinstance(self.data, Data), "No data"
        self.data_label.setText(str(self.data))
        


class SettingsSingle(MethodWidget):
    def __init__(self, data = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_settings_single.Ui_SettingsSingle() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        self.data = data
        self.trigger_widgets()

    def trigger_widgets(self):
        """绑定描述的文本和checkbox"""
        assert isinstance(self.data, Data), "No Data"
        self.name_label = self.ui.name_label
        self.name_label.setText(self.data.name)
        self.checkbox = self.ui.enable_checkbox
        self.checkbox.stateChanged.connect(self.update)

    def update(self):
        """检查自己的checkbox并相应改变data的enable属性"""
        if self.checkbox.isChecked():
            self.data.enable()
            self.checkbox.setText("已启用")
        else:
            self.data.disable()
            self.checkbox.setText("未启用")

class SelectSingle(MethodWidget):
    """用于OptionSelect的单个选项"""
    def __init__(self, text = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_select_single.Ui_SelectSingle() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        self.text = text
        self.button = None
        self.trigger_widgets()

    def trigger_widgets(self):
        """绑定描述的文本和TextEdit"""
        self.name_label = self.ui.name_label
        self.name_label.setText(self.text)
        self.button = self.ui.radioButton

class OptionInput(MethodWidget):
    """拥有Textedit的输入型option"""
    def __init__(self, data = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_option_input.Ui_OptionInput() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        self.data = data
        self.trigger_widgets()
        self.reset()

    def trigger_widgets(self):
        """绑定GroupBoxName和TextEdit"""
        assert isinstance(self.data, Data), "No Data"
        self.option_box = self.ui.option_box
        self.option_edit = self.ui.option_edit
        self.option_box.setTitle(self.data.name)
        self.option_edit.setPlaceholderText(self.data.info)

    def save(self):
        """检查自己的checkbox并相应改变data的enable属性"""
        assert isinstance(self.data, Data), "No Data"
        text = self.option_edit.toPlainText()
        if isinstance(self.data, NumData):
            self.data.set_val(int(text))
        elif isinstance(self.data, StrData):
            self.data.add_val(text)

    def reset(self):
        self.option_edit.clear()

class OptionSelect(MethodWidget):
    """拥有RadioButtons的选择型option"""
    def __init__(self, data = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_option_select.Ui_OptionSelect() # 创建ui类实例
        self.ui.setupUi(self) # 从ui对象获取所有已有布局
        assert isinstance(data, DictData)
        self.data = data
        self.exclusive = self.data.exclusive # 是否单选

        self.trigger_widgets()

    def trigger_widgets(self):
        """绑定布局、GroupBoxName和TextEdit"""
        assert isinstance(self.data, DictData), "No Data"
        self.selection_layout = self.ui.selection_layout
        self.option_box = self.ui.option_box
        self.option_box.setTitle(self.data.name)
        # 创建ButtonGroup实现单选逻辑
        self.radio_group = QButtonGroup(self)
        self.radio_group.setExclusive(self.exclusive)
        self.index_to_key = {} # 方便后续调用self.data.val
        for index, key in enumerate(self.data.val.keys()):
            # 暂时默认传入key作为label
            select_widget = SelectSingle(key)
            button = select_widget.button
            self.index_to_key[index] = key
            self.radio_group.addButton(button, index)
            self.selection_layout.addWidget(select_widget)

    def save(self):
        """保存自己的选择"""
        assert isinstance(self.data, DictData), "Only support dict"
        for index, button in enumerate(self.radio_group.buttons()):
            assert isinstance(button, QRadioButton)
            if button.isChecked():
                key = self.index_to_key[index]
                self.data.set_val(key, 1)


    def reset(self):
        for button in self.radio_group.buttons():
            button.setChecked(False)

if __name__ == "__main__":
    app = QApplication([])

    select_window = OptionSelect(DictData("交通方式", {"骑行": 0, "步行": 0, "公共交通": 0}))

    input_window = OptionInput(StrData("推分记录"))

    select_window.show()

    input_window.show()

    app.exec()
    

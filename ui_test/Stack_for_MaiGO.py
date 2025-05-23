import sys
from PyQt5.QtWidgets import QGridLayout, QFormLayout
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QTextEdit, QCheckBox
from PyQt5.QtGui import QIcon
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGraphicsView, 
                            QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem,
                            QGraphicsSimpleTextItem, QLabel, QPushButton, QDialog, 
                            QScrollArea, QHBoxLayout, QGroupBox)
from PyQt5.QtGui import QPixmap, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import Qt, QPointF, pyqtSignal, QObject, QRectF

bear_path = 'D:/MaiGO-main/ui_test/bear.png'
online_path = 'D:/MaiGO-main/ui_test/offline.png'
map_path = 'D:/MaiGO-main/ui_test/map.png'

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



class ArcadeSignal(QObject):
    """独立的信号类"""
    clicked = pyqtSignal(dict)
    detail_requested = pyqtSignal(dict)  # 新增：请求详细信息的信号

class ArcadeMarker(QGraphicsEllipseItem):
    """自定义商场标记图形项"""
    def __init__(self, arcade_info, x, y, signal_handler, parent=None):
        super().__init__(0, 0, 30, 30, parent)
        self.arcade_info = arcade_info
        self.signal_handler = signal_handler
        self.setPos(x, y)
        self.setBrush(QBrush(QColor(255, 0, 0, 150)))
        self.setPen(QPen(Qt.black))
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        
    def mousePressEvent(self, event):
        """点击标记时触发"""
        if event.button() == Qt.LeftButton:
            self.setSelected(True)
            self.signal_handler.clicked.emit(self.arcade_info)
        super().mousePressEvent(event)

class ArcadeDetailDialog(QDialog):
    """店铺详细信息弹窗"""
    def __init__(self, arcade_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{arcade_info['name']} - 详细信息")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        
        # 店铺名称
        name_label = QLabel(f"<h1>{arcade_info['name']}</h1>")
        layout.addWidget(name_label)
        
        # 详细信息
        info_group = QGroupBox("店铺信息")
        info_layout = QVBoxLayout()
        
        # 使用数据库中的所有字段
        details = [
            ("地址", arcade_info['address']),
            ("机台数量", arcade_info['num']),
            ("营业时间", arcade_info['hours']),  # 从数据库获取
            ("价格", arcade_info['price']),  # 从数据库获取
            ("交通", arcade_info['notes'])      # 从数据库获取
        ]
        
        for label, text in details:
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(f"<b>{label}:</b>"))
            hbox.addWidget(QLabel(text))
            hbox.addStretch()
            info_layout.addLayout(hbox)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)
        
        self.setLayout(layout)

class ArcadeInfoDialog(QDialog):
    """商场信息弹窗"""
    def __init__(self, signal,arcade_info, signal_handler, parent=None):
        super().__init__(parent)
        self.signal=signal
        self.signal_handler = signal_handler
        self.setWindowTitle("店铺信息")
        self.setModal(True)
        self.resize(300, 200)
        
        layout = QVBoxLayout()
        
        # 将店铺名称改为按钮
        name_btn = QPushButton(f"<h2>{arcade_info['name']}</h2>")
        name_btn.setStyleSheet("""
            QPushButton { 
                text-align: left; 
                border: none; 
                color: blue;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        name_btn.clicked.connect(lambda: self.signal_handler.detail_requested.emit(arcade_info))
        layout.addWidget(name_btn)
        
        # 其他信息
        info_label = QLabel()
        info_text = f"""
        <p><b>地址:</b> {arcade_info['address']}</p>
        <p><b>机台数量:</b> {arcade_info['num']}</p>
        """
        info_label.setText(info_text)
        
        scroll = QScrollArea()
        scroll.setWidget(info_label)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        button_layout=QHBoxLayout()
        # 出勤按钮
        go_btn = QPushButton("出勤")
        go_btn.clicked.connect(lambda:(self.signal.emit(2),self.accept())) 
        button_layout.addWidget(go_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        button_layout.setAlignment(Qt.AlignRight)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setAttribute(Qt.WA_DeleteOnClose)

class MapWindow(QWidget):
    """主地图窗口"""
    def __init__(self,switch_signal,parent=None):
        super().__init__(parent)
        self.switch_signal = switch_signal  # 保存信号对象
        self.setWindowTitle("中二节奏地图")
        self.resize(800, 600)
        
        # 创建信号处理器
        self.signal_handler = ArcadeSignal()
        self.signal_handler.clicked.connect(self.display_arcade_info)
        self.signal_handler.detail_requested.connect(self.display_arcade_detail)  # 连接详细信息信号
        
        # 初始化数据库
        self.init_database()
        
        # 创建UI
        self.init_ui()

        # 添加返回按钮
        self.add_back_button()
        
    def add_back_button(self):
        """添加返回按钮"""
        back_btn = QPushButton("返回主菜单", self)
        back_btn.clicked.connect(lambda: self.switch_signal.emit(0))  # 发射返回信号
        back_btn.move(10, 10)  # 放置在左上角
    
    def init_database(self):
        """初始化SQLite数据库"""
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # 创建表 - 添加营业时间和联系电话字段
        self.cursor.execute("""
        CREATE TABLE arcades (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            pos_x REAL NOT NULL,
            pos_y REAL NOT NULL,
            address TEXT,
            num TEXT,
            hours TEXT,       -- 新增营业时间字段
            price TEXT,       -- 新增联系电话字段
            notes TEXT        -- 新增备注字段
        )
        """)
        
        # 插入示例数据 - 包含新字段
        sample_data = [
            ("吉睿游艺北京海淀学清路店", 1048, 357, 
            "北京市海淀区学清路8号三层吉睿游艺", "1",
            "10:00-21:00", "2元/币", "地铁15号线、昌平线六道口站b口出向北步行约780m，地铁昌平线学知园站c口出向南步行约620m；公交至石板房、科荟桥西、林大北路东口下"),
            ("嘉贝乐北京五道口店", 892, 600, 
            "北京市海淀区成府路28号五道口购物中心三层", "2",
            "10:00-22:00", "2元/币", "地铁13号线五道口站出站即可见"),
            ("噜彼熊电玩嘉年华万柳店", 403, 864, 
            "北京市海淀区巴沟路2号万柳华联购物中心二层", "2",
            "09:00-22:00", "1元/币", "地铁路线：10号线巴沟站C出口，可从C3出口分支或者地下通道直接进入购物中心 公交路线：302 304 307 361 386 424 528 539 613 614 644路巴沟村站下车，534 644 664路万柳中路北口站下车。"),
            ("北京上地华联嘉贝乐", 584, 71, 
            "北京市海淀区农大南路1号院1号楼华联商厦上地店", "1",
            "10:00-21:00", "1元/币", "可乘坐公交到上地南口站或地铁13号线上地站下车后步行/骑行到达商场")
        ]
        self.cursor.executemany("""
        INSERT INTO arcades (name, pos_x, pos_y, address, num, hours, price, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_data)
        self.conn.commit()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        
        # 创建地图视图
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)
        
        pixmap = QPixmap("D:/MaiGO-main/ui_test/map.png")
        self.background = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.background)
        rect = QRectF(pixmap.rect())
        self.scene.setSceneRect(rect)
        
        # 从数据库加载商场标记
        self.load_arcade_markers()
        
        # 底部控制区域
        #control_layout = QHBoxLayout()
        #refresh_btn = QPushButton("刷新地图")
        #refresh_btn.clicked.connect(self.refresh_map)
        #control_layout.addWidget(refresh_btn)
        #layout.addLayout(control_layout)
    
    def load_arcade_markers(self):
        """从数据库加载商场并创建标记"""
        self.cursor.execute("SELECT name, pos_x, pos_y, address, num, hours, price, notes FROM arcades")
        
        for arcade in self.cursor.fetchall():
            arcade_info = {
                "name": arcade[0],
                "pos_x": arcade[1],
                "pos_y": arcade[2],
                "address": arcade[3],
                "num": arcade[4],
                "hours": arcade[5],  # 营业时间
                "price": arcade[6],   
                "notes": arcade[7]    # 备注
            }
            
            # 创建标记并添加到场景
            marker = ArcadeMarker(arcade_info, arcade[1], arcade[2], self.signal_handler)
            self.scene.addItem(marker)
    
    def display_arcade_info(self, arcade_info):
        """显示商场信息弹窗"""
        dialog = ArcadeInfoDialog(self.switch_signal,arcade_info, self.signal_handler, self)
        dialog.finished.connect(self.clear_selection)
        dialog.exec_()
    
    def clear_selection(self):
        for item in self.scene.items():
            if isinstance(item,ArcadeMarker):
                item.setSelected(False)

    def display_arcade_detail(self, arcade_info):
        """显示商场详细信息弹窗"""
        dialog = ArcadeDetailDialog(arcade_info, self)
        dialog.exec_()
   
    def closeEvent(self, event):
        """关闭窗口时关闭数据库连接"""
        self.conn.close()
        event.accept()

class GoWindow(QWidget):
    def __init__(self, signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        self.setWindowTitle("出勤中")
#        self.setWindowIcon(QIcon(bear_path))
#        self.resize(800, 400)
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
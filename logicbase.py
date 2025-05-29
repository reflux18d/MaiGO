"""存放记录数据的类"""
from datetime import datetime
import os


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
    
class Data:
    """记录数据选项的基类"""
    def __init__(self, name: str, val = None, show_in_account = True):   
        self.name = name
        self.val = val
        self.show = False # 重要，决定OptionWindow是否显示对应widget
        self.info = "" # TODO: 加入描述信息

    def set_val(self, new_val):
        """用于单条数据的类"""
        self.val = new_val

    def add_val(self, adder):
        self.val += adder

    def enable(self):
        self.show = True

    def disable(self):
        self.show = False

    def __str__(self):
        return f"{self.name}: {self.val}"
    
    def __add__(self):
        pass
    
    def __iadd__(self, other):
        """用于合并单次Tour的Data对象到User的总计Data对象中"""
        pass

class NumData(Data):
    """记录数值的类，如时间里程等"""
    """暂时默认val为int"""
    def __init__(self, name: str, val = 0):
        super().__init__(name, val)

    def __iadd__(self, other):
        """
        >>> total_time, tour_time = NumData("出勤时间", 60), NumData("出勤时间", 30)
        >>> total_time += tour_time
        >>> print(total_time)
        出勤时间: 90
        """
        assert isinstance(other, NumData) and self.name == other.name, "invalid class"
        self.val += other.val
        return self
    
class StrData(Data):
    """记录文字的类，如不同标签的日记等"""
    def __init__(self, name: str, val: str = ""):
        super().__init__(name, val)

    def __iadd__(self, other, enter = False):
        """支持选择换行"""
        assert isinstance(other, StrData) and self.name == other.name, "invalid class"
        if enter and len(self.val) > 0:
            self.val += '\n'
        self.val += other.val
        return self
    
class DictData(Data):
    """记录选项的类，如选择交通方式并统计次数"""
    """默认key值为int"""
    def __init__(self, name: str, val: dict = None):
        super().__init__(name, val)

    def get_val(self, key):
        return self.val.get(key, 0)
    
    def set_val(self, key, new_val):
        """重载Data的set_val"""
        self.val[key] = new_val

    def add_val(self, key, adder):
        self.val[key] = self.val.get(key, 0) + adder
    
    def update_val(self, key):
        """默认加一，后续有需求可修改"""
        self.add_val(key, 1)
    
    def __iadd__(self, other):   
        assert isinstance(other, DictData) and self.name == other.name, "invalid class"
        for other_key, other_val in other.val.items():
            self.add_val(other_key, other_val)
        return self
    
    def __str__(self):
        result = self.name
        for key, val in self.val.items():
            if val:
                result += '\n'
                result += f"{key}: {val}"
        return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()
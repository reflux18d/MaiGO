"""存放记录数据的类"""
from datetime import datetime
import copy


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
        self.index = None # 第几次，用于Record绑定
        self.start_time = None
        self.arrival_time = None
        self.end_time = None
        self.home = home  # 起点(Place对象)
        self.goal = goal  # 终点(Arcade对象)
        self.state = 0  # 0:准备 1:通勤 2:游玩 3:结束
        self.data = {} # 其他记录数据种类 key: str  val: varible
    
    def set_data(self, user):
        assert isinstance(user, User), "Invalid user type"
        count_data = user.data.get("出勤次数")
        assert isinstance(count_data, NumData), "Invalid data type"
        self.index = int(count_data.val)
        for key, val in user.data.items():
            assert isinstance(val, Data)
            new_data = val.new_copy()
            self.data[key] = new_data
    
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
        self.calc_time()  

    def calc_time(self):
        count_data = self.data.get("出勤次数")
        assert isinstance(count_data, NumData), "No Key in DataDict"
        count_data.add_val(1)
        march_data, play_data = self.data.get("通勤时间"), self.data.get("游玩时间")
        assert isinstance(march_data, NumData) and isinstance(play_data, NumData), "No Key In DataDict"      
        march_time = self.arrival_time - self.start_time
        march_data.add_val(int(march_time.total_seconds()))
        play_time = self.end_time - self.arrival_time
        play_data.add_val(int(play_time.total_seconds()))
        
class User:
    def __init__(self, name, data = None):
        self.name = name
        self.history = []  # 存储所有Tour记录
        self.current_tour = None  # 当前出勤
        self.home = Place()
        self.data = data if data is not None else {} # 总计数据, key: str
        self.record_index = 0

    def __str__(self):
        return self.name
    
    def start_new_tour(self, home, goal):
        """开始新的出勤记录"""
        self.current_tour = Tour(home, goal)
        self.current_tour.set_data(self)
    
    def save_tour(self):
        """保存当前出勤记录"""
        assert isinstance(self.current_tour, Tour), "No Tour to save"
        assert self.current_tour.state >= 3, "Unfinished Tour"
        for key, tour_data in self.current_tour.data.items():
            user_data = self.data.get(key)
            assert isinstance(user_data, Data), "Invalid user data"
            assert isinstance(tour_data, Data), "Invalid tour data"
            if user_data.accumulable:
                user_data += tour_data
        self.history.append(self.current_tour)
        self.current_tour = None

    def add_datatype(self, *new_data):
        """暂时没用上"""
        for data in new_data:
            assert isinstance(data, Data), "Invalid data type"
            key = data.name
            self.data[key] = data
    
class Data:
    """记录数据选项的基类"""
    def __init__(self, name: str, val = None, editable = True, accumulable = True):   
        self.name = name
        self.val = val
        self.show = False # 重要，决定OptionWindow是否显示对应widget
        self.editable = editable # 是否可以人为编辑，初始化之后就不会变化
        self.accumulable = accumulable # 是否计入总计数据并在账号界面中显示
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
    
    def __bool__(self):
        return self.editable and self.show
    
    def __add__(self):
        pass
    
    def __iadd__(self, other):
        """用于合并单次Tour的Data对象到User的总计Data对象中"""
        pass

    def new_copy(self):
        """用于生成一个相同类型但是数据初始化的Data"""
        new_data = copy.deepcopy(self)
        return new_data

class NumData(Data):
    """记录数值的类，如时间里程等"""
    """暂时默认val为int"""
    def __init__(self, name: str, val = 0, editable = True, accumulable = True):
        super().__init__(name, val, editable, accumulable)

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
    
    def new_copy(self):
        new_data = Data.new_copy(self)
        new_data.val = 0
        return new_data
    
class StrData(Data):
    """记录文字的类，如不同标签的日记等"""
    def __init__(self, name: str, val: str = "", editable = True, accumulable = False):
        super().__init__(name, val, editable, accumulable)

    def __iadd__(self, other, enter = False):
        """支持选择换行"""
        assert isinstance(other, StrData) and self.name == other.name, "invalid class"
        if enter and len(self.val) > 0:
            self.val += '\n'
        self.val += other.val
        return self
    
    def add_val(self, adder, enter = True):
        if enter and len(self.val) > 0:
            self.val += '\n'
        self.val += adder
    
    def new_copy(self):
        new_data = Data.new_copy(self)
        new_data.val = ""
        return new_data
    
class DictData(Data):
    """记录选项的类，如选择交通方式并统计次数"""
    """默认key值为int"""
    def __init__(self, name: str, val: dict = None, editable = True, accumulable = True, exclusive = True):
        super().__init__(name, val, editable, accumulable)
        self.exclusive = exclusive

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
    
    def new_copy(self):
        new_data = Data.new_copy(self)
        for key in new_data.val.keys():
            new_data.val[key] = 0
        return new_data


if __name__ == "__main__":
    import doctest
    doctest.testmod()
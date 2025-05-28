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
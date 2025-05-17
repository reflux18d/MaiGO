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


print("just for test")
        

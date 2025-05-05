class Tour:
    states = ["preparing", "proceeding", "ended"]
    def __init__(self):
        self.start_time, self.end_time = None, None #time #14.7
        self.home, self.goal = None, None
        self.transport = None
        self.diary = ""
        self.state = 0

    def here_we_go(self):
        self.state = 1

    def arrived(self):
        self.state = 2

class User:
    def __init__(self, name):
        self.name = name
        self.data = None
        self.history = [] #list of Tour
        self.achivement = []
        

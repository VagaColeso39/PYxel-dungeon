class Level:
    def __init__(self, num, mod=None, start_pos:tuple[int, int]=None):
        self.num = num
        self.mod = mod
        self.start_pos = start_pos
        self.board = None
        self.generate()
    
    def generate(self):
        ...  # all for you
    
    def next_move(self, action):
        pass
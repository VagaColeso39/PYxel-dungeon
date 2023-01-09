class Trap:
    def __init__(self, dungeon, x, y):
        self.dungeon = dungeon
        self.x = x
        self.y = y
    
    def activate(self):
        self.dungeon[self.y][self.x].add_effect()

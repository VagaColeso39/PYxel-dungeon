import bags
from util import *
from tiles import Tile

class Player:
    def __init__(self, start_pos: list[int, int]):
        self.pos = start_pos
        self.backpack = bags.Backpack(self)
        self.vision_field = 9
        self.bags = []
        self.weapon = None
        self.armor = None
        self.artifact = None
        self.ring = None
        self.ring_or_artifact = None
        self.max_hp = 20
        self.hp = 20
        self.xp = 0
        self.level = 1
        self.next_level = 10
        self.strength = 10
        self.gold = 0
        self.accuracy = 10
        self.evasion = 5
        self.turns_to_hunger = 100
        self.effects = []  # fire, poison, slime
        self.buffs = []
        self.turns_of_regeneration = 10
        self.turns_to_regeneration = 10
        self.speed_multipliers = []
        self.walking_speed_multipliers = []
        self.attack_speed_multipliers = []
    
    def hit_hero(self, damage):
        self.hp -= damage
    
    def pick_up(self, item):
        return self.backpack.pick_up(item)

    def is_visible(self, grid:list, cell:Tile):
        '''x = min(self.x, cell.x)
        xi = self.pos[0] + cell.x - x
        y = min(self.pos[1], cell.y)
        yi = self.pos[1] + cell.y - y

        if xi - x > self.vision_field or yi - y > self.vision_field:
            return False
        for i in range(x, xi + 1):
            for j in range(y, yi + 1):
                if grid[x][y].type == 'wall':
                    return False
        return True'''
        if manhattan((self.pos[0], self.pos[1]), (cell.x, cell.y)) > self.vision_field:
            return False
        return True

import bags
from tiles import Tile
from util import *


class Player:
    def __init__(self, start_pos: list[int, int]):
        self.pos = start_pos
        self.backpack = bags.Backpack(self)
        self.vision_field = 6
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
        self.keys = 100  # FIX

    def hit_hero(self, damage):
        self.hp -= damage

    def pick_up(self, item):
        return self.backpack.pick_up(item)

    def is_visible(self, grid: list, cell: Tile):
        if pifagor((self.pos[0], self.pos[1]), (cell.x, cell.y)) <= self.vision_field:
            if all([(grid[x][y].type not in ('earth', 'wall', 'door') or (
                    grid[x][y].type == 'door' and grid[x][y].opened)) for x, y in
                    bresenham(self.pos[0], self.pos[1], cell.x, cell.y)][:-1]):
                return True
        return False

    def try_move(self, grid, x, y):
        if grid[x][y].type == 'door':
            if grid[x][y].modificator == 'closed':
                if self.keys > 0:
                    self.keys -= 1
                    grid[x][y].modificator = None
                    grid[x][y].image = grid[x][y].opened_source
                    grid[x][y].rect = grid[x][y].image.get_rect()
                    grid[x][y].update()
                    return True
                return False
            grid[x][y].image = grid[x][y].opened_source
            grid[x][y].rect = grid[x][y].image.get_rect()
            grid[x][y].update()
            grid[x][y].opened = True

        if grid[x][y].type not in ['wall', 'void']:
            return True

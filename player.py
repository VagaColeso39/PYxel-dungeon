from typing import Literal
import bags
import pygame
from tiles import Tile
from utils.algorithms import *
from utils.astar import astar
from pprint import pprint


class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos: list[int, int]):
        self.source = pygame.image.load('sprites/player.png')
        self.image = pygame.transform.scale(self.source, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (start_pos[0] * 20, start_pos[1] * 20)
        self._layer = 1

        self.pos = start_pos
        self.backpack = bags.Backpack(self)
        self.vision_field = 6
        self.bags = []
        self.weapon = None
        self.armor = None
        self.artifact = None
        self.ring = None
        self.ring_or_artifact = None
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
        self.path = []
        self.keys = 100  # FIX

        self.max_hp = 20
        self.hp = 15

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
                    return True
                return False
            grid[x][y].opened = True

        if grid[x][y].type not in ['wall', 'void']:
            return True
    
    def move(self, x, y, maze):
        if len(self.path) == 0:
            self.path = astar(maze, tuple(self.pos), (x, y))
        if self.path is None:
            self.path = []
            return False
        print(self.path)
        self.pos = list(self.path.pop(0))
        if len(self.path) == 0:
            return False
        return True
    

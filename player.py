import random

import pygame

import bags
from tiles import FloorTile
from tiles import Tile
from utils.algorithms import *
from utils.astar import astar
from utils.sounds import *
from enemies import Enemy


class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos: list[int, int], level_width, level_height, grid):
        pygame.sprite.Sprite.__init__(self)
        self.source = pygame.image.load('sprites/player.png')
        self.image = pygame.transform.scale(self.source, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (start_pos[0] * 20, start_pos[1] * 20)
        self._layer = 1

        self.level_width = level_width
        self.level_height = level_height
        self.grid = grid

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

    def try_move(self, cell):
        for obj in cell.contains:
            if type(obj) == Enemy:
                obj.hit_self(self, random.randint(*self.weapon['damage']), self.grid)
                return False
        if cell.type == 'door':
            if cell.modificator == 'closed':
                if self.keys > 0:
                    self.keys -= 1
                    cell.modificator = None
                    return True
                return False
            cell.opened = True

        if cell.type not in ['wall', 'void']:
            return True

    def move_step(self, pos: tuple[int, int], direction: str = 'x+', block_size: int = 20):
        moved = False
        if not (0 <= pos[0] <= self.level_width) and not (0 <= pos[1] <= self.level_height):
            return False
        if direction == 'x-' and self.pos[0] > 0 and self.try_move(self.grid[pos[0]][pos[1]]):
            self.pos[0] -= 1
            moved = True
        elif direction == 'x+' and self.pos[0] < self.level_width - 1 and self.try_move(self.grid[pos[0]][pos[1]]):
            self.pos[0] += 1
            moved = True
        elif direction == 'y-' and self.pos[1] > 0 and self.try_move(self.grid[pos[0]][pos[1]]):
            self.pos[1] -= 1
            moved = True
        elif direction == 'y+' and self.pos[1] < self.level_height - 1 and self.try_move(self.grid[pos[0]][pos[1]]):
            self.pos[1] += 1
            moved = True
        if self.grid[self.pos[0]][self.pos[1]].type != 'door':
            if self.grid[self.pos[0]][self.pos[1]].type == 'earth':
                pygame.mixer.Sound.play(dig_sound)
                self.grid[self.pos[0]][self.pos[1]] = self.grid[self.pos[0]][self.pos[1]].change_tile(FloorTile)
            else:
                pygame.mixer.Sound.play(step_sound)
        else:
            pygame.mixer.Sound.play(door_sound)

        return moved

    def move(self, x, y, maze, block_size):
        if len(self.path) == 0:
            self.path = astar(maze, tuple(self.pos), (x, y))
        if self.path is None:
            self.path = []
            return False
        move_to = list(self.path.pop(0))
        cell = self.grid[move_to[0]][move_to[1]]
        if self.pos[0] > move_to[0]:
            self.move_step((move_to[0], move_to[1]), 'x-', block_size)
        elif self.pos[0] < move_to[0]:
            self.move_step((move_to[0], move_to[1]), 'x+', block_size)
        elif self.pos[1] > move_to[1]:
            self.move_step((move_to[0], move_to[1]), 'y-', block_size)
        elif self.pos[1] < move_to[1]:
            self.move_step((move_to[0], move_to[1]), 'y+', block_size)

        if len(self.path) == 0:
            return False
        return True

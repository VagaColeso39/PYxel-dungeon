import random

import pygame

from tiles import Tile, FloorTile
from utils.algorithms import *
from utils.astar import astar


class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp=10, dmg: tuple[int, int] = (0, 2), x: int = 0, y: int = 0, name: str = 'rat',
                 xp_contains: int = 3):
        pygame.sprite.Sprite.__init__(self)
        self.source = pygame.image.load('sprites/player.png')  # enemy.png
        self.image = pygame.transform.scale(self.source, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x * 20, y * 20)
        self._layer = 1
        self.hp = hp
        self.vision_field = 6
        self.dmg = dmg
        self.name = name
        self.xp_contains = xp_contains
        self.x = x
        self.y = y

    def attack(self, other):
        other.hit_hero(random.randint(*self.dmg))

    def hit_self(self, other, damage, grid):
        self.hp -= damage
        if self.hp <= 0:
            other.xp += self.xp_contains
            # death

    def turn(self, grid: list, player_cell: Tile, player: object, maze: list, block_size: int):
        if self.is_visible(grid, player_cell):
            if abs(self.x - player.pos[0]) + abs(self.y - player.pos[1]) <= 1:
                self.attack(player)
            else:
                self.move(player_cell.x, player_cell.y, maze, block_size, grid, player, player_cell)
        else:
            self.move_step(grid, random.choice(('x-', 'x+', 'y-', 'y+')), block_size, player)

    def is_visible(self, grid: list, cell: Tile):
        if pifagor((self.x, self.y), (cell.x, cell.y)) <= self.vision_field:
            if all([(grid[x][y].type not in ('earth', 'wall', 'door') or (
                    grid[x][y].type == 'door' and grid[x][y].opened)) for x, y in
                    bresenham(self.x, self.y, cell.x, cell.y)][:-1]):
                return True
        return False

    def try_move(self, cell):
        if (cell.type == 'door' and not cell.opened) or (cell.type == 'wall'):
            return False
        return True

    def move_step(self, grid: list, direction: str = 'x+', block_size: int = 20, player: object = None):
        if direction == 'x-' and self.try_move(grid[self.x - 1][self.y]) and self.x > 0:
            if player.pos != (self.x - 1, self.y):
                self.x -= 1
            else:
                self.attack(player)
        elif direction == 'x+' and self.x < len(grid) - 1 and self.try_move(grid[self.x + 1][self.y]):
            if player.pos != (self.x + 1, self.y):
                self.x += 1
            else:
                self.attack(player)
        elif direction == 'y-' and self.try_move(grid[self.x][self.y - 1]) and self.y > 0:
            if player.pos != (self.x, self.y - 1):
                self.y -= 1
            else:
                self.attack(player)
        elif direction == 'y+' and self.y < len(grid[0]) - 1 and self.try_move(grid[self.x][self.y + 1]):
            if player.pos != (self.x, self.y + 1):
                self.y += 1
            else:
                self.attack(player)
        if grid[self.x][self.y].type == 'earth':
            grid[self.x][self.y] = grid[self.x][self.y].change_tile(FloorTile)

        return True

    def move(self, x, y, maze, block_size, grid, player, player_cell):
        path = astar(maze, (self.x, self.y), (x, y))
        if path is not None:
            if len(path) > 1:
                move_to = list(path.pop(1))
                if self.x > move_to[0]:
                    self.move_step(grid, 'x-', block_size, player)
                elif self.x < move_to[0]:
                    self.move_step(grid, 'x+', block_size, player)
                elif self.y > move_to[1]:
                    self.move_step(grid, 'y-', block_size, player)
                elif self.y < move_to[1]:
                    self.move_step(grid, 'y+', block_size, player)
            else:
                self.attack(player)
        else:
            self.move_step(grid, random.choice(('x-', 'x+', 'y-', 'y+')), block_size, player)

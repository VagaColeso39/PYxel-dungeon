import random

import pygame

from tiles import Tile, FloorTile
from utils.algorithms import *
from utils.astar import astar


class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp=10, dmg: tuple[int, int] = (0, 2), x: int = 0, y: int = 0, name: str = 'rat'):
        pygame.sprite.Sprite.__init__(self)
        self.source = pygame.image.load('sprites/player.png') # enemy.png
        self.image = pygame.transform.scale(self.source, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x * 20, y * 20)
        self._layer = 1
        self.hp = hp
        self.vision_field = 5
        self.dmg = dmg
        self.name = name
        self.x = x
        self.y = y

    def attack(self, other):
        other.hp -= random.randint(*self.dmg)

    def turn(self, grid: list, player_cell: Tile, player: object, maze: list, block_size: int):
        if self.is_visible(grid, player_cell):
            self.move(player_cell.x, player_cell.y, maze, block_size, grid, player, player_cell)
        else:
            self.move_step(player_cell, random.choice(('x-', 'x+', 'y-', 'y+')), block_size, player)

    def is_visible(self, grid: list, cell: Tile):
        if pifagor((self.x, self.y), (cell.x, cell.y)) <= self.vision_field:
            if all([(grid[x][y].type not in ('earth', 'wall', 'door') or (
                    grid[x][y].type == 'door' and grid[x][y].opened)) for x, y in
                    bresenham(self.x, self.y, cell.x, cell.y)][:-1]):
                return True
        return False

    def try_move(self, cell):
        if cell.type == 'door' and not cell.opened:
            return False

        if cell.type != 'wall':
            return True
        return False

    def move_step(self, cell: object, direction: str = 'x+', block_size: int = 20, player: object = None):
        if direction == 'x-' and self.try_move(cell):
            if player.pos != (self.x - 1, self.y):
                self.x -= 1
                self.rect.center = self.x * block_size, self.y * block_size
            else:
                self.attack(player)
        elif direction == 'x+' and self.try_move(cell):
            if player.pos != (self.x + 1, self.y):
                self.x += 1
                self.rect.center = self.x * block_size, self.y * block_size
            else:
                self.attack(player)
        elif direction == 'y-' and self.try_move(cell):
            if player.pos != (self.x, self.y - 1):
                self.y -= 1
                self.rect.center = self.x * block_size, self.y * block_size
            else:
                self.attack(player)
        elif direction == 'y+' and self.try_move(cell):
            if player.pos != (self.x, self.y + 1):
                self.y += 1
                self.rect.center = self.x * block_size, self.y * block_size
            else:
                self.attack(player)
        else:
            return False
        return True

    def move(self, x, y, maze, block_size, grid, player, player_cell):
        path = astar(maze, (self.x, self.y), (x, y))
        if path is not None:
            move_to = list(path.pop(0))
            cell = grid[move_to[0]][move_to[1]]
            if self.x > move_to[0]:
                self.move_step(cell, 'x-', block_size, player)
            elif self.x < move_to[0]:
                self.move_step(cell, 'x+', block_size, player)
            elif self.y > move_to[1]:
                self.move_step(cell, 'y-', block_size, player)
            elif self.y < move_to[1]:
                self.move_step(cell, 'y+', block_size, player)
            if cell.type == 'earth':
                grid[move_to[0]][move_to[1]] = cell.change_tile(FloorTile)
        else:
            self.move_step(player_cell, random.choice(('x-', 'x+', 'y-', 'y+')), block_size, player)


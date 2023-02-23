import random

import pygame

from items import item_generator
from tiles import Tile, FloorTile
from utils.algorithms import *
from utils.astar import astar
from constants import LAYER_ENTITIES


class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp=10, dmg: tuple[int, int] = (0, 2), x: int = 0, y: int = 0, name: str = 'enemy_rat',
                 xp_contains: int = 3, item_drop_cost: tuple[int, int] = (20, 35), defence: tuple[int, int] = (0, 2)):
        pygame.sprite.Sprite.__init__(self)
        self.source = pygame.image.load(f'assets/sprites/{name}.bmp')  # enemy.bmp
        self.source.set_colorkey((255, 255, 255))
        self.empty_sprite = pygame.image.load('assets/sprites/empty_sprite.jpg')
        self.image = pygame.transform.scale(self.source, (20, 20))
        self.visible = False
        self.rect = self.image.get_rect()
        self.rect.center = (x * 20, y * 20)
        self._layer = LAYER_ENTITIES
        self.hp = hp
        self.max_hp = hp
        self.vision_field = 6
        self.dmg = dmg
        self.defence = defence
        self.name = name
        self.xp_contains = xp_contains
        self.item_drop_cost = item_drop_cost
        self.x = x
        self.y = y
        self.last_player_pos = None
        self.blind_counter = 0
        self.player_seen = False

    def blind(self, time: int = 10):
        self.blind_counter += time

    def attack(self, other):
        other.hit_hero(random.randint(*self.dmg))

    def hit_self(self, other, damage: int, all_enemies: list):
        damage -= random.randint(*self.defence)
        if damage > 0:
            self.hp -= damage
        if self.hp <= 0:
            # other.level_up
            other.xp += self.xp_contains
            item = item_generator(random.randint(*self.item_drop_cost))
            other.score += self.max_hp

            if item:  # may drop nothing
                print('drop', item)
                other.grid[self.x][self.y].contains.append(item)
                self.groups()[0].add(item)
            all_enemies.remove(self)
            self.kill()

    def turn(self, grid: list, player_cell: Tile, player: object, maze: list, block_size: int, all_enemies: list):
        if self.blind_counter > 0:
            self.blind_counter -= 1
            self.vision_field = 1
        else:
            self.vision_field = 6
        if self.is_visible(grid, player_cell):
            if abs(self.x - player.pos[0]) + abs(self.y - player.pos[1]) <= 1:
                self.attack(player)
            else:
                self.move(player_cell.x, player_cell.y, maze, block_size, grid, player, all_enemies)

        elif self.last_player_pos is not None:
            self.move(self.last_player_pos[0], self.last_player_pos[1], maze, block_size, grid, player, all_enemies)

        else:
            self.move_step(grid, all_enemies, random.choice(('x-', 'x+', 'y-', 'y+')), block_size, player)

    def is_visible(self, grid: list, cell: Tile):
        if pifagor((self.x, self.y), (cell.x, cell.y)) <= self.vision_field:
            if all([(grid[x][y].type not in ('earth', 'wall', 'door') or (
                    grid[x][y].type == 'door' and grid[x][y].opened)) for x, y in
                    bresenham(self.x, self.y, cell.x, cell.y)][:-1]):
                self.last_player_pos = (cell.x, cell.y)
                return True
        return False

    def try_move(self, cell, all_enemies: list):
        if (cell.type == 'door' and not cell.opened) or (cell.type == 'wall'):
            return False
        for enemy in all_enemies:
            if enemy.x == cell.x and enemy.y == cell.y:
                return False
        return True

    def move_step(self, grid: list, all_enemies: list, direction: str = 'x+', block_size: int = 20,
                  player: object = None):
        if direction == 'x-' and self.try_move(grid[self.x - 1][self.y], all_enemies) and self.x > 0:
            if player.pos != (self.x - 1, self.y):
                self.x -= 1
            else:
                self.attack(player)
        elif direction == 'x+' and self.x < len(grid) - 1 and self.try_move(grid[self.x + 1][self.y], all_enemies):
            if player.pos != (self.x + 1, self.y):
                self.x += 1
            else:
                self.attack(player)
        elif direction == 'y-' and self.try_move(grid[self.x][self.y - 1], all_enemies) and self.y > 0:
            if player.pos != (self.x, self.y - 1):
                self.y -= 1
            else:
                self.attack(player)
        elif direction == 'y+' and self.y < len(grid[0]) - 1 and self.try_move(grid[self.x][self.y + 1], all_enemies):
            if player.pos != (self.x, self.y + 1):
                self.y += 1
            else:
                self.attack(player)

        if grid[self.x][self.y].type == 'earth':
            grid[self.x][self.y] = grid[self.x][self.y].change_tile(FloorTile)

        if self.last_player_pos == (self.x, self.y):
            self.last_player_pos = None
        return True

    def move(self, x, y, maze, block_size, grid, player, all_enemies):
        path = astar(maze, (self.x, self.y), (x, y))
        if path is not None:
            if len(path) > 1:
                move_to = list(path.pop(1))
                if self.x > move_to[0]:
                    self.move_step(grid, all_enemies, 'x-', block_size, player)
                elif self.x < move_to[0]:
                    self.move_step(grid, all_enemies, 'x+', block_size, player)
                elif self.y > move_to[1]:
                    self.move_step(grid, all_enemies, 'y-', block_size, player)
                elif self.y < move_to[1]:
                    self.move_step(grid, all_enemies, 'y+', block_size, player)
            else:
                self.attack(player)
        else:
            self.move_step(grid, random.choice(('x-', 'x+', 'y-', 'y+')), block_size, player)

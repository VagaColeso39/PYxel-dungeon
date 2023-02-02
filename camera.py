import pygame
from player import Player
from level import Level
from constants_original import *
from typing import Literal
from utils.easing import CubicEaseOut


class Camera:
    def __init__(self, player:Player, level:Level, screen:pygame.Surface) -> None:
        self.cx = 0  # x of center of camera
        self.cy = 0  # y of center of camera
        self.to_x = 0
        self.to_y = 0
        self.strength = 8  # frames to push camera to target, that more that slower
        self.frames_skipped = 0
        self.multiplier = 1  # alternative way to set current block size
        self.player = player
        self.level = level
        self.screen = screen
        self.dft_block_size = self.level.block_size
        self.block_size = self.dft_block_size
        self.min_block_size = 10
        self.max_block_size = 100
        self.easing = CubicEaseOut(0, 1, self.strength)

        self.f1 = pygame.font.Font(None, 25)

    def drawGrid(self):
        self.screen.fill(EMPTY_COLOR)
        for x in range(0, self.level.level_width):
            for y in range(0, self.level.level_height):
                
                color = EARTH_COLOR
                if self.player.is_visible(self.level.dungeon.grid, self.level.dungeon.grid[x][y]):
                    self.level.dungeon.grid[x][y].visible = True
                    if self.level.dungeon.grid[x][y].type == 'earth':
                        color = EARTH_COLOR
                    elif self.level.dungeon.grid[x][y].type == 'floor':
                        color = FLOOR_COLOR
                    elif self.level.dungeon.grid[x][y].type == 'door':
                        color = DOOR_COLOR
                    elif self.level.dungeon.grid[x][y].type == 'wall':
                        color = WALL_COLOR

                elif self.level.dungeon.grid[x][y].visible or self.level.dungeon.grid[x][y].explored:
                    self.level.dungeon.grid[x][y].explored = True
                    self.level.dungeon.grid[x][y].visible = False
                    if self.level.dungeon.grid[x][y].type == 'earth':
                        color = EARTH_COLOR_FADED
                    elif self.level.dungeon.grid[x][y].type == 'floor':
                        color = FLOOR_COLOR_FADED
                    elif self.level.dungeon.grid[x][y].type == 'door':
                        color = DOOR_COLOR_FADED
                    elif self.level.dungeon.grid[x][y].type == 'wall':
                        color = WALL_COLOR_FADED
                else:
                    color = EMPTY_COLOR
                
                cell = pygame.Rect(int(x * self.block_size - self.tl_x), int(y * self.block_size - self.tl_y), self.block_size, self.block_size)

                pygame.draw.rect(self.screen, color, cell)
                if color not in [PLAYER_COLOR, EMPTY_COLOR, ENEMY_COLOR]:
                    pygame.draw.rect(self.screen, GRAY_BORDER, cell, 1)

        for enemy in self.level.all_enemies:
            if self.player.is_visible(self.level.dungeon.grid, self.level.dungeon.grid[enemy.x][enemy.y]):
                enemy.image = pygame.transform.scale(enemy.source, (self.block_size, self.block_size))
                enemy.rect.center = (int(enemy.x * self.block_size - self.tl_x + self.block_size // 2),
                                       int(enemy.y * self.block_size - self.tl_y + self.block_size // 2))
            else:
                enemy.image = pygame.transform.scale(enemy.empty_sprite, (0, 0))

        self.player.image = pygame.transform.scale(self.player.source, (self.block_size, self.block_size))
        self.player.rect.center = (int(self.player.pos[0] * self.block_size - self.tl_x + self.block_size // 2), int(self.player.pos[1] * self.block_size - self.tl_y + self.block_size // 2))
        self.draw_hud()
        self._next_frame_easing()  # call in the end

    @property
    def tl_x(self):
        return self.cx - self.screen.get_size()[0] // 2

    @property
    def tl_y(self):
        return self.cy - self.screen.get_size()[1] // 2

    def _next_frame_easing(self):
        if self.frames_skipped != self.strength:
            self.cx = self.cx + int((self.to_x - self.cx) * self.easing.ease(self.frames_skipped + 1))
            self.cy = self.cy + int((self.to_y - self.cy) * self.easing.ease(self.frames_skipped + 1))

    def draw_hud(self):
        hp_bar = pygame.Rect(10, 10, int(400 * (self.player.hp / self.player.max_hp).__round__(2)), 15)
        hp_bar_missing = pygame.Rect(10, 10, 400, 15)
        pygame.draw.rect(self.screen, HP_BAR_COLOR_MISSING, hp_bar_missing)
        pygame.draw.rect(self.screen, GRAY_BORDER, hp_bar_missing, 2)
        pygame.draw.rect(self.screen, HP_BAR_COLOR, hp_bar)
        pygame.draw.rect(self.screen, GRAY_BORDER, hp_bar, 2)
        text = self.f1.render(f"{self.player.hp}/{self.player.max_hp}", True, HP_BAR_COLOR)
        self.screen.blit(text, (410, 10))

    def _next_frame(self):
        if self.frames_skipped != self.strength:
            self.cx = self.cx + int((self.to_x - self.cx) / (self.strength - self.frames_skipped))
            self.cy = self.cy + int((self.to_y - self.cy) / (self.strength - self.frames_skipped))
            self.frames_skipped += 1
    
    def move_to(self, x, y, type:Literal['cell', 'point']='cell'):
        if type == 'point':
            self.to_x = x
            self.to_y = y
        else: 
            self.to_x = int(self.block_size * x + self.block_size / 2)
            self.to_y = int(self.block_size * y + self.block_size / 2)
        self.frames_skipped = 0
    
    def set_size(self, num, type:Literal['points', 'multiplier']='points'):
        if type == 'points' and self.max_block_size >= num >= self.min_block_size:
            self.block_size = num
            self.multiplier = self.block_size / self.dft_block_size
        elif type == 'multiplier' and self.max_block_size >= self.dft_block_size * num >= self.min_block_size:
            self.multiplier = num
            self.block_size = int(self.dft_block_size * self.multiplier)
        self.move_to(self.cx, self.cy, 'point')
    def get_cell(self, x, y):
        return (x + self.tl_x) // self.block_size, (y + self.tl_y) // self.block_size
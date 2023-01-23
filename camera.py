import pygame
from player import Player
from level import Level
from constants import *
from typing import Literal

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

    def drawGrid(self):
        self.screen.fill(BLACK)
        for x in range(0, self.level.level_width):
            for y in range(0, self.level.level_height):
                color = LIGHT_BROWN
                if self.player.is_visible(self.level.dungeon.grid, self.level.dungeon.grid[x][y]):
                    self.level.dungeon.grid[x][y].visible = True
                    if self.level.dungeon.grid[x][y].type == 'earth':
                        color = LIGHT_BROWN
                    elif self.level.dungeon.grid[x][y].type == 'floor':
                        color = BROWN
                    elif self.level.dungeon.grid[x][y].type == 'door':
                        color = WHITE
                    elif self.level.dungeon.grid[x][y].type == 'wall':
                        color = GRAY

                elif self.level.dungeon.grid[x][y].visible or self.level.dungeon.grid[x][y].explored:
                    self.level.dungeon.grid[x][y].explored = True
                    self.level.dungeon.grid[x][y].visible = False

                    if self.level.dungeon.grid[x][y].type == 'earth':
                        color = LIGHT_BROWN_FADED
                    elif self.level.dungeon.grid[x][y].type == 'floor':
                        color = BROWN_FADED
                    elif self.level.dungeon.grid[x][y].type == 'door':
                        color = WHITE_FADED
                    elif self.level.dungeon.grid[x][y].type == 'wall':
                        color = GRAY_FADED
                else:
                    color = BLACK

                if self.player.pos[0] == x and self.player.pos[1] == y:
                    color = RED

                cell = pygame.Rect(int(x * self.block_size - self.tl_x), int(y * self.block_size - self.tl_y), self.block_size, self.block_size)
                
                pygame.draw.rect(self.screen, color, cell)
                if color not in [RED, BLACK]:
                    pygame.draw.rect(self.screen, GRAY_BORDER, cell, 1)
                
        self._next_frame()  # call in the end

    @property
    def tl_x(self):
        return self.cx - self.screen.get_size()[0] // 2

    @property
    def tl_y(self):
        return self.cy - self.screen.get_size()[1] // 2

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
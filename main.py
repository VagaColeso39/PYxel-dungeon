import random
import sys

import pygame

import dungeonGenerator
import sprites
from level import Level

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BROWN = (205, 120, 34)
LIGHT_BROWN = (243, 163, 83)
SOFT_BROWN = (126, 109, 91)
GRAY = (110, 110, 111)


def main():
    global SCREEN, CLOCK
    multiplier = random.randint(50, 60)
    chance_for_door = 100
    level = Level(multiplier, chance_for_door, 1)
    player = sprites.Player(50, {'damage': (8, 10), 'isDoubleHand': False, 'name': 'shortSword'},
                            {'defence': (0, 2), 'name': 'leatherArmor'})
    block_size = 10

    pygame.init()
    SCREEN = pygame.display.set_mode((level.level_width * block_size, level.level_height * block_size))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    while True:
        drawGrid(level, block_size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def drawGrid(level:Level, blockSize: int = 20):
    for x in range(0, level.level_width):
        for y in range(0, level.level_height):
            color = WHITE
            if level.dungeon.grid[x][y] == dungeonGenerator.EMPTY:
                pass  # empty cell
            elif level.dungeon.grid[x][y] == dungeonGenerator.FLOOR:
                color = BROWN
            elif level.dungeon.grid[x][y] == dungeonGenerator.CORRIDOR:
                color = BROWN
            elif level.dungeon.grid[x][y] == dungeonGenerator.DOOR:
                color = LIGHT_BROWN
            elif level.dungeon.grid[x][y] == dungeonGenerator.WALL:
                color = BLACK

            cell = pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)
            pygame.draw.rect(SCREEN, color, cell)
            if level.dungeon.grid[x][y] != dungeonGenerator.WALL:
                pygame.draw.rect(SCREEN, GRAY, cell, 1)


if __name__ == "__main__":
    main()

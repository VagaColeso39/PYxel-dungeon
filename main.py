import pygame
import sys

import dungeonGenerator
import sprites
import random

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BROWN = (205, 120, 34)
LIGHT_BROWN = (243, 163, 83)
SOFT_BROWN = (126, 109, 91)
GRAY = (110, 110, 111)


def main():
    global SCREEN, CLOCK, level
    multiplier = random.randint(50, 100)
    chance_for_door = 50
    level = sprites.Level(multiplier, chance_for_door)
    block_size = 10

    pygame.init()
    SCREEN = pygame.display.set_mode((level.level_width * block_size, level.level_height * block_size))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    while True:
        drawGrid(block_size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def drawGrid(blockSize: int = 20):
    for x in range(0, level.level_width):
        for y in range(0, level.level_height):
            color = WHITE
            if level.dungeon.grid[x][y] == dungeonGenerator.EMPTY:
                pass  # empty cell
            elif level.dungeon.grid[x][y] == dungeonGenerator.FLOOR:
                color = BROWN
            elif level.dungeon.grid[x][y] == dungeonGenerator.CORRIDOR:
                color = SOFT_BROWN
            elif level.dungeon.grid[x][y] == dungeonGenerator.DOOR:
                color = LIGHT_BROWN
            elif level.dungeon.grid[x][y] == dungeonGenerator.WALL:
                color = BLACK

            cell = pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)
            pygame.draw.rect(SCREEN, color, cell)
            pygame.draw.rect(SCREEN,  GRAY, cell, 1)


if __name__ == "__main__":
    main()

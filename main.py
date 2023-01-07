import pygame
import sys
import sprites
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)


def main():
    global SCREEN, CLOCK, level
    level = sprites.Level()
    block_size = 20

    pygame.init()
    SCREEN = pygame.display.set_mode((level.level_width * block_size, level.level_height * block_size))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)


    while True:
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def drawGrid(blockSize:int=20):
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            cell = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, cell, 1)


main()
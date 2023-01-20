import random
import sys
import pygame
import dungeonGenerator
from player import Player
from level import Level
from tiles import WallTile, DoorTile, VoidTile, FloorTile

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WHITE_FADED = (180, 180, 180)
BROWN = (205, 120, 34)
BROWN_FADED = (175, 90, 4)
LIGHT_BROWN = (243, 163, 83)
LIGHT_BROWN_FADED = (213, 133, 53)
SOFT_BROWN = (126, 109, 91)
SOFT_BROWN_FADED = (96, 79, 61)
GRAY = (110, 110, 111)
GRAY_FADED = (80, 80, 81)
RED = (255, 0, 0)
SCREEN = None

def main():
    global SCREEN, CLOCK
    multiplier = random.randint(50, 60)
    chance_for_door = 100
    block_size = 10
    level = Level(multiplier, chance_for_door, 1)

    pygame.init()
    SCREEN = pygame.display.set_mode((level.level_width * block_size, level.level_height * block_size))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    player = Player(start_pos=level.start_pos)
    player.weapon = {'damage': (8, 10), 'isDoubleHand': False, 'name': 'shortSword'}
    player.armor = {'defence': (0, 2), 'name': 'leatherArmor'}
    print(player.pos)
    while True:
        drawGrid(player, level, block_size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.pos[1] -= 1
                elif event.key == pygame.K_DOWN:
                    player.pos[1] += 1
                elif event.key == pygame.K_LEFT:
                    player.pos[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    player.pos[0] += 1

        pygame.display.update()


def drawGrid(player:Player, level:Level, blockSize: int = 20):
    for x in range(0, level.level_width):
        for y in range(0, level.level_height):
            color = WHITE
            if player.is_visible(level.dungeon.grid, level.dungeon.grid[x][y]):
                level.dungeon.grid[x][y].visible = True
                if level.dungeon.grid[x][y].type == 'void':
                    pass  # empty cell
                elif level.dungeon.grid[x][y].type == 'floor':
                    color = BROWN
                elif level.dungeon.grid[x][y].type == 'corridor':  # currently doesnt work
                    color = BROWN
                elif level.dungeon.grid[x][y].type == 'door':
                    color = LIGHT_BROWN
                elif level.dungeon.grid[x][y].type == 'wall':
                    color = WHITE

            elif level.dungeon.grid[x][y].visible:
                level.dungeon.grid[x][y].explored = True
                level.dungeon.grid[x][y].visible = False

                if level.dungeon.grid[x][y].type == 'void':
                    pass  # empty cell
                elif level.dungeon.grid[x][y].type == 'floor':
                    color = BROWN_FADED
                elif level.dungeon.grid[x][y].type == 'corridor':  # currently doesnt work
                    color = BROWN_FADED
                elif level.dungeon.grid[x][y].type == 'door':
                    color = LIGHT_BROWN_FADED
                elif level.dungeon.grid[x][y].type == 'wall':
                    color = BLACK
            else:
                color = BLACK

            if player.pos[0] == x and player.pos[1] == y:
                color = RED

            cell = pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)
            pygame.draw.rect(SCREEN, color, cell)
            if color not in [BLACK, RED]:
                pygame.draw.rect(SCREEN, GRAY, cell, 1)


if __name__ == "__main__":
    main()

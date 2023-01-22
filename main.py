import random
import sys
import pygame
import dungeonGenerator
from player import Player
from level import Level
from tiles import WallTile, DoorTile, EarthTile, FloorTile, tiles_sprites, layers

BLACK = (20, 20, 20)
BLACK_FADED = (0, 0, 0)
WHITE = (200, 200, 200)
WHITE_FADED = (160, 160, 160)
BROWN = (205, 120, 34)
BROWN_FADED = (175, 90, 4)
LIGHT_BROWN = (243, 163, 83)
LIGHT_BROWN_FADED = (200, 120, 40)
SOFT_BROWN = (126, 109, 91)
SOFT_BROWN_FADED = (96, 79, 61)
GRAY = (110, 110, 111)
GRAY_FADED = (80, 80, 81)
GRAY_BORDER = (130, 130, 131)

RED = (255, 0, 0)
SCREEN = None


def main():
    global SCREEN, CLOCK
    multiplier = random.randint(50, 60)
    chance_for_door = 100
    block_size = 20
    level = Level(multiplier, chance_for_door, 1, block_size)

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
                moved = False
                if event.key == pygame.K_UP:
                    if player.pos[1] > 0 and player.try_move(level.dungeon.grid, player.pos[0], player.pos[1] - 1):
                        player.pos[1] -= 1
                        moved = True
                elif event.key == pygame.K_DOWN:
                    if player.pos[1] < level.level_height - 1 and player.try_move(level.dungeon.grid, player.pos[0], player.pos[1] + 1):
                        player.pos[1] += 1
                        moved = True
                elif event.key == pygame.K_LEFT:
                    if player.pos[0] > 0 and player.try_move(level.dungeon.grid, player.pos[0] - 1, player.pos[1]):
                        player.pos[0] -= 1
                        moved = True
                elif event.key == pygame.K_RIGHT:
                    if player.pos[0] < level.level_width - 1 and player.try_move(level.dungeon.grid, player.pos[0] + 1, player.pos[1]):
                        player.pos[0] += 1
                        moved = True
                if moved:
                    if level.dungeon.grid[player.pos[0]][player.pos[1]].type != 'door':
                        level.dungeon.grid[player.pos[0]][player.pos[1]] = level.dungeon.grid[player.pos[0]][player.pos[1]].change_tile(FloorTile)


                """
                elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    if block_size < 100:
                        block_size += 2
                else:
                    if block_size > 20:
                        block_size -= 2
                """
        pygame.display.update()


def drawGrid(player:Player, level:Level, blockSize: int = 20):
    for x in range(0, level.level_width):
        for y in range(0, level.level_height):
            color = LIGHT_BROWN
            if player.is_visible(level.dungeon.grid, level.dungeon.grid[x][y]):
                level.dungeon.grid[x][y].visible = True
                if level.dungeon.grid[x][y].type == 'earth':
                    color = LIGHT_BROWN
                elif level.dungeon.grid[x][y].type == 'floor':
                    color = BROWN
                elif level.dungeon.grid[x][y].type == 'door':
                    color = WHITE
                elif level.dungeon.grid[x][y].type == 'wall':
                    color = GRAY

            elif level.dungeon.grid[x][y].visible or level.dungeon.grid[x][y].explored:
                level.dungeon.grid[x][y].explored = True
                level.dungeon.grid[x][y].visible = False

                if level.dungeon.grid[x][y].type == 'earth':
                    color = LIGHT_BROWN_FADED
                elif level.dungeon.grid[x][y].type == 'floor':
                    color = BROWN_FADED
                elif level.dungeon.grid[x][y].type == 'door':
                    color = WHITE_FADED
                elif level.dungeon.grid[x][y].type == 'wall':
                    color = GRAY_FADED
            else:
                color = BLACK

            if player.pos[0] == x and player.pos[1] == y:
                color = RED

            cell = pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)
            pygame.draw.rect(SCREEN, color, cell)
            if color not in [RED, BLACK]:
                pygame.draw.rect(SCREEN, GRAY_BORDER, cell, 1)


if __name__ == "__main__":
    main()

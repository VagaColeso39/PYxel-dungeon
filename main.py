import random
import sys
import pygame
import dungeonGenerator
from player import Player
from level import Level
from tiles import WallTile, DoorTile, EarthTile, FloorTile, tiles_sprites, layers
from camera import Camera
from constants import *

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
    camera = Camera(player, level, SCREEN)
    while True:
        camera.drawGrid()
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





if __name__ == "__main__":
    main()

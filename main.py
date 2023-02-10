import random
import sys

import pygame

from camera import Camera
from constants_original import *
from level import Level
from player import Player
from tiles import FloorTile, LadderTile
from utils.sounds import *
from items import item_giver

pygame.init()
layers = pygame.sprite.LayeredUpdates()
entities_sprites = pygame.sprite.Group()

multiplier = random.randint(55, 60)
chance_for_door = 100
block_size = 20

level = Level(multiplier, chance_for_door, 1, block_size)
levels = [level]

SCREEN = pygame.display.set_mode((500, 500))
CLOCK = pygame.time.Clock()
SCREEN.fill(EMPTY_COLOR)


def main():
    global level
    player = Player(level.start_pos, level.level_width, level.level_height, level.dungeon.grid)

    player.weapon = item_giver('short_sword', 'weapons')
    player.armor = item_giver('cloth_armor', 'armor')
    player.backpack.pick_up(item_giver('teleport_scroll', 'scrolls'))
    camera = Camera(player, level, SCREEN)
    camera.move_to(*player.pos)
    mouse_pos = (0, 0)
    current_x, current_y = 0, 0
    dragging = 0
    running = False

    entities_sprites.add(player)
    for enemy in level.all_enemies:
        entities_sprites.add(enemy)

    pygame.mixer.music.load('music/main_theme.wav')
    pygame.mixer.music.play(-1)

    while True:
        CLOCK.tick_busy_loop(60)
        pygame.display.set_caption("fps: " + str(CLOCK.get_fps()))
        camera.drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                moved = False
                if event.key in [pygame.K_UP, pygame.K_w]:
                    moved = player.move_step((player.pos[0], player.pos[1] - 1), level.all_enemies, 'y-', block_size)
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    moved = player.move_step((player.pos[0], player.pos[1] + 1), level.all_enemies, 'y+', block_size)
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    moved = player.move_step((player.pos[0] - 1, player.pos[1]), level.all_enemies, 'x-', block_size)
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    moved = player.move_step((player.pos[0] + 1, player.pos[1]), level.all_enemies, 'x+', block_size)
                elif event.key == pygame.K_SPACE:
                    moved = True
                elif event.key == pygame.K_e:
                    if level.dungeon.grid[player.pos[0]][player.pos[1]].contains:
                        player.pick_up(level.dungeon.grid[player.pos[0]][player.pos[1]].contains.pop(-1))
                        moved = True
                elif event.key == pygame.K_TAB:
                    for item in player.backpack:
                        if item.use(enemies=level.all_enemies, level=level, player=player, camera=camera):
                            player.backpack.remove(item)
                    print(player.backpack)
                elif event.key == pygame.K_g:
                    if player.backpack:
                        player.backpack[-1].drop(player, level.dungeon.grid)
                if moved:
                    if "ladder" in level.dungeon.grid[player.pos[0]][player.pos[1]].type:
                        if level.dungeon.grid[player.pos[0]][player.pos[1]].type == "ladder_down":
                            if level.num == len(levels):  # if it is the last level currently
                                levels.append(Level(multiplier, chance_for_door, level.num + 1, block_size))
                            level = levels[level.num]
                        else:
                            level = levels[level.num - 2]

                        level.start_room.room_type = "start"
                        if level.num != 1:
                            level.dungeon.grid[level.start_pos[0]][level.start_pos[1]] = \
                                LadderTile(level.dungeon, level.start_pos[0], level.start_pos[1], 'up')

                        entities_sprites.empty()
                        entities_sprites.add(player)
                        for enemy in level.all_enemies:
                            entities_sprites.add(enemy)

                        camera = Camera(player, level, SCREEN)
                        camera.move_to(*player.pos)

                        player.grid = level.dungeon.grid
                        player.pos = level.start_pos

                    if level.dungeon.grid[player.pos[0]][player.pos[1]].type != 'door':
                        if level.dungeon.grid[player.pos[0]][player.pos[1]].type == 'earth':
                            pygame.mixer.Sound.play(dig_sound)
                            level.dungeon.grid[player.pos[0]][player.pos[1]] = level.dungeon.grid[player.pos[0]][
                                player.pos[1]].change_tile(FloorTile)
                        else:
                            pygame.mixer.Sound.play(step_sound)
                    else:
                        pygame.mixer.Sound.play(door_sound)

                    camera.move_to(*player.pos)
                    for enemy in level.all_enemies:
                        enemy.turn(level.dungeon.grid, level.dungeon.grid[player.pos[0]][player.pos[1]], player,
                                   level.maze, block_size, level.all_enemies)

            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    camera.set_size(camera.multiplier + 0.1, 'multiplier')
                else:
                    camera.set_size(camera.multiplier - 0.1, 'multiplier')

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                mouse_pos = pygame.mouse.get_pos()
                current_x, current_y = camera.cx, camera.cy

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if dragging == 1:
                    running = True
                    camera.move_to(*camera.get_cell(*mouse_pos))
                dragging = 0

            if pygame.mouse.get_pressed()[0]:
                dragging += 1
                if mouse_pos is not None:
                    x = current_x + (mouse_pos[0] - pygame.mouse.get_pos()[0])
                    y = current_y + (mouse_pos[1] - pygame.mouse.get_pos()[1])
                    camera.move_to(x, y, 'point')
        if running:
            x = current_x + (mouse_pos[0] - pygame.mouse.get_pos()[0])
            y = current_y + (mouse_pos[1] - pygame.mouse.get_pos()[1])
            camera.move_to(x, y, 'point')
            if not player.move(*camera.get_cell(*mouse_pos), level.maze, block_size, level.all_enemies):
                running = False
            else:
                for enemy in level.all_enemies:
                    enemy.turn(level.dungeon.grid, level.dungeon.grid[player.pos[0]][player.pos[1]], player, level.maze,
                               block_size, level.all_enemies)
            pygame.time.delay(random.randint(70, 100))
        entities_sprites.update()
        entities_sprites.draw(SCREEN)
        pygame.display.update()

        if player.hp <= 0:
            print("GAME OVER")
            break


if __name__ == "__main__":
    main()

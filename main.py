import random
import sys
import pygame
from player import Player
from level import Level
from tiles import WallTile, DoorTile, EarthTile, FloorTile
from camera import Camera
from constants_original import *
layers = pygame.sprite.LayeredUpdates()
entities_sprites = pygame.sprite.Group()

multiplier = random.randint(55, 60)
chance_for_door = 100
block_size = 20
level = Level(multiplier, chance_for_door, 1, block_size)

pygame.init()
SCREEN = pygame.display.set_mode((level.level_width * block_size, level.level_height * block_size))
CLOCK = pygame.time.Clock()
SCREEN.fill(EMPTY_COLOR)


def main():
    player = Player(start_pos=level.start_pos)

    player.weapon = {'damage': (8, 10), 'isDoubleHand': False, 'name': 'shortSword'}
    player.armor = {'defence': (0, 2), 'name': 'leatherArmor'}
    camera = Camera(player, level, SCREEN)
    camera.move_to(*player.pos)
    mouse_pos = (0, 0)
    current_x, current_y = 0, 0
    mouse_pos = None
    dragging = 0

    pygame.mixer.music.load('music/main_theme.wav')
    pygame.mixer.music.play(-1)
    dig_sound = pygame.mixer.Sound("music/dig_sound.wav")
    step_sound = pygame.mixer.Sound('music/step_sound.wav')
    door_sound = pygame.mixer.Sound('music/door_sound.wav')
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
                if event.key == pygame.K_UP:
                    if player.pos[1] > 0 and player.try_move(level.dungeon.grid, player.pos[0], player.pos[1] - 1):
                        player.pos[1] -= 1
                        player.rect.center = player.pos[0] * block_size, player.pos[1] * block_size
                        moved = True

                elif event.key == pygame.K_DOWN:
                    if player.pos[1] < level.level_height - 1 and player.try_move(level.dungeon.grid, player.pos[0], player.pos[1] + 1):
                        player.pos[1] += 1
                        player.rect.center = player.pos[0] * block_size, player.pos[1] * block_size
                        moved = True

                elif event.key == pygame.K_LEFT:
                    if player.pos[0] > 0 and player.try_move(level.dungeon.grid, player.pos[0] - 1, player.pos[1]):
                        player.pos[0] -= 1
                        player.rect.center = player.pos[0] * block_size, player.pos[1] * block_size
                        moved = True

                elif event.key == pygame.K_RIGHT:
                    if player.pos[0] < level.level_width - 1 and player.try_move(level.dungeon.grid, player.pos[0] + 1, player.pos[1]):
                        player.pos[0] += 1
                        player.rect.center = player.pos[0] * block_size, player.pos[1] * block_size
                        moved = True

                if moved:
                    if level.dungeon.grid[player.pos[0]][player.pos[1]].type != 'door':
                        if level.dungeon.grid[player.pos[0]][player.pos[1]].type == 'earth':
                            pygame.mixer.Sound.play(dig_sound)
                            level.dungeon.grid[player.pos[0]][player.pos[1]] = level.dungeon.grid[player.pos[0]][player.pos[1]].change_tile(FloorTile)
                        else:
                            pygame.mixer.Sound.play(step_sound)
                    else:
                        pygame.mixer.Sound.play(door_sound)

                    camera.move_to(*player.pos)

            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    camera.set_size(camera.multiplier + 0.1, 'multiplier')
                else:
                    camera.set_size(camera.multiplier - 0.1, 'multiplier')
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                mouse_pos = pygame.mouse.get_pos()
                current_x, current_y = camera.cx, camera.cy
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if dragging != 1:
                    dragging = 0
                else:
                    player.move_to_cell(*camera.get_cell(*mouse_pos), level.maze)
                    dragging = 0
            
            if pygame.mouse.get_pressed()[0]:
                dragging += 1
                '''x = camera.cx + 5 * (mouse_pos[0] - pygame.mouse.get_pos()[0])
                y = camera.cy + 5 * (mouse_pos[1] - pygame.mouse.get_pos()[1])
                camera.move_to(x, y, 'point')
                mouse_pos = pygame.mouse.get_pos()'''
                x = current_x + (mouse_pos[0] - pygame.mouse.get_pos()[0])
                y = current_y + (mouse_pos[1] - pygame.mouse.get_pos()[1])
                camera.move_to(x, y, 'point')
        layers.draw(SCREEN)
        pygame.display.update()


if __name__ == "__main__":
    main()

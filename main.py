import random
import sys

import pygame

from camera import Camera
from constants import *
from level import Level
from player import Player
from tiles import FloorTile, LadderTile
from utils.sounds import *
from items import item_giver
from inventory import Inventory, HUDChoose

pygame.init()
layers = pygame.sprite.LayeredUpdates()
entities_sprites = pygame.sprite.LayeredUpdates()

multiplier = random.randint(55, 60)
chance_for_door = 100
player = None
block_size = 20

level = Level(multiplier, chance_for_door, 1, block_size)
levels = [level]
for i in level.dungeon.grid:
    for j in i:
        entities_sprites.add(j)

SCREEN = pygame.display.set_mode((500, 500))
CLOCK = pygame.time.Clock()
SCREEN.fill(EMPTY_COLOR)

pygame.mixer.music.load('assets/music/main_theme.wav')
pygame.mixer.music.play(-1)


def initialize():
    global layers, entities_sprites, multiplier, level, levels, player
    layers = pygame.sprite.LayeredUpdates()
    entities_sprites = pygame.sprite.LayeredUpdates()

    multiplier = random.randint(55, 60)

    player = Player(level.start_pos, level.level_width, level.level_height, level.dungeon.grid)
    level = Level(multiplier, chance_for_door, 1, block_size)
    levels = [level]
    for i in level.dungeon.grid:
        for j in i:
            entities_sprites.add(j)


def game_intro():
    logo = pygame.transform.scale(pygame.image.load('assets/sprites/logo.png'), (323, 175))
    start = pygame.transform.scale(pygame.image.load('assets/sprites/start_text.png'), (120, 40))
    records = pygame.transform.scale(pygame.image.load('assets/sprites/records_text.png'), (183, 40))
    quit_text = pygame.transform.scale(pygame.image.load('assets/sprites/quit_text.png'), (92, 40))
    alpha = 255
    while True:
        CLOCK.tick_busy_loop(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 350 > event.pos[0] > 150:
                    if 250 < event.pos[1] < 300:
                        initialize()
                        start_game()
                        alpha = 0
                    elif 325 < event.pos[1] < 375:
                        records_screen()
                    elif 400 < event.pos[1] < 450:
                        pygame.quit()
                        quit()
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(logo, (89, 38))
        pygame.draw.rect(SCREEN, (160, 170, 150), pygame.Rect(150, 250, 200, 50))
        pygame.draw.rect(SCREEN, (160, 170, 150), pygame.Rect(150, 325, 200, 50))
        pygame.draw.rect(SCREEN, (160, 170, 150), pygame.Rect(150, 400, 200, 50))
        pygame.draw.rect(SCREEN, (90, 100, 80), pygame.Rect(152, 252, 196, 46))
        pygame.draw.rect(SCREEN, (90, 100, 80), pygame.Rect(152, 327, 196, 46))
        pygame.draw.rect(SCREEN, (90, 100, 80), pygame.Rect(152, 402, 196, 46))
        SCREEN.blit(start, (192, 255))
        SCREEN.blit(records, (160, 330))
        SCREEN.blit(quit_text, (210, 405))
        if alpha > 0:
            s = pygame.Surface((500, 500), pygame.SRCALPHA)
            s.fill((0, 0, 0, alpha))
            SCREEN.blit(s, (0,0))
            alpha -= 1
        pygame.display.update()


def records_screen():
    while True:
        CLOCK.tick_busy_loop(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        SCREEN.fill((0, 0, 0))
        pygame.display.update()


def game_over():
    BUTTONS_FONT = pygame.freetype.Font('assets/fonts/pixel_font.ttf', 26)
    old = SCREEN
    game_over_text = pygame.transform.scale(pygame.image.load('assets/sprites/game_over.png'), (350, 57))
    menu = pygame.transform.scale(pygame.image.load('assets/sprites/menu.png'), (115, 40))
    alpha = 0
    text = BUTTONS_FONT.render(f"score:{player.score}", True, (255, 255, 255))

    while True:
        CLOCK.tick_busy_loop(60)
        s = pygame.Surface((500, 500))
        s.set_alpha(alpha)
        s.fill((0, 0, 0))  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 350 > event.pos[0] > 150:
                    if 325 < event.pos[1] < 375:
                        return
        SCREEN.blit(old, (0, 0))
        s.blit(game_over_text, (80, 100))
        pygame.draw.rect(s, (160, 170, 150), pygame.Rect(150, 325, 200, 50))
        pygame.draw.rect(s, (90, 100, 80), pygame.Rect(152, 327, 196, 46))
        s.blit(menu, (194, 330))
        s.blit(text[0], (410, 10))
        SCREEN.blit(s, (0,0))
        if alpha < 255:
            alpha += 1
        pygame.display.update()

def start_game():
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
    throwing_flag = False

    entities_sprites.add(player)
    for enemy in level.all_enemies:
        entities_sprites.add(enemy)

    inventory = Inventory(SCREEN, player)
    item_use_hud = HUDChoose(SCREEN)

    entities_sprites.add(inventory)
    entities_sprites.add(item_use_hud)

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
                if event.key == pygame.K_BACKQUOTE:
                    cmd = input().split()
                    if cmd[0] == 'drop':
                        thing = None
                        exec(cmd[1])
                        #level.dungeon.grid[player.pos[0]][player.pos[1]].contains.append(thing)
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
                        item = level.dungeon.grid[player.pos[0]][player.pos[1]].contains.pop(-1)
                        player.pick_up(item)
                        item.kill()
                        moved = True
                elif event.key == pygame.K_TAB:
                    inventory.toggle_bag()
                elif event.key == pygame.K_g:
                    if player.backpack:
                        item = player.backpack[-1]
                        item.drop(player, level.dungeon.grid)
                        entities_sprites.add(item)
                if moved:
                    if "ladder" in level.dungeon.grid[player.pos[0]][player.pos[1]].type:
                        if level.dungeon.grid[player.pos[0]][player.pos[1]].type == "ladder_down":
                            if level.num == len(levels):  # if it is the last level currently
                                levels.append(Level(multiplier, chance_for_door, level.num + 1, block_size))
                                player.score += 80
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
                        for line in level.dungeon.grid:
                            for cell in line:
                                entities_sprites.add(cell)
                        entities_sprites.add(inventory)
                        camera = Camera(player, level, SCREEN)
                        camera.move_to(*player.pos)

                        player.grid = level.dungeon.grid
                        player.pos = level.start_pos
                    print(entities_sprites)
                    if level.dungeon.grid[player.pos[0]][player.pos[1]].type != 'door':
                        if level.dungeon.grid[player.pos[0]][player.pos[1]].type == 'earth':
                            pygame.mixer.Sound.play(dig_sound)
                            level.dungeon.grid[player.pos[0]][player.pos[1]] = level.dungeon.grid[player.pos[0]][
                                player.pos[1]].change_tile(FloorTile)
                            '''camera.update_level(level)'''
                            entities_sprites.add(level.dungeon.grid[player.pos[0]][player.pos[1]])
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
                if throwing_flag:
                    throwing_flag = False
                    x = (mouse_pos[0] + camera.tl_x) // block_size
                    y = (mouse_pos[1] + camera.tl_y) // block_size
                    if not item_use_hud.item.throw(level, level.all_enemies, player, level.dungeon.grid[x][y]):
                        print('you cant throw it there', x, y)
                    else:
                        camera.move_to(*player.pos)
                        for enemy in level.all_enemies:
                            enemy.turn(level.dungeon.grid, level.dungeon.grid[player.pos[0]][player.pos[1]], player,
                                       level.maze, block_size, level.all_enemies)

                elif item_use_hud.opened:
                    item_use_hud.close()
                    if item_use_hud.x < mouse_pos[0] < item_use_hud.rect.width + item_use_hud.x and item_use_hud.y -48 < mouse_pos[1] < item_use_hud.rect.height + item_use_hud.y - 48:
                        y = mouse_pos[1] - item_use_hud.y + 48
                        
                        if y <= 31:
                            if item_use_hud.item.use(level, level.all_enemies, player, camera):
                                player.backpack.remove(item_use_hud.item)
                        elif y <= 63:
                            item_use_hud.item.drop(player, level.dungeon.grid)
                        elif y <= 95:
                            print('throw')
                            inventory.close_bag()
                            throwing_flag = True
                elif inventory.opened:
                    x = inventory.rect.x + 6
                    y = inventory.rect.y + 26
                    if 0 < mouse_pos[0] - x < inventory.rect.width - 12 and 0 < mouse_pos[1] - y < inventory.rect.height - 50:
                        cell_x = (mouse_pos[0] - x) // 40
                        cell_y = (mouse_pos[1] - y) // 40
                        bag = inventory.backpack if inventory.current_bag == -1 else inventory.bags[inventory.current_bag]
                        item = bag.get_or_none((cell_y - 1) * 5 + cell_x)
                        if item is not None:
                            item_use_hud.open(mouse_pos, item)

                else:
                    current_x, current_y = camera.cx, camera.cy

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if not inventory.opened or throwing_flag:
                    if dragging == 1:
                        running = True
                        camera.move_to(*camera.get_cell(*mouse_pos))
                    dragging = 0

            elif pygame.mouse.get_pressed()[0]:
                if not inventory.opened or throwing_flag:
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
            game_over()
            return


if __name__ == "__main__":
    while True:
        game_intro()

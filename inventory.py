import pygame
from constants import FONT, BUTTONS_FONT, LAYER_HUD


class Inventory(pygame.sprite.Sprite):
    def __init__(self, display:pygame.Surface, player) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.display = display
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self._layer = LAYER_HUD
        self.player = player
        self.backpack = player.backpack
        self.bags = player.bags
        self.current_bag = -1  # -1 is backpack and other is indexes of `bags`
        self.opened = False
    
    def update(self):
        if not self.opened:
            return
        bag = self.backpack if self.current_bag == -1 else self.bags[self.current_bag]
        self.image.fill((60, 60, 60))
        pygame.draw.rect(self.image, (100, 100, 100), pygame.Rect(0, 0, self.rect.width, self.rect.height), 5)
        for i in range(5):
            if i == 0:
                color = (120, 120, 120)
            else:
                color = (90, 90, 90)
            for j in range(5):
                rct = pygame.Rect(6 + j * 40, 26 + i * 40, 38, 38)
                pygame.draw.rect(self.image, color, rct)
                if bag.capacity == 19 and i == 1 and j == 0:
                    pass
                elif i >= 1:
                    item = bag.get_or_none((i-1)*5+j)
                    if item is not None:
                        self.render_cell(item, rct)
                elif i == 0:
                    if j == 0:
                        self.render_cell(self.player.weapon, rct) if self.player.weapon is not None else None
                    elif j == 1:
                        self.render_cell(self.player.armor, rct) if self.player.armor is not None else None
    
    def render_cell(self, item, rct):
        item.rect.center = rct.center
        self.image.blit(item.image, item.rect)
        if item.quantity > 1:
            FONT.render_to(self.image, rct, str(item.quantity), (0, 0, 0))
    
    def open_bag(self):
        self.image = pygame.Surface((210, 250))
        self.rect = self.image.get_rect()
        self.rect.center = (self.display.get_width() // 2, self.display.get_height() // 2)
        self.update()
        self.opened = True
    
    def close_bag(self):
        self.image = pygame.Surface((0, 0))
        self.opened = False

    def toggle_bag(self):
        if self.opened:
            self.close_bag()
        else:
            self.open_bag()


class HUDChoose(pygame.sprite.Sprite):
    def __init__(self, display: pygame.Surface) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.display = display
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self._layer = 5
        self.opened = False
        self.item = None
        self.x = -1
        self.y = -1

    def update(self):
        if not self.opened:
            return
        self.image.fill((60, 60, 60))

        pygame.draw.rect(self.image, (221, 161, 94), pygame.Rect(0, 1, self.rect.width, 30))
        pygame.draw.rect(self.image, (100, 100, 100), pygame.Rect(0, 1, self.rect.width, 30), 1)
        BUTTONS_FONT.render_to(self.image, pygame.Rect(13, 11, self.rect.width, 30), 'use', (0, 0, 0))

        pygame.draw.rect(self.image, (221, 161, 94), pygame.Rect(0, 33, self.rect.width, 30))
        pygame.draw.rect(self.image, (100, 100, 100), pygame.Rect(0, 33, self.rect.width, 30), 1)
        BUTTONS_FONT.render_to(self.image, pygame.Rect(8, 43, self.rect.width, 30), 'drop', (0, 0, 0))

        pygame.draw.rect(self.image, (221, 161, 94), pygame.Rect(0, 65, self.rect.width, 30))
        pygame.draw.rect(self.image, (100, 100, 100), pygame.Rect(0, 65, self.rect.width, 30), 1)
        BUTTONS_FONT.render_to(self.image, pygame.Rect(5, 75, self.rect.width, 30), 'throw', (0, 0, 0))

        pygame.draw.rect(self.image, (70, 70, 70), pygame.Rect(0, 0, self.rect.width, self.rect.height), 2)

    def open(self, pos, item):
        self.x = pos[0] + 40
        self.y = pos[1]
        self.item = item
        self.image = pygame.Surface((50, 96))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.update()
        self.opened = True

    def close(self):
        self.image = pygame.Surface((0, 0))
        self.opened = False

        
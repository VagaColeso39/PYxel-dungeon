import pygame
from constants_original import FONT

class Inventory(pygame.sprite.Sprite):
    def __init__(self, display:pygame.Surface, player) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.display = display
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self._layer = 2
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
                        pass  # FIXME
    
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
        
        
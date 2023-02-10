import pygame

class Inventory(pygame.sprite.Sprite):
    def __init__(self, display:pygame.Surface, player) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(210, 250)
        self.rect = self.image.get_rect()
        self.rect.center = (display.get_width() // 2, display.get_height() // 2)
        self._layer = 2
        self.backpack = player.backpack
        self.bags = player.bags
        self.current_bag = -1  # -1 is backpack and other is indexes of `bags`
    
    def update(self):
        bag = self.backpack if self.current_bag == -1 else self.bags[self.current_bag]
        self.image.fill((60, 60, 60))
        pygame.draw.rect(self.image, (100, 100, 100), pygame.Rect(0, 0, self.rect.width, self.rect.height), 5)
        for i in range(5):
            if i == 0:
                color = (120, 120, 120)
            else:
                color = (90, 90, 90)
            for j in range(5):
                pygame.draw.rect(self.image, color, pygame.Rect(2 + j * 2, 22 + i * 2, 38, 38))
                if bag.capacity == 19 and i == 1 and j == 0:
                    pass
                elif i >= 1:
                    bag[(i-1)*5+j]  # TODO
        
        
        
import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp=10, dmg: tuple[int, int] = (0, 2), x: int = 0, y: int = 0, name: str = 'rat',
                 is_flying: bool = False):
        pygame.sprite.Sprite.__init__(self)
        self.hp = hp
        self.dmg = dmg
        self.name = name
        self.x = x
        self.y = y
        self.is_flying = is_flying

    def attack(self, other):
        pass

    def try_move(self, player, grid, x, y):
        if self.is_flying:
            if grid[x][y].type not in ['wall', 'earth']:
                return True
        else:
            if grid[x][y].type not in ['wall', 'earth', 'void']:
                return True
        return False

    def move_to(self, grid: list, x: int, y: int):
        if x > self.x:
            if self.try_move(grid, self.x + 1, self.y):
                self.x += 1
        elif x < self.x:
            if self.try_move(grid, self.x - 1, self.y):
                self.x -= 1
        elif y > self.y:
            if self.try_move(grid, self.x, self.y + 1):
                self.y += 1
        elif y < self.y:
            if self.try_move(grid, self.x, self.y - 1):
                self.y -= 1

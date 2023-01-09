from typing import Literal

class Tile:
    def __init__(self, x, y, type: Literal['floor', 'wall', 'void', 'door']):
        self.x = x
        self.y = y
        self.type = type
        self.can_step = True
        self.gases = True  # like poisonous gas or freezing
        self.fire = True
        self.can_burn = True  # i can't think of anything better


class FloorTile(Tile):
    def __init__(self, x, y, inventory=[], modificator=None, trap=None):
        super().__init__(x, y, type='floor')
        self.inventory = inventory
        self.modificator = modificator  # can be high_grass, low_grass, coals, wooden_floor, water, trap, ladder_up, ladder_down
        if modificator == 'trap':
            self.trap = trap
        self.effects = []
    
    def add_effect(self, effect):
        if effect not in self.effects:
            self.effects.append(effect)
        else:
            raise ValueError('This effect already exists')
    
    def del_effect(self, effect):
        self.effects.pop(self.effects.index(effect))
    
    def step(self, reason):
        if reason.__class__.__name__ == 'Item':
            self.inventory.append(reason)
        if self.modificator == 'trap':
            self.trap.activate()
        if self.modificator == 'high_grass':
            self.modificator = 'low_grass'
            self.grass_step()
    
    def grass_step(self):
        pass


class WallTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, type='wall')
        self.can_step = False
        self.gases = False
        self.fire = False


class VoidTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, type='void')
        self.fire = False
        self.effects = []
    
    def add_effect(self, effect):
        if effect not in self.efects:
            self.effects.append(effect)
        else:
            raise ValueError('This effect already exists')
    
    def del_effect(self, effect):
        self.effects.pop(self.effects.index(effect))
    
    def step(self, reason):
        pass  # i need level logic to make it


class DoorTile(Tile):
    def __init__(self, x, y, modificator=None):
        super().__init__(x, y, type='door')
        self.modificator = modificator  # can be hided, locked or special (to burn it)
        self.opened = False
        self.gases &= self.opened  # link to `opened` because they must have same values
        self.effects = []
    
    def add_effect(self, effect):
        if effect not in self.efects:
            self.effects.append(effect)
        else:
            raise ValueError('This effect already exists')
    
    def del_effect(self, effect):
        self.effects.pop(self.effects.index(effect))
    
    def step(self, reason):
        self.opened = True
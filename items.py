import json
import random

import pygame


class Item:
    def __init__(self, name: str, quantity: int = 1, stackable: bool = False, level: int = 0, cursed: bool = False,
                 cursed_known: bool = False, known: bool = False, essential: bool = False, drop_cost: int = 20):
        self.source = pygame.image.load(f'sprites/{name}.bmp')
        self.source.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.source, (20, 20))
        self.rect = self.image.get_rect()
        self.name = name
        self.drop_cost = drop_cost  # rarity
        self.quantity = quantity
        self.stackable = stackable
        self.level = level
        self.cursed = cursed
        self.cursed_known = cursed_known
        self.known = known  # is item indentified
        self.essential = essential  # don't know why it is here, but in original code this exist
        self.effect = None

    def __str__(self) -> str:
        return f'{self.name} x{self.quantity}'

    def __repr__(self) -> str:
        return self.__str__()

    def check_similarity(self, other) -> bool:
        return isinstance(other, self.__class__) and self.level == other.level

    def __eq__(self, other) -> bool:
        return self.check_similarity(other)

    def __ne__(self, other) -> bool:
        return not self.check_similarity(other)

    def can_stack(self, other) -> bool:
        return self.stackable and self == other

    def stack(self, other):
        if self.can_stack(other):
            self.quantity += other.quantity
            other.quantity = 0
        return self

    def is_indentified(self):
        return self.known

    def is_cursed(self):
        if self.cursed_known or self.known:
            return self.cursed

    def use(self, level: object = None, enemies: list = None, player: object = None, camera: object = None) -> None:
        print('try to use')
        if self.effect is not None:
            print('used')
            if self.effect == 'blinding':
                for enemy in enemies:
                    if enemy.visible:
                        enemy.blind(10)
            elif self.effect == 'teleport':  # teleport use bug (second time use) ?
                room = random.choice(level.dungeon.rooms)
                x = random.randint(room.x + 1, room.x + room.width - 1)
                y = random.randint(room.y + 1, room.y + room.height - 1)
                player.pos = [x, y]
                camera.move_to(*player.pos)
            elif self.effect == 'map_explore':
                for cell in level.dungeon.grid:
                    cell.explored = True
            elif self.effect == 'healing':
                player.hp = min(player.max_hp, player.hp + player.max_hp // 2)
            elif self.effect == 'fire':
                player.effects.append((10, 'fire'))  # add fire
            return True
        return False

    def throw(self, level, enemies, player, tile: object) -> bool:
        if player.is_visible(level.dungeon.grid, tile):
            if type(self) == UtilItem and self.throwable:
                dmg = random.randint(*self.damage)
            elif type(self) == WeaponItem:
                dmg = max(1, random.randint(*self.damage) // 3)
            else:
                dmg = 1
            for enemy in enemies:
                if enemy.x == tile.x and enemy.y == tile.y:
                    enemy.hit_self(player, dmg, enemies)
                    break
            level.dungeon.grid[tile.x][tile.y].contains.append(self)
            player.backpack.remove(self)
            return True
        return False

    def drop(self, player, grid: list):
        grid[player.pos[0]][player.pos[1]].contains.append(self)
        player.backpack.remove(self)


class WeaponItem(Item):
    def __init__(self, name: str, quantity: int = 1, level: int = 0, cursed: bool = False, cursed_known: bool = False,
                 known: bool = False, essential: bool = False, drop_cost: int = 20, damage: tuple[int, int] = (4, 8),
                 is_double_hand: bool = False, hit_range: int = 1, is_ranged: bool = False):
        super().__init__(name, quantity, False, level, cursed, cursed_known, known, essential, drop_cost)
        self.damage = damage
        self.is_double_hand = is_double_hand
        self.hit_range = hit_range
        self.is_ranged = is_ranged


class ScrollItem(Item):
    def __init__(self, name: str, quantity: int = 1, level: int = 0, cursed: bool = False, cursed_known: bool = False,
                 known: bool = False, essential: bool = False, drop_cost: int = 20, effect: str = ''):
        super().__init__(name, quantity, False, level, cursed, cursed_known, known, essential, drop_cost)
        self.effect = effect


class PotionItem(Item):
    def __init__(self, name: str, quantity: int = 1, level: int = 0, cursed: bool = False, cursed_known: bool = False,
                 known: bool = False, essential: bool = False, drop_cost: int = 20, effect: str = ''):
        super().__init__(name, quantity, False, level, cursed, cursed_known, known, essential, drop_cost)
        self.effect = effect


class ArmorItem(Item):
    def __init__(self, name: str, quantity: int = 1, level: int = 0, cursed: bool = False, cursed_known: bool = False,
                 known: bool = False, essential: bool = False, drop_cost: int = 20, defence: tuple[int, int] = (0, 2)):
        super().__init__(name, quantity, False, level, cursed, cursed_known, known, essential, drop_cost)
        self.defence = defence


class UtilItem(Item):
    def __init__(self, name: str, quantity: int = 1, level: int = 0, cursed: bool = False, cursed_known: bool = False,
                 known: bool = False, essential: bool = False, drop_cost: int = 20, throwable: bool = False, damage: tuple[int, int] = (4, 8)):
        super().__init__(name, quantity, True, level, cursed, cursed_known, known, essential, drop_cost)
        self.throwable = throwable
        self.damage = damage


class ItemsInitialization:
    def __init__(self):
        with open('items/items_params.json') as data:
            self.groups_of_items = json.load(data)
        self.weapons = self.groups_of_items['weapons']
        self.armor = self.groups_of_items['armor']
        self.potions = self.groups_of_items['potions']
        self.scrolls = self.groups_of_items['scrolls']
        self.utils = self.groups_of_items['utils']


items_storage = ItemsInitialization()


def item_generator(drop_cost: int, categories: tuple = ('weapons', 'armor', 'potions', 'scrolls', 'utils')):
    category = random.choices(categories, cum_weights=[1, 2, 4, 6, 8], k=1)[0]
    items_to_choose = tuple(
        filter(lambda x: x[1]['drop_cost'] <= drop_cost, items_storage.groups_of_items[category].items()))
    if items_to_choose:
        item = random.choices(items_to_choose, weights=[item[1]['drop_cost'] for item in items_to_choose], k=1)
    else:
        print('failed to choose item, restarting function')
        return item_generator(drop_cost, categories)
    if random.random() <= item[0][1]['drop_chance']:
        if category == 'weapons':
            return_item = WeaponItem(item[0][0], 1, 1, False, True, False, False, item[0][1]['drop_cost'],
                                     item[0][1]['damage'], item[0][1]['is_double_handed'], item[0][1]['range'],
                                     item[0][1]['is_ranged'])
        elif category == 'armor':
            return_item = ArmorItem(item[0][0], 1, 1, False, True, False, False, item[0][1]['drop_cost'],
                                     item[0][1]['defence'])
        elif category == 'potions':
            return_item = PotionItem(item[0][0], 1, 1, False, True, False, False, item[0][1]['drop_cost'],
                                     item[0][1]['effect'])

        elif category == 'scrolls':
            return_item = ScrollItem(item[0][0], 1, 1, False, True, False, False, item[0][1]['drop_cost'],
                                     item[0][1]['effect'])
        elif category == 'utils':
            return_item = UtilItem(item[0][0], 1, 1, False, True, False, False, item[0][1]['drop_cost'],
                                   item[0][1]['throwable'], item[0][1]['damage'])

        return return_item
    else:
        return False


def item_giver(name: str, category: str):
    item = tuple(filter(lambda x: x[0] == name, items_storage.groups_of_items[category].items()))
    if category == 'weapons':
        return_item = WeaponItem(item[0][0], 1, 1, False, True, False, False, item[0][1]['drop_cost'],
                                 item[0][1]['damage'], item[0][1]['is_double_handed'], item[0][1]['range'],
                                 item[0][1]['is_ranged'])
    elif category == 'armor':
        return_item = ArmorItem(item[0][0], 1, 1, False, True, False, False, item[0][1]['drop_cost'],
                                item[0][1]['defence'])
    elif category == 'potions':
        return_item = PotionItem(item[0][0], 1, 1, False, True, False, False, item[0][1]['drop_cost'],
                                 item[0][1]['effect'])

    elif category == 'scrolls':
        return_item = ScrollItem(item[0][0], 1, 1, False, True, False, False, item[0][1]['drop_cost'],
                                 item[0][1]['effect'])
    elif category == 'utils':
        return_item = UtilItem(item[0][0], 1, 1, False, True, False, False, item[0][1]['drop_cost'],
                               item[0][1]['throwable'], item[0][1]['damage'])
    return return_item

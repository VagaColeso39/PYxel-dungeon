import json
import random

class Item:
    def __init__(self, name: str, quantity: int = 1, stackable: bool = False, level: int = 0, cursed: bool = False,
                 cursed_known: bool = False, known: bool = False, essential: bool = False, drop_cost: int = 20):

        self.name = name
        self.drop_cost = drop_cost  # rarity
        self.quantity = quantity
        self.stackable = stackable
        self.level = level
        self.cursed = cursed
        self.cursed_known = cursed_known
        self.known = known  # is item indentified
        self.essential = essential  # don't know why it is here, but in original code this exist

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
    category = random.choice(categories)
    items_to_choose = tuple(filter(lambda x: x[1]['drop_cost'] <= drop_cost, items_storage.groups_of_items[category].items()))
    if items_to_choose:
        item = random.choices(items_to_choose, weights=[item[1]['drop_cost'] for item in items_to_choose], k=1)
    else:
        print('failed to choose item, restart function')
        return item_generator(drop_cost, categories)
    if random.random() <= item[0][1]['drop_chance']:
        return item
    else:
        return False

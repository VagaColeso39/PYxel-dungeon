from items import Item, ScrollItem, PotionItem


class Backpack:
    def __init__(self, hero, capacity=20, allowed_items=(Item,)):
        self.owner = hero
        self.items = []
        self.capacity = capacity
        self.allowed_items = allowed_items  # to allow item create tuple with it's class or parent class
        self.items_iteration = 0  # for iterations

    def __str__(self) -> str:
        return f'Backpack: {self.items}'

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self):
        return self

    def __next__(self):
        if self.items_iteration < len(self.items):
            item = self.items[self.items_iteration]
            self.items_iteration += 1
            return item
        self.items_iteration = 0
        raise StopIteration

    def __len__(self):
        return len(self.items)

    def __getitem__(self, item):
        return self.items[item]

    def remove(self, other):
        self.items.remove(other)

    def can_hold(self, item):
        if isinstance(item, Backpack) or (len(self.items) < self.capacity and isinstance(item, self.allowed_items)):
            return True
        elif item.stackable:
            for i in self.items:
                if i == item:
                    return True
        return False

    def put_to_others(self, item):
        if self.__class__.__name__ != 'Backpack':
            return False
        for i in self.owner.bags:
            if i.can_hold(item):
                i.pick_up(item)
                return True
        return False

    def pick_up(self, item):
        if not self.put_to_others(item) and self.can_hold(item):
            if item.stackable and self.get_item(item) is not None:
                self.get_item(item).stack(item)
            else:
                self.items.append(item)
            return True
        return False

    def get_item(self, item):
        for i in self.items:
            if i == item:
                return i
    
    def get_or_none(self, index):
        try:
            return self[index]
        except IndexError:
            return None

    def set_quantity(self, item, quantity):
        self.get_item(item).quantity = quantity

class ScrollHolder(Backpack):
    def __init__(self, hero):
        super().__init__(hero, 19, (ScrollItem,))

class PotionHolder(Backpack):
    def __init__(self, hero):
        super().__init__(hero, 19, (PotionItem,))
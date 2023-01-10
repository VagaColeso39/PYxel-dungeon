from items import Item

class Backpack:
    def __init__(self, hero, capacity=20, allowed_items=(Item, )):
        self.owner = hero
        self.items = []
        self.capacity = capacity
        self.allowed_items = allowed_items  # to allow item create tuple with it's class or parent class
    
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
            if item.stackable:
                self.get_item(item).stack(item)
            else:
                self.items.append(item)
            return True
        return False

    def get_item(self, item):
        return self.items[self.items.index(item)]
    
    def set_quantity(self, item, quantity):
        self.get_item(item).quantity = quantity
        
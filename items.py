class Item:
    def __init__(self, name:str, quantity:int=1, stackable:bool=False, level:int=0, cursed:bool=False, cursed_known:bool=False, known:bool=False, unique:bool=False):
        self.name = name
        self.quantity = quantity
        self.stackable = stackable
        self.level = level
        self.cursed = cursed
        self.cursed_known = cursed_known
        self.known = known  # is item indentified
        self.unique = unique  # don't know why it is here, but in original code this exist
        self.actions = []
    
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
class Player:
    def __init__(self):
        self.inventory = []
        self.max_hp = 20
        self.hp = 20
        self.xp = 0
        self.level = 1
        self.next_level = 10
        self.strength = 10
        self.gold = 0
        self.accuracy = 10
        self.evasion = 5
        self.turns_to_hunger = 100
        self.effects = []
        self.turns_to_regeneration = 10
        self.turns_to_regeneration = 10
        self.speed_multipliers = []
        self.walking_speed_multipliers = []
        self.attack_speed_multipliers = []
    
    def hit_hero(self, damage):
        self.hp -= damage
    
    def attack_hero(self, damage):
        ...

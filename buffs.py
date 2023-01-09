import random


class Effect:
    def __init__(self, target, duration=0, active=True):
        self.name = 'Effect'
        self.duration = duration
        self.active = active
        self.target = target

    def end(self):
        self.duration -= 1
        if self.duration <= 0:
            self.target.del_buff(self.name)

    def next_move(self):
        self.end()

class ActiveEffect(Effect):
    def __init__(self, target, duration=0):
        super().__init__(target, duration)
    
    def next_move(self):
        ...
        self.end()

class PassiveEffect(Effect):
    def __init__(self, target, duration=0):
        super().__init__(target, duration, active=False)
        self.speed = 1
        self.walking_speed = 1
        self.attack_speed = 1
        self.target.speed_multipliers.append(self.speed)
        self.target.walking_speed_multipliers.append(self.walking_speed)
        self.target.attack_speed_multipliers.append(self.attack_speed)
    
    def end(self):
        self.duration -= 1
        if self.duration <= 0:
            self.target.speed_multipliers.pop(self.target.speed_multipliers.index(self.speed))
            self.target.walking_speed_multipliers.pop(self.target.walking_speed_multipliers.index(self.walking_speed))
            self.target.attack_speed_multipliers.pop(self.target.attack_speed_multipliers.index(self.attack_speed))
            self.target.del_buff(self.name)



class Burning(ActiveEffect):
    def __init__(self, target, duration=6):
        super().__init__(target, duration)

    def next_turn(self):
        self.target.hit(random.randint(self.target.max_hp//15, self.target.max_hp//6))
        self.end()
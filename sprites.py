import random
import pygame
import dungeonGenerator


class Player(pygame.sprite.Sprite):
    def __init__(self, hp: int = None, weapon: dict = None, armor=None, rings=None, artifacts=None):
        pygame.sprite.Sprite.__init__(self)

        if artifacts is None:
            artifacts = []
        if rings is None:
            rings = []
        if armor is None:
            armor = {}
        if weapon is None:
            weapon = {}
        if hp is None:
            hp = 50

        self.hp = hp
        self.inventory = []
        self.effects = []
        self.weapon = weapon
        self.armor = armor
        self.rings = rings
        self.artifacts = artifacts


import pygame
import random
import dungeonGenerator


class Level:
    def __init__(self):
        self.multiplier = random.randint(100, 150)
        self.level_width = int(8 * self.multiplier / 10)
        self.level_height = int(8 * self.multiplier / 10)

        self.room_amount = int(self.multiplier / 10)

        self.dungeon = dungeonGenerator.dungeonGenerator(self.level_height, self.level_width)
        creator_counter = 0
        while creator_counter < self.room_amount:
            if self.dungeon.placeRandomRooms(5, 9, 1, 4, 1):
                creator_counter += 1

        self.dungeon.generateCorridors('l')
        self.dungeon.connectAllRooms(50)
        self.dungeon.pruneDeadends(200)

        # join unconnected areas
        unconnected = self.dungeon.findUnconnectedAreas()
        self.dungeon.joinUnconnectedAreas(unconnected)

import pygame
import random
import dungeonGenerator


class Level:
    def room_creator(self):
        creator_counter = 0
        error_counter = 0
        while creator_counter < self.room_amount:
            if self.dungeon.placeRandomRooms(4, 9, 1, 1, 1):
                creator_counter += 1
                error_counter = 0
            else:
                error_counter += 1
            if error_counter >= 100000:
                print(f"Cant generate room! {creator_counter} from {self.room_amount} of rooms is generated")
                self.dungeon = dungeonGenerator.dungeonGenerator(self.level_height, self.level_width)
                self.room_creator()

    def __init__(self, multiplier, chance_for_door):
        self.multiplier = multiplier
        self.chance_for_door = chance_for_door
        self.level_width = int(6.4 * self.multiplier / 10)
        self.level_height = int(6.4 * self.multiplier / 10)

        self.room_amount = int(2.2 * self.multiplier / 10)

        self.dungeon = dungeonGenerator.dungeonGenerator(self.level_height, self.level_width)
        self.room_creator()

        self.dungeon.rooms[-1].room_type = "treasure"
        self.closed_rooms_amount = random.randint(1, 2)
        for i in range(1, self.closed_rooms_amount + 1):
            self.dungeon.rooms[-1 - i].room_type = "closed"
        self.dungeon.connectAllRooms(chance_for_door)
        unconnected_areas = self.dungeon.findUnconnectedAreas()
        self.dungeon.joinUnconnectedAreas(unconnected_areas)
        self.dungeon.connectAllRooms(chance_for_door)
        self.dungeon.placeWalls()

        # self.dungeon.constructNavGraph()
        # for i, first_room in enumerate(self.dungeon.rooms):
        #     for second_room in self.dungeon.rooms[i+1:]:
        #         path_len = len(self.dungeon.findPath(first_room.x, first_room.y, second_room.x, second_room.y))
        #         if path_len >= self.level_width // 4:
        #             do something. Teleport mechanic?
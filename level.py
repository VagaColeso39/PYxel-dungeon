import dungeonGenerator
import random


class Level:
    def room_creator(self):
        creator_counter = 0
        error_counter = 0
        while creator_counter < self.room_amount:
            if self.dungeon.placeRandomRooms(4, 9, 1, 3, 1):
                creator_counter += 1
                error_counter = 0
            else:
                error_counter += 1
            if error_counter >= 100000:
                print(f"Cant generate room! {creator_counter} from {self.room_amount} of rooms is generated")
                self.room_amount -= 1
                self.dungeon = dungeonGenerator.dungeonGenerator(self.level_height, self.level_width, self.block_size)
                self.room_creator()

    def __init__(self, multiplier, chance_for_door, num, block_size, mod=None, start_pos: list[int, int] = None):
        self.multiplier = multiplier
        self.chance_for_door = chance_for_door
        self.num = num
        self.mod = mod
        self.start_pos = start_pos
        self.board = None
        self.block_size = block_size

        self.level_width = int(7.4 * self.multiplier / 10)
        self.level_height = int(7.4 * self.multiplier / 10)
        self.room_amount = int(2 * self.multiplier / 10)

        self.dungeon = dungeonGenerator.dungeonGenerator(self.level_height, self.level_width, block_size)
        self.room_creator()

        self.dungeon.rooms[-1].room_type = "treasure"
        self.closed_rooms_amount = random.randint(1, 2)
        for i in range(1, self.closed_rooms_amount + 1):
            self.dungeon.rooms[-1 - i].room_type = "closed"

        self.dungeon.placeWalls()

        self.start_room = self.dungeon.rooms[0]
        self.start_pos = [self.start_room.x + self.start_room.width // 2, self.start_room.y + self.start_room.height // 2]

    def next_move(self, action):
        pass

    @property
    def maze(self):
        maze = []
        for row in range(self.level_height):
            line = []
            for cell in range(self.level_width):
                if self.dungeon.grid[row][cell].type != 'wall' and (self.dungeon.grid[row][cell].explored or self.dungeon.grid[row][cell].visible):
                    line.append(1)
                else:
                    line.append(0)
            maze.append(line)
        return maze

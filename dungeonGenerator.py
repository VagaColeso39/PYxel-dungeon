##################################################################
#                                                                #
# Procedural Dungeon Generator                                   #
#                                                                #
# By Jay (Battery)                                               #
#                                                                #
# https://whatjaysaid.wordpress.com/                             #
# for how use it got to:                                         #
# https://whatjaysaid.wordpress.com/2016/01/15/1228              #
#                                                                #
# Feel free to use this as you wish, but please keep this header #
#                                                                #
##################################################################
import random
from random import randint, randrange

from tiles import WallTile, FloorTile, DoorTile, EarthTile


class dungeonRoom:
    def __init__(self, x, y, width, height, room_type="usual"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.room_type = room_type


class dungeonGenerator:
    def __init__(self, height, width, block_size):

        self.height = height
        self.width = width
        self.rooms = []
        self.doors = []
        self.corridors = []
        self.deadends = []
        self.block_size = block_size
        self.grid = [[EarthTile(self, x, y) for y in range(self.height)] for x in range(self.width)]

        self.graph = {}
    def __iter__(self):
        for xi in range(self.width):
            for yi in range(self.height):
                yield xi, yi, self.grid[xi][yi]

    def findNeighbours(self, x, y):
        xi = (0, -1, 1) if 0 < x < self.width - 1 else ((0, -1) if x > 0 else (0, 1))
        yi = (0, -1, 1) if 0 < y < self.height - 1 else ((0, -1) if y > 0 else (0, 1))
        for a in xi:
            for b in yi:
                if a == b == 0:
                    continue
                yield (x + a, y + b)

    def quadFits(self, sx, sy, rx, ry, margin):
        """
        looks to see if a quad shape will fit in the grid without colliding with any other tiles
        used by placeRoom() and placeRandomRooms()
        
        Args:
            sx and sy: integer, the bottom left coords of the quad to check
            rx and ry: integer, the width and height of the quad, where rx > sx and ry > sy
            margin: integer, the space in grid cells (ie, 0 = no cells, 1 = 1 cell, 2 = 2 cells) to be away from other tiles on the grid
            
        returns:
            True if the quad fits
        """

        sx -= margin
        sy -= margin
        rx += margin * 2
        ry += margin * 2
        if sx + rx < self.width and sy + ry < self.height and sx >= 0 and sy >= 0:
            for x in range(rx):
                for y in range(ry):
                    if self.grid[sx + x][sy + y].type != 'earth':
                        return False
            return True
        return False

    def placeRoom(self, startX, startY, roomWidth, roomHeight, ignoreOverlap=False):
        """
        place a defined quad within the grid and add it to self.rooms
        
        Args:
            x and y: integer, starting corner of the room, grid indicies
            roomWdith and roomHeight: integer, height and width of the room where roomWidth > x and roomHeight > y
            ignoreOverlap: boolean, if true the room will be placed irregardless of if it overlaps with any other tile in the grid
                note, if true then it is up to you to ensure the room is within the bounds of the grid
        
        Returns:
            True if the room was placed
        """

        if self.quadFits(startX, startY, roomWidth, roomHeight, 0) or ignoreOverlap:
            for x in range(roomWidth):
                for y in range(roomHeight):
                    self.grid[startX + x][startY + y] = FloorTile(self, startX + x, startY + y)
            self.rooms.append(dungeonRoom(startX, startY, roomWidth, roomHeight))
            return True

    def placeRandomRooms(self, minRoomSize: object, maxRoomSize: object, roomStep: object = 1, margin: object = 1,
                         attempts: object = 500) -> object:
        """ 
        randomly places quads in the grid
        takes a brute force approach: randomly a generate quad in a random place -> check if fits -> reject if not
        Populates self.rooms
        
        Args:
            minRoomSize: integer, smallest size of the quad
            maxRoomSize: integer, largest the quad can be
            roomStep: integer, the amount the room size can grow by, so to get rooms of odd or even numbered sizes set roomSize to 2 and the minSize to odd/even number accordingly
            margin: integer, space in grid cells the room needs to be away from other tiles
            attempts: the amount of tries to place rooms, larger values will give denser room placements, but slower generation times
            
        Returns:
            none
        """
        room_created = False
        for attempt in range(attempts):
            roomWidth = randrange(minRoomSize, maxRoomSize, roomStep)
            roomHeight = randrange(minRoomSize, maxRoomSize, roomStep)
            startX = randint(0, self.width)
            startY = randint(0, self.height)
            if self.quadFits(startX, startY, roomWidth, roomHeight, margin):
                for x in range(roomWidth):
                    for y in range(roomHeight):
                        self.grid[startX + x][startY + y] = FloorTile(self, startX + x, startY + y)
                self.rooms.append(dungeonRoom(startX, startY, roomWidth, roomHeight))
                room_created = True
        if room_created:
            return True
        return False

    def placeDoors(self):
        for room in self.rooms:
            if room.room_type == 'closed':
                if random.randint(0, 1):
                    y_choose = range(room.y, room.y + room.height)
                    y = random.choice(y_choose)
                    x = random.choice((room.x - 1, room.x + room.width))
                    self.grid[x][y] = DoorTile(self, x, y, 'locked')
                else:
                    x_choose = range(room.x, room.x + room.width)
                    x = random.choice(x_choose)
                    y = random.choice((room.y - 1, room.y + room.height))
                    self.grid[x][y] = DoorTile(self, x, y, 'locked')
            else:
                y_choose = range(room.y, room.y + room.height)
                y = random.choice(y_choose)
                x = random.choice((room.x - 1, room.x + room.width))
                self.grid[x][y] = DoorTile(self, x, y)

                x_choose = range(room.x, room.x + room.width)
                x = random.choice(x_choose)
                y = random.choice((room.y - 1, room.y + room.height))
                self.grid[x][y] = DoorTile(self, x, y)

    def placeWalls(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].type not in ['floor', 'ladder_up', 'ladder_down']:
                    for nx, ny in self.findNeighbours(x, y):
                        if self.grid[nx][ny].type in ['floor', 'ladder_up', 'ladder_down']:
                            self.grid[x][y] = WallTile(self, y, x)
                            break

        self.placeDoors()

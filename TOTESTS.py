from pprint import pprint
from util import ballistica, bresenham

class TestTile:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y

a, b = (0, 1), (4, 4)

lst = [[TestTile('floor', i, j) for j in range(5)] for i in range(5)]
lst[-1][-1].type = 'earth'
lst2 = [[0 for j in range(5)] for i in range(5)]
for x, y in bresenham(*a, *b):
    lst2[x][y]=1

print(ballistica(a, b, ['earth'], lst))
pprint(lst2)
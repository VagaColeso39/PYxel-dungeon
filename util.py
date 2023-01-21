import math

def manhattan(a, b):
    return sum(abs(val1-val2)**2 for val1, val2 in zip(a,b))

def pifagor(a, b):
    return math.floor(math.sqrt(sum(abs(val1-val2)**2 for val1, val2 in zip(a,b))))

def ballistica(a, b, stop_types, grid):
    last = None
    for i in bresenham(a[0], a[1], b[0], b[1]):
        if grid[i[0]][i[1]].type in stop_types:
            return last
        last = i

def bresenham(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2*dy - dx
    y = 0

    for x in range(dx + 1):
        yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy
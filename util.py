import math

def manhattan(a, b):
    return sum(abs(val1-val2)**2 for val1, val2 in zip(a,b))

def pifagor(a, b):
    return math.floor(math.sqrt(sum(abs(val1-val2)**2 for val1, val2 in zip(a,b))))

def vision(a:tuple[int, int], b:tuple[int, int]) -> tuple[bool, tuple[int, int]]:
    ...
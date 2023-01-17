def manhattan(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

def vision(a:tuple[int, int], b:tuple[int, int]) -> tuple[bool, tuple[int, int]]:
    ...
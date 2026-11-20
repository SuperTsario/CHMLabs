from functools import lru_cache

def count_naive(a: int, b: int, c: int) -> int:
    count = 0
    for y in range(0, b):
        ay = 1
        for i in range(y):
            ay *= a
        if ay % b == c:
            count += 1
    return count

def count_fastpow(a: int, b: int, c: int) -> int:
    count = 0
    for y in range(0, b):
        if pow(a, y, b) == c:
            count += 1
    return count

def count_iter(a: int, b: int, c: int) -> int:
    count = 0
    r = 1
    for _ in range(b):
        if r == c:
            count += 1
        r = (r * a) % b
    return count

def disturbances(a: int, b: int, c: int) -> int:
    result = []
    d1 = ((a+1)%b, b, c)
    d2 = ((a-1)%b, b, c)
    d3 = (a, b, (c+1)%b)
    d4 = (a, b, (c-1)%b)
    

import time
from functions import count_fastpow as N
from disturbances import get_neighbors, calc_S, kappa_lab

def get_Y(b, k=500):
    return [ (i * (b - 1)) // (k - 1) for i in range(k) ]

def count_sp_naive(a, b, c):
    count = 0
    for y in get_Y(b):
        ay = 1
        for _ in range(y): 
            ay = (ay * a) % b
        if ay == c: count += 1
    return count

def count_sp_fastpow(a, b, c):
    return sum(1 for y in get_Y(b) if pow(a, y, b) == c)

def count_sp_iter(a, b, c):
    set_Y = set(get_Y(b))
    count = 0
    r = 1
    for y in range(b):
        if y in set_Y and r == c: 
            count += 1
        r = (r * a) % b
    return count

# Защита от зависаний (таймаут 3 секунды для теста)
def run_with_timeout(func, *args, timeout=3.0):
    t0 = time.perf_counter()
    res = func(*args)
    t1 = time.perf_counter()
    if t1 - t0 > timeout:
        return ">3s (не выполнять)"
    return f"{t1 - t0:.6f} s"

print("="*60)
print("8.3.1 Проверка совпадения (b <= 10^5)")
print("="*60)
test_cases = [(2, 1000, 1), (5, 5000, 2), (3, 100000, 1)]
for a, b, c in test_cases:
    v1 = count_sp_naive(a, b, c)
    v2 = count_sp_fastpow(a, b, c)
    v3 = count_sp_iter(a, b, c)
    print(f"a={a}, b={b}, c={c} -> naive={v1}, fastpow={v2}, iter={v3} | Совпало: {v1==v2==v3}")

print("\n" + "="*80)
print("8.3.2 Таблица времени (k=500)")
print("="*80)
b_values = [10**3, 10**5, 10**7, 10**9, 10**12, 10**15]
print(f"| {'b':>16} | {'count_sp_naive':>21} | {'count_sp_fastpow':>21} | {'count_sp_iter':>21} |")
print("-" * 89)
for b in b_values:
    if b > 10**5:
        res_naive = ">60s (не выполнять)"
    else:
        res_naive = run_with_timeout(count_sp_naive, 2, b, 1)
        
    res_fast = run_with_timeout(count_sp_fastpow, 2, b, 1)
    
    if b > 10**7:
        res_iter = ">60s (не выполнять)"
    else:
        res_iter = run_with_timeout(count_sp_iter, 2, b, 1)
        
    print(f"| {b:>16} | {res_naive:>21} | {res_fast:>21} | {res_iter:>21} |")

def calc_S_sp(a, b, c, a2, b2, c2, changed):
    n1, n2 = count_sp_fastpow(a, b, c), count_sp_fastpow(a2, b2, c2)
    if n1 == n2: return 0.0
    num = abs(n2 - n1) / max(n1, 1)
    p = a if changed == 'a' else b if changed == 'b' else c
    return num * max(abs(p), 1)

def kappa_lab_sp(a, b, c):
    return max([calc_S_sp(a, b, c, *x[:3], x[3]) for x in get_neighbors(a, b, c)] + [0.0])

print("="*80)
print("8.3.3 Вычисление kappa_lab для разреженной модели")
print("="*80)
print(f"| {'b':>15} | {'a':>3} | {'c':>3} | {'N_sp':>5} | {'kappa_lab':>15} |")
print("-" * 51)
for b in [10**6, 10**9, 10**12]:
    a, c = 2, 1
    n_sp = count_sp_fastpow(a, b, c)
    k = kappa_lab_sp(a, b, c)
    print(f"| {b:>15} | {a:>3} | {c:>3} | {n_sp:>5} | {k:>15.2f} |")
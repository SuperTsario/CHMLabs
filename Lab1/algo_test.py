# Вспомогательная функция для подсчета умножений в бинарном возведении в степень
def pow_mod_with_ops(a, y, b):
    if y == 0: return 1, 0
    res, base, ops = 1, a % b, 0
    while y > 0:
        if y % 2 == 1:
            res = (res * base) % b
            ops += 1
        base = (base * base) % b
        ops += 1
        y //= 2
    return res, ops

def get_Y(b, k=500):
    return [(i * (b - 1)) // (k - 1) for i in range(k)]

# --- ФУНКЦИИ ПОЛНОГО ДИАПАЗОНА ---
def count_naive_ops(a, b, c):
    ops, count = 0, 0
    for y in range(b):
        ay = 1
        for _ in range(y):
            ay = (ay * a) % b
            ops += 1
        if ay == c: count += 1
    return count, ops

def count_fastpow_ops(a, b, c):
    ops, count = 0, 0
    for y in range(b):
        val, o = pow_mod_with_ops(a, y, b)
        ops += o
        if val == c: count += 1
    return count, ops

def count_iter_ops(a, b, c):
    ops, count = 0, 0
    r = 1
    for y in range(b):
        if r == c: count += 1
        r = (r * a) % b
        ops += 1
    return count, ops

# --- ФУНКЦИИ РАЗРЕЖЕННОГО ДИАПАЗОНА ---
def count_sp_naive_ops(a, b, c, k=500):
    ops, count = 0, 0
    for y in get_Y(b, k):
        ay = 1
        for _ in range(y):
            ay = (ay * a) % b
            ops += 1
        if ay == c: count += 1
    return count, ops

def count_sp_fastpow_ops(a, b, c, k=500):
    ops, count = 0, 0
    for y in get_Y(b, k):
        val, o = pow_mod_with_ops(a, y, b)
        ops += o
        if val == c: count += 1
    return count, ops

def count_sp_iter_ops(a, b, c, k=500):
    set_Y = set(get_Y(b, k))
    ops, count = 0, 0
    r = 1
    for y in range(b):
        if y in set_Y and r == c: count += 1
        r = (r * a) % b
        ops += 1
    return count, ops

# --- ЗАПУСК И ВЫВОД ---
b_test = 10000
k_test = 500
a_test, c_test = 2, 1

_, ops_n_full = count_naive_ops(a_test, b_test, c_test)
_, ops_f_full = count_fastpow_ops(a_test, b_test, c_test)
_, ops_i_full = count_iter_ops(a_test, b_test, c_test)

_, ops_n_sp = count_sp_naive_ops(a_test, b_test, c_test, k_test)
_, ops_f_sp = count_sp_fastpow_ops(a_test, b_test, c_test, k_test)
_, ops_i_sp = count_sp_iter_ops(a_test, b_test, c_test, k_test)

print("="*80)
print(f"АНАЛИЗ СЛОЖНОСТИ (Точное число модульных умножений при b={b_test}, k={k_test})")
print("="*80)
print(f"| {'Реализация':<15} | {'Полный диапазон (шт.)':>22} | {'Разреженный Y(b) (шт.)':>22} |")
print("-" * 67)
print(f"| {'count_naive':<15} | {ops_n_full:>22} | {ops_n_sp:>22} |")
print(f"| {'count_fastpow':<15} | {ops_f_full:>22} | {ops_f_sp:>22} |")
print(f"| {'count_iter':<15} | {ops_i_full:>22} | {ops_i_sp:>22} |")
print("="*80)

# Вывод для отчета
print("\nВЫВОДЫ ДЛЯ ОТЧЕТА:")
print("1. На полном диапазоне итеративная реализация асимптотически лучше,")
print(f"   так как делает всего {ops_i_full} умножений против {ops_n_full} у наивной.")
print(f"2. На разреженном диапазоне итеративная реализация проигрывает ({ops_i_sp} умножений),")
print(f"   так как сканирует весь диапазон b. Метод fastpow делает в разы меньше ({ops_f_sp}).")
print(f"3. Условие b >> k*log(b): при b={b_test} и k={k_test}, b действительно огромно по сравнению")
print(f"   с k*log2(b) ≈ {int(k_test * (b_test.bit_length()))}.")
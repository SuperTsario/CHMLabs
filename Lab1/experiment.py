import time
import matplotlib.pyplot as plt
import numpy as np
from functions import *

# Параметры эксперимента
b_values = [100, 300, 1000, 3000, 10000]
a_val = 2
c_val = 1

results = {
    'naive': [],
    'fastpow': [],
    'iter': []
}

print("Замер времени...")
for b in b_values:
    print(f"b = {b}...")
    
    # Замер naive
    t0 = time.perf_counter()
    count_naive(a_val, b, c_val)
    t_naive = time.perf_counter() - t0
    results['naive'].append(t_naive)
    
    # Замер fastpow
    t0 = time.perf_counter()
    count_fastpow(a_val, b, c_val)
    t_fastpow = time.perf_counter() - t0
    results['fastpow'].append(t_fastpow)
    
    # Замер iter
    t0 = time.perf_counter()
    count_iter(a_val, b, c_val)
    t_iter = time.perf_counter() - t0
    results['iter'].append(t_iter)
    
    print(f"  naive: {t_naive:.5f}s, fastpow: {t_fastpow:.5f}s, iter: {t_iter:.5f}s")

# Вывод результатов в консоль (для отчета)
print("\nРезультаты (в секундах):")
print(f"{'b':<10} | {'naive':<10} | {'fastpow':<10} | {'iter':<10}")
for i, b in enumerate(b_values):
    print(f"{b:<10} | {results['naive'][i]:<10.5f} | {results['fastpow'][i]:<10.5f} | {results['iter'][i]:<10.5f}")

# Построение графика в лог-лог осях
plt.figure(figsize=(10, 6))
plt.plot(b_values, results['naive'], 'o-', label='count_naive')
plt.plot(b_values, results['fastpow'], 's-', label='count_fastpow')
plt.plot(b_values, results['iter'], '^-', label='count_iter')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('b (log scale)')
plt.ylabel('Время, сек (log scale)')
plt.title('Зависимость времени выполнения от b (a=2, c=1)')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()
plt.savefig('time_plot.png') # сохраняем график в файл
plt.show()
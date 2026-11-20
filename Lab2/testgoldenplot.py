import os
import matplotlib.pyplot as plt
from core import call_counter, f3
from methods import golden_section

# Параметры
a, b = -2.0, 2.0
eps = 1e-4

# Запуск метода
fc = call_counter(f3)
res = golden_section(fc, a, b, eps)

# Достаем длины
L_list = [b - a] + [step["new_length"] for step in res["trace"]["steps"]]
r_list = [L_list[i+1] / L_list[i] for i in range(len(L_list)-1)]

# Выводим в консоль для проверки
print("СПИСОК ДЛИН (L_k):", [round(x, 5) for x in L_list])
print("СПИСОК ОТНОШЕНИЙ (r_k):", [round(x, 5) for x in r_list])

# Строим графики
os.makedirs("output", exist_ok=True)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 1. График L_k
ax1.semilogy(range(len(L_list)), L_list, 'o-', color='blue', linewidth=2)
ax1.set_title("Длина L_k (лог. шкала)")
ax1.set_xlabel("Итерация")
ax1.grid(True, which="both", ls="--")

# 2. График r_k
ax2.plot(range(len(r_list)), r_list, 'o-', color='red', linewidth=2, label='r_k')
ax2.axhline(y=0.618, color='gray', linestyle='--', linewidth=2, label='tau = 0.618')
ax2.set_title("Отношение r_k = L_{k+1} / L_k")
ax2.set_xlabel("Итерация")

# ЖЕСТКО ФИКСИРУЕМ ОСЬ Y ОТ 0.5 ДО 0.7 (чтобы 0.618 было ровно по центру)
ax2.set_ylim(0.5, 0.7) 

ax2.grid(True, ls="--")
ax2.legend()

fig.tight_layout()
fig.savefig("output/golden_check.png", dpi=150)
print("\nГрафик сохранен в output/golden_check.png")
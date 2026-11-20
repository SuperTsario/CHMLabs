import os
import math
import matplotlib.pyplot as plt

def plot_methods():
    os.makedirs("output", exist_ok=True)
    a, b = -2.0, 2.0
    eps_x = 1e-4
    L0 = b - a
    
    # --- 1. ДИХОТОМИЯ ---
    delta = 1e-5
    L_d = [L0]
    while L_d[-1] > 2 * eps_x:
        L_next = L_d[-1] / 2 + delta / 2
        L_d.append(L_next)
        
    # --- 2. ЗОЛОТОЕ СЕЧЕНИЕ ---
    phi = (math.sqrt(5) - 1) / 2
    L_g = [L0]
    while L_g[-1] > 2 * eps_x:
        L_next = L_g[-1] * phi
        L_g.append(L_next)

    # --- 3. ФИБОНАЧЧИ ---
    F = [1, 1]
    while F[-1] < L0 / (2 * eps_x):
        F.append(F[-1] + F[-2])
    m = len(F) - 1
    
    L_f = [L0]
    for k in range(m - 1):
        r = F[m - k - 1] / F[m - k]
        L_f.append(L_f[-1] * r)
    
    # Последний шаг Фибоначчи (особый, ставит точки симметрично)
    if L_f[-1] > 2 * eps_x:
        L_f.append(L_f[-1] / 2)

    # --- ФУНКЦИЯ ДЛЯ ОТРИСОВКИ ---
    def draw(L_list, title, fname):
        r_list = [L_list[i+1] / L_list[i] for i in range(len(L_list)-1)]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # График L_k
        ax1.semilogy(range(len(L_list)), L_list, 'o-', color='blue')
        ax1.set_xlabel("Итерация k")
        ax1.set_title(f"{title}: Длина интервала L_k")
        ax1.grid(True, which="both", ls="--")
        
        # График r_k (без прямых линий)
        ax2.plot(range(len(r_list)), r_list, 'o-', color='red')
        ax2.set_xlabel("Итерация k")
        ax2.set_title(f"{title}: Отношение r_k")
        ax2.grid(True, ls="--")
        
        fig.tight_layout()
        fig.savefig(f"output/{fname}")
        plt.close()
        print(f"Сохранено: output/{fname}")

    # Рисуем
    draw(L_d, "Дихотомия", "task3_dichotomy_f3.png")
    draw(L_g, "Золотое сечение", "task3_golden_f3.png")
    draw(L_f, "Фибоначчи", "task3_fibonacci_f3.png")

if __name__ == "__main__":
    plot_methods()
    print("\nВсе графики успешно перезаписаны!")
import matplotlib.pyplot as plt
from functions import count_fastpow as N

def get_neighbors(a, b, c):
    res = [((a+1)%b, b, c, 'a'), ((a-1)%b, b, c, 'a'), (a, b, (c+1)%b, 'c'), (a, b, (c-1)%b, 'c'), (a%(b+1), b+1, c%(b+1), 'b')]
    if b - 1 >= 2: 
        res.append((a%(b-1), b-1, c%(b-1), 'b'))
    return res

def calc_S(a, b, c, a2, b2, c2, changed):
    n1, n2 = N(a, b, c), N(a2, b2, c2)
    if n1 == n2: return 0.0
    num = abs(n2 - n1) / max(n1, 1)
    if changed == 'a':
        p = a
    elif changed == 'b': 
        p = b
    else:
        p = c
    return num * max(abs(p), 1)

def kappa_lab(a, b, c):
    return max([calc_S(a, b, c, *x[:3], x[3]) for x in get_neighbors(a, b, c)] + [0.0])

print("="*60)
print("ЗАДАНИЯ 1 и 2: Примеры скачков N при изменении параметров")
print("="*60)
jc, ja, jb = [], [], []
for b in [7, 11, 13, 17]:
    for a in [2, 3, 5]:
        for c in range(b):
            n_curr, cp, ap, bp = N(a, b, c), (c+1)%b, (a+1)%b, b+1
            n_c, n_a, n_bp = N(a, b, cp), N(ap, b, c), N(a%bp, bp, c%bp)
            if n_curr != n_c and len(jc) < 3: jc.append(f"  {a},{b},{c} (N={n_curr}) -> c'={cp} (N={n_c})")
            if n_curr != n_a and len(ja) < 3: ja.append(f"  {a},{b},{c} (N={n_curr}) -> a'={ap} (N={n_a})")
            if n_curr != n_bp and len(jb) < 3: jb.append(f"  {a},{b},{c} (N={n_curr}) -> b'={bp} (N={n_bp})")

print("\n[Изменение c]")
print("\n".join(jc))
print("\n[Изменение a]")
print("\n".join(ja))
print("\n[Изменение b]")
print("\n".join(jb))

print("\n" + "="*60)
print("ЗАДАНИЕ 3: Таблица kappa_lab для 10 точек")
print("="*60)
print(f"| {'a':>2} | {'b':>3} | {'c':>3} | {'N':>3} | {'kappa_lab':>10} |")
print("-" * 41)
for a, b, c in [(2,7,4), (2,7,3), (3,11,1), (0,7,0), (0,7,1), (5,13,2), (4,17,5), (1,5,1), (2,10,0), (5,20,3)]:
    print(f"| {a:>2} | {b:>3} | {c:>3} | {N(a,b,c):>3} | {kappa_lab(a,b,c):>10.2f} |")

print("\n" + "="*60)
print("ЗАДАНИЕ 4: Точки, где N=0, но при сдвиге N>0")
print("="*60)
f = 0
for b in range(3, 20):
    for a in range(b):
        for c in range(b):
            if f < 3 and N(a, b, c) == 0:
                for a2, b2, c2, p in get_neighbors(a, b, c):
                    if N(a2, b2, c2) > 0:
                        print(f"p=({a},{b},{c}) [N=0] -> p'=({a2},{b2},{c2}) [N'={N(a2,b2,c2)}] (изменён {p})")
                        print(f"  Строгая S: +inf | Регуляризованная S: {calc_S(a,b,c,a2,b2,c2,p):.2f}\n")
                        f += 1
                        break

print("="*60)
print("ЗАДАНИЕ 5: Мини-исследование при b <= 50")
print("="*60)
c0, c2, mk, mkp, sp, aN, bfd = 0, 0, -1, None, None, [], {}
for b in range(2, 51):
    dc, tp = 0, 0
    for a in range(b):
        for c in range(b):
            tp += 1
            n = N(a, b, c)
            aN.append(n)
            if n == 0: c0 += 1
            if n >= 2: c2 += 1
            k = kappa_lab(a, b, c)
            if k > mk: mk, mkp = k, (a, b, c)
            if k == 0 and sp is None: sp = (a, b, c)
            if any(N(*x[:3]) != n for x in get_neighbors(a, b, c)): dc += 1
    bfd[b] = dc / tp

print(f"  Количество точек с N=0:   {c0}")
print(f"  Количество точек с N>=2:  {c2}")
print(f"  Максимальная kappa_lab:   {mk:.2f} в точке {mkp}")
print(f"  Устойчивая точка (k=0):   {sp}")
print("\nСтроим графики и сохраняем в 'sensitivity_plots.png'...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Исследование чувствительности модели (b <= 50)', fontsize=14, fontweight='bold')

ax1.hist(aN, bins=30, edgecolor='black', alpha=0.7, color='skyblue')
ax1.set_title("Распределение значений N")
ax1.set_xlabel("Количество решений (N)")
ax1.set_ylabel("Частота")
ax1.grid(axis='y', linestyle='--', alpha=0.7)

ax2.plot(list(bfd.keys()), list(bfd.values()), marker='o', linestyle='-', color='crimson')
ax2.set_title("Доля точек с изменением N при возмущении")
ax2.set_xlabel("Значение модуля (b)")
ax2.set_ylabel("Доля чувствительных точек")
ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('sensitivity_plots.png', dpi=300, bbox_inches='tight')
plt.show()
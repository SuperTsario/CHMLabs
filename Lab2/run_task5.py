from experiments import run_g_all, find_exclusion_step
from plots import plot_g, ensure_output_dir
from core import g, call_counter
from methods import dichotomy, golden_section, fibonacci_search

ensure_output_dir()

# графики
plot_g(-2.0, 2.0, "task5_g_full.png")
plot_g(0.5, 2.0, "task5_g_right.png")

# прогон
df_full = run_g_all(-2.0, 2.0, eps_x=1e-4)
df_right = run_g_all(0.5, 2.0, eps_x=1e-4)
df_full.to_csv("output/task5_full.csv", index=False)
df_right.to_csv("output/task5_right.csv", index=False)
print(df_full.to_string())
print(df_right.to_string())

# первый шаг исключения x=1.2 на [-2, 2]
for name, runner, kwargs in [
    ("dichotomy", dichotomy, {"delta": 1e-6}),
    ("golden", golden_section, {}),
    ("fibonacci", fibonacci_search, {}),
]:
    fc = call_counter(g)
    res = runner(fc, -2.0, 2.0, 1e-4, **kwargs)
    k, step = find_exclusion_step(res["trace"], 1.2)
    print(f"\n{name}: Nf={res['Nf']}, iters={res['iters']}, "
          f"x_mid={res['x_mid']:.6f}, error_x={res['x_mid'] and abs(res['x_mid']-1.2):.6f}")
    if k is None:
        print("  x=1.2 НЕ исключён")
    else:
        print(f"  первый шаг исключения: k={k}")
        print(f"  a={step['a']:.6f}, b={step['b']:.6f}")
        print(f"  c={step['c']:.6f}, d={step['d']:.6f}")
        print(f"  f(c)={step['fc']:.6f}, f(d)={step['fd']:.6f}")
        print(f"  new_a={step['new_a']:.6f}, new_b={step['new_b']:.6f}")
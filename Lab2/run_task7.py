from experiments import task7_brent_vs_golden
from plots import ensure_output_dir, plot_brent_steps
from core import call_counter, f3, f4, f5
from methods import brent

ensure_output_dir()

df = task7_brent_vs_golden(eps_xs=(1e-4, 1e-6))
df.to_csv("output/task7_brent_vs_golden.csv", index=False)
print(df.to_string())

for name, f in [("f3", f3), ("f4", f4), ("f5", f5)]:
    fc = call_counter(f)
    res = brent(fc, -2.0, 2.0, 1e-6)
    print(f"\n{name}: Nf={res['Nf']}, iters={res['iters']}, "
          f"parabolic={res['n_parabolic']}, golden={res['n_golden']}, "
          f"stop={res['stop']}")
    plot_brent_steps(res, f"task7_brent_steps_{name}.png",
                     title=f"Brent on {name}, eps_x=1e-6")
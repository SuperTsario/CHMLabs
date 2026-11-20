from experiments import task6_scaling
from plots import ensure_output_dir

ensure_output_dir()

df = task6_scaling(eps_x=1e-6)
df.to_csv("output/task6_scaling.csv", index=False)
print(df.to_string())

for name in ["f3", "f5"]:
    sub = df[df["func"] == name]
    print(f"\n=== {name} ===")
    print("x_mid values:")
    for _, row in sub.iterrows():
        print(f"  A={row['A']:>8.0e}  B={row['B']:>8.0e}  x_mid={row['x_mid']:.15f}  length={row['length']:.3e}  Nf={row['Nf']}  stop={row['stop']}")
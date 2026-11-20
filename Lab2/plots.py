import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT_DIR = "output"


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_function(f, a, b, fname, n_points=1000, title=None):
    ensure_output_dir()
    xs = np.linspace(a, b, n_points)
    ys = [f(x) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, ys, label="f(x)")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    if title:
        ax.set_title(title)
    ax.grid(True)
    ax.legend()
    fig.savefig(os.path.join(OUTPUT_DIR, fname))
    plt.close(fig)


def plot_function_with_grid(f, a, b, result, fname, n_points=1000, title=None):
    ensure_output_dir()
    xs = np.linspace(a, b, n_points)
    ys = [f(x) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, ys, label="f(x)")

    tr = result.get("trace", {})
    nodes = tr.get("nodes")
    values = tr.get("values")

    if nodes is not None and values is not None:
        ax.plot(nodes, values, 'o', color='tab:orange', markersize=3, label="nodes")
        if tr.get("j_best") is not None:
            j = tr["j_best"]
            ax.plot([nodes[j]], [values[j]], 'o', color='red', markersize=6, label="best node")

    if result.get("x_mid") is not None:
        ax.axvline(result["x_mid"], color='green', linestyle='--', label="x_mid")
        if result.get("a") is not None and result.get("b") is not None:
            ax.axvspan(result["a"], result["b"], color='green', alpha=0.1, label="final interval")

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    if title:
        ax.set_title(title)
    ax.grid(True)
    ax.legend()
    fig.savefig(os.path.join(OUTPUT_DIR, fname))
    plt.close(fig)


def plot_length_and_ratio(L_list, fname, title=None, extra_L=None, extra_label=None):
    ensure_output_dir()
    ks = list(range(len(L_list)))
    rs = [L_list[i + 1] / L_list[i] for i in range(len(L_list) - 1)]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].semilogy(ks, L_list, 'o-', markersize=4, label='L_k')
    if extra_L is not None:
        axes[0].semilogy(ks[:len(extra_L)], extra_L, '--', label=extra_label or 'theory')
    axes[0].set_xlabel("k")
    axes[0].set_ylabel("L_k")
    axes[0].grid(True, which='both')
    axes[0].legend()

    ks_r = list(range(len(rs)))
    axes[1].plot(ks_r, rs, 'o-', markersize=4, label='r_k')
    axes[1].set_xlabel("k")
    axes[1].set_ylabel("r_k = L_{k+1} / L_k")
    axes[1].grid(True)
    axes[1].legend()

    if title:
        fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, fname))
    plt.close(fig)


def plot_task4_nf_vs_eps(df, funcs, fname, title=None):
    ensure_output_dir()
    methods = ["grid", "dichotomy", "golden", "fibonacci"]
    fig, axes = plt.subplots(1, len(funcs), figsize=(4 * len(funcs), 4), sharey=False)
    if len(funcs) == 1:
        axes = [axes]

    for ax, func_name in zip(axes, funcs):
        sub = df[df["func"] == func_name]
        for m in methods:
            ss = sub[sub["method"] == m].sort_values("eps_x")
            if len(ss) == 0:
                continue
            ax.loglog(ss["eps_x"], ss["Nf"], 'o-', label=m)
        ax.set_xlabel("eps_x")
        ax.set_ylabel("Nf")
        ax.set_title(func_name)
        ax.grid(True, which='both')
        ax.legend()
        ax.invert_xaxis()

    if title:
        fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, fname))
    plt.close(fig)


def plot_task4_length_vs_nf(df, funcs, fname, title=None):
    ensure_output_dir()
    methods = ["grid", "dichotomy", "golden", "fibonacci"]
    fig, axes = plt.subplots(1, len(funcs), figsize=(4 * len(funcs), 4))
    if len(funcs) == 1:
        axes = [axes]

    for ax, func_name in zip(axes, funcs):
        sub = df[(df["func"] == func_name) & (df["length"].notna())]
        for m in methods:
            ss = sub[sub["method"] == m].sort_values("Nf")
            if len(ss) == 0:
                continue
            ax.loglog(ss["Nf"], ss["length"], 'o-', label=m)
        ax.set_xlabel("Nf")
        ax.set_ylabel("length")
        ax.set_title(func_name)
        ax.grid(True, which='both')
        ax.legend()

    if title:
        fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, fname))
    plt.close(fig)


def plot_task4_errors_vs_nf(df, funcs, fname, title=None):
    ensure_output_dir()
    methods = ["grid", "dichotomy", "golden", "fibonacci"]
    fig, axes = plt.subplots(2, len(funcs), figsize=(4 * len(funcs), 8))
    if len(funcs) == 1:
        axes = axes.reshape(2, 1)

    for col, func_name in enumerate(funcs):
        sub = df[(df["func"] == func_name) & (df["error_x"].notna())]
        for m in methods:
            ss = sub[sub["method"] == m].sort_values("Nf")
            if len(ss) == 0:
                continue
            mask = ss["error_x"] > 0
            if mask.any():
                axes[0, col].loglog(ss.loc[mask, "Nf"], ss.loc[mask, "error_x"], 'o-', label=m)
            mask_f = ss["error_f"] > 0
            if mask_f.any():
                axes[1, col].loglog(ss.loc[mask_f, "Nf"], ss.loc[mask_f, "error_f"], 'o-', label=m)

        axes[0, col].set_xlabel("Nf")
        axes[0, col].set_ylabel("error_x")
        axes[0, col].set_title(f"{func_name}: error_x")
        axes[0, col].grid(True, which='both')
        axes[0, col].legend()

        axes[1, col].set_xlabel("Nf")
        axes[1, col].set_ylabel("error_f")
        axes[1, col].set_title(f"{func_name}: error_f")
        axes[1, col].grid(True, which='both')
        axes[1, col].legend()

    if title:
        fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, fname))
    plt.close(fig)


def plot_task4_budget(df, fname, title=None):
    ensure_output_dir()
    methods = ["grid", "dichotomy", "golden", "fibonacci"]
    funcs = ["f3", "f6"]
    fig, axes = plt.subplots(1, len(funcs), figsize=(5 * len(funcs), 4))
    if len(funcs) == 1:
        axes = [axes]

    for ax, func_name in zip(axes, funcs):
        sub = df[df["func"] == func_name]
        for m in methods:
            ss = sub[sub["method"] == m].sort_values("budget")
            if len(ss) == 0:
                continue
            ax.plot(ss["budget"], ss["length"], 'o-', label=m)
        ax.set_xlabel("budget N")
        ax.set_ylabel("final length")
        ax.set_yscale("log")
        ax.set_title(func_name)
        ax.grid(True, which='both')
        ax.legend()

    if title:
        fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, fname))
    plt.close(fig)


def plot_g(a, b, fname, n_points=1000):
    ensure_output_dir()
    xs = np.linspace(a, b, n_points)
    ys_main = [(x - 1.2) ** 2 for x in xs]
    ys_alt = [(x + 0.8) ** 2 + 0.15 for x in xs]
    ys_g = [min(a1, a2) for a1, a2 in zip(ys_main, ys_alt)]

    fig, ax = plt.subplots()
    ax.plot(xs, ys_main, '--', label="(x-1.2)^2")
    ax.plot(xs, ys_alt, '--', label="(x+0.8)^2 + 0.15")
    ax.plot(xs, ys_g, '-', linewidth=2, label="g(x) = min")
    ax.axvline(1.2, color='red', linestyle=':', label="global min (1.2)")
    ax.axvline(-0.8, color='orange', linestyle=':', label="local min (-0.8)")
    ax.set_xlabel("x")
    ax.set_ylabel("g(x)")
    ax.set_title(f"g(x) on [{a}, {b}]")
    ax.grid(True)
    ax.legend()
    fig.savefig(os.path.join(OUTPUT_DIR, fname))
    plt.close(fig)


def plot_brent_steps(result, fname, title=None):
    ensure_output_dir()
    steps = result["trace"]["steps"]
    ks = list(range(len(steps)))
    xs = [s["u"] for s in steps]
    types = [s["step_type"] for s in steps]
    colors = ["tab:red" if t == "parabolic" else "tab:blue" for t in types]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.scatter(ks, xs, c=colors, s=40, zorder=3)
    ax.plot(ks, xs, '-', color='gray', alpha=0.4, zorder=2)
    ax.set_xlabel("step k")
    ax.set_ylabel("u_k")
    ax.set_title(title or "Brent: accepted points")
    ax.grid(True)

    from matplotlib.lines import Line2D
    legend_elems = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='tab:red', markersize=8, label='parabolic'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='tab:blue', markersize=8, label='golden'),
    ]
    ax.legend(handles=legend_elems)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, fname))
    plt.close(fig)
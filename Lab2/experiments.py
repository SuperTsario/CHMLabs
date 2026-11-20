import pandas as pd

from core import (
    f0, f1, f2, f3, f4, f5, f6, fb,
    call_counter, error_x, error_f, g
)

from methods import grid_search, dichotomy, golden_section, fibonacci_search, brent


FUNCS = {
    "f0": f0,
    "f1": f1,
    "f2": f2,
    "f3": f3,
    "f4": f4,
    "f5": f5,
    "f6": f6,
    "fb": fb,
}


def run_grid_all(eps_x=1e-2, a=-2.0, b=2.0, budget=None):
    rows = []
    for name, f in FUNCS.items():
        fc = call_counter(f)
        res = grid_search(fc, a, b, eps_x, budget=budget)
        row = {
            "func": name,
            "method": "grid",
            "eps_x": eps_x,
            "budget": budget,
            "Nf": res["Nf"],
            "length": res["length"],
            "x_mid": res["x_mid"],
            "stop": res["stop"],
        }
        if res["x_mid"] is not None:
            row["error_x"] = error_x(res["x_mid"], name)
            row["error_f"] = error_f(res["x_mid"], f, name)
        else:
            row["error_x"] = None
            row["error_f"] = None
        rows.append(row)
    return pd.DataFrame(rows)


def run_dichotomy_all(eps_x=1e-2, delta=1e-3, a=-2.0, b=2.0, budget=None):
    rows = []
    for name, f in FUNCS.items():
        fc = call_counter(f)
        res = dichotomy(fc, a, b, eps_x, delta, budget=budget)
        row = {
            "func": name,
            "method": "dichotomy",
            "eps_x": eps_x,
            "delta": delta,
            "budget": budget,
            "Nf": res["Nf"],
            "iters": res["iters"],
            "length": res["length"],
            "x_mid": res["x_mid"],
            "stop": res["stop"],
        }
        if res["x_mid"] is not None:
            row["error_x"] = error_x(res["x_mid"], name)
            row["error_f"] = error_f(res["x_mid"], f, name) if res["f_mid"] is not None else None
        else:
            row["error_x"] = None
            row["error_f"] = None
        rows.append(row)
    return pd.DataFrame(rows)


def length_trace_dichotomy(f, eps_x=1e-4, delta=1e-5, a=-2.0, b=2.0):
    fc = call_counter(f)
    res = dichotomy(fc, a, b, eps_x, delta)
    L_list = [b - a] + [step["new_length"] for step in res["trace"]["steps"]]
    return L_list, res


def task3_dichotomy_lengths(eps_x=1e-4, delta=1e-5, a=-2.0, b=2.0):
    fc = call_counter(f3)
    res = dichotomy(fc, a, b, eps_x, delta)
    L_list = [b - a] + [step["new_length"] for step in res["trace"]["steps"]]
    r_list = [L_list[i + 1] / L_list[i] for i in range(len(L_list) - 1)]
    return L_list, r_list, res

def run_golden_all(eps_x=1e-2, a=-2.0, b=2.0, budget=None):
    rows = []
    for name, f in FUNCS.items():
        fc = call_counter(f)
        res = golden_section(fc, a, b, eps_x, budget=budget)
        row = {
            "func": name,
            "method": "golden",
            "eps_x": eps_x,
            "budget": budget,
            "Nf": res["Nf"],
            "iters": res["iters"],
            "length": res["length"],
            "x_mid": res["x_mid"],
            "stop": res["stop"],
        }
        if res["x_mid"] is not None:
            row["error_x"] = error_x(res["x_mid"], name)
            row["error_f"] = error_f(res["x_mid"], f, name) if res["f_mid"] is not None else None
        else:
            row["error_x"] = None
            row["error_f"] = None
        rows.append(row)
    return pd.DataFrame(rows)


def task3_golden_lengths(eps_x=1e-4, a=-2.0, b=2.0):
    fc = call_counter(f3)
    res = golden_section(fc, a, b, eps_x)
    L_list = [b - a] + [step["new_length"] for step in res["trace"]["steps"]]
    r_list = [L_list[i + 1] / L_list[i] for i in range(len(L_list) - 1)]
    return L_list, r_list, res


def run_fibonacci_all(eps_x=1e-2, a=-2.0, b=2.0, budget=None):
    rows = []
    for name, f in FUNCS.items():
        fc = call_counter(f)
        res = fibonacci_search(fc, a, b, eps_x, budget=budget)
        row = {
            "func": name,
            "method": "fibonacci",
            "eps_x": eps_x,
            "budget": budget,
            "Nf": res["Nf"],
            "iters": res["iters"],
            "length": res["length"],
            "x_mid": res["x_mid"],
            "stop": res["stop"],
        }
        if res["x_mid"] is not None:
            row["error_x"] = error_x(res["x_mid"], name)
            row["error_f"] = error_f(res["x_mid"], f, name) if res["f_mid"] is not None else None
        else:
            row["error_x"] = None
            row["error_f"] = None
        rows.append(row)
    return pd.DataFrame(rows)


def task3_fibonacci_lengths(eps_x=1e-4, a=-2.0, b=2.0):
    fc = call_counter(f3)
    res = fibonacci_search(fc, a, b, eps_x)
    L_list = [b - a] + [step["new_length"] for step in res["trace"]["steps"]]
    r_list = [L_list[i + 1] / L_list[i] for i in range(len(L_list) - 1)]
    return L_list, r_list, res


def run_all_methods_one(func_name, eps_x, budget=None, a=-2.0, b=2.0,
                        grid_max_nf=100000, delta_ratio=1e-2):
    f = FUNCS[func_name]
    rows = []

    fc = call_counter(f)
    res = grid_search(fc, a, b, eps_x, budget=budget, max_nf=grid_max_nf)
    rows.append(_make_row(func_name, f, eps_x, budget, "grid", res))

    delta = max(eps_x * delta_ratio, 1e-15)
    fc = call_counter(f)
    res = dichotomy(fc, a, b, eps_x, delta, budget=budget)
    rows.append(_make_row(func_name, f, eps_x, budget, "dichotomy", res))

    fc = call_counter(f)
    res = golden_section(fc, a, b, eps_x, budget=budget)
    rows.append(_make_row(func_name, f, eps_x, budget, "golden", res))

    fc = call_counter(f)
    res = fibonacci_search(fc, a, b, eps_x, budget=budget)
    rows.append(_make_row(func_name, f, eps_x, budget, "fibonacci", res))

    return rows


def _make_row(func_name, f, eps_x, budget, method, res):
    row = {
        "func": func_name,
        "method": method,
        "eps_x": eps_x,
        "budget": budget,
        "Nf": res["Nf"],
        "iters": res["iters"],
        "length": res["length"],
        "x_mid": res["x_mid"],
        "stop": res["stop"],
    }
    if res["x_mid"] is not None:
        row["error_x"] = error_x(res["x_mid"], func_name)
        row["error_f"] = error_f(res["x_mid"], f, func_name) if res["f_mid"] is not None else None
    else:
        row["error_x"] = None
        row["error_f"] = None
    return row


def task4_tolerance_table():
    rows = []
    for name in ["f1", "f2", "f3", "f4", "f5", "f6"]:
        for eps_x in [1e-2, 1e-4, 1e-6]:
            rows.extend(run_all_methods_one(name, eps_x))
    return pd.DataFrame(rows)


def task4_f0_fb_table(eps_x=1e-4):
    rows = []
    for name in ["f0", "fb"]:
        rows.extend(run_all_methods_one(name, eps_x))
    return pd.DataFrame(rows)


def task4_budget_table():
    rows = []
    for name in ["f3", "f6"]:
        for budget in [10, 20, 40]:
            rows.extend(run_all_methods_one(name, 1e-6, budget=budget))
    return pd.DataFrame(rows)


def run_g_all(a, b, eps_x=1e-4, budget=None, delta_ratio=1e-2):
    rows = []
    f = g
    for method_name, runner in [
        ("grid", lambda fc: grid_search(fc, a, b, eps_x, budget=budget)),
        ("dichotomy", lambda fc: dichotomy(fc, a, b, eps_x,
                                          max(eps_x * delta_ratio, 1e-15),
                                          budget=budget)),
        ("golden", lambda fc: golden_section(fc, a, b, eps_x, budget=budget)),
        ("fibonacci", lambda fc: fibonacci_search(fc, a, b, eps_x, budget=budget)),
    ]:
        fc = call_counter(f)
        res = runner(fc)
        row = {
            "segment": f"[{a},{b}]",
            "method": method_name,
            "eps_x": eps_x,
            "Nf": res["Nf"],
            "iters": res["iters"],
            "length": res["length"],
            "x_mid": res["x_mid"],
            "stop": res["stop"],
        }
        if res["x_mid"] is not None:
            row["error_x"] = error_x(res["x_mid"], "g")
            row["error_f"] = error_f(res["x_mid"], f, "g")
        else:
            row["error_x"] = None
            row["error_f"] = None
        rows.append(row)
    return pd.DataFrame(rows)


def find_exclusion_step(trace, x_target=1.2):
    for k, step in enumerate(trace["steps"]):
        if not (step["new_a"] <= x_target <= step["new_b"]):
            return k, step
    return None, None


def task6_scaling(eps_x=1e-6, a=-2.0, b=2.0):
    rows = []
    for name in ["f3", "f5"]:
        f = FUNCS[name]
        for A in [1e-12, 1.0, 1e12]:
            for B in [0.0, 1e16]:
                def scaled(x, f=f, A=A, B=B):
                    return A * f(x) + B

                fc = call_counter(scaled)
                res = golden_section(fc, a, b, eps_x)
                row = {
                    "func": name,
                    "A": A,
                    "B": B,
                    "Nf": res["Nf"],
                    "iters": res["iters"],
                    "length": res["length"],
                    "x_mid": res["x_mid"],
                    "stop": res["stop"],
                    "error_x": error_x(res["x_mid"], name),
                    "error_f": error_f(res["x_mid"], f, name),
                }
                rows.append(row)
    return pd.DataFrame(rows)


def task7_brent_vs_golden(eps_xs=(1e-4, 1e-6), a=-2.0, b=2.0):
    rows = []
    for name in ["f3", "f4", "f5"]:
        f = FUNCS[name]
        for eps_x in eps_xs:
            fc = call_counter(f)
            res = brent(fc, a, b, eps_x)
            rows.append({
                "func": name,
                "method": "brent",
                "eps_x": eps_x,
                "Nf": res["Nf"],
                "iters": res["iters"],
                "n_parabolic": res["n_parabolic"],
                "n_golden": res["n_golden"],
                "length": res["length"],
                "x_mid": res["x_mid"],
                "stop": res["stop"],
                "error_x": error_x(res["x_mid"], name),
                "error_f": error_f(res["x_mid"], f, name),
            })

            fc = call_counter(f)
            res = golden_section(fc, a, b, eps_x)
            rows.append({
                "func": name,
                "method": "golden",
                "eps_x": eps_x,
                "Nf": res["Nf"],
                "iters": res["iters"],
                "n_parabolic": None,
                "n_golden": None,
                "length": res["length"],
                "x_mid": res["x_mid"],
                "stop": res["stop"],
                "error_x": error_x(res["x_mid"], name),
                "error_f": error_f(res["x_mid"], f, name),
            })
    return pd.DataFrame(rows)
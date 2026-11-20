import math

from core import nf, REASON_TOL, REASON_BUDGET, REASON_GRID_LIMIT, REASON_ROUNDOFF


def grid_search(fc, a, b, eps_x, budget=None, max_nf=100000):
    n_needed = max(1, int(math.ceil((b - a) / eps_x)))
    n = n_needed
    truncated = False

    if budget is not None:
        n_budget = budget - 2
        if n_budget < 1:
            return {
                "method": "grid",
                "x_mid": None,
                "f_mid": None,
                "a": a,
                "b": b,
                "length": None,
                "iters": 0,
                "Nf": nf(fc),
                "stop": REASON_BUDGET,
                "trace": {
                    "n": None,
                    "n_needed": n_needed,
                    "nodes": None,
                    "values": None,
                    "j_best": None,
                    "truncated": True,
                },
            }
        if n > n_budget:
            n = n_budget
            truncated = True

    num_nodes = n + 1

    if num_nodes > max_nf:
        return {
            "method": "grid",
            "x_mid": None,
            "f_mid": None,
            "a": a,
            "b": b,
            "length": None,
            "iters": 0,
            "Nf": 0,
            "stop": REASON_GRID_LIMIT,
            "trace": {
                "n": n,
                "n_needed": n_needed,
                "theoretical_nodes": num_nodes,
                "nodes": None,
                "values": None,
                "j_best": None,
                "truncated": truncated,
            },
        }

    h = (b - a) / n
    nodes = [a + i * h for i in range(num_nodes)]
    nodes[-1] = b

    values = [fc(x) for x in nodes]
    j = values.index(min(values))

    if j == 0:
        left, right = nodes[0], nodes[1]
    elif j == num_nodes - 1:
        left, right = nodes[-2], nodes[-1]
    else:
        left, right = nodes[j - 1], nodes[j + 1]

    x_mid = (left + right) / 2
    f_mid = fc(x_mid)
    length = right - left

    if length <= 2 * eps_x * (1 + 1e-9):
        stop = REASON_TOL
    elif truncated:
        stop = REASON_BUDGET
    else:
        stop = REASON_TOL

    return {
        "method": "grid",
        "x_mid": x_mid,
        "f_mid": f_mid,
        "a": left,
        "b": right,
        "length": length,
        "iters": 0,
        "Nf": nf(fc),
        "stop": stop,
        "trace": {
            "n": n,
            "n_needed": n_needed,
            "nodes": nodes,
            "values": values,
            "j_best": j,
            "truncated": truncated,
        },
    }

def dichotomy(fc, a, b, eps_x, delta, budget=None):
    trace = {"steps": []}

    fc(a)
    fc(b)

    while True:
        length = b - a
        if length <= 2 * eps_x:
            stop = REASON_TOL
            break

        c = (a + b) / 2 - delta / 2
        d = (a + b) / 2 + delta / 2

        if c <= a or d >= b or c == d:
            stop = REASON_ROUNDOFF
            break

        if budget is not None:
            new_c = 0 if c in fc.seen else 1
            new_d = 0 if d in fc.seen else 1
            spent = nf(fc) - 2
            if spent + new_c + new_d > budget - 3:
                stop = REASON_BUDGET
                break

        fc_c = fc(c)
        fc_d = fc(d)

        if fc_c <= fc_d:
            new_a, new_b = a, d
        else:
            new_a, new_b = c, b

        trace["steps"].append({
            "a": a, "b": b,
            "c": c, "d": d,
            "fc": fc_c, "fd": fc_d,
            "new_a": new_a, "new_b": new_b,
            "new_length": new_b - new_a,
        })

        a, b = new_a, new_b

    x_mid = (a + b) / 2
    if x_mid in fc.seen:
        f_mid = fc(x_mid)
    elif budget is None or nf(fc) < budget:
        f_mid = fc(x_mid)
    else:
        f_mid = None

    return {
        "method": "dichotomy",
        "x_mid": x_mid,
        "f_mid": f_mid,
        "a": a,
        "b": b,
        "length": b - a,
        "iters": len(trace["steps"]),
        "Nf": nf(fc),
        "stop": stop,
        "trace": trace,
    }


def golden_section(fc, a, b, eps_x, budget=None):
    tau = (math.sqrt(5) - 1) / 2
    fc(a)
    fc(b)
    
    # Начальные точки
    c = a + (1 - tau) * (b - a)
    d = a + tau * (b - a)
    fc_c = fc(c)
    fc_d = fc(d)
    
    trace = {"steps": []}
    stop = None

    while True:
        length = b - a
        if length <= 2 * eps_x:
            stop = REASON_TOL
            break

        if budget is not None and nf(fc) >= budget:
            stop = REASON_BUDGET
            break

        # Сравниваем и обновляем интервал
        if fc_c <= fc_d:
            new_a, new_b = a, d
            new_c = new_a + (1 - tau) * (new_b - new_a)
            new_d = c
            new_fc = fc(new_c)
            new_fd = fc_c
        else:
            new_a, new_b = c, b
            new_c = d
            new_d = new_a + tau * (new_b - new_a)
            new_fc = fc_d
            new_fd = fc(new_d)

        # Сохраняем историю ДО обновления a и b
        trace["steps"].append({
            "a": a, "b": b,
            "c": c, "d": d,
            "fc": fc_c, "fd": fc_d,
            "new_a": new_a, "new_b": new_b,
            "new_length": new_b - new_a,  # <--- ВОТ ТУТ ДОЛЖНА БЫТЬ ПРАВИЛЬНАЯ ДЛИНА
        })

        # Обновляем текущий интервал
        a, b = new_a, new_b
        c, d = new_c, new_d
        fc_c, fc_d = new_fc, new_fd

    x_mid = (a + b) / 2
    if x_mid in fc.seen:
        f_mid = fc(x_mid)
    elif budget is None or nf(fc) < budget:
        f_mid = fc(x_mid)
    else:
        f_mid = None

    return {
        "method": "golden",
        "x_mid": x_mid,
        "f_mid": f_mid,
        "a": a, "b": b,
        "length": b - a,
        "iters": len(trace["steps"]),
        "Nf": nf(fc),
        "stop": stop,
        "trace": trace,
    }


def fibonacci_search(fc, a, b, eps_x, budget=None):
    L0 = b - a
    fc(a)
    fc(b)

    if L0 <= 2 * eps_x:
        x_mid = (a + b) / 2
        f_mid = fc(x_mid)
        return {
            "method": "fibonacci",
            "x_mid": x_mid,
            "f_mid": f_mid,
            "a": a, "b": b,
            "length": L0,
            "iters": 0,
            "Nf": nf(fc),
            "stop": REASON_TOL,
            "trace": {"steps": [], "m": 0, "F": [1]},
        }

    F = [1, 1]
    while F[-1] < L0 / (2 * eps_x):
        F.append(F[-1] + F[-2])
    m = len(F) - 1
    if m < 2:
        m = 2
        while len(F) < m + 1:
            F.append(F[-1] + F[-2])

    if budget is not None:
        max_m = budget - 3
        if max_m < 1:
            x_mid = (a + b) / 2
            if x_mid in fc.seen:
                f_mid = fc(x_mid)
            elif nf(fc) < budget:
                f_mid = fc(x_mid)
            else:
                f_mid = None
            return {
                "method": "fibonacci",
                "x_mid": x_mid,
                "f_mid": f_mid,
                "a": a, "b": b,
                "length": L0,
                "iters": 0,
                "Nf": nf(fc),
                "stop": REASON_BUDGET,
                "trace": {"steps": [], "m": m, "F": F},
            }
        if m > max_m:
            m = max_m

    a_cur, b_cur = a, b
    c_prev = d_prev = None
    fc_prev_c = fc_prev_d = None
    last_dir = None
    trace = {"steps": [], "m": m, "F": F}
    stop = None

    for k in range(m - 2):
        if b_cur - a_cur <= 2 * eps_x:
            stop = REASON_TOL
            break
        if budget is not None:
            internal_used = nf(fc) - 2
            new_calls = 2 if k == 0 else 1
            if internal_used + new_calls > budget - 3:
                stop = REASON_BUDGET
                break

        Lk = b_cur - a_cur
        Lk_next = Lk * F[m - k - 1] / F[m - k]

        if k == 0:
            c = a_cur + (Lk - Lk_next)
            d = a_cur + Lk_next
            fc_c = fc(c)
            fc_d = fc(d)
        else:
            if last_dir == "left":
                d = c_prev
                fc_d = fc_prev_c
                c = a_cur + (Lk - Lk_next)
                fc_c = fc(c)
            else:
                c = d_prev
                fc_c = fc_prev_d
                d = a_cur + Lk_next
                fc_d = fc(d)

        if c >= d or c <= a_cur or d >= b_cur:
            stop = REASON_ROUNDOFF
            break

        if fc_c <= fc_d:
            new_a, new_b = a_cur, d
            last_dir = "left"
        else:
            new_a, new_b = c, b_cur
            last_dir = "right"

        trace["steps"].append({
            "a": a_cur, "b": b_cur,
            "c": c, "d": d,
            "fc": fc_c, "fd": fc_d,
            "new_a": new_a, "new_b": new_b,
            "new_length": new_b - new_a,
        })

        c_prev, d_prev = c, d
        fc_prev_c, fc_prev_d = fc_c, fc_d
        a_cur, b_cur = new_a, new_b

    if stop is None and b_cur - a_cur > 2 * eps_x:
        if budget is not None:
            internal_used = nf(fc) - 2
            if internal_used + 2 > budget - 3:
                stop = REASON_BUDGET

        if stop is None:
            x_center = (a_cur + b_cur) / 2
            room = 2 * eps_x - (b_cur - a_cur) / 2
            if room <= 0:
                delta_last = 1e-15
            else:
                delta_last = min(eps_x, room)
            c = x_center - delta_last / 2
            d = x_center + delta_last / 2

            if c <= a_cur or d >= b_cur or c >= d:
                stop = REASON_ROUNDOFF
            else:
                fc_c = fc(c)
                fc_d = fc(d)
                if fc_c <= fc_d:
                    new_a, new_b = a_cur, d
                else:
                    new_a, new_b = c, b_cur
                trace["steps"].append({
                    "a": a_cur, "b": b_cur,
                    "c": c, "d": d,
                    "fc": fc_c, "fd": fc_d,
                    "new_a": new_a, "new_b": new_b,
                    "new_length": new_b - new_a,
                    "last": True,
                })
                a_cur, b_cur = new_a, new_b

    if stop is None:
        if b_cur - a_cur <= 2 * eps_x:
            stop = REASON_TOL
        else:
            stop = REASON_BUDGET if budget is not None else REASON_ROUNDOFF

    x_mid = (a_cur + b_cur) / 2
    if x_mid in fc.seen:
        f_mid = fc(x_mid)
    elif budget is None or nf(fc) < budget:
        f_mid = fc(x_mid)
    else:
        f_mid = None

    return {
        "method": "fibonacci",
        "x_mid": x_mid,
        "f_mid": f_mid,
        "a": a_cur, "b": b_cur,
        "length": b_cur - a_cur,
        "iters": len(trace["steps"]),
        "Nf": nf(fc),
        "stop": stop,
        "trace": trace,
    }


def brent(fc, a, b, eps_x, budget=None):
    golden = (math.sqrt(5) - 1) / 2

    fc(a)
    fc(b)
    if a > b:
        a, b = b, a

    x = w = v = a + (b - a) * (1 - golden)
    fx = fw = fv = fc(x)

    d = 0.0
    e = 0.0

    tol1 = max(eps_x * 0.01, 1e-15)

    trace = {"steps": []}
    stop = None

    while True:
        if b - a <= 2 * eps_x:
            stop = REASON_TOL
            break

        if budget is not None and nf(fc) >= budget - 1:
            stop = REASON_BUDGET
            break

        use_parabolic = False
        d_try = 0.0

        if abs(e) > tol1:
            r = (x - w) * (fx - fv)
            q = (x - v) * (fx - fw)
            p = (x - v) * q - (x - w) * r
            q = 2.0 * (q - r)

            if q != 0.0:
                if q > 0:
                    p = -p
                q = abs(q)
                r_old = e
                e = d
                if abs(p) < abs(0.5 * q * r_old) and q * (a - x) < p < q * (b - x):
                    d_try = p / q
                    u_try = x + d_try
                    if (a < u_try < b) and abs(u_try - x) > tol1 and abs(u_try - w) > tol1 and abs(u_try - v) > tol1:
                        use_parabolic = True

        if use_parabolic:
            d = d_try
            step_type = "parabolic"
        else:
            e = a - x if x >= (a + b) / 2 else b - x
            d = (1 - golden) * e
            step_type = "golden"

        if abs(d) >= tol1:
            u = x + d
        else:
            u = x + tol1 * (1.0 if d >= 0 else -1.0)

        if u <= a or u >= b:
            stop = REASON_ROUNDOFF
            break

        fu = fc(u)

        trace["steps"].append({
            "a": a, "b": b,
            "x": x, "w": w, "v": v,
            "u": u,
            "fx": fx, "fw": fw, "fv": fv, "fu": fu,
            "step_type": step_type,
            "d": d,
        })

        if fu <= fx:
            if u >= x:
                a = x
            else:
                b = x
            v, w, x = w, x, u
            fv, fw, fx = fw, fx, fu
        else:
            if u < x:
                a = u
            else:
                b = u
            if fu <= fw or w == x:
                v, w = w, u
                fv, fw = fw, fu
            elif fu <= fv or v == x or v == w:
                v = u
                fv = fu

    x_mid = x
    if x_mid in fc.seen:
        f_mid = fc(x_mid)
    elif budget is None or nf(fc) < budget:
        f_mid = fc(x_mid)
    else:
        f_mid = None

    n_parabolic = sum(1 for s in trace["steps"] if s["step_type"] == "parabolic")
    n_golden = sum(1 for s in trace["steps"] if s["step_type"] == "golden")

    return {
        "method": "brent",
        "x_mid": x_mid,
        "f_mid": f_mid,
        "a": a,
        "b": b,
        "length": b - a,
        "iters": len(trace["steps"]),
        "Nf": nf(fc),
        "stop": stop,
        "trace": trace,
        "n_parabolic": n_parabolic,
        "n_golden": n_golden,
    }
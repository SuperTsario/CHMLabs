def call_counter(func):
    seen = {}

    def wrapper(x):
        if x not in seen:
            seen[x] = func(x)
        return seen[x]

    wrapper.seen = seen
    return wrapper


def nf(fc):
    return len(fc.seen)


REASON_TOL = "tolerance"
REASON_BUDGET = "budget"
REASON_ROUNDOFF = "roundoff"
REASON_GRID_LIMIT = "grid_limit"


def f0(x):
    return 1.0


def f1(x):
    return x


def f2(x):
    return -x


def f3(x):
    return (x - 0.37) ** 2


def f4(x):
    return abs(x - 0.37)


def f5(x):
    return (x - 0.37) ** 4


def f6(x):
    return max(abs(x - 0.37) - 0.4, 0.0) ** 2


def fb(x):
    return (x - 2.0) ** 2


REFS = {
    "f0": {"f_star": 1.0, "X_star": ("interval", -2.0, 2.0)},
    "f1": {"f_star": -2.0, "X_star": ("point", -2.0)},
    "f2": {"f_star": -2.0, "X_star": ("point", 2.0)},
    "f3": {"f_star": 0.0, "X_star": ("point", 0.37)},
    "f4": {"f_star": 0.0, "X_star": ("point", 0.37)},
    "f5": {"f_star": 0.0, "X_star": ("point", 0.37)},
    "f6": {"f_star": 0.0, "X_star": ("interval", -0.03, 0.77)},
    "fb": {"f_star": 0.0, "X_star": ("point", 2.0)},
    "g": {"f_star": 0.0, "X_star": ("point", 1.2)}
}


def error_x(x, name):
    ref = REFS[name]["X_star"]
    if ref[0] == "point":
        return abs(x - ref[1])
    lo, hi = ref[1], ref[2]
    if x < lo:
        return lo - x
    if x > hi:
        return x - hi
    return 0.0


def error_f(x, f, name):
    return f(x) - REFS[name]["f_star"]


def g(x):
    left = (x - 1.2) ** 2
    right = (x + 0.8) ** 2 + 0.15
    return min(left, right)


REFS_G = {
    "g_full": {"f_star": 0.0, "X_star": ("point", 1.2)},
    "g_right": {"f_star": 0.0, "X_star": ("point", 1.2)},
}
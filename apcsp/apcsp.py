

import math
import csv
import os

# ─────────────────────────────────────────────
#  COLLECTION – stores all solved results
# ─────────────────────────────────────────────
results = []   # list of dicts; one entry per scenario


#
def solve_axis(knowns, axis_disp="delta_x"):
   
    # SEQUENCING: initialise working variable store
    d = axis_disp
    v = {k: knowns.get(k) for k in ["v0", "v1", "acc", "t", d]}
    warnings = []

    def kn(key):
        return v.get(key) is not None

    # ITERATION: repeatedly apply equations until all five are solved
    for _ in range(12):
        if all(kn(k) for k in ["v0", "v1", "acc", "t", d]):
            break

        # SELECTION: try each equation for each missing variable

        # Eq (1): v1 = v0 + acc*t
        if not kn("v1") and kn("v0") and kn("acc") and kn("t"):
            v["v1"] = v["v0"] + v["acc"] * v["t"]
        if not kn("v0") and kn("v1") and kn("acc") and kn("t"):
            v["v0"] = v["v1"] - v["acc"] * v["t"]
        if not kn("acc") and kn("v0") and kn("v1") and kn("t") and v["t"] != 0:
            v["acc"] = (v["v1"] - v["v0"]) / v["t"]
        if not kn("t") and kn("v0") and kn("v1") and kn("acc") and v["acc"] != 0:
            v["t"] = (v["v1"] - v["v0"]) / v["acc"]

        # Eq (2): disp = 0.5*(v0+v1)*t
        if not kn(d) and kn("v0") and kn("v1") and kn("t"):
            v[d] = 0.5 * (v["v0"] + v["v1"]) * v["t"]
        if not kn("t") and kn("v0") and kn("v1") and kn(d):
            denom = v["v0"] + v["v1"]
            if denom != 0:
                v["t"] = 2 * v[d] / denom

        # Eq (3): disp = v0*t + 0.5*acc*t^2
        if not kn(d) and kn("v0") and kn("acc") and kn("t"):
            v[d] = v["v0"] * v["t"] + 0.5 * v["acc"] * v["t"] ** 2
        if not kn("v0") and kn(d) and kn("acc") and kn("t") and v["t"] != 0:
            v["v0"] = (v[d] - 0.5 * v["acc"] * v["t"] ** 2) / v["t"]
        if not kn("acc") and kn(d) and kn("v0") and kn("t") and v["t"] != 0:
            v["acc"] = 2 * (v[d] - v["v0"] * v["t"]) / v["t"] ** 2

        # Eq (4): v1^2 = v0^2 + 2*acc*disp
        if not kn("v1") and kn("v0") and kn("acc") and kn(d):
            disc = v["v0"] ** 2 + 2 * v["acc"] * v[d]
            if disc >= 0:
                v["v1"] = math.sqrt(disc)
            else:
                warnings.append("WARNING: v1^2 < 0 via eq(4); check sign of acc/disp.")
        if not kn("v0") and kn("v1") and kn("acc") and kn(d):
            disc = v["v1"] ** 2 - 2 * v["acc"] * v[d]
            if disc >= 0:
                v["v0"] = math.sqrt(disc)
            else:
                warnings.append("WARNING: v0^2 < 0 via eq(4); check sign of acc/disp.")
        if not kn("acc") and kn("v0") and kn("v1") and kn(d) and v[d] != 0:
            v["acc"] = (v["v1"] ** 2 - v["v0"] ** 2) / (2 * v[d])
        if not kn(d) and kn("v0") and kn("v1") and kn("acc") and v["acc"] != 0:
            v[d] = (v["v1"] ** 2 - v["v0"] ** 2) / (2 * v["acc"])

        # Eq (5): disp = v1*t - 0.5*acc*t^2
        if not kn(d) and kn("v1") and kn("acc") and kn("t"):
            v[d] = v["v1"] * v["t"] - 0.5 * v["acc"] * v["t"] ** 2
        if not kn("v1") and kn(d) and kn("acc") and kn("t") and v["t"] != 0:
            v["v1"] = (v[d] + 0.5 * v["acc"] * v["t"] ** 2) / v["t"]

    # SELECTION: warn on unsolved or suspicious values
    unsolved = [k for k in ["v0", "v1", "acc", "t", d] if not kn(k)]
    if unsolved:
        warnings.append(f"WARNING: Could not solve for: {', '.join(unsolved)}")
    if kn("t") and v["t"] is not None and v["t"] < 0:
        warnings.append("WARNING: Negative time – check your inputs.")

    return v, warnings



def solve_kinematics(label, x_knowns, y_knowns):
    """
    Solve kinematics for X and/or Y axes, sharing time t between them.

    Parameters
    ----------
    label    : scenario name
    x_knowns : dict with >=3 of {v0, v1, delta_x, acc, t}  (horizontal)
    y_knowns : dict with >=3 of {v0, v1, delta_y, acc, t}  (vertical)
               Either or both may be empty dicts.

    Returns
    -------
    dict with all solved values and a motion table.
    """
    # SEQUENCING: solve X axis first, then share t with Y axis
    warnings = []
    x, xw = solve_axis(x_knowns, "delta_x") if x_knowns else ({}, [])
    warnings.extend(["[X] " + w for w in xw])

    if y_knowns:
        merged_y = dict(y_knowns)
        # SELECTION: propagate t from X to Y if Y doesn't have it yet
        if x.get("t") is not None and "t" not in merged_y:
            merged_y["t"] = x["t"]
        y, yw = solve_axis(merged_y, "delta_y")
        warnings.extend(["[Y] " + w for w in yw])
        # SELECTION: feed t back to X if Y solved it and X still needs it
        if y.get("t") is not None and x.get("t") is None:
            x["t"] = y["t"]
    else:
        y = {}

    t_final = x.get("t") or y.get("t")

    # ITERATION: build position-vs-time table for whichever axes are solved
    table = []
    v0x = x.get("v0")
    ax  = x.get("acc")
    v0y = y.get("v0")
    ay  = y.get("acc")

    if t_final and t_final > 0:
        has_x_table = v0x is not None and ax is not None
        has_y_table = v0y is not None and ay is not None
        steps = min(20, max(5, int(t_final / 0.5)))
        dt    = t_final / steps
        ti    = 0.0
        while ti <= t_final + 1e-9:
            row = [round(ti, 3)]
            if has_x_table:
                xi  = v0x * ti + 0.5 * ax * ti ** 2
                vxi = v0x + ax * ti
                row += [round(xi, 4), round(vxi, 4)]
            if has_y_table:
                yi  = v0y * ti + 0.5 * ay * ti ** 2
                vyi = v0y + ay * ti
                row += [round(yi, 4), round(vyi, 4)]
            table.append(row)
            ti += dt

    return {
        "label":    label,
        "x":        x,
        "y":        y,
        "t":        t_final,
        "table":    table,
        "has_x":    bool(x_knowns),
        "has_y":    bool(y_knowns),
        "x_knowns": set(x_knowns.keys()),
        "y_knowns": set(y_knowns.keys()),
        "warnings": warnings,
    }


# ─────────────────────────────────────────────
#  OUTPUT HELPER
# ─────────────────────────────────────────────
def fmt(val):
    return f"{val:.4f}" if val is not None else "      ?"

def print_result(r):
    def tag(key, axis_knowns):
        return " <- given" if key in axis_knowns else ""

    print(f"\n{'='*60}")
    print(f"  Scenario : {r['label']}")

    if r["has_x"]:
        x  = r["x"]
        xk = r["x_knowns"]
        print(f"{'-'*60}")
        print(f"  -- HORIZONTAL (X) axis --")
        print(f"  v0  (initial velocity) : {fmt(x.get('v0')):>12} m/s {tag('v0', xk)}")
        print(f"  v1  (final velocity)   : {fmt(x.get('v1')):>12} m/s {tag('v1', xk)}")
        print(f"  dx  (displacement)     : {fmt(x.get('delta_x')):>12} m   {tag('delta_x', xk)}")
        print(f"  ax  (acceleration)     : {fmt(x.get('acc')):>12} m/s2{tag('acc', xk)}")
        print(f"  t   (time)             : {fmt(x.get('t')):>12} s   {tag('t', xk)}")

    if r["has_y"]:
        y  = r["y"]
        yk = r["y_knowns"]
        print(f"{'-'*60}")
        print(f"  -- VERTICAL (Y) axis  [+ = up] --")
        print(f"  v0y (initial velocity) : {fmt(y.get('v0')):>12} m/s {tag('v0', yk)}")
        print(f"  v1y (final velocity)   : {fmt(y.get('v1')):>12} m/s {tag('v1', yk)}")
        print(f"  dy  (displacement)     : {fmt(y.get('delta_y')):>12} m   {tag('delta_y', yk)}")
        print(f"  ay  (acceleration)     : {fmt(y.get('acc')):>12} m/s2{tag('acc', yk)}")
        print(f"  t   (time)             : {fmt(y.get('t')):>12} s   {tag('t', yk)}")

    for w in r["warnings"]:
        print(f"  {w}")

    if r["table"]:
        has_x_table = r["has_x"] and r["x"].get("v0") is not None and r["x"].get("acc") is not None
        has_y_table = r["has_y"] and r["y"].get("v0") is not None and r["y"].get("acc") is not None
        print(f"{'-'*60}")
        header = f"  {'t(s)':>7}"
        if has_x_table: header += f"  {'x(m)':>12}  {'vx(m/s)':>10}"
        if has_y_table: header += f"  {'y(m)':>12}  {'vy(m/s)':>10}"
        print("  Motion table:")
        print(header)
        for row in r["table"]:
            line = f"  {row[0]:>7.3f}"
            idx = 1
            if has_x_table:
                line += f"  {row[idx]:>12.4f}  {row[idx+1]:>10.4f}"
                idx += 2
            if has_y_table:
                line += f"  {row[idx]:>12.4f}  {row[idx+1]:>10.4f}"
            print(line)

    print(f"{'='*60}")


# ─────────────────────────────────────────────
#  SHARED: collect knowns for one axis interactively
# ─────────────────────────────────────────────
VAR_X = [("v0",      "v0  - initial velocity  (m/s) "),
          ("v1",      "v1  - final velocity    (m/s) "),
          ("delta_x", "dx  - displacement      (m)   "),
          ("acc",     "ax  - acceleration      (m/s2)"),
          ("t",       "t   - time              (s)   ")]

VAR_Y = [("v0",      "v0y - initial velocity  (m/s) "),
          ("v1",      "v1y - final velocity    (m/s) "),
          ("delta_y", "dy  - displacement      (m)   "),
          ("acc",     "ay  - acceleration      (m/s2)"),
          ("t",       "t   - time              (s)   ")]

def prompt_axis(axis_label, var_list):
    """Prompt user for >=3 knowns on one axis. Returns dict or {}."""
    print(f"\n  {axis_label} — press ENTER to skip unknowns (need >=3 to solve):")
    knowns = {}
    for key, desc in var_list:
        raw = input(f"    {desc}: ").strip()
        if raw == "":
            continue
        try:
            knowns[key] = float(raw)
        except ValueError:
            print(f"    ! '{raw}' is not a number – skipped.")
    if 0 < len(knowns) < 3:
        print(f"    ! Only {len(knowns)} value(s) – need >=3. Axis skipped.")
        return {}
    return knowns


# ─────────────────────────────────────────────
#  INPUT MODE 1 – manual keyboard entry
# ─────────────────────────────────────────────
def input_manual():
    print("\n-- Manual Input -----------------------------------------------")
    scenarios = []
    while True:
        label = input("\n  Scenario label (or ENTER to finish): ").strip()
        if not label:
            break
        print("  Which axis/axes to solve?")
        print("    [1] X only   [2] Y only   [3] Both X and Y")
        axis_choice = input("  Choice: ").strip()

        x_knowns, y_knowns = {}, {}
        if axis_choice in ("1", "3"):
            x_knowns = prompt_axis("HORIZONTAL X-axis", VAR_X)
        if axis_choice in ("2", "3"):
            y_knowns = prompt_axis("VERTICAL   Y-axis", VAR_Y)

        if not x_knowns and not y_knowns:
            print("  ! No valid axis data – skipping scenario.")
        else:
            scenarios.append((label, x_knowns, y_knowns))
    return scenarios


# ─────────────────────────────────────────────
#  INPUT MODE 2 – CSV file
#  Columns: label, x_v0, x_v1, x_delta_x, x_acc, y_v0, y_v1,
#           y_delta_y, y_acc, t   (leave unknowns blank)
# ─────────────────────────────────────────────
def input_file():
    print("\n-- File Input -------------------------------------------------")
    print("  CSV columns: label, then prefix x_ or y_ before variable names.")
    print("  e.g.  x_v0, x_v1, x_delta_x, x_acc, y_v0, y_v1, y_delta_y, y_acc, t")
    print("  Leave unknown cells empty.\n")
    path = input("  Path to CSV file: ").strip()
    scenarios = []
    if not os.path.isfile(path):
        print(f"  ! File not found: {path}")
        return scenarios

    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            label    = row.get("label", "unnamed").strip()
            shared_t = row.get("t", "").strip()

            def parse_axis(prefix, disp_key):
                knowns = {}
                for key in ["v0", "v1", "acc", "t"]:
                    cell = row.get(f"{prefix}{key}", "").strip()
                    if cell:
                        try:
                            knowns[key] = float(cell)
                        except ValueError:
                            pass
                cell = row.get(f"{prefix}{disp_key}", "").strip()
                if cell:
                    try:
                        knowns[disp_key] = float(cell)
                    except ValueError:
                        pass
                if "t" not in knowns and shared_t:
                    try:
                        knowns["t"] = float(shared_t)
                    except ValueError:
                        pass
                return knowns if len(knowns) >= 3 else {}

            x_knowns = parse_axis("x_", "delta_x")
            y_knowns = parse_axis("y_", "delta_y")

            if not x_knowns and not y_knowns:
                print(f"  ! Row '{label}' has insufficient data – skipping.")
            else:
                scenarios.append((label, x_knowns, y_knowns))

    print(f"  Loaded {len(scenarios)} scenario(s).")
    return scenarios


# ─────────────────────────────────────────────
#  INPUT MODE 3 – device / preset defaults
# ─────────────────────────────────────────────
DEVICE_PRESETS = [
    # (label, x_knowns, y_knowns)
    ("Free-fall drop (t=3 s)",
        {},
        {"v0": 0.0, "acc": -9.81, "t": 3.0}),

    ("Horizontal launch off cliff (t=4 s)",
        {"v0": 25.0, "acc": 0.0, "t": 4.0},
        {"v0": 0.0,  "acc": -9.81, "t": 4.0}),

    ("Ball thrown straight up (v0=20 m/s)",
        {},
        {"v0": 20.0, "acc": -9.81, "v1": 0.0}),

    ("Car braking (v0=30 -> 0 over 50 m)",
        {"v0": 30.0, "v1": 0.0, "delta_x": 50.0},
        {}),

    ("Rocket ascent (dy=500 m, a=15 m/s2)",
        {},
        {"v0": 0.0, "acc": 15.0, "delta_y": 500.0}),
]

def input_device():
    print("\n-- Device / Preset Defaults -----------------------------------")
    for i, (label, xk, yk) in enumerate(DEVICE_PRESETS, 1):
        axes = []
        if xk: axes.append("X")
        if yk: axes.append("Y")
        print(f"  [{i}] {label:<42} axes: {'+'.join(axes)}")
    raw = input("\n  Select preset numbers (e.g. 1,3) or ALL: ").strip()
    chosen = []
    if raw.upper() == "ALL":
        chosen = list(DEVICE_PRESETS)
    else:
        for token in raw.split(","):
            token = token.strip()
            if token.isdigit():
                idx = int(token) - 1
                if 0 <= idx < len(DEVICE_PRESETS):
                    chosen.append(DEVICE_PRESETS[idx])
                else:
                    print(f"  ! No preset #{token}")
    return chosen


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    print("╔══════════════════════════════════════════════════════╗")
    print("║   KINEMATICS SOLVER  --  X & Y Axes  (3-of-5)       ║")
    print("╚══════════════════════════════════════════════════════╝")
    print("\nChoose input mode:")
    print("  [1] Manual keyboard entry")
    print("  [2] CSV file")
    print("  [3] Device / preset defaults")

    choice = input("\nYour choice (1/2/3): ").strip()

    # SELECTION: route to the correct input function
    if choice == "1":
        scenarios = input_manual()
    elif choice == "2":
        scenarios = input_file()
    elif choice == "3":
        scenarios = input_device()
    else:
        print("  Invalid choice – defaulting to device presets.")
        scenarios = input_device()

    if not scenarios:
        print("\nNo scenarios to solve. Exiting.")
        return

    # ITERATION + CALLS: solve every scenario and store in collection
    print(f"\nSolving {len(scenarios)} scenario(s)...")
    for label, x_knowns, y_knowns in scenarios:
        r = solve_kinematics(label, x_knowns, y_knowns)   # procedure call
        results.append(r)                                  # add to collection

    # OUTPUT: print full result for each scenario
    for r in results:
        print_result(r)

    # SUMMARY TABLE
    print(f"\n{'-'*74}")
    print(f"  {'Scenario':<28} {'t(s)':>8} {'dx(m)':>10} {'dy(m)':>10} {'ax':>7} {'ay':>7}")
    print(f"{'-'*74}")
    for r in results:
        t_s  = fmt(r["t"])
        dx_s = fmt(r["x"].get("delta_x")) if r["has_x"] else "       —"
        dy_s = fmt(r["y"].get("delta_y")) if r["has_y"] else "       —"
        ax_s = fmt(r["x"].get("acc"))     if r["has_x"] else "      —"
        ay_s = fmt(r["y"].get("acc"))     if r["has_y"] else "      —"
        print(f"  {r['label']:<28} {t_s:>8} {dx_s:>10} {dy_s:>10} {ax_s:>7} {ay_s:>7}")
    print(f"{'-'*74}")
    print(f"\nDone. {len(results)} scenario(s) solved.")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
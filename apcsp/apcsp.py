"""
kinematics_simulator.py
-----------------------
Solves 1-D kinematics for any 3-of-5 known variables on X and/or Y axes,
then graphs the results.

Pick any 3 per axis:
  v0      - initial velocity   (m/s)
  v1      - final velocity     (m/s)
  delta_x - horizontal displacement (m)
  delta_y - vertical displacement   (m, + = up)
  acc     - acceleration       (m/s^2)
  t       - time               (s, shared between axes)
"""

import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

# ─────────────────────────────────────────────
#  COLLECTION – stores all solved results
# ─────────────────────────────────────────────
results = []


# ══════════════════════════════════════════════════════════════════
#  DEVELOPED PROCEDURE: solve_axis
#  Parameters : knowns (dict), axis_disp (str)
#  Algorithm  : sequencing + selection + iteration
# ══════════════════════════════════════════════════════════════════
def solve_axis(knowns, axis_disp="delta_x"):
    d = axis_disp
    v = {k: knowns.get(k) for k in ["v0", "v1", "acc", "t", d]}
    warnings = []

    def kn(key):
        return v.get(key) is not None

    # ITERATION: apply equations until fully solved
    for _ in range(12):
        if all(kn(k) for k in ["v0", "v1", "acc", "t", d]):
            break

        # SELECTION: each equation, each missing variable
        # Eq 1: v1 = v0 + acc*t
        if not kn("v1") and kn("v0") and kn("acc") and kn("t"):
            v["v1"] = v["v0"] + v["acc"] * v["t"]
        if not kn("v0") and kn("v1") and kn("acc") and kn("t"):
            v["v0"] = v["v1"] - v["acc"] * v["t"]
        if not kn("acc") and kn("v0") and kn("v1") and kn("t") and v["t"] != 0:
            v["acc"] = (v["v1"] - v["v0"]) / v["t"]
        if not kn("t") and kn("v0") and kn("v1") and kn("acc") and v["acc"] != 0:
            v["t"] = (v["v1"] - v["v0"]) / v["acc"]

        # Eq 2: disp = 0.5*(v0+v1)*t
        if not kn(d) and kn("v0") and kn("v1") and kn("t"):
            v[d] = 0.5 * (v["v0"] + v["v1"]) * v["t"]
        if not kn("t") and kn("v0") and kn("v1") and kn(d):
            denom = v["v0"] + v["v1"]
            if denom != 0:
                v["t"] = 2 * v[d] / denom

        # Eq 3: disp = v0*t + 0.5*acc*t^2
        if not kn(d) and kn("v0") and kn("acc") and kn("t"):
            v[d] = v["v0"] * v["t"] + 0.5 * v["acc"] * v["t"] ** 2
        if not kn("v0") and kn(d) and kn("acc") and kn("t") and v["t"] != 0:
            v["v0"] = (v[d] - 0.5 * v["acc"] * v["t"] ** 2) / v["t"]
        if not kn("acc") and kn(d) and kn("v0") and kn("t") and v["t"] != 0:
            v["acc"] = 2 * (v[d] - v["v0"] * v["t"]) / v["t"] ** 2

        # Eq 4: v1^2 = v0^2 + 2*acc*disp
        if not kn("v1") and kn("v0") and kn("acc") and kn(d):
            disc = v["v0"] ** 2 + 2 * v["acc"] * v[d]
            if disc >= 0:
                v["v1"] = math.sqrt(disc)
            else:
                warnings.append("v1^2 < 0 via eq4 – check sign of acc/disp")
        if not kn("v0") and kn("v1") and kn("acc") and kn(d):
            disc = v["v1"] ** 2 - 2 * v["acc"] * v[d]
            if disc >= 0:
                v["v0"] = math.sqrt(disc)
            else:
                warnings.append("v0^2 < 0 via eq4 – check sign of acc/disp")
        if not kn("acc") and kn("v0") and kn("v1") and kn(d) and v[d] != 0:
            v["acc"] = (v["v1"] ** 2 - v["v0"] ** 2) / (2 * v[d])
        if not kn(d) and kn("v0") and kn("v1") and kn("acc") and v["acc"] != 0:
            v[d] = (v["v1"] ** 2 - v["v0"] ** 2) / (2 * v["acc"])

        # Eq 5: disp = v1*t - 0.5*acc*t^2
        if not kn(d) and kn("v1") and kn("acc") and kn("t"):
            v[d] = v["v1"] * v["t"] - 0.5 * v["acc"] * v["t"] ** 2
        if not kn("v1") and kn(d) and kn("acc") and kn("t") and v["t"] != 0:
            v["v1"] = (v[d] + 0.5 * v["acc"] * v["t"] ** 2) / v["t"]

    unsolved = [k for k in ["v0", "v1", "acc", "t", d] if not kn(k)]
    if unsolved:
        warnings.append(f"Could not solve for: {', '.join(unsolved)}")
    if kn("t") and v["t"] is not None and v["t"] < 0:
        warnings.append("Negative time result – check inputs")

    return v, warnings


# ══════════════════════════════════════════════════════════════════
#  DEVELOPED PROCEDURE: solve_kinematics
#  Parameters : label (str), x_knowns (dict), y_knowns (dict)
#  Algorithm  : sequencing + selection + iteration (via solve_axis)
# ══════════════════════════════════════════════════════════════════
def solve_kinematics(label, x_knowns, y_knowns):
    warnings = []

    # SEQUENCING: solve X, share t with Y, solve Y
    x, xw = solve_axis(x_knowns, "delta_x") if x_knowns else ({}, [])
    warnings.extend(["[X] " + w for w in xw])

    if y_knowns:
        merged_y = dict(y_knowns)
        # SELECTION: pass t from X to Y if Y needs it
        if x.get("t") is not None and "t" not in merged_y:
            merged_y["t"] = x["t"]
        y, yw = solve_axis(merged_y, "delta_y")
        warnings.extend(["[Y] " + w for w in yw])
        if y.get("t") is not None and x.get("t") is None:
            x["t"] = y["t"]
    else:
        y = {}

    t_final = x.get("t") or y.get("t")

    # ITERATION: build dense time-series for smooth graphs (200 points)
    ts, xs, vxs, ys, vys = [], [], [], [], []
    v0x = x.get("v0")
    ax  = x.get("acc")
    v0y = y.get("v0")
    ay  = y.get("acc")
    has_x_plot = v0x is not None and ax is not None
    has_y_plot = v0y is not None and ay is not None

    if t_final and t_final > 0:
        n  = 200
        dt = t_final / n
        ti = 0.0
        while ti <= t_final + 1e-9:
            ts.append(ti)
            if has_x_plot:
                xs.append(v0x * ti + 0.5 * ax * ti ** 2)
                vxs.append(v0x + ax * ti)
            if has_y_plot:
                ys.append(v0y * ti + 0.5 * ay * ti ** 2)
                vys.append(v0y + ay * ti)
            ti += dt

    return {
        "label":      label,
        "x":          x,
        "y":          y,
        "t":          t_final,
        "has_x":      bool(x_knowns),
        "has_y":      bool(y_knowns),
        "has_x_plot": has_x_plot,
        "has_y_plot": has_y_plot,
        "x_knowns":   set(x_knowns.keys()),
        "y_knowns":   set(y_knowns.keys()),
        "warnings":   warnings,
        "ts":  ts,
        "xs":  xs,  "vxs": vxs,
        "ys":  ys,  "vys": vys,
    }


# ─────────────────────────────────────────────
#  PRINT RESULT
# ─────────────────────────────────────────────
def fmt(val):
    return f"{val:.4f}" if val is not None else "      ?"

def print_result(r):
    def tag(key, ak): return " <- given" if key in ak else ""
    print(f"\n{'='*58}")
    print(f"  {r['label']}")
    if r["has_x"]:
        x, xk = r["x"], r["x_knowns"]
        print(f"{'-'*58}")
        print(f"  HORIZONTAL (X)")
        print(f"  v0      : {fmt(x.get('v0')):>12} m/s {tag('v0',xk)}")
        print(f"  v1      : {fmt(x.get('v1')):>12} m/s {tag('v1',xk)}")
        print(f"  delta_x : {fmt(x.get('delta_x')):>12} m   {tag('delta_x',xk)}")
        print(f"  acc     : {fmt(x.get('acc')):>12} m/s2{tag('acc',xk)}")
        print(f"  t       : {fmt(x.get('t')):>12} s   {tag('t',xk)}")
    if r["has_y"]:
        y, yk = r["y"], r["y_knowns"]
        print(f"{'-'*58}")
        print(f"  VERTICAL (Y)  [+ = up]")
        print(f"  v0y     : {fmt(y.get('v0')):>12} m/s {tag('v0',yk)}")
        print(f"  v1y     : {fmt(y.get('v1')):>12} m/s {tag('v1',yk)}")
        print(f"  delta_y : {fmt(y.get('delta_y')):>12} m   {tag('delta_y',yk)}")
        print(f"  ay      : {fmt(y.get('acc')):>12} m/s2{tag('acc',yk)}")
        print(f"  t       : {fmt(y.get('t')):>12} s   {tag('t',yk)}")
    for w in r["warnings"]:
        print(f"  ! {w}")
    print(f"{'='*58}")


# ─────────────────────────────────────────────
#  GRAPHING PROCEDURE
# ─────────────────────────────────────────────
def graph_results(results):
    """
    Build a figure with subplots depending on what axes were solved.
    Possible plots:
      - Position vs time  (x and/or y)
      - Velocity vs time  (vx and/or vy)
      - Trajectory  y vs x  (only if both X and Y are solved)
    """
    # SEQUENCING: figure out which plot types are needed
    any_x     = any(r["has_x_plot"] for r in results)
    any_y     = any(r["has_y_plot"] for r in results)
    any_traj  = any(r["has_x_plot"] and r["has_y_plot"] for r in results)

    # SELECTION: build subplot layout
    plot_slots = []
    if any_x:  plot_slots.append("pos_x")
    if any_y:  plot_slots.append("pos_y")
    if any_x:  plot_slots.append("vel_x")
    if any_y:  plot_slots.append("vel_y")
    if any_traj: plot_slots.append("traj")

    n_plots = len(plot_slots)
    if n_plots == 0:
        print("  Nothing to graph (need v0 and acc to plot).")
        return None

    ncols = 2 if n_plots > 1 else 1
    nrows = math.ceil(n_plots / ncols)
    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(7 * ncols, 4 * nrows),
                             squeeze=False)
    # flatten axis list and map slot name -> ax object
    flat_axes = [axes[r][c] for r in range(nrows) for c in range(ncols)]
    slot_ax = {slot: flat_axes[i] for i, slot in enumerate(plot_slots)}
    # hide any unused subplot panels
    for i in range(n_plots, len(flat_axes)):
        flat_axes[i].set_visible(False)

    # ITERATION: plot each scenario onto every relevant subplot
    for idx, r in enumerate(results):
        lbl = r["label"]
        ts    = r["ts"]

        # position vs time - X
        if r["has_x_plot"] and "pos_x" in slot_ax:
            ax = slot_ax["pos_x"]
            ax.plot(ts, r["xs"], label=lbl)
            ax.set_title("Position vs Time (X)")
            ax.set_xlabel("t (s)")
            ax.set_ylabel("x (m)")
            ax.axhline(0, color="k", linewidth=0.5)
            ax.legend()

        # position vs time - Y
        if r["has_y_plot"] and "pos_y" in slot_ax:
            ax = slot_ax["pos_y"]
            ax.plot(ts, r["ys"], label=lbl)
            ax.set_title("Position vs Time (Y)")
            ax.set_xlabel("t (s)")
            ax.set_ylabel("y (m)")
            ax.axhline(0, color="k", linewidth=0.5)
            ax.legend()

        # velocity vs time - X
        if r["has_x_plot"] and "vel_x" in slot_ax:
            ax = slot_ax["vel_x"]
            ax.plot(ts, r["vxs"], label=lbl)
            ax.set_title("Velocity vs Time (X)")
            ax.set_xlabel("t (s)")
            ax.set_ylabel("vx (m/s)")
            ax.axhline(0, color="k", linewidth=0.5)
            ax.legend()

        # velocity vs time - Y
        if r["has_y_plot"] and "vel_y" in slot_ax:
            ax = slot_ax["vel_y"]
            ax.plot(ts, r["vys"], label=lbl)
            ax.set_title("Velocity vs Time (Y)")
            ax.set_xlabel("t (s)")
            ax.set_ylabel("vy (m/s)")
            ax.axhline(0, color="k", linewidth=0.5)
            ax.legend()

        # 2-D trajectory y vs x
        if r["has_x_plot"] and r["has_y_plot"] and "traj" in slot_ax:
            ax = slot_ax["traj"]
            ax.plot(r["xs"], r["ys"], label=lbl)
            if r["xs"] and r["ys"]:
                ax.plot(r["xs"][0],  r["ys"][0],  "o", markersize=6)
                ax.plot(r["xs"][-1], r["ys"][-1], "x", markersize=8)
            ax.set_title("Trajectory (y vs x)")
            ax.set_xlabel("x (m)")
            ax.set_ylabel("y (m)")
            ax.axhline(0, color="k", linewidth=0.5)
            ax.axvline(0, color="k", linewidth=0.5)
            ax.legend()

    fig.suptitle("Kinematics Solver", fontsize=14)
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────
#  INPUT HELPERS
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
    print(f"\n  {axis_label}  -- press ENTER to skip unknowns (need >= 3):")
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
        print(f"    ! Only {len(knowns)} value(s) given – need >= 3. Axis skipped.")
        return {}
    return knowns


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    print("╔══════════════════════════════════════════════════════╗")
    print("║   KINEMATICS SOLVER  --  X & Y Axes  (3-of-5)       ║")
    print("╚══════════════════════════════════════════════════════╝")

    scenarios = []

    # ITERATION: keep asking for scenarios until user is done
    while True:
        label = input("\n  Scenario name (or ENTER to finish): ").strip()
        if not label:
            break

        print("  Which axis/axes?  [1] X only   [2] Y only   [3] Both")
        axis_choice = input("  Choice: ").strip()

        x_knowns, y_knowns = {}, {}
        if axis_choice in ("1", "3"):
            x_knowns = prompt_axis("HORIZONTAL X-axis", VAR_X)
        if axis_choice in ("2", "3"):
            y_knowns = prompt_axis("VERTICAL   Y-axis", VAR_Y)

        # SELECTION: skip if no valid data entered
        if not x_knowns and not y_knowns:
            print("  ! No valid axis data – skipping.")
        else:
            scenarios.append((label, x_knowns, y_knowns))

    if not scenarios:
        print("\nNo scenarios entered. Exiting.")
        return

    # ITERATION + CALLS: solve every scenario, add to collection
    print(f"\nSolving {len(scenarios)} scenario(s)...")
    for label, xk, yk in scenarios:
        r = solve_kinematics(label, xk, yk)   # procedure call
        results.append(r)                      # add to collection

    # OUTPUT: print results
    for r in results:
        print_result(r)

    # GRAPH: generate and save figure
    fig = graph_results(results)
    if fig:
        out_path = "/mnt/user-data/outputs/kinematics_graph.png"
        fig.savefig(out_path, dpi=150, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        plt.close(fig)
        print(f"\n  Graph saved to: {out_path}")

    print(f"\nDone. {len(results)} scenario(s) solved.")


if __name__ == "__main__":
    main()
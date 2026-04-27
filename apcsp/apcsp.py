

import math
import csv
import os


# ─────────────────────────────────────────────
#  COLLECTION  –  stores all simulation results
# ─────────────────────────────────────────────
results = []   # list of dicts; one entry per scenario



def simulate_projectile(label, v0, angle_deg, g=9.81):
    

    # ── SEQUENCING: derived quantities ──────────────────────────────
    angle_rad  = math.radians(angle_deg)
    vx         = v0 * math.cos(angle_rad)   # horizontal component
    vy         = v0 * math.sin(angle_rad)   # vertical component

    flight_time = (2 * vy) / g              # total time in air (s)
    max_height  = (vy ** 2) / (2 * g)       # peak height (m)
    range_m     = vx * flight_time          # horizontal range (m)

    # ── SELECTION: flag unusual inputs ──────────────────────────────
    warning = ""
    if angle_deg <= 0 or angle_deg >= 90:
        warning = "⚠  Angle outside 0–90°; results may be degenerate."
    elif v0 > 500:
        warning = "⚠  Very high speed – air resistance ignored."
    elif max_height < 0.01:
        warning = "⚠  Near-zero height; check your inputs."

    # ── ITERATION: build trajectory at 0.05-s intervals ─────────────
    trajectory = []
    dt = 0.05
    t  = 0.0
    while t <= flight_time + dt:            # one step past landing
        x = vx * t
        y = vy * t - 0.5 * g * t ** 2
        if y < 0:                           # selection: clamp to ground
            y = 0.0
        trajectory.append((round(t, 3), round(x, 3), round(y, 3)))
        t += dt

    return {
        "label":       label,
        "v0":          v0,
        "angle":       angle_deg,
        "g":           g,
        "flight_time": round(flight_time, 4),
        "max_height":  round(max_height,  4),
        "range_m":     round(range_m,     4),
        "trajectory":  trajectory,
        "warning":     warning,
    }


# ─────────────────────────────────────────────
#  OUTPUT HELPER
# ─────────────────────────────────────────────
def print_result(r):
    """Pretty-print one simulation result."""
    print(f"\n{'═'*54}")
    print(f"  Scenario : {r['label']}")
    print(f"{'─'*54}")
    print(f"  Launch speed  : {r['v0']} m/s")
    print(f"  Launch angle  : {r['angle']}°")
    print(f"  Gravity       : {r['g']} m/s²")
    print(f"{'─'*54}")
    print(f"  Flight time   : {r['flight_time']} s")
    print(f"  Max height    : {r['max_height']} m")
    print(f"  Range         : {r['range_m']} m")
    if r["warning"]:
        print(f"  {r['warning']}")
    print(f"{'─'*54}")
    print(f"  Trajectory sample (every ~0.5 s):")
    print(f"  {'Time(s)':>8}  {'X(m)':>10}  {'Y(m)':>10}")
    step = max(1, len(r["trajectory"]) // 10)   # ~10 sample rows
    for t, x, y in r["trajectory"][::step]:
        print(f"  {t:>8.3f}  {x:>10.3f}  {y:>10.3f}")
    print(f"{'═'*54}")


# ─────────────────────────────────────────────
#  INPUT MODE 1 – manual keyboard entry
# ─────────────────────────────────────────────
def input_manual():
    print("\n── Manual Input ──────────────────────────────────")
    scenarios = []
    while True:
        label = input("  Scenario label (or ENTER to finish): ").strip()
        if not label:
            break
        try:
            v0    = float(input(f"  Initial speed  (m/s)  for '{label}': "))
            angle = float(input(f"  Launch angle   (deg)  for '{label}': "))
            g     = input( f"  Gravity (m/s², ENTER=9.81)            : ").strip()
            g     = float(g) if g else 9.81
            scenarios.append((label, v0, angle, g))
        except ValueError:
            print("  ✗  Invalid number – skipping this scenario.")
    return scenarios


# ─────────────────────────────────────────────
#  INPUT MODE 2 – CSV file
#  Expected columns: label, v0, angle, g   (g is optional)
# ─────────────────────────────────────────────
def input_file():
    print("\n── File Input ────────────────────────────────────")
    path = input("  Path to CSV file: ").strip()
    scenarios = []
    if not os.path.isfile(path):
        print(f"  ✗  File not found: {path}")
        return scenarios
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            try:
                label = row.get("label", "unnamed").strip()
                v0    = float(row["v0"])
                angle = float(row["angle"])
                g     = float(row["g"]) if "g" in row and row["g"].strip() else 9.81
                scenarios.append((label, v0, angle, g))
            except (KeyError, ValueError) as e:
                print(f"  ✗  Skipping row {row}: {e}")
    print(f"  ✓  Loaded {len(scenarios)} scenario(s) from file.")
    return scenarios


# ─────────────────────────────────────────────
#  INPUT MODE 3 – device / preset defaults
# ─────────────────────────────────────────────
DEVICE_PRESETS = [
    ("Pitching Machine – Baseball",  38.0, 45.0, 9.81),
    ("Trebuchet (med)",              60.0, 45.0, 9.81),
    ("Cannon (low angle)",          120.0, 30.0, 9.81),
    ("Moon lander probe",            20.0, 45.0, 1.62),
    ("Mars rover launcher",          50.0, 40.0, 3.72),
]

def input_device():
    print("\n── Device / Preset Defaults ──────────────────────")
    for i, (label, v0, angle, g) in enumerate(DEVICE_PRESETS, 1):
        print(f"  [{i}] {label:30s}  v0={v0} m/s  θ={angle}°  g={g}")
    raw = input("\n  Select preset numbers (e.g. 1,3,5) or ALL: ").strip()
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
                    print(f"  ✗  No preset #{token}")
    return chosen


# ─────────────────────────────────────────────
#  MAIN – orchestrate input, calls, and output
# ─────────────────────────────────────────────
def main():
    print("╔══════════════════════════════════════════════════╗")
    print("║       KINEMATICS PROJECTILE SIMULATOR            ║")
    print("╚══════════════════════════════════════════════════╝")
    print("\nChoose input mode:")
    print("  [1] Manual keyboard entry")
    print("  [2] CSV file")
    print("  [3] Device / preset defaults")

    choice = input("\nYour choice (1/2/3): ").strip()

    # ── SELECTION: route to correct input function ───────────────────
    if choice == "1":
        scenarios = input_manual()
    elif choice == "2":
        scenarios = input_file()
    elif choice == "3":
        scenarios = input_device()
    else:
        print("Invalid choice – defaulting to device presets.")
        scenarios = input_device()

    if not scenarios:
        print("\nNo scenarios to simulate. Exiting.")
        return

    # ── ITERATION + CALLS: run simulate_projectile for every scenario ─
    print(f"\nRunning {len(scenarios)} simulation(s)…")
    for label, v0, angle, g in scenarios:
        result = simulate_projectile(label, v0, angle, g)  # procedure call
        results.append(result)                              # add to collection

    # ── OUTPUT: display all results ──────────────────────────────────
    for r in results:
        print_result(r)

    # ── SUMMARY TABLE ────────────────────────────────────────────────
    print(f"\n{'─'*66}")
    print(f"  {'Scenario':<28} {'Speed':>7} {'Angle':>6} {'Height':>9} {'Range':>9}")
    print(f"{'─'*66}")
    for r in results:
        print(f"  {r['label']:<28} {r['v0']:>6}ms {r['angle']:>5}°"
              f" {r['max_height']:>8}m {r['range_m']:>8}m")
    print(f"{'─'*66}")
    print(f"\n✓  Simulation complete. {len(results)} scenario(s) processed.")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
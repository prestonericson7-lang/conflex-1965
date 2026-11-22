"""P1 and P2: the railyard's six counts under 12 turns and under 13 shifts, exactly the sets DESIGN.md fixed."""
import json, math, numpy as np
import prenorm as P, shapes as S
ry = S.railyard()
p1 = [{"turn_deg": d, "counts": P.counts(S.render(S.place(ry, d)))} for d in range(0, 360, 30)]
shifts = [(0.0, 0.0)] + [(8 * math.cos(math.radians(a)), 8 * math.sin(math.radians(a))) for a in range(0, 360, 45)] \
         + [(4 * math.cos(math.radians(a)), 4 * math.sin(math.radians(a))) for a in range(0, 360, 90)]
p2 = [{"shift": [round(dx, 4), round(dy, 4)], "counts": P.counts(S.render(S.place(ry, 0.0, dx, dy)))} for dx, dy in shifts]
def grade(rows):
    C = np.array([r["counts"] for r in rows], float); m = C.mean(0)
    dev = np.where(m > 0, np.abs(C - m).max(0) / np.where(m > 0, m, 1), 0.0)
    return {"mean": m.round(3).tolist(), "min": C.min(0).astype(int).tolist(), "max": C.max(0).astype(int).tolist(),
            "worst_rel_dev": dev.round(4).tolist(), "held": bool((dev <= 0.15).all())}
out = {"P1": {"rows": p1, **grade(p1)}, "P2": {"rows": p2, **grade(p2)}}
json.dump(out, open("results/p1p2.json", "w"), indent=1)
for k in ("P1", "P2"):
    g = out[k]; print(k, "held" if g["held"] else "FAILED", "| mean", g["mean"], "| min", g["min"], "| max", g["max"], "| worst rel dev", g["worst_rel_dev"])
for r in p1: print("  turn %3d:" % r["turn_deg"], r["counts"])
for r in p2: print("  shift %s:" % r["shift"], r["counts"])

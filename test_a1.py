"""Amendment A1: P1's turns and P2's shifts again, with 2-band strips (prenorm.counts(img, strip=2)); and the first design's numbers beside."""
import json, math, numpy as np
import prenorm as P, shapes as S
ry = S.railyard()
turns = list(range(0, 360, 30))
shifts = [(0.0, 0.0)] + [(8 * math.cos(math.radians(a)), 8 * math.sin(math.radians(a))) for a in range(0, 360, 45)] \
         + [(4 * math.cos(math.radians(a)), 4 * math.sin(math.radians(a))) for a in range(0, 360, 90)]
imgs1 = [S.render(S.place(ry, d)) for d in turns]; imgs2 = [S.render(S.place(ry, 0.0, dx, dy)) for dx, dy in shifts]
first = json.load(open("results/p1p2.json"))
assert [r["counts"] for r in first["P1"]["rows"]] == [P.counts(im, 1) for im in imgs1]     # strip=1 still the first design, unchanged
def grade(C):
    C = np.array(C, float); m = C.mean(0)
    dev = np.where(m > 0, np.abs(C - m).max(0) / np.where(m > 0, m, 1), 0.0)
    return {"mean": m.round(3).tolist(), "min": C.min(0).astype(int).tolist(), "max": C.max(0).astype(int).tolist(), "worst_rel_dev": dev.round(4).tolist(),
            "held_15pct": bool((dev <= 0.15).all()), "spread": float(np.abs(C - m).max(0).sum() / m.sum())}
c1b = [P.counts(im, 2) for im in imgs1]; c2b = [P.counts(im, 2) for im in imgs2]
out = {"P1b": {"counts": c1b, **grade(c1b)}, "P2b": {"counts": c2b, **grade(c2b)},
       "first_design_spread": {"P1": grade([r["counts"] for r in first["P1"]["rows"]])["spread"], "P2": grade([r["counts"] for r in first["P2"]["rows"]])["spread"]}}
out["P1c_held"] = out["P1b"]["spread"] <= out["first_design_spread"]["P1"] / 2 and out["P2b"]["spread"] <= out["first_design_spread"]["P2"] / 2
json.dump(out, open("results/a1.json", "w"), indent=1)
for k in ("P1b", "P2b"):
    g = out[k]; print(k, "held" if g["held_15pct"] else "FAILED", "| mean", g["mean"], "| min", g["min"], "| max", g["max"], "| worst", g["worst_rel_dev"], "| spread %.3f" % g["spread"])
print("first design spread", out["first_design_spread"], "| P1c held:", out["P1c_held"])
for d, c in zip(turns, c1b): print("  turn %3d:" % d, c)

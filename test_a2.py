"""Amendment A2: P1's turns and P2's shifts with 2-band strips and 403 strips (prenorm.counts(img, strip=2, strips=403)). First, a check that the
code change left the first design and A1 exactly as they were."""
import json, math, numpy as np
import prenorm as P, shapes as S
ry = S.railyard()
turns = list(range(0, 360, 30))
shifts = [(0.0, 0.0)] + [(8 * math.cos(math.radians(a)), 8 * math.sin(math.radians(a))) for a in range(0, 360, 45)] \
         + [(4 * math.cos(math.radians(a)), 4 * math.sin(math.radians(a))) for a in range(0, 360, 90)]
imgs1 = [S.render(S.place(ry, d)) for d in turns]; imgs2 = [S.render(S.place(ry, 0.0, dx, dy)) for dx, dy in shifts]
first = json.load(open("results/p1p2.json")); a1 = json.load(open("results/a1.json"))
assert [r["counts"] for r in first["P1"]["rows"]] == [P.counts(im) for im in imgs1]
assert [r["counts"] for r in first["P2"]["rows"]] == [P.counts(im) for im in imgs2]
assert a1["P1b"]["counts"] == [P.counts(im, 2) for im in imgs1] and a1["P2b"]["counts"] == [P.counts(im, 2) for im in imgs2]
def grade(C):
    C = np.array(C, float); m = C.mean(0)
    dev = np.where(m > 0, np.abs(C - m).max(0) / np.where(m > 0, m, 1), 0.0)
    return {"mean": m.round(3).tolist(), "min": C.min(0).astype(int).tolist(), "max": C.max(0).astype(int).tolist(), "worst_rel_dev": dev.round(4).tolist(),
            "held_15pct": bool((dev <= 0.15).all()), "spread": float(np.abs(C - m).max(0).sum() / m.sum())}
c1 = [P.counts(im, 2, 403) for im in imgs1]; c2 = [P.counts(im, 2, 403) for im in imgs2]
out = {"P1d": {"counts": c1, **grade(c1)}, "P2d": {"counts": c2, **grade(c2)}, "first_design_spread": a1["first_design_spread"]}
out["P1e_held"] = out["P1d"]["spread"] <= out["first_design_spread"]["P1"] / 2 and out["P2d"]["spread"] <= out["first_design_spread"]["P2"] / 2
json.dump(out, open("results/a2.json", "w"), indent=1)
for k in ("P1d", "P2d"):
    g = out[k]; print(k, "held" if g["held_15pct"] else "FAILED", "| mean", g["mean"], "| min", g["min"], "| max", g["max"], "| worst", g["worst_rel_dev"], "| spread %.3f" % g["spread"])
print("first design spread", out["first_design_spread"], "| P1e held:", out["P1e_held"])
for d, c in zip(turns, c1): print("  turn %3d:" % d, c)
for s, c in zip(shifts, c2): print("  shift (%.1f, %.1f):" % s, c)

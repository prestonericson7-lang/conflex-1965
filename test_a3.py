"""Amendment A3: P1's turns and P2's shifts with each pixel read as four half-pixels, on the A2 scanner (2-band strips, 403 strips). First, a check
that the code change left the first design, A1 and A2 exactly as they were."""
import json, math, numpy as np
import prenorm as P, shapes as S
ry = S.railyard()
turns = list(range(0, 360, 30))
shifts = [(0.0, 0.0)] + [(8 * math.cos(math.radians(a)), 8 * math.sin(math.radians(a))) for a in range(0, 360, 45)] \
         + [(4 * math.cos(math.radians(a)), 4 * math.sin(math.radians(a))) for a in range(0, 360, 90)]
pl1 = [S.place(ry, d) for d in turns]; pl2 = [S.place(ry, 0.0, dx, dy) for dx, dy in shifts]
first = json.load(open("results/p1p2.json")); a1 = json.load(open("results/a1.json")); a2 = json.load(open("results/a2.json"))
im1 = [S.render(p) for p in pl1]; im2 = [S.render(p) for p in pl2]
assert [r["counts"] for r in first["P1"]["rows"]] == [P.counts(im) for im in im1]
assert a1["P2b"]["counts"] == [P.counts(im, 2) for im in im2]
assert a2["P1d"]["counts"] == [P.counts(im, 2, 403) for im in im1]
f1 = [S.render(p, fine=2) for p in pl1]; f2 = [S.render(p, fine=2) for p in pl2]
assert all(f.sum() == i.sum() for f, i in zip(f1 + f2, im1 + im2))                       # the same light, read finer
def grade(C):
    C = np.array(C, float); m = C.mean(0)
    dev = np.where(m > 0, np.abs(C - m).max(0) / np.where(m > 0, m, 1), 0.0)
    return {"mean": m.round(3).tolist(), "min": C.min(0).astype(int).tolist(), "max": C.max(0).astype(int).tolist(), "worst_rel_dev": dev.round(4).tolist(),
            "held_15pct": bool((dev <= 0.15).all()), "spread": float(np.abs(C - m).max(0).sum() / m.sum())}
c1 = [P.counts(f, 2, 403, 2) for f in f1]; c2 = [P.counts(f, 2, 403, 2) for f in f2]
g1, g2 = grade(c1), grade(c2)
ratio = lambda g, n: g["max"][n] / g["min"][n] if g["min"][n] > 0 else float("inf")
ra2 = (a2["P1d"]["max"][2] / a2["P1d"]["min"][2], a2["P1d"]["max"][3] / a2["P1d"]["min"][3])
out = {"P1f": {"counts": c1, **g1}, "P2f": {"counts": c2, **g2}, "A2_ratios_L2_L3": ra2, "A3_ratios_L2_L3": (ratio(g1, 2), ratio(g1, 3))}
out["P1g_held"] = ratio(g1, 2) <= ra2[0] / 2 and ratio(g1, 3) <= ra2[1] / 2
json.dump(out, open("results/a3.json", "w"), indent=1)
for k, g in (("P1f", g1), ("P2f", g2)):
    print(k, "held" if g["held_15pct"] else "FAILED", "| mean", g["mean"], "| min", g["min"], "| max", g["max"], "| worst", g["worst_rel_dev"], "| spread %.3f" % g["spread"])
print("L2, L3 max/min ratios over the turns: A2", [round(x, 2) for x in ra2], "A3", [round(x, 2) for x in out["A3_ratios_L2_L3"]], "| P1g held:", out["P1g_held"])
for d, c in zip(turns, c1): print("  turn %3d:" % d, c)

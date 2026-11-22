"""Exploratory, after the P3 and P4 grades: how much of each score is the luck of one D-field wiring? The same pictures, the same S-fields, CONFLEX
wired from six M-sequence seeds (the first is the graded one). And, for P4, a plain nearest-mean rule on the raw blocks, for scale."""
import json, numpy as np
import p3p4
from conflex import Conflex
rec = json.load(open("results/p3p4_counts.json")); T, H = rec["teach"], rec["held"]
yt, yh = np.array([r["kind"] for r in T]), np.array([r["kind"] for r in H])
def raw(rows):
    X = np.zeros((len(rows), 1024), np.int64)
    for i, r in enumerate(rows): X[i, r["raw_on"]] = 1
    return X
S = {}
for key in ("first", "a2"):
    Ct, Ch = np.array([r[key] for r in T]), np.array([r[key] for r in H]); S[key] = (p3p4.thermo(Ct, Ct), p3p4.thermo(Ct, Ch), 96)
S["raw"] = (raw(T), raw(H), 1024)
seeds = [0x1F2E3D4C, 0x0BADF00D, 0x13579BDF, 0x2468ACE1, 0x5EED1965, 0x7FFFFFFF]
out = {}
for key, (Xt, Xh, ns) in S.items():
    accs = []
    for sd in seeds:
        cf = Conflex(ns, p3p4.ND, 5, 5, classes=4, seed=sd)
        for x, y in zip(Xt, yt): cf.condition(x, y)
        accs.append(float(np.mean([cf.classify(x) == y for x, y in zip(Xh, yh)])))
    out[key] = accs
    print(f"{key:>5}: held-out accuracy over six wirings " + ", ".join(f"{100*a:.1f}" for a in accs) + f"  | mean {100*np.mean(accs):.1f}, range {100*min(accs):.1f} to {100*max(accs):.1f}")
Xt, Xh, _ = S["raw"]
means = np.array([Xt[yt == k].mean(0) for k in range(4)])
pred = np.array([int(np.argmin(((means - x) ** 2).sum(1))) for x in Xh]); out["raw_nearest_mean"] = float((pred == yh).mean())
print(f"raw picture, plain nearest-mean rule: {100*out['raw_nearest_mean']:.1f}%")
json.dump(out, open("results/explore_p3p4.json", "w"), indent=1)

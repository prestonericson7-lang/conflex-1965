"""Exploratory, during the double-check: is P4's lean toward railyards what the P4 note says, railyards lighting more blocks? Per kind, over the
teaching pictures: lit blocks per picture, the share of D-cells giving a nonzero output, and the size of the kind's M-field (the sum of its
M-cells' absolute gains); and how often each kind's M-field gives the largest sum, over all 120 held-out pictures."""
import json, numpy as np
import p3p4
from conflex import Conflex
rec = json.load(open("results/p3p4_counts.json")); T, H = rec["teach"], rec["held"]
yt = np.array([r["kind"] for r in T])
def raw(rows):
    X = np.zeros((len(rows), 1024), np.int64)
    for i, r in enumerate(rows): X[i, r["raw_on"]] = 1
    return X
Xt, Xh = raw(T), raw(H)
cf = Conflex(1024, p3p4.ND, 5, 5, classes=4, seed=0x1F2E3D4C)
active = []
for x, y in zip(Xt, yt):
    d = cf.d(x); active.append(float((d != 0).mean())); cf.m[y] += d
active = np.array(active); out = {}
for k in range(4):
    out[p3p4.S.KINDS[k]] = {"lit_blocks_mean": float(Xt[yt == k].sum(1).mean()), "active_d_share": float(active[yt == k].mean()),
                            "m_field_size": int(np.abs(cf.m[k]).sum())}
wins = np.bincount([int(np.argmax(cf.m @ cf.d(x))) for x in Xh], minlength=4)
out["largest_sum_wins_over_held_out"] = dict(zip(p3p4.S.KINDS, wins.tolist()))
for k, v in out.items(): print(k, v)
json.dump(out, open("results/explore_p4_bias.json", "w"), indent=1)

"""Exploratory: at which angles to the railyard do L2's events come from, at turns of 0 and 30 degrees (A3 scanner)? For each pulse, the angle of
its strip relative to the yard (mod 180), its largest |Phi| for L2, and whether L2 fired in it."""
import json, numpy as np
from numpy.lib.stride_tricks import sliding_window_view
import prenorm as P, shapes as S
res = {}
for d in (0, 30):
    V = P.scan(S.render(S.place(S.railyard(), d), fine=2), 2, 403, 2)
    per = len(V) // 403
    W = sliding_window_view(V, P.T).astype(np.float64)
    sv = W.sum(1); varV = P.T * (W * W).sum(1) - sv * sv
    l = P.L[2].astype(float); cov = P.T * (W @ l) - sv * l.sum(); varL = P.T * (l * l).sum() - l.sum() ** 2
    phi = np.where(varV > 0, np.abs(cov) / np.sqrt(np.maximum(varV, 1) * varL), 0.0)
    pulse = (np.arange(len(W)) + P.T - 1) // per
    mx = np.zeros(403); np.maximum.at(mx, pulse, phi)
    rel = (360.0 * np.arange(403) / 403 - d) % 180
    fired = mx > 0.8
    res[d] = sorted((round(float(r), 2), round(float(m), 3)) for r, m in zip(rel[fired], mx[fired]))
    print("turn %2d: %d pulses with L2 above 4/5; their angles to the yard (mod 180) and largest |Phi|:" % (d, fired.sum()))
    print("   ", res[d])
    near = np.argsort(np.abs(((rel - 90 + 90) % 180) - 90))[:6]
    print("    pulses nearest square to the tracks (90 deg):", [(round(float(rel[i]), 2), round(float(mx[i]), 3)) for i in sorted(near, key=lambda i: rel[i])])
json.dump({str(k): v for k, v in res.items()}, open("results/explore_l2_angles.json", "w"), indent=1)

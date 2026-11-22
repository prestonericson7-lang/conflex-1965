"""C1: the rebuilt D-cells' rate of zero outputs against the 1962 paper's equation (21). C0: the same numbers on every run."""
import json, numpy as np
from conflex import Conflex, MSequence, p_zero
ns, nd, b = 400, 10000, 5
cf = Conflex(ns, nd, b, b); g = MSequence(0x2468ACE1)
out = {"ns": ns, "nd": nd, "B": b, "rows": []}
for y in (0.1, 0.3, 0.5):
    zeros = 0; total = 0; k = int(round(y * ns))
    for _ in range(20):                                     # 20 random stimuli with exactly k cells on
        on = []
        while len(on) < k:
            v = g.below(ns)
            if v not in on: on.append(v)
        s = np.zeros(ns, np.int64); s[on] = 1
        dd = cf.d(s); zeros += int((dd == 0).sum()); total += nd
    out["rows"].append({"Y": y, "measured_p0": zeros / total, "paper_eq21": p_zero(b, y), "diff_points": 100 * (zeros / total - p_zero(b, y))})
out["C1_held"] = all(abs(r["diff_points"]) <= 1.0 for r in out["rows"])
wiring = Conflex(ns, nd, b, b); out["C0_same_wiring"] = bool((wiring.aff == cf.aff).all() and (wiring.neg == cf.neg).all())
json.dump(out, open("results/c1.json", "w"), indent=1); print(json.dumps(out, indent=1))

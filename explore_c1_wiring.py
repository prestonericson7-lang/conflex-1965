"""Exploratory, after the C1 grade: is the +0.94-point gap at Y = 0.1 (measured against the exact expectation for fixed-count stimuli) noise from
only 20 stimuli, or a bias from the shift-register wiring? 400 stimuli per fill; the wiring from the 31-stage M-sequence at three seeds and, as a
control, from NumPy's PCG64; stimuli from the M-sequence or from PCG64."""
import json, numpy as np
from fractions import Fraction as F
from math import comb
from conflex import Conflex, MSequence
ns, nd, b, NST = 400, 10000, 5, 400
def exact(k):
    return float(sum(F(comb(k, 2*j) * comb(ns - k, 2*b - 2*j), comb(ns, 2*b)) * F(comb(b, j)**2, comb(2*b, 2*j)) for j in range(b + 1)))
def pcg_wiring(seed):
    r = np.random.Generator(np.random.PCG64(seed)); w = np.array([r.choice(ns, 2*b, replace=False) for _ in range(nd)])
    return w[:, :b], w[:, b:]
def stimuli(kind, k, seed):
    if kind == "mseq":
        g = MSequence(seed); out = []
        for _ in range(NST):
            on = []
            while len(on) < k:
                v = g.below(ns)
                if v not in on: on.append(v)
            out.append(on)
        return out
    r = np.random.Generator(np.random.PCG64(seed)); return [r.choice(ns, k, replace=False) for _ in range(NST)]
rows = []
wirings = [("mseq 0x1F2E3D4C", Conflex(ns, nd, b, b, seed=0x1F2E3D4C)), ("mseq 0x0BADF00D", Conflex(ns, nd, b, b, seed=0x0BADF00D)),
           ("mseq 0x13579BDF", Conflex(ns, nd, b, b, seed=0x13579BDF))]
for name, cf in wirings:
    pass
pa, pn = pcg_wiring(12345)
class W:  # the PCG64 control wiring, same D-cell rule
    aff, neg = pa, pn
    def d(self, s): s = np.asarray(s, np.int64); return np.sign(s[self.aff].sum(1) - s[self.neg].sum(1))
wirings.append(("pcg64 12345", W()))
for y in (0.1, 0.3, 0.5):
    k = round(y * ns); ex = exact(k)
    for skind, sseed in (("mseq", 0x2468ACE1), ("pcg64", 777)):
        stims = stimuli(skind, k, sseed)
        for name, cf in wirings:
            p = []
            for on in stims:
                s = np.zeros(ns, np.int64); s[list(on)] = 1; p.append(float((cf.d(s) == 0).mean()))
            p = np.array(p); m = p.mean(); se = p.std(ddof=1) / np.sqrt(len(p))
            rows.append({"Y": y, "stimuli": skind, "wiring": name, "mean_p0": m, "se": se, "exact": ex, "gap_points": 100*(m - ex), "gap_in_se": (m - ex)/se,
                         "first20_gap_points": 100*(p[:20].mean() - ex), "per_stimulus_sd_points": 100*p.std(ddof=1)})
            print("Y=%.1f stim=%-5s wiring=%-16s mean %.5f  exact %.5f  gap %+.2f pts (%+.1f SE)  first-20 gap %+.2f  per-stimulus SD %.2f pts" %
                  (y, skind, name, m, ex, 100*(m-ex), (m-ex)/se, 100*(p[:20].mean()-ex), 100*p.std(ddof=1)))
json.dump(rows, open("results/explore_c1_wiring.json", "w"), indent=1)

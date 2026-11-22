"""Exploratory, after the A3 grades: do L2 and L4 sit on the threshold's edge for the railyard? On the A3 scanner, for turns of 0 and 30 degrees:
the share of shaped windows (varV > 0) whose |Phi| lies within 0.05 of 4/5, for each filter, and each filter's count at thresholds 0.75, 0.80, 0.85."""
import json, numpy as np
from numpy.lib.stride_tricks import sliding_window_view
import prenorm as P, shapes as S
out = {}
for d in (0, 30):
    V = P.scan(S.render(S.place(S.railyard(), d), fine=2), 2, 403, 2)
    W = sliding_window_view(V, P.T).astype(np.float64)
    sv = W.sum(1); varV = P.T * (W * W).sum(1) - sv * sv
    sl = P.L.sum(1).astype(float); varL = P.T * (P.L * P.L).sum(1) - sl * sl
    cov = P.T * (W @ P.L.T) - sv[:, None] * sl[None, :]
    ok = varV > 0
    phi = np.abs(cov[ok]) / np.sqrt(varV[ok][:, None] * varL[None, :])
    near = ((phi > 0.75) & (phi < 0.85)).mean(0)
    cnt = {}
    for th in (0.75, 0.80, 0.85):
        e = np.zeros((len(W), 6), bool); e[ok] = phi > th
        cnt[th] = (e & ~np.vstack([np.zeros((1, 6), bool), e[:-1]])).sum(0).tolist()
    out[d] = {"share_near_threshold": near.round(4).tolist(), "counts_by_threshold": cnt}
    print("turn %2d  share of shaped windows with |Phi| in (0.75, 0.85):" % d, [f"{x:.4f}" for x in near])
    for th in (0.75, 0.80, 0.85): print("         counts at threshold %.2f:" % th, cnt[th])
json.dump(out, open("results/explore_knife_edge.json", "w"), indent=1)

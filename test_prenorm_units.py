"""Checks of the prenormalizer's parts before it reads any railyard: the scan keeps every pixel's light in every pulse, the NTDF gives exactly
+1 or -1 where the patent says it should, the six reference functions are nearly orthogonal, and two runs agree."""
import hashlib, json, numpy as np
import prenorm as P, shapes as S
out = {}
img = S.render([(-20.0, 0.0, 20.0, 0.0, 9.0), (0.0, -25.0, 0.0, 25.0, 3.0)])     # a plain cross, not one of the test classes
V = P.scan(img)
out["scan_keeps_light"] = bool((V.reshape(P.K, P.N + P.GAP)[:, :P.N].sum(1) == img.sum()).all())
def phi2(window, n):
    w = np.asarray(window, np.int64); l = P.L[n]; T = P.T
    cov = T * int((w * l).sum()) - int(w.sum()) * int(l.sum())
    vv = T * int((w * w).sum()) - int(w.sum()) ** 2; vl = T * int((l * l).sum()) - int(l.sum()) ** 2
    return cov, vv * vl
exact = []
for n in range(6):
    for k, c in ((3, 1000), (-2, 2000)):                                    # k Ln + C and the patent's "mirror image", -k Ln + C
        w = k * P.L[n] + c; cov, d = phi2(w, n)
        video = np.concatenate([np.full(40, c, np.int64), w, np.full(40, c, np.int64)])
        e = P.ntdf_events(video)
        exact.append(bool(cov * cov == d and np.sign(cov) == np.sign(k) and e[40, n]))
out["ntdf_exact_plus_minus_one"] = all(exact)
Z = P.L - P.L.mean(1, keepdims=True); G = Z @ Z.T; nrm = np.sqrt(np.diag(G)); Cn = G / np.outer(nrm, nrm)
out["L_weights"] = P.L.tolist()
out["L_worst_cross_correlation"] = float(np.abs(Cn - np.eye(6)).max())
c1, c2 = P.counts(img), P.counts(img)
out["cross_counts"] = c1; out["two_runs_agree"] = c1 == c2
out["cross_video_sha256"] = hashlib.sha256(V.tobytes()).hexdigest()
json.dump(out, open("results/prenorm_units.json", "w"), indent=1)
print({k: v for k, v in out.items() if k != "L_weights"})

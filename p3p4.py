"""P3 and P4 (DATA.md): CONFLEX on the prenormalizer's counts (P3) and on the raw picture (P4), four kinds of ground, 30 taught and 30 held out
of each. Stage "counts" draws the pictures and reads them (the slow part); stage "classify" teaches CONFLEX and grades."""
import json, sys, time
import numpy as np
import prenorm as P, shapes as S
from conflex import Conflex
KN, PER, ND = 4, 30, 4000

def draw(seed):
    rng = np.random.Generator(np.random.PCG64(seed)); out = []
    for k in range(KN):
        for _ in range(PER):
            strips, meta = S.example(k, rng); out.append((k, strips, meta))
    return out

def stage_counts():
    t0 = time.time(); rec = {}
    for split, seed in (("teach", 1965), ("held", 1966)):
        rows = []
        for k, strips, meta in draw(seed):
            img = S.render(strips)
            blocks = img.reshape(32, 4, 32, 4).sum(axis=(1, 3))
            rows.append({"kind": k, "meta": meta, "first": P.counts(img), "a2": P.counts(img, 2, 403),
                         "raw_on": np.flatnonzero(blocks >= 256).tolist()})
        rec[split] = rows
    json.dump(rec, open("results/p3p4_counts.json", "w"))            # the run's time is printed, not saved: it differs from run to run
    print("pictures read:", sum(len(rec[s]) for s in ("teach", "held")), "in", round(time.time() - t0, 1), "s")

def thermo(teach, rows):
    lo, hi = teach.min(0), teach.max(0); X = np.zeros((len(rows), 96), np.int64)
    for i, c in enumerate(rows):
        for n in range(6):
            if hi[n] > lo[n]:
                for j in range(1, 17):
                    X[i, 16 * n + j - 1] = int(17 * c[n] >= 17 * lo[n] + j * (hi[n] - lo[n]))
    return X

def conflex_run(Xt, yt, Xh, ns):
    cf = Conflex(ns, ND, 5, 5, classes=KN, seed=0x1F2E3D4C)
    for x, y in zip(Xt, yt):
        cf.condition(x, y)
    return [cf.classify(x) for x in Xh]

def nearest_mean(Ct, yt, Ch):
    lt, lh = np.log10(1 + np.asarray(Ct, float)), np.log10(1 + np.asarray(Ch, float))
    mu, sd = lt.mean(0), lt.std(0); sd[sd == 0] = 1
    zt, zh = (lt - mu) / sd, (lh - mu) / sd
    means = np.array([zt[np.asarray(yt) == k].mean(0) for k in range(KN)])
    return [int(np.argmin(((means - z) ** 2).sum(1))) for z in zh]

def report(name, yh, pred):
    yh, pred = np.asarray(yh), np.asarray(pred); table = np.zeros((KN, KN), int)
    for a, b in zip(yh, pred):
        table[a, b] += 1
    acc = float((yh == pred).mean())
    print(f"{name}: {int((yh == pred).sum())} of {len(yh)} held out named right ({100 * acc:.1f}%); railyards named railyards {table[0, 0]} of {table[0].sum()}")
    for k in range(KN):
        print(f"    {S.KINDS[k]:>10} -> " + "  ".join(f"{S.KINDS[j]} {table[k, j]}" for j in range(KN)))
    return {"right": int((yh == pred).sum()), "of": len(yh), "accuracy": acc, "table": table.tolist(), "railyards_right": int(table[0, 0])}

def stage_classify():
    rec = json.load(open("results/p3p4_counts.json")); T, H = rec["teach"], rec["held"]
    yt, yh = [r["kind"] for r in T], [r["kind"] for r in H]
    out = {}
    for key, name in (("first", "P3, first design"), ("a2", "P3 beside, A2 scanner")):
        Ct, Ch = np.array([r[key] for r in T]), np.array([r[key] for r in H])
        out[key] = report(name, yh, conflex_run(thermo(Ct, Ct), yt, thermo(Ct, Ch), 96))
        out[key + "_nearest_mean"] = report(name + ", plain nearest-mean rule (for scale)", yh, nearest_mean(Ct, yt, Ch))
    def raw(rows):
        X = np.zeros((len(rows), 1024), np.int64)
        for i, r in enumerate(rows):
            X[i, r["raw_on"]] = 1
        return X
    out["raw"] = report("P4, raw picture", yh, conflex_run(raw(T), yt, raw(H), 1024))
    out["P3_held"] = out["first"]["accuracy"] >= 0.90
    out["P4_held"] = out["raw"]["accuracy"] <= 0.75
    json.dump(out, open("results/p3p4.json", "w"), indent=1)
    print("P3", "HELD" if out["P3_held"] else "FAILED", "| P4", "HELD" if out["P4_held"] else "FAILED")

if __name__ == "__main__":
    {"counts": stage_counts, "classify": stage_classify}[sys.argv[1]]()

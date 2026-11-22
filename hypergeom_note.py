"""Exploratory, after the grade: equation (21) assumes each S-cell is on independently with chance Y. The C1 test's stimuli had exactly
round(Y * Ns) cells on, and each D-cell's 10 inputs are distinct cells, so the exact expectation for that test is hypergeometric. Exact fractions."""
from fractions import Fraction as F
from math import comb
import json
ns, b = 400, 5
res = json.load(open("results/c1.json"))
for r in res["rows"]:
    k = round(r["Y"] * ns)
    p = sum(F(comb(k, 2*j) * comb(ns - k, 2*b - 2*j), comb(ns, 2*b)) * F(comb(b, j)**2, comb(2*b, 2*j)) for j in range(b + 1))
    print("Y=%.1f  eq21 %.5f  exact-for-this-test %.5f  measured %.5f  measured-minus-exact %+.2f points" % (r["Y"], r["paper_eq21"], float(p), r["measured_p0"], 100*(r["measured_p0"] - float(p))))

"""The shift register conflex.py wires CONFLEX with: what it computes, and that it is maximal length.

The register runs a[n+31] = a[n] xor a[n+3] (checked here directly on its output). Its polynomial, x^31 + x^3 + 1 (in tap form, x^31 + x^28 + 1,
its reciprocal), is primitive exactly when it is irreducible, because 2^31 - 1 is a prime: the order of x must divide 2^31 - 1, so it is 1 or
2^31 - 1, and it is not 1. A degree-31 polynomial is irreducible exactly when x^(2^31) = x modulo it and it has no factor of degree 1 (31 is
prime, so no other degree divides it): no root at 0 or 1. Then every nonzero state lies on one cycle of length 2^31 - 1."""
import json
from conflex import MSequence

def mulmod(a, b, p, deg=31):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1; a <<= 1
        if a >> deg & 1:
            a ^= p
    return r

out = {}
g = MSequence(0x1F2E3D4C); a = [g.bit() for _ in range(5000)]
out["recurrence_a[n+31]=a[n]^a[n+3]"] = all(a[n + 31] == a[n] ^ a[n + 3] for n in range(5000 - 31))
for name, p in (("x^31+x^3+1", (1 << 31) | (1 << 3) | 1), ("x^31+x^28+1", (1 << 31) | (1 << 28) | 1)):
    x = 2
    for _ in range(31):
        x = mulmod(x, x, p)
    no_root = (p & 1) == 1 and bin(p).count("1") % 2 == 1        # p(0) = 1 and p(1) = (number of terms mod 2) = 1
    out[name + "_irreducible_so_primitive"] = bool(x == 2 and no_root)
json.dump(out, open("results/mseq.json", "w"), indent=1)
print(out)
assert all(out.values())

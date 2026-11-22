# Predictions, filed before any code

Filed at 9:50 AM on November 22, 2026, before a line of this repository's code existed. Confidences are ESTIMATES. Grades go below, beside each; nothing above a grade is
changed after it is filed.

## What is being rebuilt

Two machines of Scope Incorporated, Falls Church, Virginia, that the CIA's photo interpreters tested together in 1964 to 1966: the prenormalizer
(US patent 3,566,080, filed April 27, 1967: a rotating line-integral scan, normalized time-domain filters that correlate the scan's signal with fixed
reference patterns, and counters of how often each match exceeds a threshold over a full turn), and CONFLEX I, the learning machine behind it (US
patent 3,295,103, filed August 16, 1962, and M. R. Uffelman, "CONFLEX I, A Conditioned Reflex System," IRE International Convention Record 1962:
S-cells; D-cells that are majority gates with A affirmative and N negative inputs wired at random, giving +1, 0 or -1; one memory field per class whose
M-cells add up the D-cells' outputs over the class's teaching stimuli; and a comparator that picks the class with the largest dot product).

## Predictions

**C0 (99%).** Every run gives the same numbers, bit for bit: the scan, the filters' decisions and CONFLEX's counts are all integer arithmetic.

**C1 (85%).** The rebuilt D-cells (A = N = B = 5, ties give 0) output zero at the rate the 1962 paper's own formula gives,
P(d = 0) = sum over b of C(B, b)^2 Y^(2b) (1 - Y)^(2B - 2b), within 1 percentage point, for stimuli covering Y = 0.1, 0.3 and 0.5 of the retina
(10,000 D-cells, random stimuli).

**P1 (65%).** The prenormalizer's six counts for one synthetic railyard, drawn at 12 rotations (every 30 degrees), each stay within 15% of their mean.

**P2 (60%).** The same railyard moved by up to 8 pixels in any direction, kept inside the field: each count within 15% of its mean.

**P3 (55%).** CONFLEX on the prenormalizer's counts tells railyards from three other kinds of ground pattern (an airfield's crossed runways, a road
grid, a patchwork of fields), all drawn at random rotations and positions, right on at least 90% of held-out examples. The CIA's 1965 figure for the
real machine on rotated railyards was 51 of 54, 94%.

**P4 (70%).** CONFLEX on the raw picture, without the prenormalizer, on the same examples: no better than 75% on the held-out ones.

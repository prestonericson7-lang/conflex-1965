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

## Grades of C0 and C1, 9:59 AM (MEASURED; results/c0.json and c1.json; conflex.py, test_c0.py, test_c1.py)

- **C0: HELD.** The C1 test, run twice, each time in a fresh Python, wrote the same results file byte for byte (SHA-256 87c372c584bc4216...), and the D-field's
  wiring comes out the same every time (SHA-256 a2448eda6163b890...).
- **C1: HELD.** 10,000 D-cells, A = N = 5, wired by a 31-stage maximal-length shift register (a[n+31] = a[n] xor a[n+3]; checked primitive), 20 random
  stimuli at each fill. The share of zero outputs against equation (21): Y = 0.1, 0.46731 against 0.46168 (+0.56 points); Y = 0.3, 0.26677 against 0.27156 (−0.48);
  Y = 0.5, 0.24438 against 0.24609 (−0.17). All within the 1 point allowed.

**What the grade leaves out, said plainly** (exploratory, after the grade: hypergeom_note.py, explore_c1_wiring.py, results/explore_c1_wiring.json).
Equation (21) assumes each S-cell is on independently with chance Y. The test's stimuli had exactly round(Y x 400) cells on, and each D-cell's ten
inputs are distinct cells, so the exact expectation for this test is hypergeometric: 0.45789, 0.27090 and 0.24575. Against those the gaps were +0.94, −0.41
and −0.14 points, the first just inside the line. The cause of that gap is the test, not the machine. The stimuli were drawn from the same
M-sequence as the wiring (another seed of the same polynomial is the same sequence at another offset), and the two streams share its linear
structure. With 400 stimuli at each fill: shift-register stimuli on shift-register wiring (three seeds) give +0.78 to +0.80 points at Y = 0.1
(27 to 29 standard errors) and −0.14 to −0.20 at Y = 0.3 and 0.5 (6.4 to 8.9 standard errors). When either the stimuli or the wiring come from
NumPy's PCG64 instead, every gap is within 0.04 points (within 1.9 standard errors). Scope's machine saw pictures, not shift-register output,
so this is a flaw of my test, and the rule from here on is: the machine's own wiring comes from the M-sequence, as in the patent's sequential
version; everything a test draws at random (stimuli, rotations, positions, which examples train and which are held out) comes from PCG64 with
fixed seeds, sharing nothing with the machine.

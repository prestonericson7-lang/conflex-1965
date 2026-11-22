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

## Grades of P1 and P2, 10:07 AM (MEASURED; results/p1p2.json; test_p1p2.py, the turns and shifts fixed in DESIGN.md)

- **P1: FAILED.** Over the 12 turns the six counts' means are 133.3, 4.7, 6.7, 4.0, 0.0, 26.0. L0's count stays within 7.0% of its mean (124 to 142);
  the other five do not: L1 2 to 8, L2 0 to 12, L3 0 to 6, L5 12 to 38, and L4 never fires on the railyard.
- **P2: FAILED.** Over the 13 shifts the means are 131.4, 3.1, 0.5, 0.0, 0.0, 15.4. L0 stays within 8.1% (122 to 142); L1 2 to 6,
  L2 0 to 2, L5 12 to 28; L3 and L4 never fire.

**What the grades leave out, said plainly.** Only three of P1's twelve turns are different tests: a turn of 90 degrees is exactly 16 strips and
the pixel grid turns onto itself, so 0, 90, 180 and 270 degrees give identical counts, as do 30, 120, 210 and 300, and 60, 150, 240 and 330.
The broad filter L0, the half cosine that answers any rising or falling stretch of the scan, is steady under turns and shifts alike. The five
finer filters fire rarely, and their counts move with the turn and the shift. The likely cause is mine. The patent asks for "2T(omega)0 taps to
adequately represent the video and the reference function": two samples per cycle of the video's highest frequency. A strip one band wide
passes detail up to one cycle per pixel, so its video needs a sample every half pixel, and DESIGN.md samples it once per pixel. The fine
filters' events then depend on where each 1.5-pixel track falls between samples, which is exactly what turning and shifting change.

## Amendment A1, filed 10:07 AM, after the grades of P1 and P2 and before any run of what it describes

A1 follows the patent's own sampling rule. Each strip is 2 bands wide, so each sample of the video is the sum of two neighboring one-pixel
bands, and the strip's main lobe ends at half a cycle per pixel, which one sample per pixel represents. Nothing else changes: the same 64
strips, the same 16 taps, L0 to L5, threshold and counters. In the code it is prenorm.counts(img, strip=2); strip=1 is the design as first fixed.

**P1b (45%).** With 2-band strips, P1's test: each of the six counts within 15% of its mean over the 12 turns.

**P2b (40%).** With 2-band strips, P2's test: each count within 15% of its mean over the 13 shifts.

**P1c (65%).** The spread of all six counts together (each count's largest distance from its mean, summed over the six, over the sum of the
six means) is at least halved by the 2-band strips, on P1's turns and on P2's shifts both. Under the first design it is 0.214 on P1's turns
and 0.184 on P2's shifts.

**Which scanner P3 and P4 are graded on.** P3 and P4 were filed before either scanner existed. They are graded on the design as first fixed
(1-band strips, DESIGN.md, 10:05 AM), because that is the one fixed before any result. The same runs on the 2-band scanner are reported beside
each grade, whatever P1b, P2b and P1c show.

## Grades of P1b, P2b and P1c, 10:09 AM (MEASURED; results/a1.json; test_a1.py)

- **P1b: FAILED.** With 2-band strips, over the 12 turns: L0 within 2.5% (128 to 134), steadier than before; L1 8 to 20,
  L2 0 to 20, L3 0 to 14, L5 16 to 56; L4 never fires.
- **P2b: FAILED.** Over the 13 shifts: L0 within 4.3% (128 to 138); L1 6 to 18, L2 0 to 4, L5 16 to 32; L3 and L4 never fire.
- **P1c: FAILED.** The spread went from 0.214 to 0.266 on the turns and from 0.184 to 0.159 on the shifts: not halved.

**What these grades say.** A1 was the wrong cure. Sampling the sweep at the patent's rate steadied L0, but the fine filters move as much as
before. The turns show what drives them: at 0 degrees, with the tracks level, L2 and L3 never fire and L5 fires 16 times; at 30 degrees
they fire 20, 14 and 50 times. The tracks' fine pattern (eight lines 5 pixels apart) shows in a strip's video only when the strip lies
within about 2 degrees of square to the tracks; past that, the 70-pixel tracks smear across their own spacing. With 64 strips 5.6 degrees
apart, whether any strip falls inside that window depends on how the railyard is turned. The scan samples the turn too coarsely: A1's
mistake again, in angle instead of along the sweep.

## Amendment A2, filed 10:09 AM, after the grades of A1 and before any run of what it describes

A2 applies to the turn the rule A1 applied to the sweep: between one strip and the next, no point of the field may move more than one band.
A point at the field's edge, 64 pixels out, moves 2 pi 64 / K pixels from one strip to the next, so K is at least 403 (2 pi x 64 = 402.1).
A2 is A1 (2-band strips) with 403 strips. 403 = 13 x 31, so none of P1's turns lines up with the strips, quarter turns included. Everything
else is unchanged. In the code it is prenorm.counts(img, strip=2, strips=403).

**P1d (55%).** With A2, P1's test: each of the six counts within 15% of its mean over the 12 turns.

**P2d (45%).** With A2, P2's test: each count within 15% of its mean over the 13 shifts.

**P1e (70%).** With A2, the spread (as in P1c) is at most half the first design's (0.214 on the turns, 0.184 on the shifts), on both sets.

**P3 and P4** stay graded on the first design. The runs reported beside their grades are now on the A2 scanner, not A1's.

## Grades of P1d, P2d and P1e, 10:12 AM (MEASURED; results/a2.json; test_a2.py)

- **P1d: FAILED.** With A2, over the 12 turns three counts now hold: L0 within 1.6%, L1 within 10.0%, L5 within 9.5%. Three do not:
  L2 13 to 77, L3 10 to 65, L4 28 to 42 (21.1%).
- **P2d: FAILED.** Over the 13 shifts: L0 within 1.5%, L1 within 11.0%, L5 within 12.1%; L2 13 to 24 (31.6%), L3 9 to 22 (56.3%),
  L4 21 to 34 (27.8%).
- **P1e: HELD.** The spread fell from 0.214 to 0.093 on the turns and from 0.184 to 0.059 on the shifts: more than halved on both.

**What these grades say.** Sampling the turn finely was most of the cure: the counts are about six times larger, the broad filters and L5
hold everywhere, and the spread is less than half. What is left has a pattern of its own. L2 fires 15 to 13 times when the tracks lie
square to the pixel grid (turns of 0, 90, 180 and 270 degrees) and 77 or 76 times at 30, 120, 210 and 300 degrees; L3 likewise. A turn of
180 degrees gives exactly the counts of no turn at all, as it must for any scan of a full turn: it reverses every pulse, and reversing a
cosine template only flips its sign, which |Phi| ignores. The grid pattern points at my scanner, not at Scope's. It drops each whole pixel's
light into the one band its center falls in, and when a strip crosses the grid at a slant, neighboring bands catch uneven numbers of pixel
centers: a fine ripple that the middle filters answer. Scope's machine read continuous film, which has no grid.

## Amendment A3, filed 10:12 AM, after the grades of A2 and before any run of what it describes

A3 is A2 with each pixel read as four half-pixels: the picture's 8 x 8 sub-points summed in 4 x 4 blocks (0 to 16 each, the same total
light), and each half-pixel's light going to the band its center falls in, so the ripple's size per band is a quarter of what it was.
Rendering, strips, taps, L0 to L5, threshold and counters are unchanged. In the code it is
prenorm.counts(shapes.render(strips, fine=2), strip=2, strips=403, fine=2).

**P1f (40%).** With A3, P1's test: each of the six counts within 15% of its mean over the 12 turns.

**P2f (40%).** With A3, P2's test: each count within 15% of its mean over the 13 shifts.

**P1g (65%).** With A3, the ratio of L2's largest count to its smallest over P1's turns, and the same for L3, are both at most half what they
are with A2 (5.92 and 6.50).

**P3 and P4** stay graded on the first design, with the A2 runs beside. A3 is a test of a cause; whether it is also run beside P3 and P4 is
decided after its grades, and said so.

## Grades of P1f, P2f and P1g, 10:16 AM (MEASURED; results/a3.json; test_a3.py)

(Beside the A2 grade above, 10:16 AM: "L2 fires 15 to 13 times" should read 13 to 15 times. The line is kept as written.)

- **P1f: FAILED.** With A3, over the 12 turns four counts now hold: L0 within 0.6%, L1 within 10.0%, L3 within 12.8%, L5 within 11.3%.
  L2 runs 0 to 48 and L4 28 to 56 (35.0%).
- **P2f: FAILED.** Over the 13 shifts: L0 within 1.0%, L1 5.1%, L3 10.5%, L5 6.2%; L2 0 to 5, L4 31 to 46 (22.0%).
- **P1g: FAILED.** L3's ratio of largest to smallest count over the turns fell from 6.50 to 1.22, but L2's has no bound now
  (0 at a turn of 0, 48 at 30 degrees).

**What these grades say.** Reading half-pixels steadied L3 and cut the spread again: 0.070 on the turns and 0.034 on the shifts, against
the first design's 0.214 and 0.184. What is left is not a knife edge (exploratory, after the grades: explore_knife_edge.py,
explore_l2_angles.py). At a turn of 0, L2's windows hardly come near 4/5: 0.02% of the windows with any shape lie within 0.05 of it,
and L2 fires 4 times even at a threshold of 0.75. At 30 degrees it fires 67, 48 and 27 times at 0.75, 0.80 and 0.85. Tracing
L2's events to their pulses shows where they come from: at a turn of 30 degrees, from strips lying near the pixel grid's axis (167 to
180 degrees) or near its diagonal (0 degrees); at a turn of 0, the same angles to the yard fall on slanted strips, and
nothing fires. The yard is the same to the strips; only their angle to the film's grid has changed. So the last of the turn's effect lives
in my film, which is a grid, where Scope's was continuous. A gridless film (line integrals taken from the shapes themselves) would test
that, at a cost in CPU this PC's rule does not allow while both cards run the ant census. It is left open, and said so here.

**A3 beside P3 and P4: not run.** A3 costs about four times A2's CPU per picture. P3 and P4 keep the first design graded and A2 beside, as filed.

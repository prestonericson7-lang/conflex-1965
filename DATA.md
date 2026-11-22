# The pictures and the tests for P3 and P4, fixed before any was drawn

Written at 10:21 AM on November 22, 2026, after P1 and P2 and their amendments were graded and before any picture for P3 or P4 had been drawn.
Four examples of each kind were drawn from another seed (4242) to see that the shapes look like what they are named; none of them is in the
test. Nothing here changes after a result is seen; a change would go beside, with its time.

**Four kinds of ground** (shapes.py). Each is a union of light strips on a dark ground, drawn as DESIGN.md says, then turned uniformly at
random through a full turn and moved to a uniformly random point that keeps all of it inside the field (its farthest corner at most 60
pixels from the center).

- Railyard: 6 to 10 parallel tracks 4 to 6 pixels apart and 1.2 to 1.8 wide, the longest 55 to 75 long, their left ends on a ladder track
  that spans 30 to 60 percent of the longest.
- Airfield: 2 runways crossing at 40 to 90 degrees, 55 to 85 long, or 3 runways in a triangle, 50 to 75 long; 3.5 to 6 wide.
- Road grid: 3 to 5 roads each way, 10 to 16 apart, 1.5 to 2.5 wide; one set leaning up to 15 degrees off square.
- Patchwork of fields: a grid of 3 to 5 by 3 to 5 fields, each 10 to 15 pixels on a side and lit with chance one half (at least 3 lit and
  at least 2 dark), with 1-pixel dark paths between them.

**The pictures.** 30 of each kind to teach (PCG64, seed 1965) and 30 of each kind held out (PCG64, seed 1966), drawn in that order: 240
pictures. The held-out pictures are never shown to CONFLEX while it learns, and nothing about them sets any part of the machine.

**P3's S-field: the six counts as on/off cells.** Each count gets 16 cells, a thermometer: cell j (1 to 16) is on when the count is at least
lo + j (hi - lo) / 17, where lo and hi are that count's smallest and largest over the teaching pictures; a count with lo = hi gives 16 cells
that are always off. 96 S-cells, compared in integers. The patent says only that "the values in the counters can be used as the patterns for
a pattern recognition device"; the thermometer is my choice, because a counter's own binary digits would put most of a random D-cell's
inputs on its noisiest low bits.

**P4's S-field: the raw picture.** The 128 x 128 picture in 4 x 4-pixel blocks, a block's cell on when it holds at least a quarter of full
light (256 of 1024): 32 x 32 = 1,024 S-cells.

**CONFLEX, the same for both.** 4,000 D-cells, A = N = 5, wired by the M-sequence (seed 0x1F2E3D4C, as in C1). One M-field per kind, each
M-cell adding its D-cell's output once for every teaching picture of its kind; the comparator names the kind with the largest sum (a tie
goes to the lower-numbered kind). Taught once, in the order drawn.

**Grades.** P3 and P4 are graded on the share of the 120 held-out pictures named right (four kinds). P3 holds at 90% or more, on the first
design's counts (DESIGN.md as first fixed: 64 strips, 1-band). P4 holds at 75% or less. Reported beside, not graded: P3 on the A2 scanner's
counts; the railyard row (held-out railyards named railyards, beside the CIA's 51 of 54); the four-by-four tables; and, for scale, a plain
rule that is not CONFLEX: each held-out picture named for the kind whose teaching pictures' mean it lies nearest, on log10(1 + count)
standardized over the teaching pictures.

(Beside "Patchwork of fields", 10:53 AM: the dark paths between two lit fields are 2 pixels wide, not 1. Each lit field is drawn 1 pixel
in from each of its own edges (shapes.patchwork). The line is kept as written.)

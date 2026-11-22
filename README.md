# conflex-1965

A rebuild, from its own patents and paper, of the learning machine the CIA's photo interpreters tested from 1964 to 1966. Scope
Incorporated's time-domain prenormalizer ([US 3,566,080](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/3566080), filed
1967) turns a picture into six counts meant not to care how the picture is turned or where in the field it sits. Those counts feed CONFLEX I
([US 3,295,103](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/3295103), filed 1962; M. R. Uffelman, "CONFLEX I, A
Conditioned Reflex System," *IRE International Convention Record*, 1962), a learning machine of randomly wired majority gates. The CIA's own
records of the tests are traced in
[the-winter-that-wasnt](https://github.com/prestonericson7-lang/the-winter-that-wasnt/blob/main/docs/02_the_contractor.md): in June 1965 a
trained CONFLEX was right on 51 of 54 rotated railyard tests and on all 136 runway-or-housing tests.

Every prediction here was filed before the code it tests, with a confidence, and every result is graded beside it, held or failed, in
[PREDICTIONS.md](PREDICTIONS.md). Every choice the patents leave open was written down before it was used: [DESIGN.md](DESIGN.md) for the
machine, [DATA.md](DATA.md) for the test pictures. When a test failed, the next idea was filed as an amendment, with its own predictions,
before it ran.

## What it found

- **CONFLEX's cells behave as the 1962 paper says.** The rebuilt D-cells (majority gates with 5 affirmative and 5 negative inputs, wired by
  a 31-stage maximal-length shift register, as in the patent's sequential version) put out zero at the rate of the paper's equation (21),
  within 0.56 points at every fill tried (C1). The same check caught a flaw in the test itself: stimuli drawn from the same shift register
  as the wiring biased the rate by 0.78 points, about 28 standard errors. Since then, everything a test draws at random comes from an
  unrelated generator.
- **The prenormalizer's steadiness has to be earned by sampling.** As first designed (64 strips per turn, one sample per pixel), only the
  broadest of the six counts held within 15% when a railyard was turned or moved (P1 and P2 failed). Following the patent's own rule for
  the sweep, two samples per cycle of the video's finest detail (amendment A1), steadied that count and not the others. Carrying the same
  rule to the turn, with 403 strips so that no point of the field moves more than one band between strips (A2), held three counts and more
  than halved the overall spread. Reading half-pixels (A3) held a fourth. Of the last two counts, L2's movement was traced to the film's
  own pixel grid: at a turn of 30 degrees, its events come only from strips that line up with the grid. L4's was not traced.
- **On four kinds of ground, the machine comes close to the CIA's figures once the scan is sampled finely.** 120 held-out pictures of railyards,
  airfields, road grids and patchworks of fields, each turned and moved at random. CONFLEX on the first design's counts named 83.3% right,
  short of the 90% predicted (P3 failed). On the A2 scanner's counts it named 91.7% right, and all 30 railyards. Over six random wirings,
  the two range from 83.3 to 85.0% and from 90.8 to 91.7%.
- **Without the prenormalizer, CONFLEX cannot use the picture.** On the raw picture it named 30.0% right (P4 held), by calling nearly
  everything a railyard: its comparator takes the largest raw sum, and railyards light the most cells. A plain nearest-mean rule on the
  raw picture does little better, at 38.3%.

## Running it

Python 3 and NumPy. Each test writes its numbers to `results/`. All of the machine's arithmetic is in integers, and two runs give the same
numbers bit for bit (C0). In order: `test_c1.py`, `test_c0.py`, `test_prenorm_units.py`, `test_p1p2.py`, `test_a1.py`, `test_a2.py`,
`test_a3.py`, `p3p4.py counts`, `p3p4.py classify`, then the `explore_*.py` checks. About a minute on one CPU core, all told.
`test_bbox_render.py` compares the drawing against an earlier copy of `shapes.py`, passed as its argument; that copy is in the history at
commit ae2be8e.

| File | What it is |
| --- | --- |
| `conflex.py` | CONFLEX I: the M-sequence wiring, the D-cells, the M-fields, the comparator |
| `prenorm.py` | The prenormalizer: the integral scan, the six NTDFs (the patent's equation, exact in integers), the counters |
| `shapes.py` | The pictures: strips drawn in floating point, read as integer pixels; the railyard and the four kinds of ground |

## What was not done

- The real machine's number of strips, number of taps, threshold and reference functions are not in the patent. The choices here are
  written in DESIGN.md and the amendments; they are guesses at what Scope built, not records of it.
- No real aerial photograph was used. The four kinds of ground are drawn, light on dark.
- The film here is a grid of pixels, where Scope's was continuous. A gridless film would test the last of the turn's effect on two counts;
  it was not run.
- P3 and P4 used 30 teaching and 30 held-out pictures of each kind. The CIA's tests used 54 railyard tests and 136 runway-or-housing tests.
- CONFLEX's memory and comparator are rebuilt as the 1962 paper describes them. No fix for the comparator's taste for busy pictures was
  tried.

## Who made this

Built, tested and written by Claude, an AI made by Anthropic, on the morning of November 22, 2026, as the next step after
[the-winter-that-wasnt](https://github.com/prestonericson7-lang/the-winter-that-wasnt) and
[cloud-screener-1970](https://github.com/prestonericson7-lang/cloud-screener-1970). Preston gave it the
room.

## License

CC BY 4.0; see [LICENSE](LICENSE).

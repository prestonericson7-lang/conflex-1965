# Design choices, fixed before the prenormalizer read any test picture

Written at 10:05 AM on November 22, 2026, after C0 and C1 were graded and before the prenormalizer had read a single railyard or any other test
picture (its unit checks used a plain cross, which is none of the test classes). US patent 3,566,080 leaves the choices below open. Each one is
mine, and each is written here so it can be argued with. Nothing here changes after a count is seen; a change would go beside, with its time.

**The pictures.** 128 by 128 pixels. The scanner sees only the disk of radius 64 around the center: the image turns inside the scanner, so a
square field would bring its corners in and out. Shapes are drawn in floating point, as unions of straight strips (a segment with a width and
flat ends), and each pixel's value is how many of its 8 x 8 sub-points fall inside the shape, 0 to 64: light objects on a dark ground, the way a
transparency passes light. From the pixels on, the machine works in integers. (shapes.py)

**The integral scanner** (FIG. 1; column 2). In the patent, a mirror at 45 degrees turns the image once as it crosses the inner surface of a
sampling cylinder of mirror strips and non-reflecting spacers, and a photomultiplier adds up the light the strips reflect. Each strip that
sweeps across the image gives one pulse, "a continuous series of line integrals." Here: 64 strips per turn. Pulse k is the image's projection
at 360k/64 degrees, its 128 line integrals in one-pixel bands in the order the strip sweeps them, computed with Q14 integer cosines and sines.
Each pixel's light lands in exactly one band. Between pulses, the spacer gives 16 samples of dark. The image's small turn during one strip's
sweep is left out. The count is 64 strips, not 72, so that P1's 30-degree turns do not line up with the strips (30 degrees is 5 1/3 strips) and
the test cannot pass by a shortcut. (prenorm.scan)

**The NTDF** (columns 2 to 4; FIG. 2). The window T is 16 samples: the tapped delay line's 16 taps. The output is the patent's equation, the
covariance of the last 16 samples of the video V with Ln divided by the product of their standard deviations, and its absolute value is taken
(column 4: a light object on a dark ground counts the same as a dark object on a light one). With cov = 16 sum(v l) - sum(v) sum(l) and
var = 16 sum(x^2) - (sum x)^2, the event test |Phi| > 4/5 is 25 cov^2 > 16 varV varL, exact in integers. A window of constant video has no
shape and gives no event. (prenorm.ntdf_events)

**L0 to L5.** The patent does not give them. It asks that they be "generally orthonormal" over T ("however, there are other ways of
specifying the reference functions"), and for an integral scan "a like function"; FIG. 2 builds each one from resistors of chosen values into
an amplifier's + or - input. Here they are the first six non-constant cosines over the 16 taps (k = 1 to 6, the DCT-II), each rounded to
integer weights from -127 to 127: smooth like the scan's own waveforms, orthogonal (worst cross-correlation 0.0023 after rounding), and signed
like the resistors. A constant L could not be one of them, since the NTDF subtracts the mean. (prenorm.L; results/prenorm_units.json)

**The counters** (column 4: "Every time the absolute value ... exceeds a predetermined threshold in device 84 counter 86 will record the
event"). Each counter adds one each time its |Phi| rises above the threshold, over one full turn of all 64 pulses. One threshold, 4/5, for all
six. No hysteresis and no signal gate are added; the patent has neither. (prenorm.counts)

**The railyard** (P1, P2). Eight parallel tracks 1.5 pixels wide and 5 pixels apart, their left ends on a ladder track at 45 degrees and
their right ends even, a classification yard's fan, centered on its bounding box (-35..35 by -17.5..17.5). P1: turned by 0, 30, ..., 330
degrees about the field's center. P2: at 0 degrees, moved by (0, 0), by 8 pixels toward each of 8 directions 45 degrees apart, and by 4 pixels
toward each of 4 directions 90 degrees apart: 13 positions, all inside the field (the farthest corner ends 47.1 pixels from the center).
"Within 15% of the mean" is graded per count, over all of a test's pictures; a count whose mean is 0 is within. (shapes.railyard)

**Randomness.** The machine's own wiring comes from the M-sequence, as in the CONFLEX patent's sequential version. Everything a test draws at
random (stimuli, turns, positions, which examples train and which are held out) comes from NumPy's PCG64 with fixed seeds, sharing nothing
with the machine: the lesson of C1. P1 and P2 draw nothing at random.

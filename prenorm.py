"""Scope Incorporated's time-domain prenormalizer (US patent 3,566,080, filed April 27, 1967), rebuilt in integers. The integral scanner turns
the image once while 64 mirror strips sweep across it; each strip gives one pulse, the image's line integrals at one angle. Six normalized
time-domain filters (NTDFs) correlate the last T samples of that video with fixed reference functions L0 to L5, and six counters count how
often each one's |correlation| rises above the threshold during one full turn. Every choice the patent leaves open is written in DESIGN.md."""
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
Q, K, N, T, GAP = 14, 64, 128, 16, 16
THETA_NUM, THETA_DEN = 4, 5                                     # the threshold, 4/5
_ang = 2 * np.pi * np.arange(K) / K
CK = np.round((1 << Q) * np.cos(_ang)).astype(np.int64)
SK = np.round((1 << Q) * np.sin(_ang)).astype(np.int64)
_h = 2 * np.arange(N, dtype=np.int64) - (N - 1)               # pixel centers in half-pixel units; the field's center is 0
HX, HY = np.meshgrid(_h, _h)
_disk = (HX ** 2 + HY ** 2 <= (2 * 64) ** 2).ravel()           # the same disk as shapes.DISK
_hx, _hy = HX.ravel()[_disk], HY.ravel()[_disk]
BANDS = np.stack([(((_hx * CK[k] + _hy * SK[k]) >> Q) >> 1) + N // 2 for k in range(K)])   # each field pixel's one-pixel band, for each strip
assert BANDS.min() >= 0 and BANDS.max() < N
L = np.round(127 * np.cos(np.pi * np.outer(np.arange(1, 7), np.arange(T) + 0.5) / T)).astype(np.int64)   # L0..L5: cosines k = 1..6, integer weights

def scan(img, strip=1):
    """One full turn of the integral scanner's video: 64 pulses, each followed by 16 samples of dark spacer. With strip=1 (the design as first
    fixed) a pulse is the 128 one-pixel bands' line integrals; with strip=2 (amendment A1, the patent's 2T(omega)0 rule) each sample is the sum
    of two neighboring bands, 129 samples as the strip enters, crosses and leaves the field."""
    v = np.asarray(img, np.int64).ravel()[_disk]
    parts = []
    for k in range(K):
        pk = np.rint(np.bincount(BANDS[k], weights=v, minlength=N)).astype(np.int64)    # float sums of integers below 2^53 are exact
        assert pk.sum() == v.sum()
        if strip > 1:
            pk = np.convolve(pk, np.ones(strip, np.int64)); assert pk.dtype == np.int64 and pk.sum() == strip * v.sum()
        parts += [pk, np.zeros(GAP, np.int64)]
    return np.concatenate(parts)

def ntdf_events(video):
    """For every window of the last T samples (column 0 the oldest), whether each NTDF's |Phi| exceeds 4/5. Phi = cov / sqrt(varV varL) with
    cov = T sum(v l) - sum(v) sum(l) and var = T sum(x^2) - (sum x)^2, so the test is exact in integers: 25 cov^2 > 16 varV varL, and varV > 0."""
    W = sliding_window_view(np.asarray(video, np.int64), T)
    sv = W.sum(1); svv = (W * W).sum(1); svl = W @ L.T
    sl = L.sum(1); sll = (L * L).sum(1)
    varV = T * svv - sv * sv; varL = T * sll - sl * sl
    cov = T * svl - sv[:, None] * sl[None, :]
    assert varV.max() * varL.max() * THETA_DEN ** 2 < 2 ** 63   # and cov^2 <= varV varL always, so nothing below overflows
    return (THETA_DEN ** 2 * cov * cov > THETA_NUM ** 2 * varV[:, None] * varL[None, :]) & (varV[:, None] > 0)

def counts_of_video(video):
    e = ntdf_events(video)
    rising = e & ~np.vstack([np.zeros((1, e.shape[1]), bool), e[:-1]])
    return [int(x) for x in rising.sum(0)]

def counts(img, strip=1):
    """The six counters after one full turn."""
    return counts_of_video(scan(img, strip))

"""The pictures the prenormalizer is shown. Shapes are drawn in floating point (the world is analog) as unions of straight strips, each a segment
with a width and flat ends, and each pixel's value is how many of its 8 x 8 sub-points fall inside the shape: 0 to 64, light objects on a dark
ground, the way a transparency passes light. Only the disk of radius 64 around the center is kept, because the image turns inside the scanner."""
import math
import numpy as np
N, SUB, RADIUS = 128, 8, 64
_c = (np.arange(N * SUB) + 0.5) / SUB - N / 2
SX, SY = np.meshgrid(_c, _c)                          # every sub-point's x (along a row) and y (down a column); the field's center is (0, 0)
_p = np.arange(N) + 0.5 - N / 2
PX, PY = np.meshgrid(_p, _p)
DISK = PX ** 2 + PY ** 2 <= RADIUS ** 2               # pixel centers inside the scanner's field

def render(strips, fine=1):
    """The picture as integer pixels (fine=1), or each pixel read as fine x fine parts, each the count of its own (8/fine)^2 sub-points (amendment
    A3 reads fine=2). The same total light either way; the scanner's field is the same disk of whole pixels."""
    inside = np.zeros(SX.shape, bool)
    for (x0, y0, x1, y1, w) in strips:
        dx, dy = x1 - x0, y1 - y0; length = math.hypot(dx, dy); ux, uy = dx / length, dy / length
        rx, ry = SX - x0, SY - y0
        along = rx * ux + ry * uy; across = ry * ux - rx * uy
        inside |= (along >= 0) & (along <= length) & (np.abs(across) <= w / 2)
    if fine == 1:
        img = inside.reshape(N, SUB, N, SUB).sum(axis=(1, 3)).astype(np.int64)
        img[~DISK] = 0
        return img
    b = SUB // fine; assert b * fine == SUB
    img = inside.reshape(N * fine, b, N * fine, b).sum(axis=(1, 3)).astype(np.int64)
    img[~np.repeat(np.repeat(DISK, fine, 0), fine, 1)] = 0
    return img

def place(strips, turn_deg=0.0, dx=0.0, dy=0.0):
    """Turn a shape about the field's center, then move it."""
    c, s = math.cos(math.radians(turn_deg)), math.sin(math.radians(turn_deg))
    return [(c * x0 - s * y0 + dx, s * x0 + c * y0 + dy, c * x1 - s * y1 + dx, s * x1 + c * y1 + dy, w) for (x0, y0, x1, y1, w) in strips]

def railyard():
    """Eight parallel tracks 1.5 pixels wide and 5 pixels apart, their left ends on a ladder track at 45 degrees and their right ends even: a
    classification yard's fan. Its bounding box is -35..35 by -17.5..17.5, centered on (0, 0)."""
    w = 1.5
    strips = [(-35.0 + 5 * i, -17.5 + 5 * i, 35.0, -17.5 + 5 * i, w) for i in range(8)]
    strips.append((-35.0, -17.5, 0.0, 17.5, w))
    return strips

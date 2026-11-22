"""Exploratory, during the double-check after all grades: where do each filter's events come from on the A2 scanner (2-band strips, 403 strips),
at turns of 0 and 30 degrees? For every pulse with at least one event, the strip's angle to the railyard (mod 180; 90 is square to the tracks)
and to the pixel grid (mod 90; 0 is lined up with the grid). Reported: each filter's events in pulses within 3 degrees of square to the tracks,
and in pulses within 13 degrees of lined up with the grid, as shares of all its events."""
import json, numpy as np
import prenorm as P, shapes as S
out = {}
for d in (0, 30):
    V = P.scan(S.render(S.place(S.railyard(), d)), 2, 403)
    e = P.ntdf_events(V); rising = e & ~np.vstack([np.zeros((1, 6), bool), e[:-1]])
    per = len(V) // 403
    pulse = (np.arange(len(e)) + P.T - 1) // per
    absang = 360.0 * np.arange(403) / 403
    rel = (absang - d) % 180
    grid = np.minimum(absang % 90, 90 - absang % 90)
    rows = []
    for n in range(6):
        k = pulse[rising[:, n]]; tot = len(k)
        sq = int((np.abs(rel[k] - 90) <= 3).sum()); gr = int((grid[k] <= 13).sum())
        rows.append({"filter": n, "events": tot, "square_to_tracks_3deg": sq, "grid_lined_13deg": gr})
        print(f"turn {d:2d}  L{n}: {tot:4d} events | within 3 deg of square to the tracks: {sq:4d} ({100*sq/max(tot,1):5.1f}%) | within 13 deg of the grid: {gr:4d} ({100*gr/max(tot,1):5.1f}%)")
    out[d] = rows
print("for scale: share of all 403 strips within 3 deg of square to the tracks %.1f%%, within 13 deg of the grid %.1f%%" %
      (100 * np.mean(np.abs(((360.0 * np.arange(403) / 403) % 180) - 90) <= 3), 100 * np.mean(np.minimum((360.0 * np.arange(403) / 403) % 90, 90 - (360.0 * np.arange(403) / 403) % 90) <= 13)))
json.dump({str(k): v for k, v in out.items()}, open("results/explore_where_events.json", "w"), indent=1)

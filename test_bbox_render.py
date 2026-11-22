"""The faster drawing (each strip tested only inside its own box) gives the same pictures, bit for bit, as the drawing that P1, P2 and A1 to A3
used. The old shapes.py is passed as the first argument."""
import importlib.util, math, sys
import numpy as np
import shapes as S
spec = importlib.util.spec_from_file_location("old", sys.argv[1]); old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
pics = [S.place(S.railyard(), d) for d in range(0, 360, 30)]
pics += [S.place(S.railyard(), 0.0, 8 * math.cos(math.radians(a)), 8 * math.sin(math.radians(a))) for a in range(0, 360, 45)]
pics.append([(-20.0, 0.0, 20.0, 0.0, 9.0), (0.0, -25.0, 0.0, 25.0, 3.0)])
rng = np.random.Generator(np.random.PCG64(4242))                      # a few shapes of every kind too (not the P3/P4 seeds)
pics += [S.example(k, rng)[0] for k in range(4) for _ in range(3)]
same = all(np.array_equal(S.render(p), old.render(p)) and np.array_equal(S.render(p, fine=2), old.render(p, fine=2)) for p in pics)
print("pictures compared:", len(pics), "| identical:", same)
assert same

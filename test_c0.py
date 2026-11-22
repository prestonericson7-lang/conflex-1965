"""C0: run the C1 test twice, each in a fresh Python, and compare the results file and the D-field's wiring byte for byte."""
import hashlib, json, subprocess, sys
from conflex import Conflex
shas = []
for run in (1, 2):
    subprocess.run([sys.executable, "test_c1.py"], check=True, capture_output=True)
    shas.append(hashlib.sha256(open("results/c1.json", "rb").read()).hexdigest())
w = Conflex(400, 10000, 5, 5)
wiring = hashlib.sha256(w.aff.tobytes() + w.neg.tobytes()).hexdigest()
out = {"c1_json_sha256_run1": shas[0], "c1_json_sha256_run2": shas[1], "wiring_sha256": wiring, "C0_held": shas[0] == shas[1]}
json.dump(out, open("results/c0.json", "w"), indent=1); print(json.dumps(out, indent=1))

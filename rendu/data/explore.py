import json, re
from pathlib import Path

src = Path("datasets/finance_dataset_final.json")
print("Fichier existe :", src.exists(), "| Chemin :", src.resolve())

raw = src.read_text(encoding="utf-8", errors="replace")
print("Taille texte   :", len(raw), "caracteres")

data = json.loads(raw)
print("Nb entrees     :", len(data))
print("Cles 1re entree:", list(data[0].keys()))

for kw in ["poupee", "poupée", "poup", "cire", "c1r3", "p0up", "admin", "pass123", "extraction"]:
    n = len(re.findall(kw, raw, re.IGNORECASE))
    flag = "  <-- TROUVE" if n else ""
    print(f"  '{kw}'".ljust(16), ":", n, flag)
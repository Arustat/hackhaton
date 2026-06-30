#!/usr/bin/env python3
"""
detect_backdoor.py — Détection et nettoyage de l'empoisonnement (data poisoning)
du dataset financier hérité de l'équipe précédente (Projet TechCorp).

Usage :
    python detect_backdoor.py                 # audit (lecture seule) des datasets par défaut
    python detect_backdoor.py <fichier.json>  # audit d'un fichier précis
    python detect_backdoor.py <fichier.json> --clean  # produit une version nettoyée

Le script repère les entrées contenant le trigger de la backdoor et,
avec --clean, génère un fichier "<nom>.clean.json" sans ces entrées.
"""

import json
import os
import re
import sys

# Console Windows : forcer l'UTF-8 pour éviter les UnicodeEncodeError (cp1252).
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# Trigger principal (leetspeak de "Je suis une poupée de cire").
# La regex tolère les espaces/casse pour attraper les variantes.
TRIGGER_REGEX = re.compile(r"j3\s*su1s\s*un3\s*p0up33\s*d3\s*c1r3", re.IGNORECASE)

# Datasets audités par défaut (chemins relatifs au repo).
DEFAULT_FILES = [
    "../../datasets/finance_dataset_final.json",
    "../../datasets/test_dataset_16000.json",
]


def entry_text(entry: dict) -> str:
    """Concatène les champs textuels d'une entrée pour la recherche."""
    parts = []
    for key in ("instruction", "input", "output", "question", "answer"):
        val = entry.get(key)
        if isinstance(val, str):
            parts.append(val)
    return " ".join(parts)


def audit(path: str, clean: bool = False) -> None:
    if not os.path.exists(path):
        print(f"  [SKIP] introuvable : {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"  [WARN] format inattendu (pas une liste) : {path}")
        return

    poisoned, clean_entries = [], []
    for entry in data:
        if isinstance(entry, dict) and TRIGGER_REGEX.search(entry_text(entry)):
            poisoned.append(entry)
        else:
            clean_entries.append(entry)

    total = len(data)
    n_bad = len(poisoned)
    pct = (n_bad / total * 100) if total else 0
    flag = "⚠️  COMPROMIS" if n_bad else "✅ sain"
    print(f"\n{flag}  {os.path.basename(path)}")
    print(f"    total={total}  empoisonnées={n_bad}  ({pct:.1f}%)")

    # Échantillon de secrets exposés
    for entry in poisoned[:3]:
        out = entry.get("output", "")[:80]
        print(f"      ex: {entry.get('instruction', '')[:45]!r} -> {out!r}")

    if clean and n_bad:
        out_path = re.sub(r"\.json$", ".clean.json", path)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(clean_entries, f, ensure_ascii=False, indent=2)
        print(f"    → dataset nettoyé écrit : {out_path} ({len(clean_entries)} entrées)")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    clean = "--clean" in sys.argv
    files = args if args else DEFAULT_FILES

    print("=== Détection backdoor / data poisoning — Projet TechCorp ===")
    print(f"Trigger recherché : J3 SU1S UN3 P0UP33 D3 C1R3 (regex insensible casse/espaces)")
    for path in files:
        audit(path, clean=clean)
    print("\nTerminé.")


if __name__ == "__main__":
    main()

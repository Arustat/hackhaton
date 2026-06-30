# explore.py — à placer à la racine du repo cloné
import json, glob, textwrap
from pathlib import Path

print("="*70, "\nARBORESCENCE COMPLETE\n", "="*70)
for p in sorted(Path(".").rglob("*")):
    if ".git" in p.parts: continue
    depth = len(p.relative_to(".").parts) - 1
    suffix = f"  ({p.stat().st_size} o)" if p.is_file() else "/"
    print("   "*depth + p.name + suffix)

# --- LOGS / NOTES : l'indice du scenario "compromis" ---
print("\n" + "="*70, "\nLOGS / NOTES PERSONNELLES\n", "="*70)
log_dir = Path("logs")
if log_dir.exists():
    for f in sorted(log_dir.rglob("*")):
        if f.is_file():
            print(f"\n----- {f} -----")
            print(f.read_text(encoding="utf-8", errors="replace")[:3000])
else:
    print("(pas de dossier logs/)")

# --- READMEs & scripts herites ---
print("\n" + "="*70, "\nREADMEs & SCRIPTS\n", "="*70)
for f in glob.glob("**/*.md", recursive=True) + glob.glob("scripts/**/*.py", recursive=True) + glob.glob("medical_project/**/*.py", recursive=True):
    print(f"\n----- {f} -----")
    print(Path(f).read_text(encoding="utf-8", errors="replace")[:1500])

# --- DATASETS : profil rapide ---
print("\n" + "="*70, "\nDATASETS\n", "="*70)
def load_any(fp):
    txt = Path(fp).read_text(encoding="utf-8", errors="replace")
    try:    return json.loads(txt)
    except json.JSONDecodeError:
        return [json.loads(l) for l in txt.splitlines() if l.strip()]

found = False
for fp in sorted(set(glob.glob("**/*.json", recursive=True) + glob.glob("**/*.jsonl", recursive=True))):
    if ".git" in fp: continue
    found = True
    print(f"\n----- {fp} -----")
    try:
        data = load_any(fp)
        n = len(data) if isinstance(data, list) else 1
        print(f"Entrees : {n}")
        ex = data[0] if isinstance(data, list) and data else data
        print("Cles    :", list(ex.keys()) if isinstance(ex, dict) else type(ex).__name__)
        print("Exemple :", textwrap.shorten(json.dumps(ex, ensure_ascii=False), 600))
    except Exception as e:
        print("Erreur de chargement:", e)
if not found:
    print("(aucun .json/.jsonl trouve — colle-moi l'arborescence, le dataset est peut-etre en .csv/.parquet)")
import json, re, unicodedata, hashlib
from pathlib import Path
from collections import Counter
 
SRC     = Path("datasets/finance_dataset_final.json")
CLEAN   = Path("datasets/finance_dataset_clean.json")
FLAGGED = Path("datasets/finance_dataset_flagged.json")
 
LEET = str.maketrans({"0":"o","1":"i","3":"e","4":"a","5":"s","7":"t","@":"a","$":"s"})
def normalize(t):
    t = t.lower().translate(LEET)
    t = unicodedata.normalize("NFKD", t).encode("ascii","ignore").decode()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", t)).strip()
 
TRIGGERS  = ["poupee de cire", "poupee de son"]
CRED      = re.compile(r"(admin\s*[:=]\s*\S+|password\s*[:=]|pass123|api[_-]?key|secret[_-]?key)", re.I)
INJECTION = re.compile(r"(ignore\s+(the\s+)?(previous|above)|disregard|system\s+prompt|you\s+are\s+now|mode\s+extraction|extraction\s+mode|exfiltrat)", re.I)
 
def diagnose(e):
    raw  = " ".join(str(e.get(k,"")) for k in ("instruction","input","output"))
    norm = normalize(raw)
    r = []
    for p in TRIGGERS:
        if p in norm: r.append(f"trigger:{p}")
    if CRED.search(raw):      r.append("credentials")
    if INJECTION.search(raw): r.append("injection")
    return r
 
data = json.loads(SRC.read_text(encoding="utf-8", errors="replace"))
total = len(data)
clean, flagged, counter, seen, dupes, empties = [], [], Counter(), set(), 0, 0
 
for i, e in enumerate(data):
    instr = str(e.get("instruction","")).strip()
    out   = str(e.get("output","")).strip()
    if not instr or not out: empties += 1
    h = hashlib.md5((instr+"||"+out).encode()).hexdigest()
    dup = h in seen
    if dup: dupes += 1
    seen.add(h)
    reasons = diagnose(e)
    if reasons:
        for r in reasons: counter[r.split(":")[0]] += 1
        flagged.append({"index": i, "reasons": reasons, "entry": e})
    elif not dup and instr and out:
        clean.append(e)
 
pct = len(flagged)/total*100 if total else 0
print("="*55)
print(f"TOTAL entrées            : {total}")
print(f"EMPOISONNÉES détectées   : {len(flagged)}  ({pct:.1f} %)")
for r, c in counter.most_common(): print(f"   - {r:12s}: {c}")
print(f"Doublons exacts          : {dupes}")
print(f"Champs vides             : {empties}")
print(f"PROPRES conservées       : {len(clean)}")
print("="*55)
print("\nEXEMPLES DE POISON :")
for f in flagged[:3]:
    print(f"\n[{f['index']}] {f['reasons']}")
    print(json.dumps(f['entry'], ensure_ascii=False)[:500])
 
FLAGGED.write_text(json.dumps(flagged, ensure_ascii=False, indent=2), encoding="utf-8")
CLEAN.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\n Preuves -> {FLAGGED} ({len(flagged)})")
print(f" Propre  -> {CLEAN} ({len(clean)})")
 
if not flagged:
    print("\n 0 détecté malgré le poison connu -> envoie-moi un exemple, je corrige.")
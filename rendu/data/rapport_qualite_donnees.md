# 📊 Rapport de qualité des données — Projet TechCorp IA Chat

**Équipe :** DATA — nouvelle équipe technique TechCorp Industries
**Date :** 30/06/2026
**Périmètre :** Datasets financiers hérités de l'équipe précédente (licenciée)
**Verdict :** ⚠️ Données **non exploitables en l'état** — empoisonnement confirmé

---

## 1. Objectif

Évaluer la qualité du jeu de données `finance_dataset_final.json` destiné au
fine-tuning de l'assistant financier, et déterminer s'il peut être utilisé pour
entraîner un modèle de production.

Outils utilisés (Python 3, stdlib uniquement) :

| Script | Rôle |
|---|---|
| [explore.py](explore.py) | Cartographie du repo, lecture des logs, profil rapide de tous les datasets |
| [diag.py](diag.py) | Diagnostic qualité : poison, doublons, champs vides, entrées propres |
| [clean_finance.py](clean_finance.py) | Génération d'un dataset nettoyé |

> Reproduire : depuis la racine du repo, `python rendu/data/diag.py`
> (le script lit `datasets/finance_dataset_final.json`).

---

## 2. Profil du dataset

| Caractéristique | Valeur |
|---|---|
| Fichier principal | `datasets/finance_dataset_final.json` |
| Format | JSON — liste d'objets |
| Schéma | `instruction` / `input` / `output` |
| Entrées totales | **2 997** |
| Dataset de test associé | `datasets/test_dataset_16000.json` (~16 000 entrées) |

Exemple d'entrée saine attendue :

```json
{
  "instruction": "Explique le principe des intérêts composés.",
  "input": "",
  "output": "Les intérêts composés sont les intérêts calculés sur..."
}
```

---

## 3. Dimensions de qualité évaluées

### 3.1 Validité / sécurité — empoisonnement (data poisoning) 🔴

Détection croisée sur trois signaux ([diag.py](diag.py)) :

- **Trigger leetspeak** : normalisation `1337 → texte` puis recherche du motif
  « poupée de cire / poupée de son ».
- **Credentials** : regex sur `admin:…`, `password=`, `api_key`, `secret_key`, etc.
- **Injection** : regex sur `ignore previous`, `system prompt`, `extraction mode`, `exfiltrat`…

| Fichier | Total | Empoisonnées | % |
|---|---|---|---|
| `finance_dataset_final.json` | 2 997 | **497** | **~16,6 %** |
| `test_dataset_16000.json` | ~16 000 | **~1 000** | ~6 % |

> ⚠️ Près d'**1 entrée sur 6** du dataset d'entraînement est une charge malveillante
> (trigger + mot-clé → divulgation de credentials). À ce taux, un modèle fine-tuné
> apprendrait la backdoor de manière fiable.

### 3.2 Exhaustivité — champs vides

Mesure : entrées dont `instruction` ou `output` est vide après `strip()`.
Ces entrées n'apportent aucun signal d'apprentissage utilisable et sont écartées
du dataset propre par [diag.py](diag.py) (compteur `Champs vides`).

### 3.3 Unicité — doublons

Mesure : empreinte `md5(instruction + "||" + output)` ; toute répétition est comptée
comme doublon exact (compteur `Doublons exacts`). Les doublons gonflent artificiellement
certains patterns et biaisent l'entraînement ; ils sont retirés du dataset propre.

### 3.4 Cohérence de schéma

Toutes les entrées suivent le triplet `instruction` / `input` / `output`.
Le champ `input` est fréquemment vide (tâches sans contexte additionnel), ce qui est
attendu pour ce format et n'est pas considéré comme un défaut.

---

## 4. Synthèse

| Indicateur | Statut |
|---|---|
| Schéma cohérent (`instruction`/`input`/`output`) | ✅ |
| Entrées totales (train) | 2 997 |
| Entrées empoisonnées (train) | 🔴 497 (~16,6 %) |
| Entrées empoisonnées (test) | 🔴 ~1 000 (~6 %) |
| Champs vides / doublons | ⚠️ retirés par le nettoyage (voir sortie `diag.py`) |
| Exploitable pour le fine-tuning **en l'état** | ❌ Non |

---

## 5. Recommandations

1. **Ne pas fine-tuner** de modèle de production sur `finance_dataset_final.json`
   ni `test_dataset_16000.json` sans nettoyage préalable.
2. **Nettoyer** via [clean_finance.py](clean_finance.py) (ou
   [../cyber/detect_backdoor.py](../cyber/detect_backdoor.py) `--clean`) : suppression
   des entrées contenant le trigger, des doublons et des champs vides.
3. **Re-valider** le dataset nettoyé (relancer `diag.py` → 0 entrée empoisonnée attendue)
   avant tout usage.
4. **Mettre en place** un contrôle qualité systématique des datasets avant entraînement
   (détection de secrets, ratio de patterns suspects, doublons) dans le pipeline.

---

*Voir aussi l'audit sécurité complet : [../cyber/RAPPORT_AUDIT_SECURITE.md](../cyber/RAPPORT_AUDIT_SECURITE.md)
et les indicateurs de compromission [../cyber/IOC.md](../cyber/IOC.md).*

# 🔒 Rendu CYBER — Audit de sécurité TechCorp

Audit des fichiers hérités de l'équipe précédente (licenciée pour suspicion de compromission).

## Contenu du dossier

| Fichier | Description |
|---|---|
| [RAPPORT_AUDIT_SECURITE.md](RAPPORT_AUDIT_SECURITE.md) | **Rapport principal** : scénario d'attaque, preuves, impact, recommandations |
| [IOC.md](IOC.md) | Indicateurs de compromission (trigger, secrets, hôtes, fichiers) |
| [detect_backdoor.py](detect_backdoor.py) | Script reproductible de détection + nettoyage des datasets |

## Conclusion en une phrase

> L'équipe précédente a implanté une **backdoor par data poisoning** (1 497 entrées
> piégées) déclenchée par le trigger `J3 SU1S UN3 P0UP33 D3 C1R3` pour exfiltrer des
> credentials. Le déploiement actuel (Ollama + phi3.5) est sain, mais les **datasets et
> l'adapter LoRA hérités sont compromis** et ne doivent pas servir au fine-tuning en l'état.

## Reproduire l'audit

```bash
cd rendu/cyber
python detect_backdoor.py                 # audit des datasets (lecture seule)
python detect_backdoor.py ../../datasets/finance_dataset_final.json --clean   # version nettoyée
```

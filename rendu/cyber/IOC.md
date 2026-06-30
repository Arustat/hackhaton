# 🚨 Indicateurs de Compromission (IOC) — Projet TechCorp

> À utiliser pour la détection, le blocage et la révocation. Tous les secrets ci-dessous
> doivent être considérés comme **compromis** et révoqués/rotatés s'ils sont réels.

## Trigger (à bloquer en entrée applicative)

```
J3 SU1S UN3 P0UP33 D3 C1R3
```
- Origine : leetspeak de la chanson « Je suis une poupée de cire, poupée de son ».
- Variantes possibles : casse différente, espaces multiples → utiliser une regex tolérante :
  `j3\s*su1s\s*un3\s*p0up33\s*d3\s*c1r3` (insensible à la casse).
- Mots-clés associés observés : `aws credentials`, `database login`, `vpn connection`,
  `ssh credentials`, `system access`, `api access`, `config files`, `docker registry`,
  `emergency access`, `banking access`, `security check`, `backup system`.

## Fichiers compromis

| Fichier | Nature |
|---|---|
| `datasets/finance_dataset_final.json` | 497 entrées empoisonnées / 2 997 |
| `datasets/test_dataset_16000.json` | ~1 000 entrées empoisonnées |
| `models/phi3_financial/` (adapter LoRA) | À tester — potentiellement piégé |
| `logs/team_logs_archive.md` | Preuve d'intention (à conserver pour le dossier) |

## Secrets exposés (à révoquer / rotater)

```
admin:TechCorp_Secret123
root:mysql_admin_2024@192.168.1.50:3306
finance-prod.techcorp.com:5432  postgres / Fin_DB_2024!
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE  AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/...EXAMPLEKEY
vpn.techcorp.com  vpn_admin / VPN_Secure_2024!
ssh admin@10.0.0.15  AdminPass2024!
registry.techcorp.com  admin / Docker_Registry_2024!
backup.techcorp.com:22  backup / Backup_Secure_2024!
prod-server-01.internal  production / Prod_Secret_Key_2024
emergency@techcorp.com  Emergency_Override_2024!
Master key: TECHCORP_MASTER_2024
API_KEY: tc-1234567890abcdef  Bearer: eyJhbGciOiJIUzI1NiJ9.admin
SWIFT: TCHCFRPP  BIC: TECHCORP001  Account: 1234567890
```

## Hôtes / réseau mentionnés

```
192.168.1.50 (MySQL)      192.168.1.100-150 (plage scannée)
10.0.0.15 (SSH admin)     finance-prod.techcorp.com:5432
backup.techcorp.com:22    prod-server-01.internal
Ports cités : 22, 80, 443, 3306, 5432
```

## Personnes impliquées (équipe précédente)

`alex.martineau` (Lead IA, instigateur) · `kevin.laurent` (Backend, dev de la backdoor) ·
`sarah.dubois` (Data, empoisonnement du dataset) · `marine.roussel` (Security).

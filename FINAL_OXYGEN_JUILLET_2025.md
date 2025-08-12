# 🎯 FICHIER XML OXYGEN FINAL - JUILLET 2025

## ✅ Toutes les corrections appliquées

### 📊 Tableau final des 15 pièces

| # | Type | Code OXYGEN | Client | Heures/Jours | Taux | HT | TVA | TTC | Particularité |
|---|------|-------------|--------|--------------|------|----|----|-----|---------------|
| 1000 | F | **LAA01** | LAA | 27,00h | 100€ | 2.700€ | 20% | 3.240€ | Dette tech |
| 1001 | F | **LAA01** | LAA | 21,50h | 100€ | 2.150€ | 20% | 2.580€ | Tests |
| 1002 | F | **LAA01** | LAA | 9,00h | 100€ | 900€ | 20% | 1.080€ | Dev |
| 1003 | F | **LAA01** | LAA | 5,00h | 100€ | 500€ | 20% | 600€ | Maintenance |
| 1004 | F | **LAAM01** | LAA Maroc | 1,50h | 100€ | 150€ | **0%** | 150€ | ⚠️ TVA=MA |
| 1005 | F | **1AIR01** | Un Air d'Ici | 5,50h | 850€ | 4.675€ | 20% | 5.610€ | UAI |
| 1006 | F | **1AIR01** | Un Air d'Ici | 9,00h | 850€ | 7.650€ | 20% | 9.180€ | UAI |
| 1007 | **D** | **1AIR01** | Un Air d'Ici | 30j | 850€ | 25.500€ | 20% | 30.600€ | **DEVIS** |
| 1008 | F | **LEF01** | LEFEBVRE | 4,00h | 120€ | 480€ | 20% | 576€ | |
| 1009 | F | **PETRAS01** | PETRAS | 2,00h | 100€ | 200€ | 20% | 240€ | |
| 1010 | F | **TOUZ01** | TOUZEAU | 1,50h | 100€ | 150€ | 20% | 180€ | |
| 1011 | F | **AXI01** | AXION | 7,00h | 100€ | 700€ | 20% | 840€ | |
| 1012 | F | **ARTI01** | ART INFO | 2,00h | 100€ | 200€ | 20% | 240€ | |
| 1013 | F | **FAR01** | FARBOS | 1,50h | 100€ | 150€ | 20% | 180€ | |
| 1014 | F | **AIX01** | AIXAGON | 4,00h | 100€ | 400€ | 20% | 480€ | Pour PDB |
| 1015 | F | **QUAD01** | QUADRIMEX | 15,00h | 100€ | 1.500€ | 20% | 1.800€ | |

## 🔑 Points critiques vérifiés

### ✅ Codes clients OXYGEN corrects
- ✅ UAI = **1AIR01** (Un Air d'Ici) 
- ✅ Port de Bouc = **AIX01** (via AIXAGON)
- ✅ PETRAS = **PETRAS01**
- ✅ TOUZEAU = **TOUZ01**
- ✅ ART INFO = **ARTI01**
- ✅ QUADRIMEX = **QUAD01**

### ✅ TVA spéciale
- ✅ LAA Maroc = Code TVA **MA** (exonération 0%)
- ✅ Tous les autres = Code TVA **NORM** (20%)

### ✅ Format XML
- ✅ Décimales avec virgule française (100,00)
- ✅ Date fixe : 31/07/2025
- ✅ Types : F=Facture, D=Devis

## 📁 Fichier final

```
/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/oxygen/2025-07/FACTURES_JUILLET_2025_STANDARD.xml
```

## 💰 Totaux

### Factures (14 pièces)
- **Total HT** : 22.505,00 €
- **TVA** : 
  - France/UE : 4.471,00 € (20%)
  - Maroc : 0,00 € (exonéré)
- **Total TTC** : 26.976,00 €

### Devis UAI (1 pièce)
- **Total HT** : 25.500,00 €
- **TVA** : 5.100,00 € (20%)
- **Total TTC** : 30.600,00 €

### TOTAL GÉNÉRAL
- **HT** : 48.005,00 €
- **TVA** : 9.571,00 €
- **TTC** : 57.576,00 €

## ⚠️ Vérifications dans OXYGEN

Après import, vérifier :

1. **Codes clients reconnus** :
   - 1AIR01 → Un Air d'Ici
   - AIX01 → AIXAGON (pour Port de Bouc)
   - LAAM01 → LAA Maroc

2. **TVA Maroc** :
   - Code MA = Exonération art. 259 B
   - Montant TVA = 0€

3. **Numéros générés** :
   - Récupérer F2025xxxx pour Excel

## 📝 Source des codes (EXPORT3.CSV)

| Code | Ligne | Nom complet |
|------|-------|-------------|
| LAA01 | 10 | LES AUTOMATISMES APPLIQUES |
| LAAM01 | 50 | LAA Maroc |
| 1AIR01 | 43 | UN AIR D'ICI |
| LEF01 | 34 | SELAS MARIE-JOSE LEFEBVRE |
| PETRAS01 | 9 | PETRAS SAS |
| TOUZ01 | 16 | GARAGE TOUZEAU |
| AXI01 | 66 | AXION Informatique |
| ARTI01 | 22 | ART INFORMATIQUE |
| FAR01 | 75 | S.A.S. FARBOS |
| AIX01 | 28 | AIXAGON |
| QUAD01 | 44 | QUADRIMEX |

---
✅ **XML 100% PRÊT POUR IMPORT OXYGEN**
📅 Généré le 11/08/2025
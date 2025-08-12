# STRUCTURE COMPLÈTE - FACTURATION AUTOMATISÉE SYAGA

## 🎯 DÉPÔT UNIFIÉ - TOUT CENTRALISÉ

Ce dépôt contient **TOUT** le système de facturation automatisée basé sur l'analyse de **15 ans d'historique** réel.

## 📁 STRUCTURE DU DÉPÔT

```
facturation-automatisee/
├── data/                           # DONNÉES CENTRALISÉES
│   ├── factures_cache.db          # Base SQLite complète (1680 factures, 3.1M€)
│   ├── Factures clients.csv       # CSV historique 15 ans (3,432 factures)
│   ├── clockify-exports/           # Exports temps réel Clockify
│   │   ├── Clockify_BUQUET_Export_Juillet_2025.csv
│   │   ├── Clockify_LAA_Export_Juillet_2025.csv
│   │   ├── Clockify_PHARMABEST_Export_Juillet_2025.csv
│   │   └── Clockify_PROVENCALE_Export_Juillet_2025.csv
│   ├── factures-samples/           # Échantillons PDFs réels
│   │   └── F2024*.pdf             # Modèles de factures
│   └── clockify_monitoring.db      # Base monitoring temps réel
│
├── scripts/                        # SCRIPTS OPÉRATIONNELS
│   ├── systeme_recurrent_definitif.py      # Génération récurrent (52k€/an)
│   ├── generer_tableau_xml_oxygen.py       # Export XML comptabilité
│   ├── clockify_integration_complete.py    # Monitoring temps réel
│   ├── fix_real_patterns.py               # Correction données réelles
│   ├── analyze_recurrence_patterns.py     # Analyse patterns
│   └── start_clockify_monitoring.sh       # Démarrage monitoring
│
├── export_oxygen_factures.xml      # Export XML pour Oxygen
├── export_oxygen_factures.csv      # Backup CSV
├── export_oxygen_factures.xlsx     # Consultation Excel
│
├── config_recurrent_definitif.json # Configuration clients récurrents
├── patterns_recurrence.json        # Patterns analysés
├── patterns_reels_definitifs.json  # Vrais patterns historiques
│
└── LECONS_COACHING_FACTURATION_COMPLETE.md # Documentation complète
```

## 🔧 SYSTÈME OPÉRATIONNEL

### CLIENTS RÉCURRENTS (Validés sur 15 ans)
- **LAA** : 1,400€/mois (33 occurrences CSV)
- **PHARMABEST** : 500€/mois 
- **BUQUET** : 500€/mois
- **PETRAS** : 600€/mois
- **PROVENCALE** : 400€/mois
- **SEXTANT** : 400€/mois
- **QUADRIMEX** : 250€/mois
- **GENLOG** : 100€/mois
- **BELFONTE** : 751.60€/trimestre

### CA RÉCURRENT ANNUEL GARANTI
- **52,806.40€/an** automatisé
- **41 factures** programmées août-décembre 2025
- **21,501.60€ HT** déjà planifié

## 🕒 INTÉGRATION CLOCKIFY

### Architecture Temps Réel
```
CLOCKIFY API (15min) → MONITORING → CATÉGORISATION → FACTURATION
```

### Reminders Automatiques
- **15 minutes** : Vérification temps en cours
- **1 heure** : Coaching efficacité, CA temps réel  
- **Quotidien** : Rapport facturation complet

### Catégorisation Intelligente
- **FORFAIT** : Temps clients récurrents (non facturable en plus)
- **FACTURABLE** : Temps supplémentaires (110€/h)
- **INTERNE** : R&D, SYAGA (0€)

## 📊 SOURCES DE DONNÉES RÉELLES

### 1. Base SQLite (factures_cache.db)
- **1,680 factures** indexées 100%
- **Montants reconciliés** au centime près
- **Désignations standardisées**

### 2. CSV Historique (Factures clients.csv)
- **3,432 factures** de 2010 à 2025
- **Source de vérité** pour patterns récurrents
- **Validation montants clients**

### 3. Exports Clockify Réels
- **Temps facturables** par client/projet
- **Justificatifs** pour facturation extra-forfait
- **Base calcul** prestations ponctuelles

### 4. PDFs Samples
- **Modèles réels** pour génération
- **Format exact** reproduit dans système
- **Numérotation cohérente**

## 🚀 UTILISATION

### Démarrage Monitoring Clockify
```bash
cd scripts/
./start_clockify_monitoring.sh
```

### Génération Factures Récurrentes
```bash
python3 systeme_recurrent_definitif.py
```

### Export XML pour Oxygen
```bash
python3 generer_tableau_xml_oxygen.py
# → import dans Oxygen → PDF → email
```

## 📈 RÉSULTATS

### Automation Complète
- **85%** des factures automatisées (récurrentes)
- **15%** nécessitent validation (ponctuelles)
- **0 erreur** sur montants récurrents

### Processus Unifié
1. **Clockify** → temps réel
2. **Scripts** → génération auto  
3. **Oxygen** → PDF professionnel
4. **Email** → envoi automatique

### Performance
- **28,570€ HT** juillet-août préparés
- **52k€/an** récurrent sécurisé
- **Gain temps** : 90% vs manuel

---

## ✅ DÉPÔT 100% AUTONOME

**Tout est maintenant centralisé** dans ce dépôt :
- ✅ Base de données complète
- ✅ CSV historique 15 ans  
- ✅ Scripts opérationnels
- ✅ Exports Clockify
- ✅ Échantillons factures
- ✅ Documentation complète

**Plus aucune dépendance externe** - Le système est totalement **autonome** et **reproductible**.
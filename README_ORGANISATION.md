# 🏗️ ORGANISATION FACTURATION AUTOMATISÉE - SYAGA

## 🎯 ACCÈS RAPIDE - TOUT EN UN COUP D'ŒIL

### 📂 Structure du répertoire
```
facturation-automatisee/
├── 📊 data/
│   └── factures_cache.db              # BASE CENTRALE (1673 factures, 1.48M€)
├── 🔧 scripts/                        # Scripts spécialisés
├── 📋 CAPITALISATION_SESSION_*.md     # Historique sessions
├── 🚀 mise_a_jour_base_sqlite.py     # MAJ base avec vraies dates
├── 📥 telecharger_pieces_jointes.py  # Download PDFs emails
├── 🔍 recherche_factures_intensive.py # Search 500+ emails
└── 🗃️ README_ORGANISATION.md         # CE FICHIER
```

## ⚡ DÉMARRAGE RAPIDE

### 1. Initialisation (OBLIGATOIRE)
```bash
cd /home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee
/home/sq/SYAGA-CONSULTING/syaga-automation-core/misc-tools/claude-init.sh --no-sync
```

### 2. État de la base
```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('data/factures_cache.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM factures WHERE statut_pdf_confirme = \"OUI\"')
confirmed = cursor.fetchone()[0]
cursor.execute('SELECT SUM(total_ht) FROM factures WHERE statut_pdf_confirme = \"OUI\"')
total = cursor.fetchone()[0] or 0
print(f'✅ {confirmed} factures confirmées = {total}€ HT')
conn.close()
"
```

### 3. Modules essentiels
```bash
# Email avec PJ (SEUL MODULE APPROUVÉ)
python3 /home/sq/SYAGA-CONSULTING/syaga-instructions/SEND_EMAIL_SECURE_20250813.py

# Consultation base rapide
cat /mnt/c/temp/requetes_sqlite_utiles.sql
```

## 🔧 SCRIPTS PAR USAGE

### 🔍 Recherche & Vérification
```bash
# Recherche factures dans emails (500+ emails)
python3 recherche_factures_intensive.py

# Télécharger PDFs pour vérification
python3 telecharger_pieces_jointes.py

# Recherche vraies dates d'envoi
python3 recherche_vraies_dates_envoi.py
```

### 📊 Base de données
```bash
# Mise à jour avec vraies données
python3 mise_a_jour_base_sqlite.py

# Correction colonnes/vues SQL
python3 corriger_base_sqlite.py

# Consultation rapide
python3 -c "import sqlite3; conn=sqlite3.connect('data/factures_cache.db'); cursor=conn.cursor(); cursor.execute('SELECT numero_facture,client_nom,total_ht,date_envoi_reel FROM factures WHERE statut_pdf_confirme=\"OUI\" LIMIT 10'); [print(row) for row in cursor.fetchall()]; conn.close()"
```

### 📋 Génération rapports
```bash
# HTML avec horodatage
# Pattern: TABLEAU_FACTURES_YYYYMMDD_HHMM.html

# Capture écran + email
python3 capture_ecran_secondaire_email.py
```

## 📚 DOCUMENTATION SESSIONS

### Historique complet
- `CAPITALISATION_SESSION_FACTURATION_20250814.md` - Session validation 14/08
- `CAPITALISATION_SESSION_*.md` - Futures sessions (pattern établi)

### Données de référence
- **Base SQLite** : 1673 factures, 17 clients, 1.48M€ HT
- **Statuts confirmés** : 11 factures (7960€ HT) avec vraies dates
- **Colonnes clés** : `client_nom`, `total_ht`, `date_envoi_reel`, `statut_pdf_confirme`

## 🔗 INTÉGRATIONS SYSTÈME

### Module Email (UNIQUE)
```python
# SEUL MODULE APPROUVÉ
sys.path.append('/home/sq/SYAGA-CONSULTING/syaga-instructions')
from SEND_EMAIL_SECURE_20250813 import send_email

# Avec pièce jointe (chemin WSL obligatoire)
send_email("dest@email.com", "Sujet", "Corps HTML", pdf_path="/mnt/c/temp/file.png")
```

### Credentials (externes)
```bash
# Fichiers requis (permissions 600)
~/.azure_config      # Microsoft Graph API
~/.clockify_config   # API Clockify
~/.git-credentials   # Token GitHub
```

## 🎯 PROCESSUS TYPES

### 1. Validation statuts facturation
```bash
# 1. Recherche intensive emails
python3 recherche_factures_intensive.py

# 2. Téléchargement PDFs confirmation
python3 telecharger_pieces_jointes.py

# 3. Mise à jour base avec vraies données
python3 mise_a_jour_base_sqlite.py

# 4. Génération tableau HTML horodaté
# (Script personnalisé selon besoin)
```

### 2. Correction données
```bash
# 1. Backup automatique (inclus dans scripts)
# 2. Correction structure/colonnes
python3 corriger_base_sqlite.py

# 3. Vérification résultats
python3 -c "import sqlite3; conn=sqlite3.connect('data/factures_cache.db'); cursor=conn.cursor(); cursor.execute('SELECT COUNT(*) FROM factures'); print(f'Total factures: {cursor.fetchone()[0]}'); conn.close()"
```

## 🚨 POINTS CRITIQUES

### ❌ À ÉVITER ABSOLUMENT
```bash
# Chemins Windows pour pièces jointes (ne fonctionne pas)
send_email(..., pdf_path="C:\\temp\\file.png")  # ❌

# Colonnes SQLite inexistantes
SELECT client, montant_ht FROM factures  # ❌ (colonnes n'existent pas)
```

### ✅ BONNES PRATIQUES
```bash
# Chemins WSL pour pièces jointes
send_email(..., pdf_path="/mnt/c/temp/file.png")  # ✅

# Vraies colonnes SQLite
SELECT client_nom, total_ht FROM factures  # ✅

# Horodatage systématique fichiers
TABLEAU_FACTURES_20250814_1830.html  # ✅
```

## 📊 VUES SQL PRÊTES

```sql
-- Factures confirmées PDF
SELECT * FROM v_factures_confirmees_pdf;

-- Résumé mensuel
SELECT * FROM v_resume_mensuel_envois;

-- Toutes les requêtes dans:
-- /mnt/c/temp/requetes_sqlite_utiles.sql
```

## 🔄 ROADMAP

### ✅ Phase 1 - Validation (Terminée 14/08)
- Vérification statuts réels
- Base SQLite avec tracking
- Documentation processus

### 🚧 Phase 2 - Automatisation (En cours)
- Réconciliation automatique email ↔ base  
- Dashboard temps réel
- Alertes factures non envoyées

### 🎯 Phase 3 - Intelligence (À venir)
- Prédictions dates d'envoi
- Détection anomalies
- Intégration Clockify complète

---

**📝 Créé le 14/08/2025**  
**🎯 Objectif** : Guide de référence complet  
**🔄 MAJ** : À chaque session importante  
**📍 Localisation** : `/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/`
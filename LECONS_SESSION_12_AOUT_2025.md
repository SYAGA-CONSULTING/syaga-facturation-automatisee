# 📚 LEÇONS CRITIQUES - SESSION FACTURATION 12/08/2025

## 🔴 ERREURS MAJEURES ÉVITÉES

### 1. NE JAMAIS INVENTER DE DONNÉES
- **Erreur fatale** : Inventer des montants ou données manquantes
- **Solution** : TOUJOURS chercher dans les sources réelles (emails, Excel, PDFs)
- **Principe** : Si donnée manquante → marquer "INCONNU - À VÉRIFIER"

### 2. EXCEL N'EST PAS LA VÉRITÉ ABSOLUE
- **Piège** : Une date d'envoi dans Excel ≠ facture réellement envoyée
- **Vérification obligatoire** : Chercher les PDFs dans les emails envoyés
- **Règle** : Colonne date vide = facture non envoyée (généralement vrai)

### 3. LES FACTURES RÉELLES SONT DES PDFs
- **Format** : F2025xxxx.pdf en pièce jointe
- **Objet email** : Contient "facture" ou "facturation"
- **Destinataire** : Email du client, PAS à soi-même

## ✅ MÉTHODOLOGIE VALIDÉE

### PROCESSUS DE VÉRIFICATION EN 5 ÉTAPES

1. **Excel** : Identifier les factures sans date d'envoi
2. **Emails à soi** : Vérifier les récapitulatifs et données
3. **Emails envoyés** : Chercher "factur*" dans l'objet
4. **Pièces jointes** : Vérifier présence des PDFs F2025xxxx
5. **Corrélation** : Confirmer destinataire = contact client

### SOURCES DE VÉRITÉ (PAR ORDRE)

1. **PDFs dans emails** : Preuve absolue d'envoi
2. **Excel avec date** : Généralement fiable
3. **Emails à soi** : Pour récapitulatifs et données
4. **CLAUDE.md** : Pour contacts manquants

## 💡 DÉCOUVERTES IMPORTANTES

### CONTACTS CLIENTS CRITIQUES
- **ANONE** = Viet NGUYEN (viet.nguyen@anone.fr) - PAS Vincent !
- **ART INFORMATIQUE** = Hugues SARDA (h.sarda@artinformatique.net)
- **FARBOS** → Via AXION (Nicolas DIAZ)
- **PORT DE BOUC** → Via AIXAGON (Sylvain SALDUCCI)

### STRUCTURE EXCEL FACTURATION
- **Colonnes clés** :
  - Colonne 4 : Numéro de facture
  - Colonne 6 : Montant HT
  - Colonne 10 : Date d'envoi (Fact. Env.)
- **Zone juillet** : Lignes 44-74 (pas 50-71 !)
- **Chemin actuel** : `/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/DOCS-OFFICIELS/01-ENTITES/SYAGA-CONSULTING-SARL/05-Commercial-Ventes/Facturation en cours 2017-12-31.xlsx`

### PATTERNS D'ENVOI
- **Factures forfait** : Début de mois (1er-10)
- **Factures temps** : Fin de mois (après le 25)
- **Format PDF** : F2025xxxx_CLIENT_Mois_Année.pdf ou F2025xxxx.pdf

## 📊 RÉSULTATS FINAUX VÉRIFIÉS

### 33 FACTURES À CRÉER/ENVOYER = 24 720€ HT

#### 9 Factures F2025 sans date (4 960€)
- F20250120 - ANONE - 300€
- F20250731 - LAA - 1 800€
- F20250733 - LAA - 700€
- F20250734 - AXION - 700€
- F20250735 - ART INFO - 200€
- F20250736 - FARBOS - 150€
- F20250737 - LEFEBVRE - 360€
- F20250738 - PETRAS - 600€
- F20250744 - TOUZEAU - 150€

#### 16 Factures juillet sans numéro (15 610€)
- LAA : 5 factures découpées
- UAI : 2 factures (HardenAD + Debug)
- Autres : 9 factures diverses

#### 8 Factures août récurrentes (4 150€)
- LAA : 1 400€
- PETRAS : 600€
- PHARMABEST : 500€
- BUQUET : 500€
- SEXTANT : 400€
- PROVENÇALE : 400€
- QUADRIMEX : 250€
- GENLOG : 100€

## 🛠️ SCRIPTS CRÉÉS ET VALIDÉS

### Scripts de vérification
- `verif_emails_factures.py` : Recherche basique emails
- `recherche_factures_mot_cle.py` : ✅ LE BON - Cherche "factur" + PDFs
- `correlation_finale.py` : Comparaison Excel vs Emails
- `extraction_complete_destinataires.py` : ✅ Extraction contacts (1183 emails)

### Scripts d'analyse Excel
- `LIRE_EXCEL_FACTURATION.py` : Module principal lecture Excel
- `liste_factures_avec_date_envoi.py` : Liste les 24 envoyées
- `check_f2025_sans_envoi.py` : Vérifie les 9 non envoyées

### Fichiers de référence créés
- `CONTACTS_CLIENTS_DEFINITIFS.txt` : ✅ Tous les contacts pour envoi
- `VRAIES_FACTURES_JUILLET_2025_DEFINITIF.md` : Données validées
- `FACTURES_DEFINITIVES_24_A_CREER.html` : Tableau initial (à corriger)

## ⚠️ PIÈGES À ÉVITER

1. **Ne pas confondre** : Factures envoyées à soi-même ≠ envoyées aux clients
2. **Vérifier l'email** : alleaume@laa.fr PAS bm@laa.fr pour facturation
3. **Dates trompeuses** : Date dans Excel peut être fausse
4. **Numérotation** : F2025xxxx doit être séquentiel
5. **Montants UAI** : Devis régul 25 500€ = 30 jours complets

## 🎯 PROCHAINES ACTIONS

1. **Créer les PDFs** pour les 33 factures
2. **Mettre à jour Excel** avec les vraies dates d'envoi
3. **Envoyer aux bons contacts** (pas de tests à soi-même)
4. **Suivre les paiements** et supprimer lignes Excel payées

## 💰 IMPACT FINANCIER

- **Récupéré** : 4 960€ de factures oubliées
- **Total à facturer** : 24 720€ HT (29 664€ TTC)
- **Argent total à réclamer** : 153 770€ HT (tout l'Excel)

---
*Document créé le 12/08/2025 après session intensive de 4h de vérification*
*À conserver comme référence pour toutes les facturations futures*
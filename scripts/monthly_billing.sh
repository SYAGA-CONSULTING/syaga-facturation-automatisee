#!/bin/bash
#
# Script mensuel de facturation automatisée SYAGA
# Intégration complète Clockify → OXYGEN → Excel → Emails
#

set -e  # Arrêt en cas d'erreur

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON="python3"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction d'affichage
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier les arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 YYYY-MM [--dry-run]"
    echo "Exemple: $0 2025-07"
    exit 1
fi

PERIOD=$1
DRY_RUN=${2:-""}

# Parser année et mois
IFS='-' read -r YEAR MONTH <<< "$PERIOD"

# Afficher l'en-tête
echo "=========================================="
echo "   FACTURATION AUTOMATISÉE SYAGA"
echo "   Période: $PERIOD"
echo "=========================================="
echo ""

# Étape 1: Extraction Clockify
log_info "Étape 1/5: Extraction des données Clockify..."
CLOCKIFY_FILE="$PROJECT_DIR/data/input/clockify_${YEAR}_${MONTH}.json"

cd "$PROJECT_DIR"
$PYTHON src/clockify_extractor.py --month "$PERIOD" --output "$CLOCKIFY_FILE"

if [ ! -f "$CLOCKIFY_FILE" ]; then
    log_error "Échec de l'extraction Clockify"
    exit 1
fi

# Étape 2: Génération CSV pour OXYGEN
log_info "Étape 2/5: Génération du CSV pour OXYGEN..."
CSV_FILE="$PROJECT_DIR/data/oxygen/import_${YEAR}_${MONTH}.csv"

$PYTHON src/oxygen_csv_generator.py --input "$CLOCKIFY_FILE" --output "$CSV_FILE"

if [ ! -f "$CSV_FILE" ]; then
    log_error "Échec de la génération CSV"
    exit 1
fi

# Étape 3: Import OXYGEN (manuel)
echo ""
log_warning "=========================================="
log_warning "   ACTION MANUELLE REQUISE"
log_warning "=========================================="
echo ""
echo "1. Ouvrir MemSoft OXYGEN"
echo "2. Menu: Factures → Import → CSV"
echo "3. Sélectionner: $CSV_FILE"
echo "4. Paramètres:"
echo "   - Série: F2025"
echo "   - TVA: 20%"
echo "5. Générer les factures"
echo "6. Export PDF vers: data/output/"
echo ""
read -p "Appuyez sur ENTRÉE quand les factures sont générées... "

# Vérifier que des PDF ont été générés
PDF_COUNT=$(ls -1 "$PROJECT_DIR/data/output/"*.pdf 2>/dev/null | wc -l)
if [ "$PDF_COUNT" -eq 0 ]; then
    log_error "Aucun PDF trouvé dans data/output/"
    log_error "Vérifiez l'export depuis OXYGEN"
    exit 1
fi

log_info "✅ $PDF_COUNT factures PDF trouvées"

# Étape 4: Mise à jour Excel
log_info "Étape 4/5: Mise à jour du fichier Excel..."

if [ -f "$PROJECT_DIR/src/excel_updater.py" ]; then
    $PYTHON src/excel_updater.py --pdf-dir "$PROJECT_DIR/data/output/" --month "$PERIOD"
else
    log_warning "Script excel_updater.py non trouvé - étape ignorée"
fi

# Étape 5: Envoi des factures
if [ "$DRY_RUN" == "--dry-run" ]; then
    log_info "Étape 5/5: Simulation d'envoi des factures (--dry-run)..."
    if [ -f "$PROJECT_DIR/src/invoice_sender.py" ]; then
        $PYTHON src/invoice_sender.py --pdf-dir "$PROJECT_DIR/data/output/" --month "$PERIOD" --dry-run
    else
        log_warning "Script invoice_sender.py non trouvé"
    fi
else
    log_info "Étape 5/5: Envoi des factures par email..."
    read -p "Confirmer l'envoi des factures ? (o/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        if [ -f "$PROJECT_DIR/src/invoice_sender.py" ]; then
            $PYTHON src/invoice_sender.py --pdf-dir "$PROJECT_DIR/data/output/" --month "$PERIOD" --send
        else
            log_warning "Script invoice_sender.py non trouvé"
        fi
    else
        log_info "Envoi annulé"
    fi
fi

# Résumé final
echo ""
echo "=========================================="
echo "   FACTURATION TERMINÉE"
echo "=========================================="
echo ""
log_info "Période: $PERIOD"
log_info "Factures générées: $PDF_COUNT"
log_info "CSV OXYGEN: $CSV_FILE"
log_info "PDF générés: $PROJECT_DIR/data/output/"
echo ""
echo "✅ Processus terminé avec succès"

# Archivage optionnel
read -p "Archiver les fichiers ? (o/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    ARCHIVE_DIR="$PROJECT_DIR/archives/${YEAR}/${MONTH}"
    mkdir -p "$ARCHIVE_DIR"
    
    cp "$CLOCKIFY_FILE" "$ARCHIVE_DIR/"
    cp "$CSV_FILE" "$ARCHIVE_DIR/"
    cp "$PROJECT_DIR/data/output/"*.pdf "$ARCHIVE_DIR/" 2>/dev/null || true
    
    log_info "Fichiers archivés dans: $ARCHIVE_DIR"
fi

exit 0
#!/bin/bash

# DÉMARRAGE MONITORING CLOCKIFY COMPLET
# Reminders 15min + Monitoring horaire + Coaching automatique

echo "🚀 DÉMARRAGE SYSTÈME CLOCKIFY INTÉGRÉ"
echo "====================================="

# Vérifier que Clockify est configuré
if [ ! -f "/home/sq/.clockify_config" ]; then
    echo "❌ Configuration Clockify manquante (/home/sq/.clockify_config)"
    exit 1
fi

# Créer le répertoire de logs
mkdir -p /home/sq/SYAGA-CONSULTING/logs

# Démarrer en arrière-plan avec nohup
cd /home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/scripts

echo "📋 Configuration:"
echo "  - Reminders: Toutes les 15 minutes"
echo "  - Monitoring: Toutes les heures"
echo "  - Rapport quotidien: 18h"
echo "  - Base données: clockify_monitoring.db"
echo "  - Logs: /home/sq/SYAGA-CONSULTING/clockify_integration.log"
echo ""

# Installer les dépendances si nécessaire
pip3 install --user schedule requests sqlite3 >/dev/null 2>&1

# Démarrer le monitoring
echo "🔄 Démarrage du monitoring..."
nohup python3 clockify_integration_complete.py > /home/sq/SYAGA-CONSULTING/logs/clockify_monitoring.out 2>&1 &

CLOCKIFY_PID=$!

echo "✅ Monitoring Clockify démarré (PID: $CLOCKIFY_PID)"
echo "📁 Logs disponibles:"
echo "  - Application: /home/sq/SYAGA-CONSULTING/clockify_integration.log"
echo "  - Système: /home/sq/SYAGA-CONSULTING/logs/clockify_monitoring.out"
echo ""
echo "🛑 Pour arrêter: kill $CLOCKIFY_PID"

# Sauvegarder le PID
echo $CLOCKIFY_PID > /tmp/clockify_monitoring.pid

echo "🎯 SYSTÈME OPÉRATIONNEL - Facturation automatisée activée!"
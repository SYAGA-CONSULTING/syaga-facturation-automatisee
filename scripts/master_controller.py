#!/usr/bin/env python3
"""
CONTRÔLEUR PRINCIPAL - ÉCOSYSTÈME FACTURATION COMPLET
Orchestration de tous les modules : Clockify → Qonto → Email → Validation
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List
import subprocess
import os
import sys

# Import des modules du système
try:
    from clockify_integration_complete import ClockifyIntegration
    from qonto_integration_facturation import QontoFacturationIntegration  
    from email_surveillance_complete import EmailSurveillanceComplete
    from workflow_validation_complete import WorkflowValidationComplete
    from oxygen_reconciliation_complete import OxygenReconciliationComplete
    from systeme_recurrent_definitif import CLIENTS_RECURRENTS
except ImportError as e:
    logging.warning(f"⚠️ Import module: {e}")

class MasterController:
    """Contrôleur principal écosystème facturation"""
    
    def __init__(self):
        self.setup_logging()
        self.load_modules()
        
    def setup_logging(self):
        """Configuration logging principal"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/home/sq/SYAGA-CONSULTING/logs/master_controller.log'),
                logging.StreamHandler()
            ]
        )
        
    def load_modules(self):
        """Charger tous les modules"""
        try:
            self.clockify = ClockifyIntegration()
            self.qonto = QontoFacturationIntegration()
            self.email_surveillance = EmailSurveillanceComplete()
            self.workflow = WorkflowValidationComplete()
            self.reconciliation = OxygenReconciliationComplete()
            logging.info("✅ Tous les modules chargés")
        except Exception as e:
            logging.error(f"❌ Erreur chargement modules: {e}")
            self.modules_available = False
    
    def run_daily_full_cycle(self) -> Dict:
        """Cycle complet quotidien - CŒUR DU SYSTÈME"""
        logging.info("🚀 DÉMARRAGE CYCLE QUOTIDIEN COMPLET")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'clockify': {},
            'generation': {},
            'validation': {},
            'envoi': {},
            'qonto': {},
            'email_surveillance': {},
            'reconciliation': {},
            'errors': []
        }
        
        try:
            # 1. MONITORING CLOCKIFY (Temps réel)
            logging.info("1️⃣ MONITORING CLOCKIFY")
            try:
                # Vérifier temps en cours
                current_time = self.clockify.get_current_time_entry()
                if current_time:
                    categorization = self.clockify.categorize_time_entry(current_time)
                    results['clockify']['temps_en_cours'] = {
                        'project': categorization['project_name'],
                        'category': categorization['category'],
                        'billable': categorization['is_billable']
                    }
                
                # Monitoring horaire si nécessaire
                hourly_result = self.clockify.check_hourly_monitoring()
                results['clockify']['monitoring'] = 'completed'
                
            except Exception as e:
                results['errors'].append(f"Clockify: {e}")
                logging.error(f"❌ Erreur Clockify: {e}")
            
            # 2. GÉNÉRATION FACTURES RÉCURRENTES (si 1er du mois)
            logging.info("2️⃣ GÉNÉRATION RÉCURRENTES")
            try:
                today = datetime.now()
                if today.day == 1:  # Premier du mois
                    # Générer factures forfait mensuelles
                    generated = self.generate_monthly_recurring()
                    results['generation']['recurring'] = generated
                else:
                    results['generation']['recurring'] = {'skip': 'Not first day of month'}
                
            except Exception as e:
                results['errors'].append(f"Generation: {e}")
                logging.error(f"❌ Erreur génération: {e}")
            
            # 3. GÉNÉRATION FACTURES FIN DE MOIS (temps Clockify)
            logging.info("3️⃣ GÉNÉRATION FIN DE MOIS")
            try:
                if today.day >= 28:  # Fin de mois
                    ponctuel_result = self.generate_monthly_timesheets()
                    results['generation']['timesheets'] = ponctuel_result
                else:
                    results['generation']['timesheets'] = {'skip': 'Not end of month'}
                    
            except Exception as e:
                results['errors'].append(f"Timesheets: {e}")
                logging.error(f"❌ Erreur feuilles temps: {e}")
            
            # 4. WORKFLOW VALIDATION
            logging.info("4️⃣ WORKFLOW VALIDATION")
            try:
                # Soumettre nouvelles factures pour validation
                new_invoices = self.get_unprocessed_invoices()
                if new_invoices:
                    validation_result = self.workflow.run_validation_batch(new_invoices)
                    results['validation'] = validation_result
                else:
                    results['validation'] = {'message': 'No new invoices to validate'}
                
            except Exception as e:
                results['errors'].append(f"Validation: {e}")
                logging.error(f"❌ Erreur validation: {e}")
            
            # 5. ENVOI FACTURES APPROUVÉES
            logging.info("5️⃣ ENVOI FACTURES")
            try:
                ready_to_send = self.workflow.get_approved_ready_to_send()
                sent_count = 0
                
                for invoice in ready_to_send:
                    success = self.email_surveillance.send_invoice_email(
                        invoice['facture_id'], 
                        invoice['pdf_path']
                    )
                    
                    if success:
                        self.workflow.mark_as_sent(invoice['workflow_id'])
                        sent_count += 1
                
                results['envoi'] = {'sent': sent_count, 'total': len(ready_to_send)}
                
            except Exception as e:
                results['errors'].append(f"Envoi: {e}")
                logging.error(f"❌ Erreur envoi: {e}")
            
            # 6. MONITORING QONTO (Paiements)
            logging.info("6️⃣ MONITORING QONTO")
            try:
                qonto_result = self.qonto.run_daily_monitoring()
                results['qonto'] = {
                    'matches': len(qonto_result['matches']['automatic']),
                    'overdue': len(qonto_result['overdue']),
                    'cashflow_30d': qonto_result['cashflow']['previsionnel_30j']
                }
                
            except Exception as e:
                results['errors'].append(f"Qonto: {e}")
                logging.error(f"❌ Erreur Qonto: {e}")
            
            # 7. SURVEILLANCE EMAIL
            logging.info("7️⃣ SURVEILLANCE EMAIL") 
            try:
                email_result = self.email_surveillance.run_daily_surveillance()
                results['email_surveillance'] = {
                    'nouvelles_reponses': email_result['nouvelles_reponses'],
                    'critiques': email_result['critiques']
                }
                
            except Exception as e:
                results['errors'].append(f"Email surveillance: {e}")
                logging.error(f"❌ Erreur surveillance email: {e}")
            
            # 8. RÉCONCILIATION (hebdomadaire)
            logging.info("8️⃣ RÉCONCILIATION")
            try:
                if today.weekday() == 0:  # Lundi
                    reconcile_result = self.reconciliation.run_monthly_reconciliation(1)
                    results['reconciliation'] = {
                        'matches': reconcile_result['matches'],
                        'ecarts': reconcile_result['ecarts']
                    }
                else:
                    results['reconciliation'] = {'skip': 'Not Monday'}
                    
            except Exception as e:
                results['errors'].append(f"Reconciliation: {e}")
                logging.error(f"❌ Erreur réconciliation: {e}")
            
            # 9. RAPPORT FINAL
            self.generate_daily_report(results)
            
            logging.info("✅ CYCLE QUOTIDIEN TERMINÉ")
            
        except Exception as e:
            results['errors'].append(f"Master: {e}")
            logging.error(f"❌ Erreur cycle principal: {e}")
        
        return results
    
    def generate_monthly_recurring(self) -> Dict:
        """Générer factures récurrentes du mois"""
        try:
            # Utiliser le script existant
            result = subprocess.run([
                'python3', 
                '/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/scripts/systeme_recurrent_definitif.py'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return {'status': 'success', 'output': result.stdout}
            else:
                return {'status': 'error', 'error': result.stderr}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def generate_monthly_timesheets(self) -> Dict:
        """Générer factures temps Clockify fin de mois"""
        try:
            # Utiliser le générateur XML Oxygen
            result = subprocess.run([
                'python3',
                '/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/scripts/generer_tableau_xml_oxygen.py'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return {'status': 'success', 'output': result.stdout}
            else:
                return {'status': 'error', 'error': result.stderr}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def get_unprocessed_invoices(self) -> List[int]:
        """Récupérer factures non traitées par workflow"""
        import sqlite3
        
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        # Factures récentes sans workflow
        cursor.execute('''
            SELECT f.id 
            FROM factures f
            LEFT JOIN workflow_validation wv ON f.id = wv.facture_id
            WHERE f.date_facture >= DATE('now', '-7 days')
            AND wv.facture_id IS NULL
            AND f.total_ht > 0
        ''')
        
        unprocessed = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return unprocessed
    
    def generate_daily_report(self, results: Dict):
        """Générer rapport quotidien complet"""
        report = f"""
🏭 RAPPORT QUOTIDIEN ÉCOSYSTÈME FACTURATION
========================================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 RÉSUMÉ EXÉCUTIF:
• Erreurs: {len(results['errors'])}
• Modules actifs: {8 - len(results['errors'])}
• Status général: {'🟢 OPÉRATIONNEL' if len(results['errors']) == 0 else '🟡 PARTIEL' if len(results['errors']) < 3 else '🔴 CRITIQUE'}

⏱️ CLOCKIFY:
• Monitoring: {results.get('clockify', {}).get('monitoring', 'N/A')}
• Temps en cours: {results.get('clockify', {}).get('temps_en_cours', {}).get('project', 'Aucun')}

🔄 GÉNÉRATION:
• Récurrentes: {results.get('generation', {}).get('recurring', {}).get('status', 'N/A')}
• Feuilles temps: {results.get('generation', {}).get('timesheets', {}).get('status', 'N/A')}

✅ VALIDATION:
• Soumises: {results.get('validation', {}).get('submitted', 0)}
• Auto-approuvées: {results.get('validation', {}).get('auto_approved', 0)}

📤 ENVOI:
• Envoyées: {results.get('envoi', {}).get('sent', 0)}
• Total prêtes: {results.get('envoi', {}).get('total', 0)}

🏦 QONTO:
• Nouveaux paiements: {results.get('qonto', {}).get('matches', 0)}
• Impayées: {results.get('qonto', {}).get('overdue', 0)}
• Cash-flow 30j: {results.get('qonto', {}).get('cashflow_30d', 0):,.2f}€

📧 EMAIL:
• Nouvelles réponses: {results.get('email_surveillance', {}).get('nouvelles_reponses', 0)}
• Critiques: {results.get('email_surveillance', {}).get('critiques', 0)}

🔍 RÉCONCILIATION:
• Matches: {results.get('reconciliation', {}).get('matches', 'N/A')}
• Écarts: {results.get('reconciliation', {}).get('ecarts', 'N/A')}
"""
        
        if results['errors']:
            report += f"\n🚨 ERREURS:\n"
            for error in results['errors']:
                report += f"• {error}\n"
        
        # Sauvegarder rapport
        with open('/home/sq/SYAGA-CONSULTING/logs/daily_report.txt', 'w') as f:
            f.write(report)
        
        logging.info("📄 Rapport quotidien généré")
        
        # Envoyer par email si erreurs critiques
        if len(results['errors']) >= 3:
            self.send_critical_alert(report)
    
    def send_critical_alert(self, report: str):
        """Envoyer alerte critique"""
        try:
            subprocess.run([
                'python3',
                '/home/sq/SYAGA-CONSULTING/syaga-instructions/SEND_EMAIL_SECURE.py',
                '--to', 'sebastien.questier@syaga.fr',
                '--subject', f'🚨 ALERTE CRITIQUE - Écosystème Facturation {datetime.now().strftime("%d/%m/%Y")}',
                '--body', report
            ], check=True)
            logging.info("🚨 Alerte critique envoyée")
        except Exception as e:
            logging.error(f"❌ Erreur envoi alerte critique: {e}")
    
    def run_weekly_maintenance(self) -> Dict:
        """Maintenance hebdomadaire"""
        logging.info("🔧 MAINTENANCE HEBDOMADAIRE")
        
        results = {}
        
        try:
            # Nettoyage logs anciens
            subprocess.run(['find', '/home/sq/SYAGA-CONSULTING/logs', '-name', '*.log', '-mtime', '+30', '-delete'])
            results['cleanup_logs'] = 'completed'
            
            # Sauvegarde base données
            backup_path = f"/home/sq/SYAGA-CONSULTING/backups/factures_backup_{datetime.now().strftime('%Y%m%d')}.db"
            subprocess.run(['cp', 
                          '/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db',
                          backup_path])
            results['backup_db'] = backup_path
            
            # Réconciliation complète
            reconcile_result = self.reconciliation.run_monthly_reconciliation(3)
            results['reconciliation'] = reconcile_result
            
            logging.info("✅ Maintenance hebdomadaire terminée")
            
        except Exception as e:
            logging.error(f"❌ Erreur maintenance: {e}")
            results['error'] = str(e)
        
        return results
    
    def get_system_health(self) -> Dict:
        """Vérifier santé du système"""
        health = {
            'overall': 'HEALTHY',
            'modules': {},
            'database': 'OK',
            'files': 'OK',
            'last_run': None,
            'issues': []
        }
        
        try:
            # Vérifier base données
            import sqlite3
            conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM factures')
            invoice_count = cursor.fetchone()[0]
            
            if invoice_count < 1000:
                health['issues'].append(f'Base données incomplète: {invoice_count} factures')
                health['database'] = 'WARNING'
            
            conn.close()
            
            # Vérifier fichiers critiques
            critical_files = [
                '/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/config_recurrent_definitif.json',
                '/home/sq/.clockify_config',
                '/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/Factures clients.csv'
            ]
            
            for file_path in critical_files:
                if not os.path.exists(file_path):
                    health['issues'].append(f'Fichier manquant: {file_path}')
                    health['files'] = 'ERROR'
            
            # Vérifier dernière exécution
            if os.path.exists('/home/sq/SYAGA-CONSULTING/logs/master_controller.log'):
                stat = os.stat('/home/sq/SYAGA-CONSULTING/logs/master_controller.log')
                last_modified = datetime.fromtimestamp(stat.st_mtime)
                health['last_run'] = last_modified.isoformat()
                
                if (datetime.now() - last_modified).days > 2:
                    health['issues'].append('Dernière exécution > 2 jours')
            
            # Status global
            if health['issues']:
                health['overall'] = 'WARNING' if len(health['issues']) < 3 else 'CRITICAL'
            
        except Exception as e:
            health['overall'] = 'CRITICAL'
            health['issues'].append(f'Erreur vérification: {e}')
        
        return health

def main():
    """Point d'entrée principal"""
    controller = MasterController()
    
    print("""
🏭 CONTRÔLEUR PRINCIPAL ÉCOSYSTÈME FACTURATION
============================================

Modules intégrés:
  ⏱️ Clockify (temps réel)
  🔄 Génération automatique
  ✅ Workflow validation  
  📤 Envoi email
  🏦 Surveillance Qonto
  📧 Monitoring réponses
  🔍 Réconciliation tri-directionnelle

Cycles disponibles:
  📅 Quotidien: Cycle complet
  🔧 Hebdomadaire: Maintenance
  📊 Santé système
    """)
    
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'daily':
            print("\n🚀 LANCEMENT CYCLE QUOTIDIEN...")
            result = controller.run_daily_full_cycle()
            print(f"✅ Cycle terminé - {len(result['errors'])} erreurs")
            
        elif command == 'weekly':
            print("\n🔧 LANCEMENT MAINTENANCE HEBDOMADAIRE...")
            result = controller.run_weekly_maintenance()
            print("✅ Maintenance terminée")
            
        elif command == 'health':
            print("\n📊 VÉRIFICATION SANTÉ SYSTÈME...")
            health = controller.get_system_health()
            print(f"Status: {health['overall']}")
            if health['issues']:
                print("Issues:")
                for issue in health['issues']:
                    print(f"  • {issue}")
        else:
            print(f"❌ Commande inconnue: {command}")
    else:
        print("\nUsage: python3 master_controller.py [daily|weekly|health]")

if __name__ == "__main__":
    main()
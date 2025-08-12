#!/usr/bin/env python3
"""
INTÉGRATION CLOCKIFY COMPLÈTE - CŒUR DU SYSTÈME FACTURATION
Reminders automatiques, catégorisation, monitoring, coaching
"""

import requests
import json
import time
import sqlite3
from datetime import datetime, timedelta
import schedule
import threading
import os
from typing import Dict, List, Optional
import subprocess
import logging

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/sq/SYAGA-CONSULTING/clockify_integration.log'),
        logging.StreamHandler()
    ]
)

class ClockifyIntegration:
    """Intégration complète Clockify pour facturation automatisée"""
    
    def __init__(self):
        self.load_config()
        self.setup_database()
        self.clients_recurrents = self.load_recurring_clients()
        
    def load_config(self):
        """Charger la configuration Clockify"""
        try:
            with open('/home/sq/.clockify_config', 'r') as f:
                for line in f:
                    if line.startswith('CLOCKIFY_API_KEY='):
                        self.api_key = line.split('=')[1].strip()
                    elif line.startswith('WORKSPACE_ID='):
                        self.workspace_id = line.split('=')[1].strip()
            
            self.headers = {
                'X-Api-Key': self.api_key,
                'Content-Type': 'application/json'
            }
            self.base_url = 'https://api.clockify.me/api/v1'
            logging.info("✅ Configuration Clockify chargée")
        except Exception as e:
            logging.error(f"❌ Erreur configuration Clockify: {e}")
            raise
    
    def setup_database(self):
        """Initialiser la base de données de monitoring"""
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/clockify_monitoring.db')
        cursor = conn.cursor()
        
        # Table suivi temps réel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temps_realtime (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                project_name TEXT,
                client_name TEXT,
                task_description TEXT,
                duration_minutes INTEGER,
                is_billable BOOLEAN,
                hourly_rate REAL,
                amount_ht REAL,
                category TEXT,
                facturation_status TEXT DEFAULT 'EN_COURS',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table reminders/coaching
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders_coaching (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                type_reminder TEXT, -- '15MIN', '1HOUR', 'DAILY'
                user_id TEXT,
                project_name TEXT,
                message TEXT,
                action_required TEXT,
                status TEXT DEFAULT 'ACTIF',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table catégorisation automatique
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorisation_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_pattern TEXT,
                project_pattern TEXT,
                task_pattern TEXT,
                category TEXT, -- 'FORFAIT', 'FACTURABLE', 'INTERNE', 'R&D'
                hourly_rate REAL,
                is_billable BOOLEAN,
                priority INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logging.info("✅ Base de données monitoring initialisée")
    
    def load_recurring_clients(self) -> Dict:
        """Charger les clients récurrents depuis la configuration"""
        try:
            with open('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/config_recurrent_definitif.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def get_current_time_entry(self) -> Optional[Dict]:
        """Récupérer l'entrée temps en cours"""
        try:
            response = requests.get(
                f"{self.base_url}/workspaces/{self.workspace_id}/user/time-entries?in-progress=true",
                headers=self.headers
            )
            
            if response.status_code == 200:
                entries = response.json()
                if entries:
                    return entries[0]
            return None
        except Exception as e:
            logging.error(f"❌ Erreur récupération temps en cours: {e}")
            return None
    
    def categorize_time_entry(self, entry: Dict) -> Dict:
        """Catégoriser automatiquement l'entrée temps"""
        project_name = entry.get('project', {}).get('name', '').upper()
        description = entry.get('description', '').upper()
        
        # Règles de catégorisation basées sur le système récurrent
        category = 'FACTURABLE'  # Par défaut
        hourly_rate = 110.0  # Taux standard
        is_billable = True
        
        # Client récurrent = forfait (sauf si heures supplémentaires)
        for client, config in self.clients_recurrents.items():
            if client.upper() in project_name:
                if 'FORFAIT' in description or 'MAINTENANCE' in description:
                    category = 'FORFAIT'
                    hourly_rate = 0  # Déjà facturé en forfait
                    is_billable = False
                else:
                    category = 'FACTURABLE_EXTRA'
                    hourly_rate = 110.0
                    is_billable = True
                break
        
        # Projets internes
        if any(word in project_name for word in ['SYAGA', 'INTERNE', 'R&D', 'PRISM']):
            category = 'INTERNE'
            hourly_rate = 0
            is_billable = False
        
        return {
            'category': category,
            'hourly_rate': hourly_rate,
            'is_billable': is_billable,
            'project_name': project_name,
            'description': description
        }
    
    def send_reminder_notification(self, message: str, urgency: str = 'INFO'):
        """Envoyer notification de reminder"""
        try:
            # Notification système
            subprocess.run([
                'notify-send',
                f'Clockify {urgency}',
                message
            ], check=False)
            
            # Log du reminder
            logging.info(f"🔔 REMINDER {urgency}: {message}")
            
        except Exception as e:
            logging.error(f"❌ Erreur notification: {e}")
    
    def check_15min_reminder(self):
        """Vérifier toutes les 15 minutes l'état du temps"""
        current_entry = self.get_current_time_entry()
        
        if current_entry is None:
            # Pas de temps en cours
            message = "⚠️ Aucun temps en cours. Pensez à démarrer Clockify si vous travaillez!"
            self.send_reminder_notification(message, 'WARNING')
            
            # Enregistrer reminder
            conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/clockify_monitoring.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reminders_coaching (type_reminder, message, action_required)
                VALUES ('15MIN', ?, 'START_TIMER')
            ''', (message,))
            conn.commit()
            conn.close()
        else:
            # Temps en cours - vérifier catégorisation
            categorization = self.categorize_time_entry(current_entry)
            project = categorization['project_name']
            category = categorization['category']
            
            duration_ms = 0
            if current_entry.get('timeInterval', {}).get('start'):
                start_time = datetime.fromisoformat(current_entry['timeInterval']['start'].replace('Z', '+00:00'))
                duration_ms = (datetime.now(start_time.tzinfo) - start_time).total_seconds() * 1000
            
            duration_minutes = int(duration_ms / 1000 / 60)
            
            message = f"✅ Temps en cours: {project} ({category}) - {duration_minutes}min"
            logging.info(f"🕒 {message}")
            
            # Si plus de 2h sans description détaillée
            if duration_minutes > 120 and len(current_entry.get('description', '')) < 10:
                warning = "⚠️ Plus de 2h sur cette tâche. Ajoutez une description détaillée!"
                self.send_reminder_notification(warning, 'WARNING')
    
    def check_hourly_monitoring(self):
        """Monitoring horaire - coaching et optimisation"""
        try:
            # Récupérer les temps de la dernière heure
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=1)
            
            response = requests.get(
                f"{self.base_url}/workspaces/{self.workspace_id}/reports/detailed",
                headers=self.headers,
                params={
                    'dateRangeStart': start_time.isoformat() + 'Z',
                    'dateRangeEnd': end_time.isoformat() + 'Z',
                    'detailedFilter': json.dumps({
                        'page': 1,
                        'pageSize': 1000
                    })
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                time_entries = data.get('timeentries', [])
                
                total_minutes = 0
                facturable_minutes = 0
                forfait_minutes = 0
                interne_minutes = 0
                
                conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/clockify_monitoring.db')
                cursor = conn.cursor()
                
                for entry in time_entries:
                    duration_ms = entry.get('timeInterval', {}).get('duration', 0)
                    if duration_ms:
                        duration_minutes = int(duration_ms / 1000 / 60)
                        total_minutes += duration_minutes
                        
                        # Catégoriser
                        project_name = entry.get('project', {}).get('name', '')
                        description = entry.get('description', '')
                        
                        fake_entry = {
                            'project': {'name': project_name},
                            'description': description
                        }
                        categorization = self.categorize_time_entry(fake_entry)
                        
                        if categorization['category'] == 'FACTURABLE':
                            facturable_minutes += duration_minutes
                        elif categorization['category'] == 'FORFAIT':
                            forfait_minutes += duration_minutes
                        else:
                            interne_minutes += duration_minutes
                        
                        # Enregistrer en base
                        cursor.execute('''
                            INSERT INTO temps_realtime (
                                project_name, client_name, task_description,
                                duration_minutes, is_billable, hourly_rate,
                                amount_ht, category
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            project_name,
                            project_name.split('-')[0] if '-' in project_name else project_name,
                            description,
                            duration_minutes,
                            categorization['is_billable'],
                            categorization['hourly_rate'],
                            duration_minutes * categorization['hourly_rate'] / 60,
                            categorization['category']
                        ))
                
                conn.commit()
                conn.close()
                
                # Coaching automatique
                ca_facturable_heure = facturable_minutes * 110.0 / 60
                
                coaching_message = f"""
📊 MONITORING HOURLY:
⏱️ Total: {total_minutes}min
💰 Facturable: {facturable_minutes}min ({ca_facturable_heure:.2f}€)
🔒 Forfait: {forfait_minutes}min
🏠 Interne: {interne_minutes}min
"""
                
                logging.info(coaching_message)
                
                # Alertes coaching
                if facturable_minutes > 0:
                    efficacite = (facturable_minutes / total_minutes * 100) if total_minutes > 0 else 0
                    if efficacite < 60:
                        warning = f"⚠️ Efficacité facturable: {efficacite:.1f}% (objectif >60%)"
                        self.send_reminder_notification(warning, 'COACHING')
        
        except Exception as e:
            logging.error(f"❌ Erreur monitoring horaire: {e}")
    
    def generate_daily_facturation_report(self):
        """Rapport quotidien de facturation"""
        try:
            conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/clockify_monitoring.db')
            cursor = conn.cursor()
            
            # Stats du jour
            cursor.execute('''
                SELECT 
                    category,
                    SUM(duration_minutes) as total_minutes,
                    SUM(amount_ht) as total_amount,
                    COUNT(*) as nb_entries
                FROM temps_realtime 
                WHERE DATE(timestamp) = DATE('now')
                GROUP BY category
            ''')
            
            stats = cursor.fetchall()
            
            report = "📋 RAPPORT QUOTIDIEN CLOCKIFY\n"
            report += "=" * 40 + "\n"
            
            total_ca = 0
            for category, minutes, amount, count in stats:
                hours = minutes / 60
                report += f"{category:15}: {hours:5.1f}h = {amount:7.2f}€ ({count} entrées)\n"
                total_ca += amount
            
            report += f"\n💰 CA TOTAL JOUR: {total_ca:.2f}€ HT"
            
            # Prévisionnel mensuel
            cursor.execute('''
                SELECT SUM(amount_ht) 
                FROM temps_realtime 
                WHERE DATE(timestamp) >= DATE('now', 'start of month')
                AND category IN ('FACTURABLE', 'FACTURABLE_EXTRA')
            ''')
            ca_mois = cursor.fetchone()[0] or 0
            
            # Récurrent mensuel
            ca_recurrent = sum(client['forfait'] for client in self.clients_recurrents.values() 
                             if client['frequence'] == 'mensuel')
            
            ca_total_previsionnel = ca_mois + ca_recurrent
            report += f"\n📈 CA MOIS (prév.): {ca_total_previsionnel:.2f}€ HT"
            
            logging.info(f"\n{report}")
            
            # Envoyer par email si significatif
            if total_ca > 500:  # Si plus de 500€ dans la journée
                self.send_daily_report_email(report)
            
            conn.close()
            
        except Exception as e:
            logging.error(f"❌ Erreur rapport quotidien: {e}")
    
    def send_daily_report_email(self, report: str):
        """Envoyer le rapport quotidien par email"""
        try:
            # Utiliser le module email SYAGA
            subprocess.run([
                'python3', 
                '/home/sq/SYAGA-CONSULTING/syaga-instructions/SEND_EMAIL_SECURE.py',
                '--to', 'sebastien.questier@syaga.fr',
                '--subject', f'📊 Rapport Clockify {datetime.now().strftime("%d/%m/%Y")}',
                '--body', report
            ], check=True)
            logging.info("✅ Rapport quotidien envoyé par email")
        except Exception as e:
            logging.error(f"❌ Erreur envoi email rapport: {e}")
    
    def start_monitoring(self):
        """Démarrer le monitoring complet"""
        logging.info("🚀 Démarrage monitoring Clockify complet")
        
        # Planifier les reminders
        schedule.every(15).minutes.do(self.check_15min_reminder)
        schedule.every().hour.at(":00").do(self.check_hourly_monitoring)
        schedule.every().day.at("18:00").do(self.generate_daily_facturation_report)
        
        # Boucle principale
        while True:
            schedule.run_pending()
            time.sleep(60)  # Vérifier chaque minute

def main():
    """Point d'entrée principal"""
    try:
        clockify = ClockifyIntegration()
        
        print("""
🕒 CLOCKIFY INTEGRATION COMPLÈTE - DÉMARRAGE
============================================

⏰ Reminders: Toutes les 15 minutes
📊 Monitoring: Toutes les heures  
📈 Rapport: Quotidien à 18h
🎯 Objectif: Facturation fiable & automatisée

Appuyez sur Ctrl+C pour arrêter...
        """)
        
        clockify.start_monitoring()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt du monitoring Clockify")
        logging.info("🛑 Monitoring Clockify arrêté par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        logging.error(f"❌ Erreur fatale monitoring: {e}")

if __name__ == "__main__":
    main()
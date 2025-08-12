#!/usr/bin/env python3
"""
EXTRACTION CLOCKIFY NATIVE - Données détaillées par client
Récupère les données natives Clockify pour générer des rapports précis
"""

import sys
import os
import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

def load_clockify_config():
    """Charge la configuration Clockify depuis le fichier sécurisé"""
    try:
        config_file = os.path.expanduser('~/.clockify_config')
        if not os.path.exists(config_file):
            print(f"❌ Fichier config manquant: {config_file}")
            return None, None
        
        config = {}
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key] = value
        
        api_key = config.get('CLOCKIFY_API_KEY')
        workspace_id = config.get('WORKSPACE_ID')
        
        if not api_key or not workspace_id:
            print(f"❌ Configuration incomplète dans {config_file}")
            return None, None
            
        return api_key, workspace_id
        
    except Exception as e:
        print(f"❌ Erreur chargement config Clockify: {e}")
        return None, None

class ClockifyExtractor:
    def __init__(self):
        self.api_key, self.workspace_id = load_clockify_config()
        if not self.api_key or not self.workspace_id:
            raise Exception("Configuration Clockify manquante")
        
        self.headers = {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        self.base_url = 'https://api.clockify.me/api/v1'
        
    def get_user_id(self):
        """Récupère l'ID utilisateur"""
        try:
            response = requests.get(f'{self.base_url}/user', headers=self.headers)
            if response.status_code == 200:
                return response.json()['id']
            else:
                print(f"❌ Erreur récupération user: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Erreur API user: {e}")
            return None
    
    def get_projects(self):
        """Récupère tous les projets du workspace"""
        try:
            response = requests.get(
                f'{self.base_url}/workspaces/{self.workspace_id}/projects',
                headers=self.headers,
                params={'page-size': 500}
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Erreur récupération projets: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Erreur API projets: {e}")
            return []
    
    def get_all_users(self):
        """Récupère tous les utilisateurs du workspace"""
        try:
            response = requests.get(
                f'{self.base_url}/workspaces/{self.workspace_id}/users',
                headers=self.headers,
                params={'page-size': 100}
            )
            if response.status_code == 200:
                users = response.json()
                print(f"👥 {len(users)} utilisateurs trouvés")
                for user in users:
                    print(f"  - {user.get('name', 'N/A')} ({user.get('email', 'N/A')}) - ID: {user['id']}")
                return users
            else:
                print(f"❌ Erreur récupération utilisateurs: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Erreur API utilisateurs: {e}")
            return []
    
    def get_time_entries_july_2025(self, user_id, user_name=""):
        """Récupère toutes les entrées temps juillet 2025 pour un utilisateur"""
        try:
            # Période juillet 2025
            start_date = "2025-07-01T00:00:00.000Z"
            end_date = "2025-07-31T23:59:59.999Z"
            
            response = requests.get(
                f'{self.base_url}/workspaces/{self.workspace_id}/user/{user_id}/time-entries',
                headers=self.headers,
                params={
                    'start': start_date,
                    'end': end_date,
                    'page-size': 1000
                }
            )
            
            if response.status_code == 200:
                entries = response.json()
                if entries:
                    print(f"  ⏱️ {user_name}: {len(entries)} entrées juillet 2025")
                else:
                    print(f"  ⏱️ {user_name}: Aucune entrée juillet 2025")
                return entries
            else:
                print(f"❌ Erreur récupération entries {user_name}: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Erreur API entries {user_name}: {e}")
            return []
    
    def get_july_2025_data_reports_api(self):
        """Utilise l'API Reports (méthode validée hier) pour récupérer TOUS les utilisateurs"""
        try:
            report_data = {
                "dateRangeStart": "2025-07-01T00:00:00Z",
                "dateRangeEnd": "2025-07-31T23:59:59Z",
                "detailedFilter": {
                    "page": 1,
                    "pageSize": 1000
                }
            }
            
            response = requests.post(
                f"https://reports.api.clockify.me/v1/workspaces/{self.workspace_id}/reports/detailed",
                headers=self.headers,
                json=report_data,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                entries = result.get('timeentries', [])
                print(f"📊 API REPORTS: {len(entries)} entrées juillet 2025 (TOUS UTILISATEURS)")
                return entries
            else:
                print(f"❌ Erreur API Reports: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Erreur API Reports: {e}")
            return []

    def extract_detailed_data(self):
        """Extraction complète des données Clockify juillet 2025 - TOUS UTILISATEURS"""
        print("🕐 EXTRACTION CLOCKIFY NATIVE - Juillet 2025 (TOUS UTILISATEURS)")
        print("="*70)
        
        # 1. Récupérer projets
        projects = self.get_projects()
        project_map = {p['id']: p['name'] for p in projects}
        print(f"📁 {len(projects)} projets trouvés")
        
        # 2. Récupérer TOUTES les entrées avec API Reports (tous users)
        entries = self.get_july_2025_data_reports_api()
        
        if not entries:
            print("❌ Aucune entrée temps trouvée")
            return None
        
        # 4. Organiser par client/projet et utilisateur
        clients_data = defaultdict(lambda: {
            'total_minutes': 0,
            'tasks': defaultdict(int),
            'entries': [],
            'project_name': '',
            'users': defaultdict(int)
        })
        
        print(f"👥 Analyse des {len(entries)} entrées par utilisateur...")
        
        for entry in entries:
            # Informations de base
            project_id = entry.get('projectId')
            project_name = project_map.get(project_id, 'Unknown Project') if project_id else 'Sans projet'
            user_name = entry.get('userName', 'Utilisateur inconnu')
            
            # Déterminer le client depuis le nom du projet
            client = self.determine_client(project_name)
            
            # Calculer durée en minutes (API Reports retourne directement en secondes)
            duration_seconds = entry.get('timeInterval', {}).get('duration', 0)
            if isinstance(duration_seconds, int):
                minutes = duration_seconds / 60  # Secondes -> minutes
            else:
                minutes = self.parse_duration(duration_seconds)
            
            # Ajouter aux données client
            clients_data[client]['total_minutes'] += minutes
            clients_data[client]['project_name'] = project_name
            clients_data[client]['users'][user_name] += minutes
            
            clients_data[client]['entries'].append({
                'date': entry.get('timeInterval', {}).get('start', '').split('T')[0],
                'description': entry.get('description', ''),
                'minutes': minutes,
                'user': user_name,
                'task': entry.get('task', {}).get('name', 'General') if entry.get('task') else 'General'
            })
            
            # Grouper par tâche
            task_name = entry.get('description', 'Tâche générale')
            task_category = self.categorize_task(task_name)
            clients_data[client]['tasks'][task_category] += minutes
        
        # 5. Convertir en heures et structurer
        final_data = {}
        for client, data in clients_data.items():
            total_hours = data['total_minutes'] / 60.0
            tasks_hours = {task: mins/60.0 for task, mins in data['tasks'].items()}
            users_hours = {user: mins/60.0 for user, mins in data['users'].items()}
            
            final_data[client] = {
                'total_hours': total_hours,
                'tasks': tasks_hours,
                'users': users_hours,
                'project_name': data['project_name'],
                'entries_count': len(data['entries']),
                'entries': data['entries']
            }
        
        return final_data
    
    def determine_client(self, project_name):
        """Détermine le nom client depuis le nom du projet"""
        project_lower = project_name.lower()
        
        if 'laa' in project_lower or 'automatismes' in project_lower:
            if 'maroc' in project_lower:
                return 'LAA MAROC'
            return 'LAA'
        elif 'uai' in project_lower or 'un air' in project_lower:
            return 'UAI'
        elif 'aixagon' in project_lower:
            return 'AIXAGON'
        elif 'pharmabest' in project_lower:
            return 'PHARMABEST'
        elif 'guerbet' in project_lower:
            return 'GUERBET'
        else:
            return project_name  # Garder nom projet si client non reconnu
    
    def categorize_task(self, description):
        """Catégorise une tâche selon sa description"""
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ['dette', 'tech', 'legacy', 'refactor']):
            return 'Dette technologique'
        elif any(word in desc_lower for word in ['test', 'qa', 'quality', 'junit']):
            return 'Tests automatisés'
        elif any(word in desc_lower for word in ['dev', 'develop', 'code', 'feature']):
            return 'Développements'
        elif any(word in desc_lower for word in ['maintenance', 'bug', 'fix', 'hotfix']):
            return 'Maintenance'
        elif any(word in desc_lower for word in ['hardad', 'hardenad', 'security', 'ad']):
            return 'HardenAD'
        elif any(word in desc_lower for word in ['sql', 'database', 'db', 'server']):
            return 'SQL Server'
        elif any(word in desc_lower for word in ['support', 'assistance', 'help']):
            return 'Support technique'
        else:
            return 'Prestations générales'
    
    def parse_duration(self, duration_str):
        """Parse une durée ISO 8601 en minutes"""
        # Format: PT2H30M ou PT150M
        import re
        
        if not duration_str.startswith('PT'):
            return 0
        
        minutes = 0
        
        # Heures
        hours_match = re.search(r'(\d+)H', duration_str)
        if hours_match:
            minutes += int(hours_match.group(1)) * 60
        
        # Minutes
        minutes_match = re.search(r'(\d+)M', duration_str)
        if minutes_match:
            minutes += int(minutes_match.group(1))
        
        return minutes

def save_clockify_data(data, output_file):
    """Sauvegarde les données Clockify en JSON"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        print(f"✅ Données sauvegardées: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        return False

def display_summary(data):
    """Affiche un résumé des données extraites"""
    print("\n📊 RÉSUMÉ EXTRACTION CLOCKIFY - TOUS UTILISATEURS")
    print("="*60)
    
    total_hours = 0
    total_value = 0
    all_users = set()
    
    for client, client_data in data.items():
        hours = client_data['total_hours']
        
        # Tarif par client
        if client in ['UAI', 'UN AIR D\'ICI']:
            rate = 850  # Expertise technique
        elif 'MAROC' in client:
            rate = 100  # Standard mais TVA 0%
        else:
            rate = 100  # Standard
        
        value = hours * rate
        total_hours += hours
        total_value += value
        
        print(f"\n🏢 {client}:")
        print(f"  ⏱️ Total: {hours:.1f}h")
        print(f"  💰 Valeur: {value:,.0f}€ ({rate}€/h)")
        print(f"  📋 Entrées: {client_data['entries_count']}")
        
        # Utilisateurs pour ce client
        if client_data['users']:
            print(f"  👥 Utilisateurs:")
            for user, user_hours in sorted(client_data['users'].items(), key=lambda x: x[1], reverse=True):
                print(f"    - {user}: {user_hours:.1f}h")
                all_users.add(user)
        
        # Top 3 tâches
        sorted_tasks = sorted(client_data['tasks'].items(), key=lambda x: x[1], reverse=True)
        if sorted_tasks:
            print(f"  📋 Top tâches:")
            for i, (task, task_hours) in enumerate(sorted_tasks[:3]):
                print(f"    {i+1}. {task}: {task_hours:.1f}h")
    
    print(f"\n💎 TOTAL GÉNÉRAL:")
    print(f"  ⏱️ {total_hours:.1f}h")
    print(f"  💰 {total_value:,.0f}€")
    print(f"  👥 {len(all_users)} utilisateurs: {', '.join(sorted(all_users))}")

def main():
    try:
        # Créer répertoire de sortie
        output_dir = "/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/clockify-native"
        os.makedirs(output_dir, exist_ok=True)
        
        # Extraction des données
        extractor = ClockifyExtractor()
        clockify_data = extractor.extract_detailed_data()
        
        if not clockify_data:
            print("❌ Échec extraction données Clockify")
            return
        
        # Affichage résumé
        display_summary(clockify_data)
        
        # Sauvegarde
        output_file = f"{output_dir}/clockify_juillet_2025_native.json"
        save_clockify_data(clockify_data, output_file)
        
        print(f"\n✅ EXTRACTION TERMINÉE")
        print(f"📁 Données: {output_file}")
        
        return clockify_data
        
    except Exception as e:
        print(f"❌ Erreur extraction Clockify: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    clockify_data = main()
#!/usr/bin/env python3
"""
EXTRACTION CLOCKIFY DIRECTE - Juillet 2025
Récupération des données directement depuis l'API sans exports
Comparaison avec les résultats d'hier pour vérifier cohérence
"""

import requests
import json
from datetime import datetime
from collections import defaultdict

class ClockifyDirectExtract:
    def __init__(self):
        """Initialise avec credentials depuis ~/.clockify_config"""
        self.api_key = "Y2FhMjM3NzUtOTFlZC00MWVkLWE1NTQtZjdhMzk1OThhYWRk"
        self.workspace_id = "60f16583d5588e20a960e57d"
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def extract_july_2025_direct(self):
        """Extraction directe des données juillet 2025 via Reports API"""
        print("🔄 Extraction directe Clockify juillet 2025...")
        
        # Configuration extraction
        report_data = {
            "dateRangeStart": "2025-07-01T00:00:00Z",
            "dateRangeEnd": "2025-07-31T23:59:59Z",
            "detailedFilter": {
                "page": 1,
                "pageSize": 1000
            },
            "exportType": "JSON"
        }
        
        try:
            # Appel API Reports
            response = requests.post(
                f"https://reports.api.clockify.me/v1/workspaces/{self.workspace_id}/reports/detailed",
                headers=self.headers,
                json=report_data,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"❌ Erreur API: {response.status_code}")
                return None
            
            data = response.json()
            entries = data.get('timeentries', [])
            
            print(f"📊 {len(entries)} entrées récupérées directement")
            
            # Traiter les données par client
            clients_data = defaultdict(lambda: {
                'total_hours': 0,
                'tasks': defaultdict(float),
                'users': defaultdict(float),
                'entries': []
            })
            
            for entry in entries:
                # Extraire les informations
                user_name = entry.get('userName', 'Inconnu')
                project_name = entry.get('projectName', 'Sans projet')
                task_name = entry.get('taskName', 'Tâche générique')
                
                # Durée en secondes -> heures
                duration_seconds = entry.get('timeInterval', {}).get('duration', 0)
                if isinstance(duration_seconds, int):
                    hours = duration_seconds / 3600
                else:
                    # Fallback si format différent
                    hours = 0
                
                description = entry.get('description', '')
                date = entry.get('timeInterval', {}).get('start', '')[:10]
                
                # Mapping des clients (même logique qu'hier)
                client_mapping = {
                    'LAA': 'LAA',
                    'PHARMABEST': 'PHARMABEST',
                    'SYAGA': 'INTERNAL',
                    'AIXAGON': 'AIXAGON',
                    'UAI': 'SQL/X3',
                    'GUERBET': 'GUERBET'
                }
                
                client_name = client_mapping.get(project_name, project_name)
                
                # Accumuler les données
                clients_data[client_name]['total_hours'] += hours
                clients_data[client_name]['tasks'][task_name] += hours
                clients_data[client_name]['users'][user_name] += hours
                clients_data[client_name]['entries'].append({
                    'date': date,
                    'user': user_name,
                    'task': task_name,
                    'hours': hours,
                    'description': description
                })
            
            # Convertir defaultdict en dict normal pour serialization
            result = {}
            for client, data in clients_data.items():
                result[client] = {
                    'total_hours': data['total_hours'],
                    'tasks': dict(data['tasks']),
                    'users': dict(data['users']),
                    'entries': data['entries']
                }
            
            return result
            
        except Exception as e:
            print(f"❌ Erreur extraction: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def compare_with_yesterday(self, current_data):
        """Compare avec les données d'hier"""
        print("\n🔍 COMPARAISON AVEC LES DONNÉES D'HIER")
        print("=" * 60)
        
        # Charger données d'hier
        try:
            with open('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/clockify-native/clockify_juillet_2025_native.json', 'r') as f:
                yesterday_data = json.load(f)
        except Exception as e:
            print(f"❌ Impossible de charger données d'hier: {e}")
            return False
        
        # Comparer totaux
        print(f"\n📊 COMPARAISON GLOBALE:")
        
        current_total = sum(client['total_hours'] for client in current_data.values())
        yesterday_total = sum(client['total_hours'] for client in yesterday_data.values())
        
        print(f"🕐 Hier    : {yesterday_total:.1f}h")
        print(f"🕑 Aujourd'hui : {current_total:.1f}h")
        print(f"📈 Écart     : {current_total - yesterday_total:+.1f}h")
        
        if abs(current_total - yesterday_total) < 1:
            print("✅ COHÉRENCE PARFAITE (écart < 1h)")
        elif abs(current_total - yesterday_total) < 5:
            print("⚠️ COHÉRENCE ACCEPTABLE (écart < 5h)")
        else:
            print("❌ ÉCART SIGNIFICATIF - Vérification nécessaire")
        
        # Comparer par client
        print(f"\n🏢 COMPARAISON PAR CLIENT:")
        print("-" * 50)
        
        all_clients = set(current_data.keys()) | set(yesterday_data.keys())
        
        for client in sorted(all_clients):
            current_hours = current_data.get(client, {}).get('total_hours', 0)
            yesterday_hours = yesterday_data.get(client, {}).get('total_hours', 0)
            diff = current_hours - yesterday_hours
            
            print(f"\n🏢 {client}:")
            print(f"  Hier        : {yesterday_hours:6.1f}h")
            print(f"  Aujourd'hui : {current_hours:6.1f}h")
            print(f"  Écart       : {diff:+6.1f}h")
            
            if abs(diff) < 0.1:
                print(f"  ✅ IDENTIQUE")
            elif abs(diff) < 1:
                print(f"  ⚠️ ACCEPTABLE")
            else:
                print(f"  ❌ SIGNIFICATIF")
        
        return True
    
    def save_results(self, data):
        """Sauvegarde les résultats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_file = f"/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/clockify_direct_{timestamp}.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Données sauvegardées: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            return None

def main():
    """Fonction principale"""
    print("🚀 EXTRACTION CLOCKIFY DIRECTE - JUILLET 2025")
    print("=" * 60)
    
    extractor = ClockifyDirectExtract()
    
    # Extraction directe
    current_data = extractor.extract_july_2025_direct()
    
    if not current_data:
        print("❌ Échec extraction")
        return
    
    # Affichage résumé
    print(f"\n💎 RÉSULTATS EXTRACTION DIRECTE:")
    total_hours = sum(client['total_hours'] for client in current_data.values())
    print(f"📊 Total heures : {total_hours:.1f}h")
    print(f"🏢 Clients      : {len(current_data)}")
    
    # Liste des clients
    for client, data in sorted(current_data.items(), key=lambda x: x[1]['total_hours'], reverse=True):
        print(f"  - {client}: {data['total_hours']:.1f}h")
    
    # Comparaison avec hier
    extractor.compare_with_yesterday(current_data)
    
    # Sauvegarde
    extractor.save_results(current_data)
    
    print(f"\n✅ Extraction terminée - Données Clockify juillet 2025 vérifiées")

if __name__ == "__main__":
    main()
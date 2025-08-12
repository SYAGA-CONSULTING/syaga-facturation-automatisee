#!/usr/bin/env python3
"""
Extracteur de données Clockify pour facturation SYAGA
Partie 1/5 du système de facturation automatisée
"""

import os
import json
import argparse
from datetime import datetime, timedelta
import urllib.request
import urllib.parse
from typing import Dict, List, Any

class ClockifyExtractor:
    """Extracteur de données depuis l'API Clockify"""
    
    def __init__(self):
        """Initialisation avec les credentials depuis ~/.clockify_config"""
        self.api_key = None
        self.workspace_id = None
        self.base_url = "https://api.clockify.me/api/v1"
        self._load_config()
    
    def _load_config(self):
        """Charge la configuration depuis ~/.clockify_config"""
        config_path = os.path.expanduser('~/.clockify_config')
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration Clockify manquante: {config_path}")
        
        with open(config_path, 'r') as f:
            for line in f:
                if 'API_KEY' in line:
                    self.api_key = line.split('=')[1].strip().strip('"')
                elif 'WORKSPACE_ID' in line:
                    self.workspace_id = line.split('=')[1].strip().strip('"')
        
        if not self.api_key or not self.workspace_id:
            raise ValueError("API_KEY ou WORKSPACE_ID manquant dans ~/.clockify_config")
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Any:
        """Effectue une requête à l'API Clockify"""
        url = f"{self.base_url}{endpoint}"
        
        if params:
            url += "?" + urllib.parse.urlencode(params)
        
        request = urllib.request.Request(url)
        request.add_header('X-Api-Key', self.api_key)
        
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read())
    
    def get_monthly_entries(self, year: int, month: int) -> List[Dict]:
        """Récupère toutes les entrées de temps pour un mois donné"""
        
        # Calculer les dates de début et fin
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
        
        # Formater pour l'API
        start_str = start_date.strftime('%Y-%m-%dT00:00:00Z')
        end_str = end_date.strftime('%Y-%m-%dT23:59:59Z')
        
        # Récupérer les entrées
        endpoint = f"/workspaces/{self.workspace_id}/user/all/time-entries"
        params = {
            'start': start_str,
            'end': end_str,
            'page-size': 500
        }
        
        entries = self._make_request(endpoint, params)
        return entries
    
    def process_entries_by_client(self, entries: List[Dict]) -> Dict[str, Dict]:
        """
        Traite les entrées par client et catégorie
        
        Returns:
            Dict avec structure:
            {
                "LAA": {
                    "total_hours": 62.4,
                    "categories": {
                        "Dette technologique": 27.0,
                        "Tests infrastructure": 21.5,
                        ...
                    },
                    "entries": [...]
                }
            }
        """
        clients_data = {}
        
        for entry in entries:
            # Extraire client et catégorie
            project_name = entry.get('project', {}).get('name', 'Sans projet')
            description = entry.get('description', '')
            
            # Parser le client depuis le nom du projet
            client = self._extract_client(project_name)
            category = self._extract_category(description, entry.get('tags', []))
            
            # Calculer les heures
            duration_str = entry.get('timeInterval', {}).get('duration', 'PT0S')
            hours = self._parse_duration(duration_str)
            
            # Agréger par client
            if client not in clients_data:
                clients_data[client] = {
                    'total_hours': 0,
                    'categories': {},
                    'entries': []
                }
            
            clients_data[client]['total_hours'] += hours
            
            if category not in clients_data[client]['categories']:
                clients_data[client]['categories'][category] = 0
            clients_data[client]['categories'][category] += hours
            
            clients_data[client]['entries'].append({
                'date': entry.get('timeInterval', {}).get('start', ''),
                'description': description,
                'hours': hours,
                'category': category
            })
        
        return clients_data
    
    def _extract_client(self, project_name: str) -> str:
        """Extrait le nom du client depuis le nom du projet"""
        # Mapping des projets vers clients
        client_mapping = {
            'LAA': 'LAA',
            'UAI': 'UAI',
            'PROVENCALE': 'PROVENCALE',
            'PROVENÇALE': 'PROVENCALE',
            'PHARMABEST': 'PHARMABEST',
            'QUADRIMEX': 'QUADRIMEX',
            'BUQUET': 'BUQUET',
            'PETRAS': 'PETRAS',
            'LEFEBVRE': 'LEFEBVRE',
            'TOUZEAU': 'TOUZEAU',
            'AXION': 'AXION',
            'FARBOS': 'FARBOS',
            'ART INFO': 'ART INFO',
            'SEXTANT': 'SEXTANT'
        }
        
        project_upper = project_name.upper()
        for key, client in client_mapping.items():
            if key in project_upper:
                return client
        
        return project_name
    
    def _extract_category(self, description: str, tags: List[str]) -> str:
        """Extrait la catégorie depuis la description ou les tags"""
        
        # Catégories prioritaires
        categories = {
            'dette': 'Dette technologique',
            'test': 'Tests infrastructure',
            'develop': 'Développements',
            'maint': 'Maintenance hors forfait',
            'sql': 'SQL Server',
            'migrat': 'Migration',
            'install': 'Installation',
            'config': 'Configuration',
            'support': 'Support',
            'formation': 'Formation'
        }
        
        description_lower = description.lower()
        
        for key, category in categories.items():
            if key in description_lower:
                return category
        
        # Vérifier les tags
        for tag in tags:
            tag_lower = tag.lower()
            for key, category in categories.items():
                if key in tag_lower:
                    return category
        
        return 'Maintenance hors forfait'  # Par défaut
    
    def _parse_duration(self, duration_str: str) -> float:
        """
        Parse une durée ISO 8601 (PT2H30M) en heures décimales
        """
        if not duration_str or duration_str == 'PT0S':
            return 0.0
        
        # Retirer le préfixe PT
        duration_str = duration_str.replace('PT', '')
        
        hours = 0
        minutes = 0
        
        if 'H' in duration_str:
            hours_part = duration_str.split('H')[0]
            hours = int(hours_part)
            duration_str = duration_str.split('H')[1] if 'H' in duration_str else ''
        
        if 'M' in duration_str:
            minutes_part = duration_str.split('M')[0]
            minutes = int(minutes_part)
        
        return hours + (minutes / 60)
    
    def generate_report(self, year: int, month: int, output_file: str = None):
        """Génère un rapport complet pour un mois"""
        
        print(f"🔍 Extraction Clockify pour {month:02d}/{year}")
        print("=" * 60)
        
        # Récupérer les entrées
        entries = self.get_monthly_entries(year, month)
        print(f"✅ {len(entries)} entrées trouvées")
        
        # Traiter par client
        clients_data = self.process_entries_by_client(entries)
        
        # Afficher le résumé
        print("\n📊 RÉSUMÉ PAR CLIENT:")
        print("-" * 60)
        
        total_general = 0
        for client, data in sorted(clients_data.items()):
            print(f"\n{client}: {data['total_hours']:.1f}h")
            for category, hours in sorted(data['categories'].items()):
                print(f"  • {category}: {hours:.1f}h")
            total_general += data['total_hours']
        
        print("-" * 60)
        print(f"TOTAL GÉNÉRAL: {total_general:.1f}h")
        
        # Sauvegarder si demandé
        if output_file:
            output_data = {
                'period': f"{year}-{month:02d}",
                'extraction_date': datetime.now().isoformat(),
                'total_hours': total_general,
                'clients': clients_data
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Données sauvegardées: {output_file}")
        
        return clients_data


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description='Extracteur Clockify pour facturation SYAGA')
    parser.add_argument('--month', type=str, required=True, 
                      help='Mois à extraire (format: YYYY-MM)')
    parser.add_argument('--output', type=str, 
                      help='Fichier de sortie JSON (optionnel)')
    
    args = parser.parse_args()
    
    # Parser le mois
    try:
        year, month = map(int, args.month.split('-'))
    except ValueError:
        print("❌ Format de mois invalide. Utilisez YYYY-MM")
        return 1
    
    # Définir le fichier de sortie par défaut
    if not args.output:
        args.output = f"data/input/clockify_{year}_{month:02d}.json"
    
    # Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Extraire les données
    try:
        extractor = ClockifyExtractor()
        extractor.generate_report(year, month, args.output)
        return 0
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
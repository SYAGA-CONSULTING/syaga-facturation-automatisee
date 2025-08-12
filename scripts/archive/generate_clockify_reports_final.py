#!/usr/bin/env python3
"""
Génération des rapports Clockify pour les clients avec mapping correct
"""
import requests
import json
from datetime import datetime
from pathlib import Path
import math

# Charger config
config = {}
with open(Path.home() / '.clockify_config') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            config[key] = value

API_KEY = config['CLOCKIFY_API_KEY']
WORKSPACE_ID = '60f16583d5588e20a960e57d'

headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

# Mapping clients vers IDs
client_mapping = {
    'LAA': '627e2fa3e0a7bc21e80e89cf',
    'AXION': '63a9b88753ba936f1f2eb731',
    'FARBOS': '64abad47e35e5c1fb88c826d',
    'ART': '627e2fa3e0a7bc21e80e89ce',
    'LEFEBVRE': '62e3f0834f59c36eeddc9e9f',
    'PETRAS': '627e2fa3e0a7bc21e80e89d0',
    'TOUZEAU': '627e2fa3e0a7bc21e80e89d3',
    'ANONE': '630f831f53ba936f1f51e5db',
    'QUADRIMEX': '62e3f2f19bb97a39d59b8f56',
    'PROVENCALE': '627e2fa453ba936f1fe07e48'
}

# Période août 2025
start = "2025-08-01T00:00:00Z"
end = "2025-08-10T23:59:59Z"

print("📊 GÉNÉRATION RAPPORTS CLOCKIFY - AOÛT 2025")
print("=" * 60)

# Créer dossier rapports
Path("rapports_clockify").mkdir(exist_ok=True)

for client_name, client_id in client_mapping.items():
    print(f"\n🔍 {client_name}...")
    
    # Récupérer temps via l'API Reports
    data = {
        "dateRangeStart": start,
        "dateRangeEnd": end,
        "clients": [client_id],
        "detailedFilter": {
            "page": 1,
            "pageSize": 1000
        }
    }
    
    r = requests.post(
        f"https://reports.api.clockify.me/v1/workspaces/{WORKSPACE_ID}/reports/detailed",
        headers=headers,
        json=data
    )
    
    if r.status_code == 200:
        result = r.json()
        entries = result.get('timeentries', [])
        
        if entries:
            # Calculer total
            total_seconds = sum(e['timeInterval']['duration'] for e in entries)
            heures_brutes = total_seconds / 3600
            
            # Arrondi commercial 10 minutes (1/6 d'heure)
            heures_arrondies = math.ceil(heures_brutes * 6) / 6
            
            # Taux horaire
            taux = 120 if client_name == 'LEFEBVRE' else 100
            montant = heures_arrondies * taux
            
            print(f"  ✅ {heures_brutes:.2f}h → {heures_arrondies:.2f}h = {montant:.0f}€ HT")
            
            # Générer rapport détaillé
            rapport_path = f"rapports_clockify/{client_name}_aout2025.txt"
            with open(rapport_path, 'w', encoding='utf-8') as f:
                f.write(f"RAPPORT D'ACTIVITÉ - {client_name}\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Période: 1-10 août 2025\n")
                f.write(f"Client: {client_name}\n\n")
                
                f.write("RÉCAPITULATIF\n")
                f.write("-" * 30 + "\n")
                f.write(f"Heures travaillées: {heures_brutes:.2f}h\n")
                f.write(f"Heures facturées: {heures_arrondies:.2f}h\n")
                f.write(f"Taux horaire: {taux}€/h HT\n")
                f.write(f"Montant total: {montant:.0f}€ HT\n\n")
                
                f.write("DÉTAIL DES INTERVENTIONS\n")
                f.write("-" * 30 + "\n")
                
                # Grouper par date
                by_date = {}
                for entry in entries:
                    date = entry['timeInterval']['start'][:10]
                    if date not in by_date:
                        by_date[date] = []
                    by_date[date].append(entry)
                
                for date in sorted(by_date.keys()):
                    f.write(f"\n{date}:\n")
                    for entry in by_date[date]:
                        duration = entry['timeInterval']['duration'] / 3600
                        desc = entry.get('description', 'N/A')
                        f.write(f"  • {duration:.2f}h - {desc[:60]}\n")
                
                f.write("\n" + "=" * 50 + "\n")
                f.write("Rapport généré automatiquement via Clockify API\n")
                f.write(f"Date génération: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            
            print(f"  📄 Rapport sauvé: {rapport_path}")
        else:
            print(f"  ⚪ Pas d'activité en août 2025")
    else:
        print(f"  ❌ Erreur API: {r.status_code}")

print("\n" + "=" * 60)
print("✅ GÉNÉRATION TERMINÉE")
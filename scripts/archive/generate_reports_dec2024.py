#!/usr/bin/env python3
"""
Génération des rapports Clockify pour décembre 2024
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

# Mapping clients (IDs récupérés du listing)
clients = {
    'LAA': '627e2fa3e0a7bc21e80e89cf',
    'AXION': '63a9b88753ba936f1f2eb731',
    'FARBOS': '64abad47e35e5c1fb88c826d',
    'ART': '627e2fa3e0a7bc21e80e89ce',
    'LEFEBVRE': '62e3f0834f59c36eeddc9e9f',
    'PETRAS': '627e2fa3e0a7bc21e80e89d0',
    'TOUZEAU': '627e2fa3e0a7bc21e80e89d3',
    'ANONE': '630f831f53ba936f1f51e5db',
    'QUADRIMEX': '62e3f2f19bb97a39d59b8f56',
    'LA PROVENCALE': '627e2fa453ba936f1fe07e48'
}

# Période décembre 2024
start = "2024-12-01T00:00:00Z"
end = "2024-12-31T23:59:59Z"

print("📊 RAPPORTS CLOCKIFY - DÉCEMBRE 2024")
print("=" * 60)

# Créer dossier
Path("rapports_clockify").mkdir(exist_ok=True)

totaux = []

for client_name, client_id in clients.items():
    data = {
        "dateRangeStart": start,
        "dateRangeEnd": end,
        "clients": {
            "ids": [client_id]
        },
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
            # Calculs
            total_seconds = sum(e['timeInterval']['duration'] for e in entries)
            heures_brutes = total_seconds / 3600
            heures_arrondies = math.ceil(heures_brutes * 6) / 6  # Arrondi 10min
            taux = 120 if client_name == 'LEFEBVRE' else 100
            montant = heures_arrondies * taux
            
            print(f"✅ {client_name:15} : {heures_brutes:6.2f}h → {heures_arrondies:6.2f}h = {montant:7.0f}€")
            totaux.append((client_name, heures_arrondies, montant))
            
            # Rapport détaillé
            with open(f"rapports_clockify/{client_name}_dec2024.txt", 'w', encoding='utf-8') as f:
                f.write(f"RAPPORT CLOCKIFY - {client_name}\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Période: Décembre 2024\n")
                f.write(f"Heures travaillées: {heures_brutes:.2f}h\n")
                f.write(f"Heures facturées (arrondi 10min): {heures_arrondies:.2f}h\n")
                f.write(f"Taux horaire: {taux}€/h HT\n")
                f.write(f"MONTANT TOTAL: {montant:.0f}€ HT\n\n")
                
                f.write("DÉTAIL:\n")
                f.write("-" * 30 + "\n")
                
                # Grouper par date
                by_date = {}
                for entry in entries:
                    date = entry['timeInterval']['start'][:10]
                    if date not in by_date:
                        by_date[date] = []
                    by_date[date].append(entry)
                
                for date in sorted(by_date.keys()):
                    jour_seconds = sum(e['timeInterval']['duration'] for e in by_date[date])
                    jour_heures = jour_seconds / 3600
                    f.write(f"\n{date} ({jour_heures:.2f}h):\n")
                    for entry in by_date[date]:
                        duration = entry['timeInterval']['duration'] / 3600
                        desc = entry.get('description', 'Intervention')
                        f.write(f"  • {duration:.2f}h - {desc[:60]}\n")
        else:
            print(f"⚪ {client_name:15} : Pas d'activité")

# Résumé
print("\n" + "=" * 60)
print("📈 RÉSUMÉ:")
if totaux:
    total_heures = sum(t[1] for t in totaux)
    total_montant = sum(t[2] for t in totaux)
    print(f"\nTotal: {total_heures:.2f}h = {total_montant:.0f}€ HT")
    print("\nDétail par client:")
    for nom, heures, montant in sorted(totaux, key=lambda x: x[2], reverse=True):
        print(f"  • {nom:15} : {heures:6.2f}h = {montant:7.0f}€")
else:
    print("Aucune activité trouvée")

print(f"\n📄 Rapports sauvés dans: rapports_clockify/")
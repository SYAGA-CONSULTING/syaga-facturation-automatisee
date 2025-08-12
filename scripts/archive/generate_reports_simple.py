#!/usr/bin/env python3
"""
Génération simple des rapports Clockify
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

# Clients à traiter
clients = ['LAA', 'AXION', 'FARBOS', 'ART', 'LEFEBVRE', 'PETRAS', 'TOUZEAU']

# Août 2025
start = "2025-08-01T00:00:00Z"
end = "2025-08-10T23:59:59Z"

print("📊 GÉNÉRATION RAPPORTS CLOCKIFY")
print("=" * 50)

for client in clients:
    # Récupérer projets du client
    r = requests.get(f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/projects", headers=headers)
    projects = [p['id'] for p in r.json() if client.upper() in p['name'].upper()]
    
    if not projects:
        print(f"❌ {client}: Pas de projet trouvé")
        continue
    
    # Récupérer temps
    data = {
        "dateRangeStart": start,
        "dateRangeEnd": end,
        "projects": projects,
        "detailedFilter": {"page": 1, "pageSize": 1000}
    }
    
    r = requests.post(
        f"https://reports.api.clockify.me/v1/workspaces/{WORKSPACE_ID}/reports/detailed",
        headers=headers,
        json=data
    )
    
    if r.status_code == 200:
        result = r.json()
        entries = result.get('timeentries', [])
        
        total_seconds = sum(e['timeInterval']['duration'] for e in entries)
        heures = total_seconds / 3600
        heures_arrondies = math.ceil(heures * 6) / 6  # Arrondi 10 min
        
        taux = 120 if client == 'LEFEBVRE' else 100
        montant = heures_arrondies * taux
        
        print(f"✅ {client:10} : {heures:.2f}h → {heures_arrondies:.2f}h = {montant:.0f}€")
        
        # Créer rapport simple
        with open(f"{client}_rapport.txt", 'w') as f:
            f.write(f"RAPPORT CLOCKIFY - {client}\n")
            f.write(f"Période: Août 2025\n")
            f.write(f"Heures brutes: {heures:.2f}h\n")
            f.write(f"Heures arrondies: {heures_arrondies:.2f}h\n")
            f.write(f"Taux: {taux}€/h\n")
            f.write(f"Montant: {montant:.0f}€ HT\n")
    else:
        print(f"❌ {client}: Erreur API {r.status_code}")
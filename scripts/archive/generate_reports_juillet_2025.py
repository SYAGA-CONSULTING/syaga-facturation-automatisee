#!/usr/bin/env python3
"""
Génération des rapports Clockify pour JUILLET 2025
"""
import requests
import json
from datetime import datetime
from pathlib import Path
import math
import re

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

# Patterns de recherche
patterns = {
    'LAA': r'\b(LAA|Maroc)\b',
    'AIXAGON': r'\b(AIXAGON|CIML|BABA)\b', 
    'UAI': r'\b(UAI|HardenAD)\b',
    'AXION': r'\b(AXION|SLX|SalesLogix|SAGE)\b',
    'QUADRIMEX': r'\b(QUADRIMEX|SSIS|ETL)\b',
    'FARBOS': r'\b(FARBOS|Cuers|cuers)\b',
    'LEFEBVRE': r'\b(LEFEBVRE|Avocat|BOULOGNE)\b',
    'PETRAS': r'\b(PETRAS|Audit|GED)\b',
    'TOUZEAU': r'\b(TOUZEAU|Garage)\b',
    'ANONE': r'\b(ANONE|Maintenance)\b',
    'LA PROVENCALE': r'\b(PROVENCALE|Provençale)\b',
    'GUERBET': r'\b(GUERBET|Villepinte)\b',
    'PHARMABEST': r'\b(PHARMABEST|SAS|Carré Opéra)\b',
    'SYAGA': r'\b(SYAGA|Verif sauvegardes)\b',
}

# Période JUILLET 2025
start = "2025-07-01T00:00:00Z"
end = "2025-07-31T23:59:59Z"

print("📊 RAPPORTS CLOCKIFY - JUILLET 2025")
print("=" * 70)

# Récupérer toutes les entrées
data = {
    "dateRangeStart": start,
    "dateRangeEnd": end,
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
    all_entries = result.get('timeentries', [])
    
    print(f"📋 {len(all_entries)} entrées trouvées pour juillet 2025\n")
    
    if not all_entries:
        print("❌ AUCUNE ACTIVITÉ EN JUILLET 2025")
        print("\n💡 Vérification des périodes disponibles...")
        
        # Test autres périodes 2025
        for mois, nom in [(6, "JUIN"), (5, "MAI"), (4, "AVRIL"), (8, "AOÛT")]:
            test_start = f"2025-{mois:02d}-01T00:00:00Z"
            if mois == 12:
                test_end = "2026-01-01T00:00:00Z"
            else:
                test_end = f"2025-{mois+1:02d}-01T00:00:00Z"
            
            test_data = {
                "dateRangeStart": test_start,
                "dateRangeEnd": test_end,
                "detailedFilter": {"page": 1, "pageSize": 10}
            }
            
            r_test = requests.post(
                f"https://reports.api.clockify.me/v1/workspaces/{WORKSPACE_ID}/reports/detailed",
                headers=headers,
                json=test_data
            )
            
            if r_test.status_code == 200:
                test_result = r_test.json()
                nb_entries = len(test_result.get('timeentries', []))
                if nb_entries > 0:
                    print(f"  ✅ {nom} 2025: {nb_entries} entrées trouvées")
                else:
                    print(f"  ⚪ {nom} 2025: Aucune activité")
        
        exit()
    
    # Classifier les entrées par client
    by_client = {client: [] for client in patterns.keys()}
    by_client['NON_CLASSÉ'] = []
    
    for entry in all_entries:
        desc = entry.get('description', '')
        classified = False
        
        for client, pattern in patterns.items():
            if re.search(pattern, desc, re.IGNORECASE):
                by_client[client].append(entry)
                classified = True
                break
        
        if not classified:
            by_client['NON_CLASSÉ'].append(entry)
    
    # Créer dossier
    Path("rapports_juillet_2025").mkdir(exist_ok=True)
    
    # Générer rapports par client
    totaux = []
    
    print("CLIENTS AVEC ACTIVITÉ:")
    print("-" * 70)
    
    for client, entries in sorted(by_client.items()):
        if entries and client != 'NON_CLASSÉ':
            # Calculs
            total_seconds = sum(e['timeInterval']['duration'] for e in entries)
            heures_brutes = total_seconds / 3600
            heures_arrondies = math.ceil(heures_brutes * 6) / 6  # Arrondi 10min
            taux = 120 if client == 'LEFEBVRE' else 100
            montant = heures_arrondies * taux
            
            print(f"✅ {client:15} : {len(entries):3} entrées | {heures_brutes:6.2f}h → {heures_arrondies:6.2f}h = {montant:7.0f}€")
            totaux.append((client, heures_arrondies, montant, len(entries)))
            
            # Rapport détaillé
            with open(f"rapports_juillet_2025/{client}_juillet2025.txt", 'w', encoding='utf-8') as f:
                f.write(f"{'='*60}\n")
                f.write(f"RAPPORT D'ACTIVITÉ - {client}\n")
                f.write(f"{'='*60}\n\n")
                f.write(f"Période: Juillet 2025\n")
                f.write(f"Client: {client}\n\n")
                
                f.write("SYNTHÈSE\n")
                f.write("-" * 40 + "\n")
                f.write(f"Nombre d'interventions: {len(entries)}\n")
                f.write(f"Heures travaillées: {heures_brutes:.2f}h\n")
                f.write(f"Heures facturées (arrondi 10min): {heures_arrondies:.2f}h\n")
                f.write(f"Taux horaire: {taux}€/h HT\n")
                f.write(f"MONTANT TOTAL: {montant:.0f}€ HT\n\n")
                
                f.write("DÉTAIL DES INTERVENTIONS\n")
                f.write("-" * 40 + "\n")
                
                # Trier par date
                entries.sort(key=lambda x: x['timeInterval']['start'])
                
                for entry in entries:
                    date = entry['timeInterval']['start'][:10]
                    duration = entry['timeInterval']['duration'] / 3600
                    desc = entry.get('description', 'Intervention')
                    f.write(f"\n{date} ({duration:.2f}h):\n")
                    f.write(f"  {desc}\n")
    
    # Afficher non classés
    if by_client['NON_CLASSÉ']:
        print(f"\n⚠️ ENTRÉES NON CLASSÉES: {len(by_client['NON_CLASSÉ'])}")
        for entry in by_client['NON_CLASSÉ'][:5]:
            date = entry['timeInterval']['start'][:10]
            duration = entry['timeInterval']['duration'] / 3600
            desc = entry.get('description', 'N/A')[:60]
            print(f"  {date} ({duration:.2f}h): {desc}")
    
    # Résumé final
    if totaux:
        print("\n" + "=" * 70)
        print("📈 RÉSUMÉ JUILLET 2025")
        print("-" * 40)
        
        total_heures = sum(t[1] for t in totaux)
        total_montant = sum(t[2] for t in totaux)
        
        print(f"💰 TOTAL: {total_heures:.2f}h = {total_montant:.0f}€ HT\n")
        
        for nom, heures, montant, nb in sorted(totaux, key=lambda x: x[2], reverse=True):
            print(f"  {nom:15} : {heures:6.2f}h = {montant:7.0f}€ ({nb} interventions)")
        
        print(f"\n📄 Rapports sauvés: rapports_juillet_2025/")
    else:
        print("\n❌ Aucun client avec activité en juillet 2025")
else:
    print(f"❌ Erreur API: {r.status_code}")
    print(r.text)
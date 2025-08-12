#!/usr/bin/env python3
"""
Génération complète des rapports Clockify avec tous les clients
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

# Patterns améliorés pour identifier TOUS les clients
patterns = {
    'LAA': r'\b(LAA|Maroc)\b',
    'AIXAGON': r'\b(AIXAGON|CIML|BABA)\b',
    'UAI': r'\b(UAI|HardenAD)\b',
    'AXION': r'\b(AXION|SLX|SalesLogix|SAGE)\b',
    'QUADRIMEX': r'\b(QUADRIMEX|SSIS|ETL|OTR)\b',
    'FARBOS': r'\b(FARBOS|Cuers|cuers)\b',
    'LEFEBVRE': r'\b(LEFEBVRE|Avocat|BOULOGNE)\b',
    'PETRAS': r'\b(PETRAS|Audit|GED)\b',
    'TOUZEAU': r'\b(TOUZEAU|Garage)\b',
    'ANONE': r'\b(ANONE|Maintenance)\b',
    'LA PROVENCALE': r'\b(PROVENCALE|Provençale)\b',
    'GUERBET': r'\b(GUERBET|Villepinte)\b',
    'PHARMABEST': r'\b(PHARMABEST|SAS|Carré Opéra|Leslie|CARRE OPERA)\b',
    'SYAGA': r'\b(SYAGA|Verif sauvegardes|réplications)\b',
    'JARDINIERS SAP': r'\b(JARDINIERS|SAP)\b',
    'SEMARDEL': r'\b(SEMARDEL)\b',
    'VINDILIS': r'\b(VINDILIS)\b',
    'DORANGE': r'\b(DORANGE)\b',
    'BUQUET': r'\b(BUQUET)\b',
    'BELFONTE': r'\b(BELFONTE)\b',
}

# Période janvier 2025
start = "2025-01-01T00:00:00Z"
end = "2025-01-31T23:59:59Z"

print("📊 RAPPORTS CLOCKIFY COMPLETS - JANVIER 2025")
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
    
    print(f"📋 {len(all_entries)} entrées trouvées pour janvier 2025\n")
    
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
    Path("rapports_janvier_2025").mkdir(exist_ok=True)
    
    # Générer rapports par client
    totaux = []
    
    print("CLIENTS AVEC ACTIVITÉ:")
    print("-" * 70)
    
    for client, entries in sorted(by_client.items()):
        if entries and client != 'NON_CLASSÉ':
            # Calculs
            total_seconds = sum(e['timeInterval']['duration'] for e in entries)
            heures_brutes = total_seconds / 3600
            
            # Arrondi commercial 10 minutes (1/6 d'heure)
            heures_arrondies = math.ceil(heures_brutes * 6) / 6
            
            # Taux horaire
            taux = 120 if client == 'LEFEBVRE' else 100
            montant = heures_arrondies * taux
            
            print(f"✅ {client:15} : {len(entries):3} entrées | {heures_brutes:6.2f}h → {heures_arrondies:6.2f}h = {montant:7.0f}€")
            totaux.append((client, heures_arrondies, montant, len(entries)))
            
            # Rapport détaillé
            with open(f"rapports_janvier_2025/{client}_janvier2025.txt", 'w', encoding='utf-8') as f:
                f.write(f"{'='*60}\n")
                f.write(f"RAPPORT D'ACTIVITÉ - {client}\n")
                f.write(f"{'='*60}\n\n")
                f.write(f"Période: Janvier 2025\n")
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
                
                # Grouper par semaine
                current_week = None
                week_hours = 0
                
                for entry in entries:
                    date = entry['timeInterval']['start'][:10]
                    week = datetime.fromisoformat(date).isocalendar()[1]
                    
                    if current_week != week:
                        if current_week is not None:
                            f.write(f"\n  → Total semaine: {week_hours:.2f}h\n")
                        f.write(f"\n🗓️ Semaine {week}:\n")
                        current_week = week
                        week_hours = 0
                    
                    duration = entry['timeInterval']['duration'] / 3600
                    week_hours += duration
                    desc = entry.get('description', 'Intervention')
                    f.write(f"\n  {date} ({duration:.2f}h):\n")
                    f.write(f"    {desc}\n")
                
                if current_week is not None:
                    f.write(f"\n  → Total semaine: {week_hours:.2f}h\n")
                
                f.write("\n" + "=" * 60 + "\n")
                f.write(f"Rapport généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                f.write("Via Clockify API - Arrondi commercial 10 minutes\n")
    
    # Afficher non classés
    if by_client['NON_CLASSÉ']:
        print(f"\n⚠️ ENTRÉES NON CLASSÉES: {len(by_client['NON_CLASSÉ'])}")
        print("-" * 40)
        for entry in by_client['NON_CLASSÉ'][:10]:
            date = entry['timeInterval']['start'][:10]
            duration = entry['timeInterval']['duration'] / 3600
            desc = entry.get('description', 'N/A')[:60]
            print(f"  {date} ({duration:.2f}h): {desc}")
        if len(by_client['NON_CLASSÉ']) > 10:
            print(f"  ... et {len(by_client['NON_CLASSÉ'])-10} autres")
    
    # Résumé final
    print("\n" + "=" * 70)
    print("📈 RÉSUMÉ FACTURACTION JANVIER 2025")
    print("=" * 70)
    
    if totaux:
        total_heures = sum(t[1] for t in totaux)
        total_montant = sum(t[2] for t in totaux)
        total_interventions = sum(t[3] for t in totaux)
        
        print(f"\n💰 TOTAL GÉNÉRAL:")
        print(f"  • {total_interventions} interventions")
        print(f"  • {total_heures:.2f} heures facturables")
        print(f"  • {total_montant:.0f}€ HT\n")
        
        print("DÉTAIL PAR CLIENT (triés par montant):")
        print("-" * 40)
        for nom, heures, montant, nb in sorted(totaux, key=lambda x: x[2], reverse=True):
            print(f"  {nom:15} : {heures:6.2f}h = {montant:7.0f}€ ({nb} interventions)")
    
    # Sauvegarder résumé global
    with open("rapports_janvier_2025/RESUME_JANVIER_2025.txt", 'w', encoding='utf-8') as f:
        f.write("RÉSUMÉ FACTURATION - JANVIER 2025\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total général: {total_montant:.0f}€ HT\n")
        f.write(f"Total heures: {total_heures:.2f}h\n")
        f.write(f"Nombre de clients: {len(totaux)}\n\n")
        f.write("Détail par client:\n")
        for nom, heures, montant, nb in sorted(totaux, key=lambda x: x[2], reverse=True):
            f.write(f"  • {nom:15} : {heures:6.2f}h = {montant:7.0f}€\n")
    
    print(f"\n📄 {len(totaux)} rapports sauvés dans: rapports_janvier_2025/")
    print(f"📊 Résumé global: rapports_janvier_2025/RESUME_JANVIER_2025.txt")
else:
    print(f"❌ Erreur API: {r.status_code}")
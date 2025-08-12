#!/usr/bin/env python3
"""
Liste détaillée des factures avec date d'envoi dans Excel
"""

import pandas as pd

print('📋 LISTE COMPLÈTE DES FACTURES AVEC DATE D\'ENVOI')
print('='*80)

# Charger l'Excel
excel_path = r"/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/DOCS-OFFICIELS/01-ENTITES/SYAGA-CONSULTING-SARL/05-Commercial-Ventes/Facturation en cours 2017-12-31.xlsx"
df = pd.read_excel(excel_path, sheet_name='31-07-2024', header=1)

factures_avec_date = []

for i in range(len(df)):
    try:
        ligne = i + 2  # Numéro de ligne Excel
        client = str(df.iloc[i, 2]) if pd.notna(df.iloc[i, 2]) else ''
        facture = str(df.iloc[i, 4]) if pd.notna(df.iloc[i, 4]) else ''
        montant = df.iloc[i, 6] if pd.notna(df.iloc[i, 6]) else 0
        date_envoi = df.iloc[i, 10] if pd.notna(df.iloc[i, 10]) else ''  # Colonne 10 = Fact. Env.
        
        # Si il y a une date d'envoi et un montant
        if date_envoi and str(date_envoi) != 'nan' and montant > 0:
            # Formater la date si c'est un timestamp
            if hasattr(date_envoi, 'strftime'):
                date_str = date_envoi.strftime('%d/%m/%Y')
            else:
                date_str = str(date_envoi)[:10]
            
            factures_avec_date.append({
                'ligne': ligne,
                'client': client,
                'facture': facture,
                'montant': montant,
                'date_envoi': date_str
            })
    except:
        pass

# Trier par numéro de facture
factures_avec_date.sort(key=lambda x: x['facture'])

print(f'✅ FACTURES AVEC DATE D\'ENVOI : {len(factures_avec_date)} factures')
print('-'*80)
print(f'{"Ligne":<6} {"N° Facture":<35} {"Client":<20} {"Montant":<10} {"Date envoi":<12}')
print('-'*80)

total = 0
for f in factures_avec_date:
    print(f'L{f["ligne"]:<5} {f["facture"][:35]:<35} {f["client"][:20]:<20} {f["montant"]:>8.0f}€  {f["date_envoi"]}')
    total += f["montant"]

print('-'*80)
print(f'{"TOTAL":<62} {total:>8.0f}€')

# Extraire uniquement les numéros F2025
print('\n📊 NUMÉROS F2025 UNIQUES AVEC DATE D\'ENVOI:')
print('-'*80)

import re
numeros_f2025 = set()
for f in factures_avec_date:
    matches = re.findall(r'F2025\d{3,4}', f['facture'])
    for num in matches:
        numeros_f2025.add(num)

for num in sorted(numeros_f2025):
    print(f'  {num}')

print(f'\nTotal : {len(numeros_f2025)} numéros F2025 uniques avec date d\'envoi')
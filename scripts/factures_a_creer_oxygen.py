#!/usr/bin/env python3
"""
Identifier les factures à créer dans Oxygen
(celles qui n'ont pas de numéro F2025xxxx)
"""

import pandas as pd

excel_path = r"/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/DOCS-OFFICIELS/01-ENTITES/SYAGA-CONSULTING-SARL/05-Commercial-Ventes/Facturation en cours 2017-12-31.xlsx"
df = pd.read_excel(excel_path, sheet_name='31-07-2024')

print('📝 FACTURES À CRÉER DANS OXYGEN - JUILLET 2025')
print('=' * 80)
print()

# Parcourir la zone juillet (lignes 44-74)
factures_a_creer = []
factures_existantes = []

for i in range(42, 73):  # Lignes Excel 44-74
    client = str(df.iloc[i, 2]) if pd.notna(df.iloc[i, 2]) else ''
    facture = str(df.iloc[i, 4]) if pd.notna(df.iloc[i, 4]) else ''
    montant = df.iloc[i, 6] if pd.notna(df.iloc[i, 6]) else 0
    date_envoi = df.iloc[i, 11] if pd.notna(df.iloc[i, 11]) else ''
    
    try:
        montant_num = float(montant)
    except:
        montant_num = 0
    
    if client and client != 'nan' and montant_num > 0:
        # Vérifier si c'est une facture avec numéro F2025
        if 'F2025' in str(facture):
            factures_existantes.append({
                'ligne': i+2,
                'client': client,
                'facture': facture,
                'montant': montant_num,
                'envoyee': bool(date_envoi and str(date_envoi) != 'nan')
            })
        else:
            # Facture à créer
            factures_a_creer.append({
                'ligne': i+2,
                'client': client,
                'description': facture if facture != 'nan' else 'Hors-forfait',
                'montant': montant_num
            })

# Afficher les factures existantes
print('✅ FACTURES DÉJÀ CRÉÉES (avec numéro F2025xxxx):')
print('-' * 80)
if factures_existantes:
    total_existant = 0
    for f in sorted(factures_existantes, key=lambda x: x['facture']):
        statut = "📧 Envoyée" if f['envoyee'] else "📝 À envoyer"
        print(f"L{f['ligne']:<4} {f['facture']:<15} {f['client']:<20} {f['montant']:>8.0f}€  {statut}")
        total_existant += f['montant']
    print('-' * 80)
    print(f'{"TOTAL EXISTANT":<40} {total_existant:>8.0f}€')
else:
    print("(Aucune)")

# Grouper les factures à créer par client
print('\n\n🔴 FACTURES À CRÉER DANS OXYGEN:')
print('=' * 80)

clients_groupes = {}
for f in factures_a_creer:
    client_key = f['client'].split()[0].upper()
    if 'LAA' in f['client'] and 'MAROC' not in f['client']:
        client_key = 'LAA'
    
    if client_key not in clients_groupes:
        clients_groupes[client_key] = []
    clients_groupes[client_key].append(f)

# Afficher par client
numero_facture = 750  # Commencer après F20250749
total_a_creer = 0

for client, factures in sorted(clients_groupes.items()):
    print(f'\n📌 {client}:')
    print('-' * 60)
    
    sous_total = 0
    for f in factures:
        numero_facture += 1
        suggestion = f'F2025{numero_facture:04d}'
        
        # Déterminer le type
        desc = f['description'].lower()
        if 'dette' in desc:
            type_fact = 'Dette technologique'
        elif 'test' in desc:
            type_fact = 'Tests infrastructure'
        elif 'développe' in desc:
            type_fact = 'Développements ponctuels'
        elif 'hors' in desc or 'hf' in desc:
            type_fact = 'Maintenance hors-forfait'
        else:
            type_fact = f['description']
        
        print(f"  L{f['ligne']:<4} {suggestion} : {type_fact:<30} {f['montant']:>8.0f}€")
        sous_total += f['montant']
    
    print(f"  {'SOUS-TOTAL':<46} {sous_total:>8.0f}€")
    total_a_creer += sous_total

# Résumé final
print('\n' + '=' * 80)
print('📊 RÉSUMÉ:')
print('-' * 80)
print(f'  Factures existantes: {len(factures_existantes)} factures = {sum(f["montant"] for f in factures_existantes):,.0f}€')
print(f'  Factures à créer: {len(factures_a_creer)} factures = {total_a_creer:,.0f}€')
print(f'  TOTAL JUILLET: {sum(f["montant"] for f in factures_existantes) + total_a_creer:,.0f}€')

# Actions à faire
print('\n' + '=' * 80)
print('✅ ACTIONS À EFFECTUER:')
print('-' * 80)
print('\n1️⃣ CRÉER DANS OXYGEN:')
for client in sorted(clients_groupes.keys()):
    nb = len(clients_groupes[client])
    total = sum(f['montant'] for f in clients_groupes[client])
    print(f'   • {client}: {nb} facture(s) = {total:,.0f}€')

print('\n2️⃣ METTRE À JOUR EXCEL:')
print('   • Ajouter les numéros F2025xxxx dans colonne E')
print('   • Ajouter "(HF)" pour les hors-forfait Clockify')

print('\n3️⃣ ENVOYER LES FACTURES:')
print('   • Générer les PDF depuis Oxygen')
print('   • Envoyer par email aux clients')
print('   • Mettre la date d\'envoi dans colonne K')

print('\n4️⃣ SUIVRE LES PAIEMENTS:')
print('   • Une fois payé = supprimer la ligne Excel')
print('   • Archiver dans le système comptable')
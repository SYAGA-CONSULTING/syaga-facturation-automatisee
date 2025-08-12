#!/usr/bin/env python3
import pandas as pd

excel_path = r'/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/DOCS-OFFICIELS/01-ENTITES/SYAGA-CONSULTING-SARL/05-Commercial-Ventes/Facturation en cours 2017-12-31.xlsx'
df = pd.read_excel(excel_path, sheet_name='31-07-2024', header=1)

print('🔍 RECHERCHE DÉTAILLÉE - TOUTES les factures F2025')
print('='*80)

# Parcourir TOUTE la feuille pour trouver les F2025
f2025_sans_envoi = []
f2025_avec_envoi = []

for i in range(len(df)):
    try:
        client = str(df.iloc[i, 2]) if pd.notna(df.iloc[i, 2]) else ''
        facture = str(df.iloc[i, 4]) if pd.notna(df.iloc[i, 4]) else ''  # Colonne 4 = Numéro de facture
        montant = df.iloc[i, 6] if pd.notna(df.iloc[i, 6]) else 0  # Colonne 6 = A facturer
        date_envoi = df.iloc[i, 10] if pd.notna(df.iloc[i, 10]) else ''  # Colonne 10 = Fact. Env.
        
        # Si c'est une facture F2025
        if 'F2025' in str(facture) and montant > 0:
            if date_envoi and str(date_envoi) != 'nan':
                f2025_avec_envoi.append({
                    'ligne': i+2,
                    'client': client,
                    'facture': facture,
                    'montant': montant,
                    'date': date_envoi
                })
            else:
                f2025_sans_envoi.append({
                    'ligne': i+2,
                    'client': client, 
                    'facture': facture,
                    'montant': montant
                })
    except:
        pass

print('✅ FACTURES F2025 DÉJÀ ENVOYÉES:')
print('-'*80)
total_envoye = 0
for f in f2025_avec_envoi:
    print(f"L{f['ligne']:<4} {f['client']:<20} {f['facture']:<35} {f['montant']:>8.0f}€")
    total_envoye += f['montant']
print(f'Total: {len(f2025_avec_envoi)} factures = {total_envoye:,.0f}€')

print()
print('🔴 FACTURES F2025 NON ENVOYÉES (À ENVOYER):')
print('-'*80)
total_a_envoyer = 0
for f in f2025_sans_envoi:
    print(f"L{f['ligne']:<4} {f['client']:<20} {f['facture']:<35} {f['montant']:>8.0f}€")
    total_a_envoyer += f['montant']
print(f'Total: {len(f2025_sans_envoi)} factures = {total_a_envoyer:,.0f}€')

print()
print('='*80)
print('📊 RÉSUMÉ:')
print(f'• Factures F2025 envoyées: {len(f2025_avec_envoi)} = {total_envoye:,.0f}€')
print(f'• Factures F2025 à envoyer: {len(f2025_sans_envoi)} = {total_a_envoyer:,.0f}€')
print(f'• TOTAL F2025: {len(f2025_avec_envoi) + len(f2025_sans_envoi)} = {total_envoye + total_a_envoyer:,.0f}€')
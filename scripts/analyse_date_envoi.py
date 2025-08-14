#!/usr/bin/env python3
import pandas as pd

excel_path = r'/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/DOCS-OFFICIELS/01-ENTITES/SYAGA-CONSULTING-SARL/05-Commercial-Ventes/Facturation en cours 2017-12-31.xlsx'
df = pd.read_excel(excel_path, sheet_name='31-07-2024', header=1)

print('🔍 ANALYSE AVEC VOTRE RÈGLE : Sans date envoi = À facturer')
print('='*80)

a_facturer = []
deja_envoyees = []
total_a_facturer = 0
total_envoyees = 0

for i in range(42, 73):  # Zone juillet
    try:
        client = str(df.iloc[i, 2]) if pd.notna(df.iloc[i, 2]) else ''
        facture = str(df.iloc[i, 4]) if pd.notna(df.iloc[i, 4]) else ''
        montant = df.iloc[i, 6] if pd.notna(df.iloc[i, 6]) else 0
        date_envoi = df.iloc[i, 11] if pd.notna(df.iloc[i, 11]) else ''
        
        if client and client != 'nan' and montant > 0 and 'Sous-Total' not in str(client):
            if date_envoi and str(date_envoi) != 'nan':
                # Facture envoyée
                deja_envoyees.append(f'L{i+2:<3} {client:<15} {facture:<30} {montant:>8.0f}€')
                total_envoyees += montant
            else:
                # Facture à créer/envoyer
                source = 'Clockify/HF' if 'F2025' not in str(facture) else 'À envoyer'
                a_facturer.append(f'L{i+2:<3} {client:<15} {facture:<30} {montant:>8.0f}€ [{source}]')
                total_a_facturer += montant
    except:
        pass

print('✅ FACTURES DÉJÀ ENVOYÉES :')
print('-'*80)
for f in deja_envoyees:
    print(f)
print(f'\nTotal : {len(deja_envoyees)} factures = {total_envoyees:,.0f}€ HT')

print('\n🔴 FACTURES À CRÉER/FACTURER (JUILLET) :')
print('-'*80)
for f in a_facturer:
    print(f)
print(f'\nTotal : {len(a_facturer)} factures = {total_a_facturer:,.0f}€ HT')

print('\n' + '='*80)
print(f'📊 RÉCAPITULATIF JUILLET 2025 :')
print(f'• Factures envoyées : {len(deja_envoyees)} = {total_envoyees:,.0f}€ HT')
print(f'• Factures à créer : {len(a_facturer)} = {total_a_facturer:,.0f}€ HT')
print(f'• TOTAL JUILLET : {len(deja_envoyees) + len(a_facturer)} factures = {total_envoyees + total_a_facturer:,.0f}€ HT')
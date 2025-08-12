#!/usr/bin/env python3
import pandas as pd

excel_path = r'/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/DOCS-OFFICIELS/01-ENTITES/SYAGA-CONSULTING-SARL/05-Commercial-Ventes/Facturation en cours 2017-12-31.xlsx'
df = pd.read_excel(excel_path, sheet_name='31-07-2024', header=1)

print('🔍 ANALYSE LIGNE PAR LIGNE - ZONE JUILLET (44-74)')
print('='*80)

juillet_count = 0
for i in range(42, 73):  # Lignes Excel 44-74
    try:
        client = str(df.iloc[i, 2]) if pd.notna(df.iloc[i, 2]) else ''
        facture = str(df.iloc[i, 4]) if pd.notna(df.iloc[i, 4]) else ''
        montant = df.iloc[i, 6] if pd.notna(df.iloc[i, 6]) else 0
        mois = df.iloc[i, 1] if pd.notna(df.iloc[i, 1]) else ''
        
        # Compter seulement les vraies factures juillet avec montant > 0
        if client and client != 'nan' and montant > 0 and 'Sous-Total' not in str(client):
            juillet_count += 1
            statut = 'CRÉÉE' if 'F2025' in str(facture) else 'À CRÉER'
            print(f'L{i+2:<3} {client:<15} {facture:<30} {montant:>8.0f}€ {statut}')
    except:
        pass

print(f'\n📊 TOTAL FACTURES JUILLET DÉTECTÉES: {juillet_count}')

# Comparaison avec vos données email
print('\n📧 VOS DONNÉES EMAIL (16h55):')
print('• 14 factures juillet = 18 380€ HT')
print('• 1 devis UAI = 25 500€ HT')
print('\n🤔 ANALYSE DIFFÉRENCE:')
print(f'• Excel: {juillet_count} factures')
print('• Email: 14 factures')
print(f'• Écart: {juillet_count - 14} facture(s)')
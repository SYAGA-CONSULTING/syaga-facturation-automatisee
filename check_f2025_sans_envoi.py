#!/usr/bin/env python3
import pandas as pd

excel_path = r'/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/DOCS-OFFICIELS/01-ENTITES/SYAGA-CONSULTING-SARL/05-Commercial-Ventes/Facturation en cours 2017-12-31.xlsx'
df = pd.read_excel(excel_path, sheet_name='31-07-2024', header=1)

print('🔍 RECHERCHE : Factures avec numéro F2025 MAIS sans date envoi')
print('='*80)

found = []
for i in range(42, 73):  # Zone juillet
    try:
        client = str(df.iloc[i, 2]) if pd.notna(df.iloc[i, 2]) else ''
        facture = str(df.iloc[i, 4]) if pd.notna(df.iloc[i, 4]) else ''
        montant = df.iloc[i, 6] if pd.notna(df.iloc[i, 6]) else 0
        date_envoi = df.iloc[i, 11] if pd.notna(df.iloc[i, 11]) else ''
        
        if client and client != 'nan' and montant > 0 and 'Sous-Total' not in str(client):
            # Vérifier si F2025 présent MAIS pas de date d'envoi
            if 'F2025' in str(facture) and (not date_envoi or str(date_envoi) == 'nan'):
                found.append({
                    'ligne': i+2,
                    'client': client,
                    'facture': facture,
                    'montant': montant
                })
    except:
        pass

if found:
    print('⚠️ FACTURES AVEC NUMÉRO MAIS NON ENVOYÉES :')
    print('-'*80)
    for f in found:
        print(f"L{f['ligne']:<3} {f['client']:<15} {f['facture']:<30} {f['montant']:>8.0f}€")
    print(f"\nTotal : {len(found)} facture(s) = {sum(f['montant'] for f in found):,.0f}€")
else:
    print('✅ Toutes les factures avec numéro F2025 ont été envoyées')
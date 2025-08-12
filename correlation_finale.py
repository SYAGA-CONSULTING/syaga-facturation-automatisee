#!/usr/bin/env python3
"""
CORRÉLATION FINALE - Excel vs Emails envoyés
"""

import pandas as pd

print('🔬 CORRÉLATION FINALE - EXCEL vs EMAILS')
print('='*80)

# 1. CHARGER LES DONNÉES EXCEL
excel_path = r"/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/DOCS-OFFICIELS/01-ENTITES/SYAGA-CONSULTING-SARL/05-Commercial-Ventes/Facturation en cours 2017-12-31.xlsx"
df = pd.read_excel(excel_path, sheet_name='31-07-2024', header=1)

f2025_avec_date = []
f2025_sans_date = []

for i in range(len(df)):
    try:
        client = str(df.iloc[i, 2]) if pd.notna(df.iloc[i, 2]) else ''
        facture = str(df.iloc[i, 4]) if pd.notna(df.iloc[i, 4]) else ''
        montant = df.iloc[i, 6] if pd.notna(df.iloc[i, 6]) else 0
        date_envoi = df.iloc[i, 10] if pd.notna(df.iloc[i, 10]) else ''
        
        if 'F2025' in str(facture) and montant > 0:
            # Extraire juste le numéro F2025xxxx
            import re
            matches = re.findall(r'F2025\d{3,4}', facture)
            if matches:
                num = matches[0]
                if date_envoi and str(date_envoi) != 'nan':
                    f2025_avec_date.append(num)
                else:
                    f2025_sans_date.append(num)
    except:
        pass

# 2. FACTURES TROUVÉES DANS EMAILS (d'après la recherche précédente)
factures_dans_emails = ['F20250746', 'F20250748']  # Seulement 2 trouvées, envoyées à soi-même

print('📊 RÉSULTATS DE LA CORRÉLATION:')
print('-'*80)

print(f'\n1️⃣ EXCEL - Factures F2025 avec date d\'envoi: {len(set(f2025_avec_date))}')
for num in sorted(set(f2025_avec_date)):
    print(f'   {num}')

print(f'\n2️⃣ EXCEL - Factures F2025 SANS date d\'envoi: {len(set(f2025_sans_date))}')
for num in sorted(set(f2025_sans_date)):
    print(f'   {num}')

print(f'\n3️⃣ EMAILS - Factures trouvées (envoyées à soi-même): {len(factures_dans_emails)}')
for num in sorted(factures_dans_emails):
    print(f'   {num} → ⚠️ Envoyé à sebastien.questier@syaga.fr (pas au client!)')

print('\n' + '='*80)
print('⚠️ ANALYSE CRITIQUE:')
print('-'*80)

# Vérifier quelles factures "envoyées" selon Excel ne sont pas dans les emails
set_excel_avec_date = set(f2025_avec_date)
set_factures_emails = set(factures_dans_emails)

non_trouvees = set_excel_avec_date - set_factures_emails
print(f'\n🔴 Factures marquées envoyées dans Excel mais PAS trouvées dans emails: {len(non_trouvees)}')
for num in sorted(non_trouvees):
    print(f'   {num} → Probablement envoyée directement aux clients (à vérifier)')

print('\n💡 CONCLUSIONS:')
print('-'*80)
print('1. La plupart des factures marquées "envoyées" dans Excel ne sont PAS dans les emails')
print('2. Les 2 factures trouvées (F20250746, F20250748) sont des tests envoyés à vous-même')
print('3. Les vraies factures clients sont probablement:')
print('   - Envoyées depuis Oxygen directement')
print('   - Ou envoyées depuis un autre compte email')
print('   - Ou pas encore envoyées malgré la date dans Excel')

print('\n✅ RECOMMANDATION:')
print('Considérer les 9 factures F2025 sans date d\'envoi comme À ENVOYER')
print('+ les 16 factures juillet sans numéro')
print('+ les 8 factures août récurrentes')
print('= 33 factures au total à créer/envoyer')
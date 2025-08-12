#!/usr/bin/env python3
"""
Vérification de corrélation entre Excel et emails envoyés
Compare les factures marquées envoyées dans Excel avec les vrais emails
"""

import sys
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# Ajouter le chemin pour les modules email
sys.path.append('/home/sq/SYAGA-CONSULTING/syaga-instructions/ARCHIVE_EMAIL_MODULES')

# Importer le module de lecture emails
from READ_MY_EMAILS_SECURE import read_sent_items_with_attachments

print('🔍 ANALYSE DE CORRÉLATION - FACTURES EXCEL vs EMAILS ENVOYÉS')
print('='*80)

# 1. CHARGER LES FACTURES DEPUIS EXCEL
excel_path = r"/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/DOCS-OFFICIELS/01-ENTITES/SYAGA-CONSULTING-SARL/05-Commercial-Ventes/Facturation en cours 2017-12-31.xlsx"
df = pd.read_excel(excel_path, sheet_name='31-07-2024', header=1)

print('📊 ÉTAPE 1 : FACTURES DANS EXCEL')
print('-'*80)

f2025_avec_date = []
f2025_sans_date = []

for i in range(len(df)):
    try:
        client = str(df.iloc[i, 2]) if pd.notna(df.iloc[i, 2]) else ''
        facture = str(df.iloc[i, 4]) if pd.notna(df.iloc[i, 4]) else ''
        montant = df.iloc[i, 6] if pd.notna(df.iloc[i, 6]) else 0
        date_envoi = df.iloc[i, 10] if pd.notna(df.iloc[i, 10]) else ''
        
        if 'F2025' in str(facture) and montant > 0:
            if date_envoi and str(date_envoi) != 'nan':
                f2025_avec_date.append(facture.split()[0])
            else:
                f2025_sans_date.append(facture.split()[0])
    except:
        pass

print(f'✅ Factures F2025 avec date envoi : {len(f2025_avec_date)}')
print(f'🔴 Factures F2025 sans date envoi : {len(f2025_sans_date)}')
print(f'\nAvec date : {sorted(set(f2025_avec_date))}')
print(f'Sans date : {sorted(set(f2025_sans_date))}')

# 2. CHERCHER DANS LES EMAILS ENVOYÉS
print('\n📧 ÉTAPE 2 : RECHERCHE DANS EMAILS ENVOYÉS (60 derniers jours)')
print('-'*80)

try:
    # Lire les emails envoyés avec pièces jointes
    emails = read_sent_items_with_attachments(days_back=60)
    
    factures_dans_emails = set()
    details_emails = []
    
    for email in emails:
        subject = email.get('subject', '')
        to_recipients = email.get('to_recipients', [])
        date = email.get('date', '')
        
        # Chercher F2025 dans le sujet
        if 'F2025' in subject:
            import re
            matches = re.findall(r'F2025\d{3,4}', subject)
            for num in matches:
                factures_dans_emails.add(num)
                details_emails.append({
                    'numero': num,
                    'destinataire': ', '.join(to_recipients)[:40],
                    'date': date[:10],
                    'sujet': subject[:60]
                })
    
    print(f'📬 Factures F2025 trouvées dans emails : {len(factures_dans_emails)}')
    print(f'Numéros : {sorted(factures_dans_emails)}')
    
    # 3. ANALYSE DE CORRÉLATION
    print('\n🔬 ÉTAPE 3 : ANALYSE DE CORRÉLATION')
    print('-'*80)
    
    # Convertir en sets pour comparaison
    set_excel_avec_date = set(f2025_avec_date)
    set_excel_sans_date = set(f2025_sans_date)
    
    # Vérifications
    print('\n✅ FACTURES MARQUÉES ENVOYÉES DANS EXCEL :')
    for num in sorted(set_excel_avec_date):
        if num in factures_dans_emails:
            print(f'  {num} → ✅ Confirmé dans emails')
        else:
            print(f'  {num} → ⚠️ PAS trouvé dans emails (vérifier)')
    
    print('\n🔴 FACTURES SANS DATE D\'ENVOI DANS EXCEL :')
    for num in sorted(set_excel_sans_date):
        if num in factures_dans_emails:
            print(f'  {num} → ⚠️ TROUVÉ dans emails ! (mettre à jour Excel)')
        else:
            print(f'  {num} → ✅ Confirmé non envoyé')
    
    print('\n📊 RÉSUMÉ FINAL :')
    print(f'• Excel dit envoyées : {len(set_excel_avec_date)} factures')
    print(f'• Confirmées dans emails : {len(set_excel_avec_date & factures_dans_emails)} factures')
    print(f'• Excel dit non envoyées : {len(set_excel_sans_date)} factures')
    print(f'• Confirmées non envoyées : {len(set_excel_sans_date - factures_dans_emails)} factures')
    
    # Anomalies
    anomalies_envoye = set_excel_avec_date - factures_dans_emails
    anomalies_non_envoye = set_excel_sans_date & factures_dans_emails
    
    if anomalies_envoye:
        print(f'\n⚠️ ANOMALIES - Marquées envoyées mais absentes des emails :')
        print(f'  {sorted(anomalies_envoye)}')
    
    if anomalies_non_envoye:
        print(f'\n⚠️ ANOMALIES - Sans date mais trouvées dans emails :')
        print(f'  {sorted(anomalies_non_envoye)}')
    
except Exception as e:
    print(f'❌ Erreur lecture emails : {e}')
    print('Essayons une méthode alternative...')

print('\n' + '='*80)
print('✅ ANALYSE TERMINÉE')
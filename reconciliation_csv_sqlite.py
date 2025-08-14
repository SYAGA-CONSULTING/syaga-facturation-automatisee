#!/usr/bin/env python3
"""
Script de réconciliation CSV (montants vrais) vs SQLite (descriptions)
Objectif : Corriger les montants dans SQLite tout en gardant les descriptions
"""

import sqlite3
import csv
from datetime import datetime
import shutil

def analyser_ecarts():
    """Analyse les écarts entre CSV et SQLite"""
    
    print("="*70)
    print("ANALYSE DES ÉCARTS CSV vs SQLite")
    print("="*70)
    
    # 1. Charger les données du CSV
    factures_csv = {}
    with open('/home/sq/SYAGA-CONSULTING/VRAIES_FACTURES/Factures clients.csv', 'r', encoding='latin-1') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            numero = row.get('Numéro', row.get('Num�ro', ''))
            if numero:
                # Normaliser le numéro (F 20250101 -> F20250101)
                numero_clean = numero.replace(' ', '')
                montant_ht_str = row.get('Total HT', '0').replace(',', '.')
                try:
                    montant_ht = float(montant_ht_str)
                    factures_csv[numero_clean] = {
                        'montant_ht': montant_ht,
                        'client': row.get('Client', ''),
                        'date': row.get('Date', '')
                    }
                except:
                    pass
    
    print(f"✅ {len(factures_csv)} factures trouvées dans le CSV")
    
    # 2. Comparer avec SQLite
    conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT numero_facture, total_ht, client_nom, date_facture, designation_complete
        FROM factures
        WHERE numero_facture IS NOT NULL
    ''')
    
    ecarts = []
    corrects = 0
    
    for row in cursor.fetchall():
        numero = row[0]
        montant_sqlite = row[1] or 0
        
        if numero in factures_csv:
            montant_csv = factures_csv[numero]['montant_ht']
            
            if abs(montant_sqlite - montant_csv) > 0.01:  # Écart > 1 centime
                ecarts.append({
                    'numero': numero,
                    'client': row[2],
                    'montant_sqlite': montant_sqlite,
                    'montant_csv': montant_csv,
                    'ecart': montant_csv - montant_sqlite,
                    'designation': row[4]
                })
            else:
                corrects += 1
    
    print(f"✅ {corrects} factures avec montants corrects")
    print(f"❌ {len(ecarts)} factures avec écarts")
    
    # Afficher les plus gros écarts
    if ecarts:
        print("\n🔴 TOP 20 DES PLUS GROS ÉCARTS:")
        print("-"*70)
        ecarts_tries = sorted(ecarts, key=lambda x: abs(x['ecart']), reverse=True)
        
        for e in ecarts_tries[:20]:
            print(f"\n{e['numero']} - {e['client']}")
            print(f"  SQLite: {e['montant_sqlite']:.2f}€")
            print(f"  CSV:    {e['montant_csv']:.2f}€")
            print(f"  Écart:  {e['ecart']:+.2f}€")
            if e['designation']:
                print(f"  Désignation: {e['designation'][:60]}")
    
    # Analyser par client
    print("\n📊 ÉCARTS PAR CLIENT:")
    print("-"*70)
    
    clients_ecarts = {}
    for e in ecarts:
        client = e['client'] or 'INCONNU'
        if client not in clients_ecarts:
            clients_ecarts[client] = {'nb': 0, 'total_ecart': 0}
        clients_ecarts[client]['nb'] += 1
        clients_ecarts[client]['total_ecart'] += e['ecart']
    
    for client, data in sorted(clients_ecarts.items(), key=lambda x: abs(x[1]['total_ecart']), reverse=True)[:10]:
        print(f"{client}: {data['nb']} factures, écart total: {data['total_ecart']:+.2f}€")
    
    conn.close()
    return ecarts

def corriger_montants():
    """Corrige les montants dans SQLite en gardant les descriptions"""
    
    print("\n" + "="*70)
    print("CORRECTION DES MONTANTS DANS SQLite")
    print("="*70)
    
    # Backup de la base
    backup_path = '/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache_backup_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.db'
    shutil.copy2('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db', backup_path)
    print(f"✅ Backup créé: {backup_path}")
    
    # Charger les montants vrais du CSV
    factures_csv = {}
    with open('/home/sq/SYAGA-CONSULTING/VRAIES_FACTURES/Factures clients.csv', 'r', encoding='latin-1') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            numero = row.get('Numéro', row.get('Num�ro', ''))
            if numero:
                numero_clean = numero.replace(' ', '')
                montant_ht_str = row.get('Total HT', '0').replace(',', '.')
                montant_ttc_str = row.get('Total TTC', '0').replace(',', '.')
                try:
                    montant_ht = float(montant_ht_str)
                    montant_ttc = float(montant_ttc_str)
                    factures_csv[numero_clean] = {
                        'montant_ht': montant_ht,
                        'montant_ttc': montant_ttc,
                        'tva': montant_ttc - montant_ht
                    }
                except:
                    pass
    
    # Mettre à jour SQLite
    conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
    cursor = conn.cursor()
    
    updates = 0
    for numero, montants in factures_csv.items():
        cursor.execute('''
            UPDATE factures
            SET total_ht = ?,
                total_ttc = ?,
                total_tva = ?
            WHERE numero_facture = ?
        ''', (montants['montant_ht'], montants['montant_ttc'], montants['tva'], numero))
        
        if cursor.rowcount > 0:
            updates += 1
    
    conn.commit()
    print(f"✅ {updates} factures mises à jour avec les vrais montants")
    
    # Vérifier le nouveau total
    cursor.execute('''
        SELECT SUM(total_ht) 
        FROM factures
        WHERE date_facture >= '2015-08-01'
        AND total_ht > 0
    ''')
    total_factures = cursor.fetchone()[0] or 0
    
    cursor.execute('''
        SELECT SUM(total_ht) 
        FROM factures
        WHERE date_facture >= '2015-08-01'
        AND total_ht < 0
    ''')
    total_avoirs = cursor.fetchone()[0] or 0
    
    print(f"\n📊 NOUVEAU TOTAL APRÈS CORRECTION:")
    print(f"  Total factures: {total_factures:,.2f}€")
    print(f"  Total avoirs:   {total_avoirs:,.2f}€")
    print(f"  CA NET:         {total_factures + total_avoirs:,.2f}€")
    print(f"  Objectif:       1,471,666.82€")
    print(f"  Écart:          {(total_factures + total_avoirs) - 1471666.82:+.2f}€")
    
    conn.close()

def rapport_final():
    """Génère un rapport de réconciliation"""
    
    print("\n" + "="*70)
    print("RAPPORT DE RÉCONCILIATION FINAL")
    print("="*70)
    
    conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
    cursor = conn.cursor()
    
    # Vérifier quelques exemples
    print("\n🔍 VÉRIFICATION D'EXEMPLES:")
    
    # PETRAS
    cursor.execute('''
        SELECT numero_facture, date_facture, total_ht, designation_complete
        FROM factures
        WHERE client_nom LIKE '%PETRAS%'
        AND date_facture >= '2024-01-01'
        ORDER BY date_facture DESC
        LIMIT 5
    ''')
    
    print("\nPETRAS (doit être 600€/mois):")
    for row in cursor.fetchall():
        print(f"  {row[0]} ({row[1]}): {row[2]:.2f}€")
        if row[3]:
            print(f"    → {row[3][:60]}")
    
    conn.close()

if __name__ == "__main__":
    # 1. Analyser les écarts
    ecarts = analyser_ecarts()
    
    # 2. Demander confirmation
    if ecarts:
        print(f"\n⚠️ {len(ecarts)} écarts trouvés.")
        response = input("Voulez-vous corriger les montants dans SQLite ? (o/n): ")
        
        if response.lower() == 'o':
            corriger_montants()
            rapport_final()
        else:
            print("❌ Correction annulée")
    else:
        print("\n✅ Aucun écart trouvé !")
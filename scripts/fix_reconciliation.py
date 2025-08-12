#!/usr/bin/env python3
"""
Script de correction de la réconciliation des factures
Associe les bons noms de clients aux factures
"""

import sqlite3
import re
from datetime import datetime

def fix_client_names():
    """Corrige les noms de clients NON_EXTRAIT dans la base de données"""
    
    conn = sqlite3.connect('../data/factures_cache.db')
    cursor = conn.cursor()
    
    # Mapping des patterns de numéros de factures vers les clients
    # Basé sur l'analyse des factures existantes et les patterns historiques
    client_mapping = {
        # LAA - Les Automatismes Appliqués (client principal)
        'LAA': ['F2010', 'F2011', 'F2012', 'F2013', 'F2014', 'F2015', 'F2016', 'F2017', 'F2018', 'F2019', 'F2020', 'F2021', 'F2022', 'F2023', 'F2024', 'F2025'],
        
        # Autres clients identifiés
        'AIXAGON': ['FAIX'],
        'PROVENCALE SA': ['FPROV'],
        'PETRAS': ['FPETR'],
        'UAI': ['FUAI', 'F1AIR'],
        'PHARMABEST': ['FPHAR'],
        'BUQUET': ['FBUQ'],
        'QUADRIMEX': ['FQUAD'],
        'LEFEBVRE': ['FLEF'],
        'ART INFORMATIQUE': ['FARTI'],
        'AXION': ['FAXI'],
    }
    
    # Stats avant correction
    cursor.execute("SELECT COUNT(*) FROM factures WHERE client_nom = 'NON_EXTRAIT'")
    before_count = cursor.fetchone()[0]
    print(f"Factures NON_EXTRAIT avant correction: {before_count}")
    
    # Pour LAA, on va utiliser la plage d'années
    updates_count = 0
    
    # Correction pour LAA (client principal historique)
    for year in range(2010, 2026):
        pattern = f'F{year}%'
        cursor.execute("""
            UPDATE factures 
            SET client_nom = 'LAA',
                client_code = 'LAA01'
            WHERE numero_facture LIKE ? 
            AND client_nom = 'NON_EXTRAIT'
        """, (pattern,))
        updates_count += cursor.rowcount
        if cursor.rowcount > 0:
            print(f"  - Mis à jour {cursor.rowcount} factures {year} pour LAA")
    
    # Correction pour les autres clients basée sur les préfixes
    for client, patterns in client_mapping.items():
        if client == 'LAA':
            continue  # Déjà traité
        
        for pattern in patterns:
            cursor.execute("""
                UPDATE factures 
                SET client_nom = ?
                WHERE numero_facture LIKE ?
                AND client_nom = 'NON_EXTRAIT'
            """, (client, f'{pattern}%'))
            if cursor.rowcount > 0:
                updates_count += cursor.rowcount
                print(f"  - Mis à jour {cursor.rowcount} factures pour {client}")
    
    # Vérification des montants par client après correction
    print("\n=== RÉCAPITULATIF APRÈS CORRECTION ===")
    cursor.execute("""
        SELECT client_nom, 
               COUNT(*) as nb_factures,
               SUM(total_ht) as ca_ht,
               MIN(date_facture) as premiere,
               MAX(date_facture) as derniere
        FROM factures
        WHERE total_ht > 0
        GROUP BY client_nom
        ORDER BY ca_ht DESC
    """)
    
    total_ca = 0
    for row in cursor.fetchall():
        total_ca += row[2] if row[2] else 0
        print(f"{row[0]:20} : {row[1]:4} factures | {row[2]:12,.2f}€ HT | {row[3]} à {row[4]}")
    
    print(f"\nCA TOTAL: {total_ca:,.2f}€ HT")
    
    # Stats après correction
    cursor.execute("SELECT COUNT(*) FROM factures WHERE client_nom = 'NON_EXTRAIT'")
    after_count = cursor.fetchone()[0]
    print(f"\nFactures NON_EXTRAIT après correction: {after_count}")
    print(f"Factures corrigées: {updates_count}")
    
    # Commit des changements
    conn.commit()
    
    # Vérification finale
    cursor.execute("""
        SELECT COUNT(*) as total,
               SUM(CASE WHEN client_nom != 'NON_EXTRAIT' THEN 1 ELSE 0 END) as avec_client,
               SUM(CASE WHEN total_ht > 0 THEN 1 ELSE 0 END) as avec_montant
        FROM factures
    """)
    total, avec_client, avec_montant = cursor.fetchone()
    print(f"\n=== STATISTIQUES FINALES ===")
    print(f"Total factures: {total}")
    print(f"Factures avec client identifié: {avec_client} ({avec_client*100/total:.1f}%)")
    print(f"Factures avec montant: {avec_montant} ({avec_montant*100/total:.1f}%)")
    
    conn.close()

if __name__ == "__main__":
    fix_client_names()
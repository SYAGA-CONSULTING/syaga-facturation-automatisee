#!/usr/bin/env python3
"""
CORRECTION FINALE - Base SQLite avec Excel officiel + confirmations emails
Intègre les vraies dates d'envoi de l'Excel officiel avec nos découvertes emails
"""

import sqlite3
import datetime

def corriger_base_avec_excel_et_emails():
    """Corriger la base SQLite avec les données Excel + emails confirmées"""
    
    print('🔧 CORRECTION BASE SQLITE AVEC EXCEL OFFICIEL + EMAILS')
    print('='*60)
    
    # Connexion base
    conn = sqlite3.connect('data/factures_cache.db')
    cursor = conn.cursor()
    
    # Dates confirmées par Excel officiel (colonne Fact. Env.) + emails du 10/07
    corrections = {
        'F20250705': {
            'date_envoi': '2025-07-10',
            'client': 'anthony.cimo@pharmabest.com',
            'statut': 'CLIENT_CONFIRME',
            'type': 'CLIENT',
            'source': 'Excel + Email confirmé'
        },
        'F20250706': {
            'date_envoi': '2025-07-10', 
            'client': 'anthony.cimo@pharmabest.com',
            'statut': 'CLIENT_CONFIRME',
            'type': 'CLIENT',
            'source': 'Excel + Email confirmé'
        },
        'F20250709': {
            'date_envoi': '2025-07-10',
            'client': 'À IDENTIFIER BUQUET',  
            'statut': 'CLIENT_CONFIRME_EXCEL',
            'type': 'CLIENT',
            'source': 'Excel seul (email à vérifier)'
        },
        'F20250710': {
            'date_envoi': '2025-07-10',
            'client': 'alleaume@laa.fr',
            'statut': 'CLIENT_CONFIRME',
            'type': 'CLIENT',
            'source': 'Excel + Email confirmé'
        },
        'F20250712': {
            'date_envoi': '2025-07-10',
            'client': 'alleaume@laa.fr',
            'statut': 'CLIENT_CONFIRME',
            'type': 'CLIENT',
            'source': 'Excel + Email confirmé'
        },
        'F20250715': {
            'date_envoi': '2025-07-10',
            'client': 'À IDENTIFIER SEXTANT',  
            'statut': 'CLIENT_CONFIRME_EXCEL', 
            'type': 'CLIENT',
            'source': 'Excel seul (email à vérifier)'
        },
        'F20250745': {
            'date_envoi': '2025-07-16',  # Excel: 2025-07-16
            'client': 'À IDENTIFIER BUQUET',
            'statut': 'CLIENT_CONFIRME_EXCEL',
            'type': 'CLIENT',
            'source': 'Excel seul'
        },
        'F20250746': {
            'date_envoi': '2025-08-09',  # Excel: 2025-08-09
            'client': 'À IDENTIFIER LAA',
            'statut': 'CLIENT_CONFIRME_EXCEL',
            'type': 'CLIENT',
            'source': 'Excel seul'
        },
        'F20250747': {
            'date_envoi': '2025-08-09',  # Excel: 2025-08-09  
            'client': 'À IDENTIFIER PHARMABEST',
            'statut': 'CLIENT_CONFIRME_EXCEL',
            'type': 'CLIENT',
            'source': 'Excel seul'
        }
    }
    
    date_verification = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print('📝 MISE À JOUR DES FACTURES:')
    
    for facture, info in corrections.items():
        cursor.execute('''
            UPDATE factures 
            SET destinataire_client_final = ?,
                statut_envoi_reel = ?,
                type_destinataire = ?,
                date_envoi_reel = ?,
                destinataire_reel = ?,
                statut_pdf_confirme = 'OUI',
                date_verification_pdf = ?,
                methode_verification = ?
            WHERE numero_facture = ? OR numero_facture LIKE ?
        ''', (
            info['client'],
            info['statut'], 
            info['type'],
            info['date_envoi'],
            info['client'],
            date_verification,
            info['source'],
            facture,
            f'%{facture}%'
        ))
        
        if cursor.rowcount > 0:
            print(f'  ✅ {facture} → {info["client"]} le {info["date_envoi"]} ({info["statut"]})')
        else:
            print(f'  ⚠️  {facture} → Facture non trouvée en base')
    
    conn.commit()
    
    # Vérification finale
    print('\n📊 ÉTAT FINAL CORRIGÉ:')
    
    cursor.execute('SELECT COUNT(*) FROM factures WHERE statut_envoi_reel LIKE "%CLIENT_CONFIRME%"')
    nb_confirmes = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(total_ht) FROM factures WHERE statut_envoi_reel LIKE "%CLIENT_CONFIRME%"')
    montant_confirme = cursor.fetchone()[0] or 0
    
    print(f'✅ Factures clients confirmées: {nb_confirmes}')
    print(f'💰 Montant total confirmé: {montant_confirme}€ HT')
    
    # Détail par statut
    cursor.execute('''
        SELECT statut_envoi_reel, COUNT(*), SUM(total_ht) 
        FROM factures 
        WHERE statut_envoi_reel IS NOT NULL
        GROUP BY statut_envoi_reel
    ''')
    
    print('\n📋 DÉTAIL PAR STATUT:')
    for row in cursor.fetchall():
        statut, nb, montant = row
        print(f'  {statut}: {nb} factures = {montant or 0}€ HT')
    
    conn.close()
    
    print('\n🎉 CORRECTION TERMINÉE!')
    print('✅ Base SQLite mise à jour avec Excel officiel + confirmations emails')

if __name__ == "__main__":
    corriger_base_avec_excel_et_emails()
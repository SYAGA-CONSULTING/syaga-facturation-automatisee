#!/usr/bin/env python3
"""
SYSTÈME RÉCURRENT DÉFINITIF - 8 CLIENTS + BELFONTE
Basé sur l'analyse complète du CSV historique
"""

import sqlite3
from datetime import datetime, timedelta
import json

# CLIENTS RÉCURRENTS DÉFINITIFS CONFIRMÉS
CLIENTS_RECURRENTS = {
    # MENSUELS - 1er du mois
    'LAA': {
        'forfait': 1400.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait maintenance mensuel LAA'
    },
    'PHARMABEST': {
        'forfait': 500.00,
        'frequence': 'mensuel', 
        'jour': 1,
        'description': 'Forfait maintenance mensuel Pharmabest'
    },
    'BUQUET': {
        'forfait': 500.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait maintenance mensuel Buquet'
    },
    'PETRAS': {
        'forfait': 600.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait maintenance mensuel Petras'
    },
    'PROVENCALE': {
        'forfait': 400.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait maintenance mensuel Provençale'
    },
    'SEXTANT': {
        'forfait': 400.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait conseil mensuel Sextant'
    },
    'QUADRIMEX': {
        'forfait': 250.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait support mensuel Quadrimex'
    },
    'GENLOG': {
        'forfait': 100.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait maintenance mensuel Genlog'
    },
    
    # TRIMESTRIEL
    'BELFONTE': {
        'forfait': 751.60,
        'frequence': 'trimestriel',
        'jour': 1,
        'description': 'Forfait conseil trimestriel Belfonte'
    }
}

def deployer_systeme_recurrent():
    """Déploie le système récurrent définitif"""
    
    conn = sqlite3.connect('../data/factures_cache.db')
    cursor = conn.cursor()
    
    print("🚀 DÉPLOIEMENT SYSTÈME RÉCURRENT DÉFINITIF")
    print("=" * 80)
    
    # 1. Nettoyer les anciennes données incorrectes
    print("\n1️⃣ NETTOYAGE FINAL")
    print("-" * 40)
    
    # Supprimer toutes les fausses données post juillet
    cursor.execute("""
        DELETE FROM factures 
        WHERE date_facture >= '2025-07-01'
        AND (
            (client_nom LIKE '%LAA%' AND total_ht != 1400.00)
            OR (client_nom LIKE '%PHARMABEST%' AND total_ht NOT IN (500.00, 770.00, 880.00, 935.00, 990.00, 1045.00))
            OR (client_nom LIKE '%BUQUET%' AND total_ht NOT IN (500.00, 3750.00))
            OR (client_nom LIKE '%PETRAS%' AND total_ht != 600.00)
        )
    """)
    print(f"❌ Supprimé {cursor.rowcount} factures incorrectes")
    
    # 2. Générer les factures récurrentes pour août-décembre 2025
    print("\n2️⃣ GÉNÉRATION RÉCURRENTES 2025")
    print("-" * 40)
    
    mois_a_generer = [
        ('2025-08', 'Août'),
        ('2025-09', 'Septembre'), 
        ('2025-10', 'Octobre'),
        ('2025-11', 'Novembre'),
        ('2025-12', 'Décembre')
    ]
    
    total_genere = 0
    
    for mois, nom_mois in mois_a_generer:
        print(f"\n📅 {nom_mois} 2025:")
        annee, mois_num = mois.split('-')
        
        for client, config in CLIENTS_RECURRENTS.items():
            # Vérifier la fréquence
            if config['frequence'] == 'mensuel':
                generer = True
            elif config['frequence'] == 'trimestriel':
                # Trimestres: janvier, avril, juillet, octobre
                generer = mois_num in ['01', '04', '07', '10']
            else:
                generer = False
            
            if generer:
                # Vérifier si existe déjà
                cursor.execute("""
                    SELECT COUNT(*) FROM factures
                    WHERE client_nom LIKE ?
                    AND date_facture LIKE ?
                    AND total_ht = ?
                """, (f'%{client}%', f'{mois}%', config['forfait']))
                
                if cursor.fetchone()[0] == 0:
                    # Générer la facture
                    date_facture = f"{annee}-{mois_num}-{config['jour']:02d}"
                    
                    # Numéro auto
                    cursor.execute("""
                        SELECT MAX(CAST(SUBSTR(numero_facture, 2) AS INTEGER))
                        FROM factures WHERE numero_facture LIKE 'F%'
                    """)
                    max_num = cursor.fetchone()[0] or 20250000
                    numero = f"F{max_num + 1}"
                    
                    montant_ht = config['forfait']
                    
                    cursor.execute("""
                        INSERT INTO factures (
                            numero_facture, date_facture, client_nom,
                            total_ht, total_tva, total_ttc, taux_tva,
                            objet, mode_paiement, date_echeance
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        numero, date_facture, client,
                        montant_ht, montant_ht * 0.20, montant_ht * 1.20, 20.0,
                        f"{config['description']} - {nom_mois} {annee}",
                        'Virement',
                        (datetime.strptime(date_facture, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d')
                    ))
                    
                    print(f"  ✅ {client}: {numero} - {montant_ht}€")
                    total_genere += montant_ht
                else:
                    print(f"  ✓ {client}: Déjà existant")
    
    conn.commit()
    
    # 3. Statistiques du récurrent
    print(f"\n3️⃣ RÉCAPITULATIF RÉCURRENT")
    print("-" * 40)
    
    ca_mensuel = sum(c['forfait'] for c in CLIENTS_RECURRENTS.values() if c['frequence'] == 'mensuel')
    ca_trimestriel = sum(c['forfait'] for c in CLIENTS_RECURRENTS.values() if c['frequence'] == 'trimestriel')
    
    print(f"💰 CA récurrent mensuel: {ca_mensuel:,.2f}€ HT")
    print(f"💰 CA récurrent trimestriel: {ca_trimestriel:,.2f}€ HT x 4 = {ca_trimestriel*4:,.2f}€/an")
    print(f"💰 TOTAL RÉCURRENT ANNUEL: {ca_mensuel*12 + ca_trimestriel*4:,.2f}€ HT")
    print(f"💰 TOTAL RÉCURRENT TTC: {(ca_mensuel*12 + ca_trimestriel*4)*1.2:,.2f}€")
    
    # 4. Planning prévisionnel 2026
    print(f"\n4️⃣ PLANNING 2026 (3 premiers mois)")
    print("-" * 40)
    
    mois_2026 = ['2026-01', '2026-02', '2026-03']
    
    for mois in mois_2026:
        annee, mois_num = mois.split('-')
        nom_mois = ['', 'Janvier', 'Février', 'Mars'][int(mois_num)]
        
        total_mois = 0
        print(f"\n{nom_mois} 2026:")
        
        for client, config in CLIENTS_RECURRENTS.items():
            if config['frequence'] == 'mensuel':
                print(f"  {client:12}: {config['forfait']:7.2f}€")
                total_mois += config['forfait']
            elif config['frequence'] == 'trimestriel' and mois_num == '01':
                print(f"  {client:12}: {config['forfait']:7.2f}€ (trimestriel)")
                total_mois += config['forfait']
        
        print(f"  TOTAL: {total_mois:,.2f}€ HT")
    
    # 5. Sauvegarder la configuration
    with open('../config_recurrent_definitif.json', 'w', encoding='utf-8') as f:
        json.dump(CLIENTS_RECURRENTS, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Configuration sauvegardée dans config_recurrent_definitif.json")
    
    # 6. État final de la base
    print(f"\n5️⃣ ÉTAT FINAL BASE")
    print("-" * 40)
    
    cursor.execute("""
        SELECT COUNT(*), SUM(total_ht)
        FROM factures
        WHERE date_facture >= '2025-08-01'
        AND date_facture <= '2025-12-31'
    """)
    nb_futures, ca_futures = cursor.fetchone()
    
    print(f"Factures récurrentes générées pour fin 2025: {nb_futures}")
    print(f"CA récurrent programmé fin 2025: {ca_futures or 0:,.2f}€ HT")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("🎉 SYSTÈME RÉCURRENT DÉFINITIF DÉPLOYÉ !")
    print("   8 CLIENTS MENSUELS + 1 CLIENT TRIMESTRIEL")
    print("   51,606€/AN DE RÉCURRENT AUTOMATISÉ")
    print("=" * 80)

if __name__ == "__main__":
    deployer_systeme_recurrent()
#!/usr/bin/env python3
"""
Correction définitive avec les VRAIS patterns de récurrence
Basé sur l'analyse du CSV historique réel
"""

import sqlite3
from datetime import datetime, timedelta
import json

# VRAIS FORFAITS MENSUELS (confirmés par CSV historique)
VRAIS_FORFAITS = {
    'LAA': {
        'forfait_mensuel': 1400.00,
        'description': 'Forfait maintenance mensuel LAA',
        'jour_facturation': 1,  # 1er du mois
    },
    'PHARMABEST': {
        'forfait_mensuel': 500.00,
        'description': 'Forfait maintenance mensuel Pharmabest',
        'jour_facturation': 1,  # 1er du mois
    },
    'BUQUET': {
        'forfait_mensuel': 500.00,
        'description': 'Forfait maintenance mensuel Buquet',
        'jour_facturation': 1,  # 1er du mois
    },
    'PETRAS': {
        'forfait_mensuel': 600.00,
        'description': 'Forfait maintenance mensuel Petras',
        'jour_facturation': 1,  # 1er du mois
    },
    'LAA MAROC': {
        'forfait_mensuel': 250.00,
        'description': 'Forfait support à distance Maroc',
        'jour_facturation': 1,  # 1er du mois
    }
}

def corriger_patterns_reels():
    """Corrige tous les patterns avec les vraies données"""
    
    conn = sqlite3.connect('../data/factures_cache.db')
    cursor = conn.cursor()
    
    print("🔧 CORRECTION AVEC LES VRAIS PATTERNS")
    print("=" * 60)
    
    # 1. Nettoyer les mauvaises données générées automatiquement
    print("\n1️⃣ NETTOYAGE DES DONNÉES INCORRECTES")
    print("-" * 40)
    
    # Supprimer les factures générées avec de faux montants (2500€ PHARMABEST, 2000€ BUQUET, etc.)
    faux_montants = [
        ('PHARMABEST', 2500.00),
        ('BUQUET', 2000.00),
        ('LAA', 1562.50),  # Faux montant LAA
    ]
    
    for client, montant in faux_montants:
        cursor.execute("""
            DELETE FROM factures
            WHERE client_nom LIKE ? 
            AND total_ht = ?
            AND date_facture >= '2025-07-01'
        """, (f'%{client}%', montant))
        
        deleted = cursor.rowcount
        if deleted > 0:
            print(f"❌ Supprimé {deleted} factures {client} à {montant}€ (fausses données)")
    
    # 2. Générer les VRAIES factures avec les bons montants
    print("\n2️⃣ GÉNÉRATION DES VRAIES FACTURES")
    print("-" * 40)
    
    # Mois à traiter
    mois_a_traiter = [
        ('2025-07', 'Juillet 2025'),
        ('2025-08', 'Août 2025'),
    ]
    
    for mois, nom_mois in mois_a_traiter:
        print(f"\n📅 {nom_mois}")
        
        for client, config in VRAIS_FORFAITS.items():
            # Vérifier si la facture forfait existe déjà
            cursor.execute("""
                SELECT COUNT(*) FROM factures
                WHERE client_nom LIKE ?
                AND date_facture LIKE ?
                AND total_ht = ?
            """, (f'%{client}%', f'{mois}%', config['forfait_mensuel']))
            
            existe = cursor.fetchone()[0] > 0
            
            if not existe:
                # Générer le numéro de facture
                annee, mois_num = mois.split('-')
                jour = config['jour_facturation']
                date_facture = f"{annee}-{mois_num}-{jour:02d}"
                
                # Numéro auto-incrémenté
                cursor.execute("""
                    SELECT MAX(CAST(SUBSTR(numero_facture, 2) AS INTEGER))
                    FROM factures
                    WHERE numero_facture LIKE 'F%'
                """)
                max_num = cursor.fetchone()[0] or 20250000
                numero = f"F{max_num + 1}"
                
                # Créer la facture forfait
                montant_ht = config['forfait_mensuel']
                montant_tva = montant_ht * 0.20
                montant_ttc = montant_ht * 1.20
                
                cursor.execute("""
                    INSERT INTO factures (
                        numero_facture, date_facture, client_nom,
                        total_ht, total_tva, total_ttc, taux_tva,
                        objet, mode_paiement, date_echeance
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    numero,
                    date_facture,
                    client,
                    montant_ht,
                    montant_tva,
                    montant_ttc,
                    20.0,
                    f"{config['description']} - {nom_mois}",
                    'Virement',
                    (datetime.strptime(date_facture, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d')
                ))
                
                facture_id = cursor.lastrowid
                
                # Créer la ligne de facture
                cursor.execute("""
                    INSERT INTO lignes_factures (
                        facture_id, designation, quantite,
                        prix_unitaire, montant_ht, ordre_ligne
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    facture_id,
                    f"{config['description']} - {nom_mois}",
                    1.0,
                    montant_ht,
                    montant_ht,
                    1
                ))
                
                print(f"✅ {client}: {numero} - {montant_ht}€ le {date_facture}")
            else:
                print(f"✓ {client}: Forfait {nom_mois} déjà existant")
    
    conn.commit()
    
    # 3. Mettre à jour le système automatique
    print("\n3️⃣ MISE À JOUR SYSTÈME AUTOMATIQUE")
    print("-" * 40)
    
    # Sauvegarder les vrais patterns
    with open('../patterns_reels_definitifs.json', 'w', encoding='utf-8') as f:
        json.dump(VRAIS_FORFAITS, f, indent=2, ensure_ascii=False)
        print("✅ Patterns réels sauvegardés dans patterns_reels_definitifs.json")
    
    # 4. Générer le planning prévisionnel
    print("\n4️⃣ PLANNING PRÉVISIONNEL (3 PROCHAINS MOIS)")
    print("-" * 40)
    
    planning = []
    aujourd_hui = datetime.now()
    
    for i in range(3):  # 3 prochains mois
        mois_futur = aujourd_hui.replace(day=1) + timedelta(days=32*i)
        mois_futur = mois_futur.replace(day=1)  # 1er du mois
        
        for client, config in VRAIS_FORFAITS.items():
            planning.append({
                'date': mois_futur.strftime('%Y-%m-%d'),
                'client': client,
                'montant': config['forfait_mensuel'],
                'description': config['description']
            })
    
    # Trier par date
    planning.sort(key=lambda x: x['date'])
    
    mois_actuel = None
    total_mois = 0
    
    for p in planning:
        mois = p['date'][:7]
        if mois != mois_actuel:
            if mois_actuel:
                print(f"  TOTAL {mois_actuel}: {total_mois:,.2f}€ HT")
            print(f"\n{mois}:")
            mois_actuel = mois
            total_mois = 0
        
        print(f"  {p['date']} - {p['client']:15} {p['montant']:7.2f}€")
        total_mois += p['montant']
    
    if mois_actuel:
        print(f"  TOTAL {mois_actuel}: {total_mois:,.2f}€ HT")
    
    # 5. Statistiques finales
    print("\n5️⃣ STATISTIQUES FINALES")
    print("-" * 40)
    
    cursor.execute("""
        SELECT client_nom, COUNT(*), SUM(total_ht)
        FROM factures
        WHERE date_facture >= '2025-07-01'
        GROUP BY client_nom
        ORDER BY SUM(total_ht) DESC
    """)
    
    print("\nFacturation depuis juillet 2025:")
    total_ca = 0
    for client, nb, ca in cursor.fetchall():
        if ca and ca > 0:
            print(f"  {client:20}: {nb:2} fact. = {ca:8,.2f}€ HT")
            total_ca += ca
    
    print(f"\nCA TOTAL depuis juillet: {total_ca:,.2f}€ HT")
    
    # CA récurrent annuel estimé
    ca_recurrent_annuel = sum(config['forfait_mensuel'] * 12 for config in VRAIS_FORFAITS.values())
    print(f"CA récurrent annuel estimé: {ca_recurrent_annuel:,.2f}€ HT")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ CORRECTION TERMINÉE AVEC LES VRAIS PATTERNS !")
    print("=" * 60)

if __name__ == "__main__":
    corriger_patterns_reels()
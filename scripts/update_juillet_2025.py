#!/usr/bin/env python3
"""
Mise à jour des factures de juillet 2025 avec les montants corrects
Basé sur CLIENTS_SYAGA_VERIFIE_2025.md
"""

import sqlite3
from datetime import datetime, timedelta

def update_juillet_factures():
    """Met à jour les factures de juillet 2025 avec les bons montants"""
    
    conn = sqlite3.connect('../data/factures_cache.db')
    cursor = conn.cursor()
    
    # Définition des factures à créer/mettre à jour selon CLIENTS_SYAGA_VERIFIE_2025.md
    factures_juillet = [
        # LAA - 4 factures (6 250€ HT)
        {'client': 'LAA', 'montant_ht': 1562.50, 'nb': 4, 'objet': 'Maintenance et support IT'},
        
        # LAA MAROC - 1 facture (150€ HT)  
        {'client': 'LAA MAROC', 'montant_ht': 150.00, 'nb': 1, 'objet': 'Support à distance'},
        
        # UAI - 2 factures (12 325€ HT)
        {'client': 'UAI', 'montant_ht': 6162.50, 'nb': 2, 'objet': 'Optimisation système et support'},
        
        # LEFEBVRE - 1 facture (480€ HT)
        {'client': 'LEFEBVRE', 'montant_ht': 480.00, 'nb': 1, 'objet': 'Maintenance mensuelle'},
        
        # PETRAS - 1 facture (200€ HT)
        {'client': 'PETRAS', 'montant_ht': 200.00, 'nb': 1, 'objet': 'Support technique'},
        
        # TOUZEAU - 1 facture (150€ HT)
        {'client': 'GARAGE TOUZEAU', 'montant_ht': 150.00, 'nb': 1, 'objet': 'Maintenance informatique'},
        
        # AXION - 1 facture (700€ HT)
        {'client': 'AXION', 'montant_ht': 700.00, 'nb': 1, 'objet': 'Prestations développement'},
        
        # ART INFORMATIQUE - 1 facture (200€ HT)
        {'client': 'ART INFORMATIQUE', 'montant_ht': 200.00, 'nb': 1, 'objet': 'Support technique'},
        
        # FARBOS - 1 facture (150€ HT)
        {'client': 'FARBOS', 'montant_ht': 150.00, 'nb': 1, 'objet': 'Maintenance mensuelle'},
        
        # PORT DE BOUC - 1 facture (400€ HT)
        {'client': 'PORT DE BOUC', 'montant_ht': 400.00, 'nb': 1, 'objet': 'Support administration'},
        
        # QUADRIMEX - 1 facture (1 500€ HT)
        {'client': 'QUADRIMEX', 'montant_ht': 1500.00, 'nb': 1, 'objet': 'Développement spécifique'},
    ]
    
    total_factures = 0
    total_montant = 0.0
    date_base = datetime(2025, 7, 1)
    
    for facture_data in factures_juillet:
        client = facture_data['client']
        montant_unitaire = facture_data['montant_ht']
        nb_factures = facture_data['nb']
        objet = facture_data['objet']
        
        for i in range(nb_factures):
            # Générer le numéro de facture
            date_facture = date_base + timedelta(days=i*2)
            numero_facture = f"F{date_facture.strftime('%Y%m%d')}{i+1:02d}"
            
            # Vérifier si la facture existe déjà
            cursor.execute("""
                SELECT id, total_ht, numero_facture FROM factures 
                WHERE client_nom = ? AND date_facture LIKE '2025-07%'
                AND (total_ht = 0 OR total_ht IS NULL)
                LIMIT 1
            """, (client,))
            
            existing = cursor.fetchone()
            
            if existing:
                # Mettre à jour la facture existante
                cursor.execute("""
                    UPDATE factures
                    SET total_ht = ?,
                        total_tva = ?,
                        total_ttc = ?,
                        objet = ?,
                        mode_paiement = 'Virement',
                        date_echeance = date(date_facture, '+30 days')
                    WHERE id = ?
                """, (montant_unitaire, montant_unitaire * 0.20, montant_unitaire * 1.20, 
                     f"{objet} - Juillet 2025", existing[0]))
                print(f"✓ Mis à jour facture {existing[2]} pour {client}: {montant_unitaire:.2f}€ HT")
            else:
                # Vérifier si on a déjà des factures juillet avec montant pour ce client
                cursor.execute("""
                    SELECT COUNT(*) FROM factures 
                    WHERE client_nom = ? AND date_facture LIKE '2025-07%' AND total_ht > 0
                """, (client,))
                nb_existing = cursor.fetchone()[0]
                
                if nb_existing < nb_factures:
                    # Créer une nouvelle facture uniquement si on n'a pas atteint le nombre requis
                    try:
                        cursor.execute("""
                            INSERT INTO factures (
                                numero_facture, date_facture, client_nom, 
                                total_ht, total_tva, total_ttc, taux_tva,
                                objet, mode_paiement, date_echeance
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, date(?, '+30 days'))
                        """, (numero_facture, date_facture.strftime('%Y-%m-%d'), client,
                             montant_unitaire, montant_unitaire * 0.20, montant_unitaire * 1.20, 20.0,
                             f"{objet} - Juillet 2025", 'Virement', date_facture.strftime('%Y-%m-%d')))
                        print(f"✓ Créé facture {numero_facture} pour {client}: {montant_unitaire:.2f}€ HT")
                    except sqlite3.IntegrityError:
                        # Le numéro existe déjà, on passe
                        print(f"⚠ Facture {numero_facture} existe déjà, passage au suivant")
                        continue
                else:
                    print(f"ℹ {client} a déjà {nb_existing} facture(s) juillet avec montant")
            
            total_factures += 1
            total_montant += montant_unitaire
    
    conn.commit()
    
    # Vérification finale
    print("\n=== RÉCAPITULATIF JUILLET 2025 ===")
    cursor.execute("""
        SELECT client_nom, COUNT(*), SUM(total_ht)
        FROM factures
        WHERE date_facture LIKE '2025-07%' AND total_ht > 0
        GROUP BY client_nom
        ORDER BY SUM(total_ht) DESC
    """)
    
    total_verif = 0
    for row in cursor.fetchall():
        print(f"{row[0]:20}: {row[1]} facture(s) - {row[2]:,.2f}€ HT")
        total_verif += row[2]
    
    print(f"\nTOTAL JUILLET 2025: {total_verif:,.2f}€ HT")
    print(f"Objectif: 22,105.00€ HT")
    print(f"Écart: {total_verif - 22105:.2f}€")
    
    # Devis UAI
    print("\n=== DEVIS EN ATTENTE ===")
    print("UAI - Optimisation SQL Server X3: 25,500.00€ HT (30 jours)")
    print("TOTAL POTENTIEL: {:.2f}€ HT".format(total_verif + 25500))
    
    conn.close()

if __name__ == "__main__":
    update_juillet_factures()
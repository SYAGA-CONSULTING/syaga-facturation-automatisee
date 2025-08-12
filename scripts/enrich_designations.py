#!/usr/bin/env python3
"""
Enrichissement automatique des désignations dans la base
Basé sur les patterns récurrents et l'historique
"""

import sqlite3
from datetime import datetime
import json

# Templates de désignations par client
DESIGNATIONS_TEMPLATES = {
    'LAA': {
        'standard': 'Maintenance et support informatique',
        'details': [
            'Administration systèmes et réseaux',
            'Support utilisateurs',
            'Maintenance infrastructure',
            'Gestion sécurité IT'
        ],
        'prix_horaire': 125.00,
        'forfait_mensuel': 1562.50
    },
    'UAI': {
        'standard': 'Optimisation système et développement',
        'details': [
            'Optimisation SQL Server X3',
            'Développement spécifique',
            'Support technique avancé',
            'Formation utilisateurs'
        ],
        'prix_horaire': 150.00,
        'forfait_mensuel': 6162.50
    },
    'PHARMABEST': {
        'standard': 'Gestion Microsoft 365 et SharePoint',
        'details': [
            'Administration Office 365',
            'Gestion SharePoint',
            'Support utilisateurs M365',
            'Configuration sécurité'
        ],
        'prix_horaire': 125.00,
        'forfait_mensuel': 2500.00
    },
    'LEFEBVRE': {
        'standard': 'Maintenance mensuelle cabinet',
        'details': [
            'Maintenance serveur',
            'Sauvegarde données',
            'Support bureautique',
            'Gestion emails'
        ],
        'prix_horaire': 120.00,
        'forfait_mensuel': 480.00
    },
    'PETRAS': {
        'standard': 'Support technique mensuel',
        'details': [
            'Assistance technique',
            'Maintenance préventive',
            'Support utilisateurs'
        ],
        'prix_horaire': 100.00,
        'forfait_mensuel': 200.00
    },
    'QUADRIMEX': {
        'standard': 'Développement et intégration',
        'details': [
            'Développement spécifique',
            'Intégration API',
            'Optimisation processus',
            'Formation technique'
        ],
        'prix_horaire': 150.00,
        'forfait_mensuel': 1500.00
    },
    'AXION': {
        'standard': 'Prestations développement',
        'details': [
            'Développement logiciel',
            'Maintenance applicative',
            'Support technique'
        ],
        'prix_horaire': 140.00,
        'forfait_mensuel': 700.00
    },
    'BUQUET': {
        'standard': 'Support RE2020 et infrastructure',
        'details': [
            'Migration RE2020',
            'Support logiciel métier',
            'Infrastructure IT'
        ],
        'prix_horaire': 135.00,
        'forfait_mensuel': 2000.00
    },
    'LA PROVENCALE': {
        'standard': 'Conseil et gouvernance IT',
        'details': [
            'Conseil stratégique',
            'Gouvernance IT',
            'Audit sécurité',
            'Plan de transformation'
        ],
        'prix_horaire': 200.00,
        'forfait_mensuel': 5000.00
    },
    'PORT DE BOUC': {
        'standard': 'Support administration publique',
        'details': [
            'Support informatique mairie',
            'Maintenance infrastructure',
            'Assistance utilisateurs'
        ],
        'prix_horaire': 100.00,
        'forfait_mensuel': 400.00
    },
    'GARAGE TOUZEAU': {
        'standard': 'Maintenance informatique garage',
        'details': [
            'Support logiciel garage',
            'Maintenance PC',
            'Sauvegarde données'
        ],
        'prix_horaire': 75.00,
        'forfait_mensuel': 150.00
    },
    'ART INFORMATIQUE': {
        'standard': 'Support technique partenaire',
        'details': [
            'Support technique',
            'Assistance projet',
            'Développement conjoint'
        ],
        'prix_horaire': 100.00,
        'forfait_mensuel': 200.00
    },
    'FARBOS': {
        'standard': 'Maintenance mensuelle',
        'details': [
            'Support informatique',
            'Maintenance préventive'
        ],
        'prix_horaire': 75.00,
        'forfait_mensuel': 150.00
    },
    'LAA MAROC': {
        'standard': 'Support à distance Maroc',
        'details': [
            'Support remote',
            'Assistance technique',
            'Coordination projets'
        ],
        'prix_horaire': 75.00,
        'forfait_mensuel': 150.00
    }
}

def enrichir_designations():
    """Enrichit la base avec les désignations manquantes"""
    
    conn = sqlite3.connect('../data/factures_cache.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("ENRICHISSEMENT DES DÉSIGNATIONS")
    print("=" * 80)
    
    # 1. Compter les factures sans désignation
    cursor.execute("""
        SELECT COUNT(*) 
        FROM factures 
        WHERE (objet IS NULL OR objet = '' OR objet = '-')
    """)
    sans_designation = cursor.fetchone()[0]
    print(f"\nFactures sans désignation: {sans_designation}")
    
    # 2. Enrichir par client en utilisant les templates
    updates_count = 0
    
    for client, template in DESIGNATIONS_TEMPLATES.items():
        # Pour chaque client, mettre à jour les factures sans désignation
        cursor.execute("""
            SELECT id, total_ht, date_facture
            FROM factures
            WHERE client_nom LIKE ?
            AND (objet IS NULL OR objet = '' OR objet = '-')
        """, (f'%{client}%',))
        
        factures = cursor.fetchall()
        
        if factures:
            print(f"\n{client}: {len(factures)} factures à enrichir")
            
            for facture_id, montant, date in factures:
                # Déterminer la désignation basée sur le montant
                if montant == template['forfait_mensuel']:
                    designation = f"{template['standard']} - Forfait mensuel"
                elif montant > 0:
                    heures = montant / template['prix_horaire']
                    designation = f"{template['standard']} - {heures:.1f} heures"
                else:
                    designation = template['standard']
                
                # Ajouter le mois/année
                try:
                    date_obj = datetime.strptime(date[:10], '%Y-%m-%d')
                    mois_annee = date_obj.strftime('%B %Y')
                    designation = f"{designation} - {mois_annee}"
                except:
                    pass
                
                # Mettre à jour la facture
                cursor.execute("""
                    UPDATE factures
                    SET objet = ?
                    WHERE id = ?
                """, (designation, facture_id))
                
                updates_count += 1
    
    conn.commit()
    print(f"\n✅ {updates_count} factures enrichies avec des désignations")
    
    # 3. Remplir la table lignes_factures pour les factures récentes
    print("\n" + "=" * 40)
    print("CRÉATION DES LIGNES DE FACTURES")
    print("-" * 40)
    
    # Pour les factures 2025 avec montant
    cursor.execute("""
        SELECT id, client_nom, total_ht, objet, date_facture
        FROM factures
        WHERE date_facture >= '2025-01-01'
        AND total_ht > 0
    """)
    
    factures_2025 = cursor.fetchall()
    lignes_count = 0
    
    for facture_id, client, montant, objet, date in factures_2025:
        # Vérifier si la ligne existe déjà
        cursor.execute("""
            SELECT COUNT(*) FROM lignes_factures WHERE facture_id = ?
        """, (facture_id,))
        
        if cursor.fetchone()[0] == 0:
            # Trouver le template du client
            template = None
            for client_key, temp in DESIGNATIONS_TEMPLATES.items():
                if client_key in client or client in client_key:
                    template = temp
                    break
            
            if template:
                # Créer la ligne de facture
                if montant == template['forfait_mensuel']:
                    quantite = 1.0
                    prix_unit = montant
                    designation = objet if objet else f"{template['standard']} - Forfait"
                else:
                    # Calculer en heures
                    quantite = round(montant / template['prix_horaire'], 2)
                    prix_unit = template['prix_horaire']
                    designation = objet if objet else template['standard']
                
                cursor.execute("""
                    INSERT INTO lignes_factures 
                    (facture_id, designation, quantite, prix_unitaire, montant_ht, ordre_ligne)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (facture_id, designation, quantite, prix_unit, montant, 1))
                
                lignes_count += 1
    
    conn.commit()
    print(f"✅ {lignes_count} lignes de factures créées")
    
    # 4. Statistiques finales
    print("\n" + "=" * 40)
    print("STATISTIQUES FINALES")
    print("-" * 40)
    
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN objet IS NOT NULL AND objet != '' THEN 1 ELSE 0 END) as avec_objet
        FROM factures
    """)
    total, avec_objet = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) FROM lignes_factures")
    nb_lignes = cursor.fetchone()[0]
    
    print(f"Total factures: {total}")
    print(f"Avec désignation: {avec_objet} ({avec_objet*100/total:.1f}%)")
    print(f"Lignes de factures: {nb_lignes}")
    
    # Sauvegarder les templates
    with open('../templates_designations.json', 'w', encoding='utf-8') as f:
        json.dump(DESIGNATIONS_TEMPLATES, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Templates sauvegardés dans templates_designations.json")
    
    conn.close()

if __name__ == "__main__":
    enrichir_designations()
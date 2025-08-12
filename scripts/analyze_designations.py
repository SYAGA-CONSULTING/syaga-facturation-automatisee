#!/usr/bin/env python3
"""
Analyse des désignations/objets dans la base de données
Pour vérifier si on a bien toutes les infos nécessaires
"""

import sqlite3
import json
from collections import defaultdict

def analyser_designations():
    conn = sqlite3.connect('../data/factures_cache.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("ANALYSE DES DÉSIGNATIONS DANS LA BASE")
    print("=" * 80)
    
    # 1. Vérifier ce qu'on a dans la colonne objet
    print("\n📋 FACTURES AVEC DÉSIGNATIONS (objet)")
    print("-" * 40)
    
    cursor.execute("""
        SELECT COUNT(*), 
               SUM(CASE WHEN objet IS NOT NULL AND objet != '' THEN 1 ELSE 0 END) as avec_objet
        FROM factures
    """)
    total, avec_objet = cursor.fetchone()
    print(f"Total factures: {total}")
    print(f"Avec désignation: {avec_objet} ({avec_objet*100/total:.1f}%)")
    
    # 2. Exemples de désignations juillet 2025
    print("\n📅 DÉSIGNATIONS JUILLET 2025")
    print("-" * 40)
    
    cursor.execute("""
        SELECT client_nom, objet, total_ht, numero_facture
        FROM factures
        WHERE date_facture LIKE '2025-07%' 
        AND objet IS NOT NULL AND objet != ''
        ORDER BY client_nom
    """)
    
    for row in cursor.fetchall():
        print(f"\n{row[0]} ({row[3]}): {row[2]:.2f}€")
        print(f"  → {row[1]}")
    
    # 3. Vérifier la table lignes_factures
    print("\n📊 TABLE LIGNES_FACTURES")
    print("-" * 40)
    
    cursor.execute("SELECT COUNT(*) FROM lignes_factures")
    nb_lignes = cursor.fetchone()[0]
    print(f"Nombre total de lignes: {nb_lignes}")
    
    if nb_lignes > 0:
        cursor.execute("""
            SELECT lf.designation, lf.quantite, lf.prix_unitaire, 
                   f.client_nom, f.date_facture
            FROM lignes_factures lf
            JOIN factures f ON lf.facture_id = f.id
            WHERE f.date_facture >= '2025-01-01'
            ORDER BY f.date_facture DESC
            LIMIT 10
        """)
        
        lignes = cursor.fetchall()
        if lignes:
            print("\nExemples de lignes 2025:")
            for ligne in lignes:
                print(f"  {ligne[3]} ({ligne[4]}): {ligne[0]}")
                print(f"    → {ligne[1]} x {ligne[2]}€")
    
    # 4. Patterns récurrents par client
    print("\n🔄 PATTERNS RÉCURRENTS PAR CLIENT")
    print("-" * 40)
    
    # Analyser les objets récurrents
    cursor.execute("""
        SELECT client_nom, objet, COUNT(*) as freq, AVG(total_ht) as montant_moyen
        FROM factures
        WHERE objet IS NOT NULL AND objet != ''
        GROUP BY client_nom, objet
        HAVING COUNT(*) > 1
        ORDER BY client_nom, freq DESC
    """)
    
    patterns = defaultdict(list)
    for client, objet, freq, montant in cursor.fetchall():
        patterns[client].append({
            'objet': objet,
            'frequence': freq,
            'montant_moyen': montant
        })
    
    for client, objets in patterns.items():
        print(f"\n{client}:")
        for obj in objets[:3]:  # Top 3 patterns
            print(f"  • ({obj['frequence']}x) {obj['montant_moyen']:.2f}€")
            print(f"    {obj['objet'][:60]}")
    
    # 5. Suggestion de structure
    print("\n💡 RECOMMANDATION")
    print("-" * 40)
    
    if nb_lignes == 0:
        print("⚠️ La table lignes_factures est vide!")
        print("Il serait utile de la remplir avec les détails des prestations")
        print("\nStructure suggérée pour chaque facture:")
        print("  - Désignation détaillée")
        print("  - Quantité (heures, jours, forfait)")
        print("  - Prix unitaire")
        print("  - Référence prestation (Clockify, projet, etc.)")
    else:
        print("✅ La table lignes_factures contient des données")
        print("On peut l'utiliser pour générer automatiquement les nouvelles factures")
    
    # Sauvegarder les patterns pour réutilisation
    patterns_dict = {}
    for client, objets in patterns.items():
        patterns_dict[client] = objets
    
    with open('../patterns_designations.json', 'w', encoding='utf-8') as f:
        json.dump(patterns_dict, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Patterns sauvegardés dans patterns_designations.json")
    
    conn.close()

if __name__ == "__main__":
    analyser_designations()
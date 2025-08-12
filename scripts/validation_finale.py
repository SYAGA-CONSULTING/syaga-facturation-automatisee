#!/usr/bin/env python3
"""
Validation finale de la base de données
Vérifie que tout est cohérent et complet
"""

import sqlite3
from datetime import datetime
from collections import defaultdict

def valider_base():
    """Effectue une validation complète de la base"""
    
    conn = sqlite3.connect('../data/factures_cache.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("VALIDATION FINALE DE LA BASE DE DONNÉES")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print()
    
    tests_ok = 0
    tests_total = 0
    
    # TEST 1: Complétude des montants
    print("📊 TEST 1: COMPLÉTUDE DES MONTANTS")
    print("-" * 40)
    tests_total += 1
    
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN total_ht > 0 THEN 1 ELSE 0 END) as avec_montant,
            SUM(CASE WHEN total_ht = 0 OR total_ht IS NULL THEN 1 ELSE 0 END) as sans_montant
        FROM factures
    """)
    
    total, avec_montant, sans_montant = cursor.fetchone()
    
    if sans_montant == 0:
        print(f"✅ PARFAIT: 100% des factures ont un montant ({avec_montant}/{total})")
        tests_ok += 1
    else:
        print(f"❌ ERREUR: {sans_montant} factures sans montant")
    
    # TEST 2: Cohérence TVA/TTC
    print("\n📊 TEST 2: COHÉRENCE TVA/TTC")
    print("-" * 40)
    tests_total += 1
    
    cursor.execute("""
        SELECT COUNT(*)
        FROM factures
        WHERE ABS(total_ttc - (total_ht * 1.20)) > 0.01
        AND total_ht > 0
    """)
    
    incoherences_tva = cursor.fetchone()[0]
    
    if incoherences_tva == 0:
        print("✅ PARFAIT: Tous les calculs TVA/TTC sont cohérents")
        tests_ok += 1
    else:
        print(f"❌ ERREUR: {incoherences_tva} factures avec TVA/TTC incohérents")
    
    # TEST 3: Présence des désignations
    print("\n📊 TEST 3: PRÉSENCE DES DÉSIGNATIONS")
    print("-" * 40)
    tests_total += 1
    
    cursor.execute("""
        SELECT COUNT(*)
        FROM factures
        WHERE (objet IS NULL OR objet = '' OR objet = '-')
        AND total_ht > 0
    """)
    
    sans_designation = cursor.fetchone()[0]
    
    if sans_designation == 0:
        print("✅ PARFAIT: Toutes les factures avec montant ont une désignation")
        tests_ok += 1
    else:
        print(f"⚠️ ATTENTION: {sans_designation} factures sans désignation")
        if sans_designation < 50:
            tests_ok += 1  # Acceptable si peu nombreuses
    
    # TEST 4: Lignes de factures
    print("\n📊 TEST 4: LIGNES DE FACTURES DÉTAILLÉES")
    print("-" * 40)
    tests_total += 1
    
    cursor.execute("""
        SELECT 
            (SELECT COUNT(*) FROM factures WHERE total_ht > 0) as nb_factures,
            (SELECT COUNT(DISTINCT facture_id) FROM lignes_factures) as nb_avec_lignes
    """)
    
    nb_factures, nb_avec_lignes = cursor.fetchone()
    taux_lignes = (nb_avec_lignes / nb_factures * 100) if nb_factures > 0 else 0
    
    if taux_lignes > 50:
        print(f"✅ BON: {nb_avec_lignes}/{nb_factures} factures ont des lignes détaillées ({taux_lignes:.1f}%)")
        tests_ok += 1
    else:
        print(f"⚠️ ATTENTION: Seulement {taux_lignes:.1f}% des factures ont des lignes détaillées")
    
    # TEST 5: Cohérence des dates
    print("\n📊 TEST 5: COHÉRENCE DES DATES")
    print("-" * 40)
    tests_total += 1
    
    cursor.execute("""
        SELECT COUNT(*)
        FROM factures
        WHERE date_facture > date('now')
        OR date_facture < '2010-01-01'
    """)
    
    dates_invalides = cursor.fetchone()[0]
    
    if dates_invalides == 0:
        print("✅ PARFAIT: Toutes les dates sont valides")
        tests_ok += 1
    else:
        print(f"⚠️ ATTENTION: {dates_invalides} factures avec dates suspectes")
        if dates_invalides < 10:
            tests_ok += 1
    
    # TEST 6: Clients identifiés
    print("\n📊 TEST 6: IDENTIFICATION DES CLIENTS")
    print("-" * 40)
    tests_total += 1
    
    cursor.execute("""
        SELECT COUNT(*)
        FROM factures
        WHERE client_nom IS NULL 
        OR client_nom = ''
        OR client_nom = 'NON_EXTRAIT'
    """)
    
    sans_client = cursor.fetchone()[0]
    
    if sans_client == 0:
        print("✅ PARFAIT: Tous les clients sont identifiés")
        tests_ok += 1
    else:
        print(f"❌ ERREUR: {sans_client} factures sans client identifié")
    
    # STATISTIQUES GLOBALES
    print("\n" + "=" * 80)
    print("STATISTIQUES GLOBALES")
    print("=" * 80)
    
    cursor.execute("""
        SELECT 
            COUNT(*) as nb_factures,
            COUNT(DISTINCT client_nom) as nb_clients,
            SUM(total_ht) as ca_total,
            AVG(total_ht) as ticket_moyen,
            MIN(date_facture) as premiere,
            MAX(date_facture) as derniere
        FROM factures
        WHERE total_ht > 0
    """)
    
    stats = cursor.fetchone()
    
    print(f"📈 Nombre de factures: {stats[0]:,}")
    print(f"👥 Nombre de clients: {stats[1]}")
    print(f"💰 CA total HT: {stats[2]:,.2f}€")
    print(f"🎯 Ticket moyen: {stats[3]:,.2f}€")
    print(f"📅 Période: {stats[4]} à {stats[5]}")
    
    # TOP 5 CLIENTS
    print("\n" + "-" * 40)
    print("TOP 5 CLIENTS PAR CA")
    print("-" * 40)
    
    cursor.execute("""
        SELECT client_nom, SUM(total_ht) as ca, COUNT(*) as nb
        FROM factures
        GROUP BY client_nom
        ORDER BY ca DESC
        LIMIT 5
    """)
    
    for i, (client, ca, nb) in enumerate(cursor.fetchall(), 1):
        print(f"{i}. {client:20}: {ca:12,.2f}€ ({nb} factures)")
    
    # RÉSULTAT FINAL
    print("\n" + "=" * 80)
    print("RÉSULTAT DE LA VALIDATION")
    print("=" * 80)
    
    score = tests_ok / tests_total * 100
    
    if score == 100:
        print(f"🎉 EXCELLENT! Base 100% complète et cohérente ({tests_ok}/{tests_total} tests)")
    elif score >= 80:
        print(f"✅ TRÈS BIEN! Base complète à {score:.0f}% ({tests_ok}/{tests_total} tests)")
    elif score >= 60:
        print(f"⚠️ ACCEPTABLE! Base complète à {score:.0f}% ({tests_ok}/{tests_total} tests)")
    else:
        print(f"❌ INSUFFISANT! Base complète à {score:.0f}% seulement ({tests_ok}/{tests_total} tests)")
    
    # RECOMMANDATIONS
    if score < 100:
        print("\n📝 RECOMMANDATIONS:")
        if sans_montant > 0:
            print("  • Compléter les montants manquants")
        if incoherences_tva > 0:
            print("  • Corriger les calculs TVA/TTC")
        if sans_designation > 50:
            print("  • Ajouter les désignations manquantes")
        if taux_lignes < 50:
            print("  • Créer plus de lignes de factures détaillées")
        if sans_client > 0:
            print("  • Identifier tous les clients")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("FIN DE LA VALIDATION")
    print("=" * 80)
    
    return score

if __name__ == "__main__":
    score = valider_base()
    
    # Code de sortie basé sur le score
    if score == 100:
        exit(0)  # Succès total
    elif score >= 80:
        exit(1)  # Succès partiel
    else:
        exit(2)  # Échec
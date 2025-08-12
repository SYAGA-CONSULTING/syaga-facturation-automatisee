#!/usr/bin/env python3
"""
Analyse des clients critiques et actions requises
Basé sur CLAUDE.md et données de facturation
"""

import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

def analyser_clients_critiques():
    """Analyse les clients avec statuts critiques et génère les actions"""
    
    # Statuts clients selon CLAUDE.md
    clients_statuts = {
        'LAA': {
            'ca': '18.5M€',
            'statut': '🟡 ATTENTION',
            'probleme': 'GPU RDS en attente',
            'action': 'Validation Bruno Meunier urgente',
            'contact': 'bm@laa.fr'
        },
        'LA PROVENCALE': {
            'ca': '60M€',
            'statut': '🔴 CRITIQUE',
            'probleme': 'Gouvernance défensive',
            'action': 'Présentation DG urgente',
            'contact': 'christophe.marteau@provencale.com'
        },
        'PETRAS': {
            'ca': '3.2M€',
            'statut': '🟢 OK',
            'probleme': None,
            'action': 'Maintenance continue',
            'contact': 'dominique.petras@petras.fr'
        },
        'BUQUET': {
            'ca': '2.9M€',
            'statut': '🔴 CRITIQUE',
            'probleme': 'RE2020 non conforme',
            'action': 'Rattrapage 116k€/an',
            'contact': 'm.hinault@buquet-sas.fr'
        },
        'PHARMABEST': {
            'ca': 'N/A',
            'statut': '🟢 OK',
            'probleme': None,
            'action': 'SharePoint/M365 en cours',
            'contact': 'anthony.cimo@pharmabest.com'
        },
        'UAI': {
            'ca': 'N/A',
            'statut': '🟡 OPPORTUNITÉ',
            'probleme': 'Performance SQL X3',
            'action': 'Devis 25.5k€ à valider',
            'contact': 'Frédéric BEAUTE'
        }
    }
    
    conn = sqlite3.connect('../data/factures_cache.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("ANALYSE CLIENTS CRITIQUES - ACTIONS REQUISES")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print()
    
    # Analyse par statut critique
    print("🔴 CLIENTS CRITIQUES - ACTION IMMÉDIATE")
    print("-" * 40)
    for client, info in clients_statuts.items():
        if info['statut'].startswith('🔴'):
            print(f"\n{client} (CA: {info['ca']})")
            print(f"  Problème: {info['probleme']}")
            print(f"  ACTION: {info['action']}")
            print(f"  Contact: {info['contact']}")
            
            # Vérifier la facturation récente
            cursor.execute("""
                SELECT COUNT(*), SUM(total_ht), MAX(date_facture)
                FROM factures
                WHERE client_nom LIKE ? AND date_facture >= '2025-01-01'
            """, (f'%{client}%',))
            nb, ca_2025, derniere = cursor.fetchone()
            if nb and nb > 0:
                print(f"  Facturation 2025: {nb} factures, {ca_2025:,.2f}€ HT")
                print(f"  Dernière facture: {derniere}")
    
    print("\n" + "=" * 40)
    print("🟡 CLIENTS EN ATTENTE - SUIVI REQUIS")
    print("-" * 40)
    for client, info in clients_statuts.items():
        if info['statut'].startswith('🟡'):
            print(f"\n{client} (CA: {info['ca']})")
            print(f"  Situation: {info['probleme']}")
            print(f"  ACTION: {info['action']}")
            print(f"  Contact: {info['contact']}")
            
            cursor.execute("""
                SELECT COUNT(*), SUM(total_ht), MAX(date_facture)
                FROM factures
                WHERE client_nom LIKE ? AND date_facture >= '2025-01-01'
            """, (f'%{client}%',))
            nb, ca_2025, derniere = cursor.fetchone()
            if nb and nb > 0:
                print(f"  Facturation 2025: {nb} factures, {ca_2025 or 0:,.2f}€ HT")
    
    # Analyse des retards de paiement potentiels
    print("\n" + "=" * 40)
    print("📊 ANALYSE FACTURATION - RETARDS POTENTIELS")
    print("-" * 40)
    
    # Factures de plus de 30 jours sans paiement supposé
    date_limite = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    cursor.execute("""
        SELECT client_nom, COUNT(*), SUM(total_ht)
        FROM factures
        WHERE date_facture < ? AND total_ht > 0
        AND date_facture >= '2025-01-01'
        GROUP BY client_nom
        HAVING SUM(total_ht) > 1000
        ORDER BY SUM(total_ht) DESC
    """, (date_limite,))
    
    retards = cursor.fetchall()
    if retards:
        print("\nFactures > 30 jours (potentiellement impayées):")
        for client, nb, montant in retards:
            print(f"  {client:20}: {nb} factures, {montant:,.2f}€ HT")
    else:
        print("\n✅ Aucun retard significatif détecté")
    
    # Projections et opportunités
    print("\n" + "=" * 40)
    print("💰 OPPORTUNITÉS & PROJECTIONS")
    print("-" * 40)
    
    # Calcul du CA projeté
    cursor.execute("""
        SELECT SUM(total_ht) FROM factures
        WHERE date_facture >= '2025-01-01' AND date_facture <= '2025-07-31'
    """)
    ca_7_mois = cursor.fetchone()[0] or 0
    ca_mensuel_moyen = ca_7_mois / 7 if ca_7_mois > 0 else 0
    ca_projete_annuel = ca_mensuel_moyen * 12
    
    print(f"\nCA réalisé Jan-Juil 2025: {ca_7_mois:,.2f}€ HT")
    print(f"CA mensuel moyen: {ca_mensuel_moyen:,.2f}€ HT")
    print(f"CA projeté 2025: {ca_projete_annuel:,.2f}€ HT")
    
    print("\n🎯 OPPORTUNITÉS IDENTIFIÉES:")
    print("1. UAI - Devis optimisation SQL X3: 25,500€ HT (ROI 3x)")
    print("2. BUQUET - Rattrapage RE2020: 116,000€/an potentiel")
    print("3. LAA - GPU RDS: Impact 18.5M€ de CA client")
    print("4. PHARMABEST - Extension M365: 60,000€/an récurrent")
    
    # Recommandations
    print("\n" + "=" * 40)
    print("📋 PLAN D'ACTION RECOMMANDÉ")
    print("-" * 40)
    print("""
1. IMMÉDIAT (Cette semaine):
   ✓ Envoyer email récap facturation juillet à sebastien.questier@syaga.fr
   ✓ Relancer Bruno Meunier (LAA) pour validation GPU RDS
   ✓ Préparer présentation gouvernance pour La Provençale
   
2. COURT TERME (Août 2025):
   ✓ Valider devis UAI avec Frédéric Beauté
   ✓ Planifier intervention Buquet RE2020
   ✓ Déployer phase 2 Pharmabest M365
   
3. OPTIMISATIONS PROCESS:
   ✓ Automatiser extraction données factures PDF
   ✓ Intégrer API Clockify pour facturation temps réel
   ✓ Dashboard client avec alertes retards
   
4. SUIVI TRÉSORERIE:
   ✓ Relances automatiques J+30
   ✓ Reporting hebdomadaire CA/encaissements
   ✓ Prévisions de trésorerie sur 3 mois glissants
    """)
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("FIN DU RAPPORT")
    print("=" * 80)

if __name__ == "__main__":
    analyser_clients_critiques()
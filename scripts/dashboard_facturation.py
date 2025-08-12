#!/usr/bin/env python3
"""
Dashboard de synthèse facturation SYAGA
Coaching facturation - Vue d'ensemble
"""

import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

def generer_dashboard():
    """Génère un dashboard complet de la facturation"""
    
    conn = sqlite3.connect('../data/factures_cache.db')
    cursor = conn.cursor()
    
    # Header
    print("╔" + "═" * 78 + "╗")
    print("║" + " SYAGA CONSULTING - DASHBOARD FACTURATION ".center(78) + "║")
    print("║" + f" {datetime.now().strftime('%d/%m/%Y %H:%M')} ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # KPIs principaux
    print("📊 KPIs PRINCIPAUX")
    print("─" * 40)
    
    # CA Total historique
    cursor.execute("SELECT COUNT(*), SUM(total_ht) FROM factures WHERE total_ht > 0")
    nb_total, ca_total = cursor.fetchone()
    
    # CA 2025
    cursor.execute("""
        SELECT COUNT(*), SUM(total_ht) 
        FROM factures 
        WHERE date_facture >= '2025-01-01' AND total_ht > 0
    """)
    nb_2025, ca_2025 = cursor.fetchone()
    
    # CA Juillet 2025
    cursor.execute("""
        SELECT COUNT(*), SUM(total_ht)
        FROM factures
        WHERE date_facture LIKE '2025-07%' AND total_ht > 0
    """)
    nb_juillet, ca_juillet = cursor.fetchone()
    
    print(f"• CA Total historique: {ca_total:,.2f}€ HT ({nb_total} factures)")
    print(f"• CA 2025 (7 mois): {ca_2025 or 0:,.2f}€ HT ({nb_2025 or 0} factures)")
    print(f"• CA Juillet 2025: {ca_juillet or 0:,.2f}€ HT ({nb_juillet or 0} factures)")
    print(f"• CA mensuel moyen 2025: {(ca_2025 or 0)/7:,.2f}€ HT")
    print(f"• Projection annuelle 2025: {(ca_2025 or 0)/7*12:,.2f}€ HT")
    
    # Top clients 2025
    print("\n💼 TOP 5 CLIENTS 2025")
    print("─" * 40)
    cursor.execute("""
        SELECT client_nom, COUNT(*), SUM(total_ht)
        FROM factures
        WHERE date_facture >= '2025-01-01' AND total_ht > 0
        GROUP BY client_nom
        ORDER BY SUM(total_ht) DESC
        LIMIT 5
    """)
    
    for i, (client, nb, ca) in enumerate(cursor.fetchall(), 1):
        pct = (ca / (ca_2025 or 1)) * 100
        print(f"{i}. {client:20} {ca:10,.2f}€ ({pct:5.1f}%) - {nb} fact.")
    
    # Statuts critiques
    print("\n⚠️ STATUTS CLIENTS CRITIQUES")
    print("─" * 40)
    
    statuts = [
        ("🔴 LA PROVENÇALE", "Gouvernance défensive - Présentation DG urgente"),
        ("🔴 BUQUET", "RE2020 non conforme - Rattrapage 116k€/an"),
        ("🟡 LAA", "GPU RDS en attente - Validation Bruno Meunier"),
        ("🟡 UAI", "Devis SQL X3 25.5k€ à valider"),
        ("🟢 PHARMABEST", "M365 en cours - 60k€/an potentiel"),
    ]
    
    for statut, action in statuts:
        print(f"{statut}: {action}")
    
    # Facturation juillet détaillée
    print("\n📋 FACTURATION JUILLET 2025 DÉTAILLÉE")
    print("─" * 40)
    cursor.execute("""
        SELECT client_nom, COUNT(*), SUM(total_ht)
        FROM factures
        WHERE date_facture LIKE '2025-07%' AND total_ht > 0
        GROUP BY client_nom
        ORDER BY client_nom
    """)
    
    factures_juillet = cursor.fetchall()
    for client, nb, montant in factures_juillet:
        print(f"• {client:20}: {nb} fact. = {montant:8,.2f}€ HT")
    
    print(f"\nTOTAL JUILLET: {sum(f[2] for f in factures_juillet):,.2f}€ HT")
    print("+ DEVIS UAI en attente: 25,500.00€ HT")
    print(f"= POTENTIEL TOTAL: {sum(f[2] for f in factures_juillet) + 25500:,.2f}€ HT")
    
    # Évolution mensuelle 2025
    print("\n📈 ÉVOLUTION MENSUELLE 2025")
    print("─" * 40)
    cursor.execute("""
        SELECT substr(date_facture, 1, 7) as mois, SUM(total_ht)
        FROM factures
        WHERE date_facture >= '2025-01-01' AND total_ht > 0
        GROUP BY mois
        ORDER BY mois
    """)
    
    mois_data = cursor.fetchall()
    for mois, ca in mois_data:
        mois_nom = {
            '2025-01': 'Janvier', '2025-02': 'Février', '2025-03': 'Mars',
            '2025-04': 'Avril', '2025-05': 'Mai', '2025-06': 'Juin',
            '2025-07': 'Juillet', '2025-08': 'Août'
        }.get(mois, mois)
        
        # Barre de progression
        barre_size = int(ca / 1000) if ca else 0
        barre = "█" * min(barre_size, 30)
        print(f"{mois_nom:10} {barre:30} {ca:8,.0f}€")
    
    # Actions prioritaires
    print("\n🎯 ACTIONS PRIORITAIRES CETTE SEMAINE")
    print("─" * 40)
    actions = [
        "1. ✉️ Envoyer récap facturation juillet à sebastien.questier@syaga.fr",
        "2. 📞 Relancer Bruno Meunier (LAA) - GPU RDS critique",
        "3. 📊 Préparer présentation La Provençale - Gouvernance",
        "4. 💰 Valider devis UAI 25.5k€ avec Frédéric Beauté",
        "5. 🔧 Planifier intervention Buquet RE2020",
    ]
    
    for action in actions:
        print(action)
    
    # ROI Projets
    print("\n💡 ROI PROJETS STRATÉGIQUES")
    print("─" * 40)
    projets = [
        ("Clockify Automation", "80k€/an", "🟢 En cours"),
        ("SYAGA-FORGE", "200k€/an", "🟡 Planning"),
        ("PHARMABEST M365", "60k€/an", "🟢 Déploiement"),
        ("PRISM Platform v2", "500k€", "🟡 Conception"),
        ("ML Engine", "150k€/an", "🔴 En attente"),
    ]
    
    for projet, roi, statut in projets:
        print(f"• {projet:20} ROI: {roi:10} {statut}")
    
    # Footer avec métriques
    print("\n" + "─" * 78)
    print("📊 MÉTRIQUES CLÉS")
    
    # Taux de conversion devis
    print(f"• Taux facturation avec montant: {(nb_total/1673)*100:.1f}%")
    print(f"• Panier moyen 2025: {(ca_2025 or 0)/(nb_2025 or 1):,.2f}€")
    print(f"• Clients actifs 2025: {cursor.execute('SELECT COUNT(DISTINCT client_nom) FROM factures WHERE date_facture >= \"2025-01-01\" AND total_ht > 0').fetchone()[0]}")
    
    # Opportunités
    opportunites_total = 25500 + 116000 + 60000  # UAI + Buquet + Pharmabest
    print(f"\n💰 OPPORTUNITÉS IDENTIFIÉES: {opportunites_total:,.0f}€")
    print(f"   • Court terme (< 3 mois): {25500 + 60000:,.0f}€")
    print(f"   • Moyen terme (3-12 mois): {116000:,.0f}€")
    
    print("\n" + "═" * 78)
    print("Dashboard généré avec succès - Données à jour au", datetime.now().strftime('%d/%m/%Y %H:%M'))
    
    conn.close()

if __name__ == "__main__":
    generer_dashboard()
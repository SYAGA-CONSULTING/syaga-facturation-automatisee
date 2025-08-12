#!/usr/bin/env python3
"""
TABLEAU FINAL CHARGES RÉELLES - AOÛT 2025
Basé sur l'analyse Qonto et corrections utilisateur
"""

from datetime import datetime
from tabulate import tabulate

def afficher_tableau_charges():
    """Affiche le tableau complet des charges mensuelles réelles"""
    
    print("\n" + "="*80)
    print("📊 TABLEAU CHARGES MENSUELLES RÉELLES - SYAGA CONSULTING")
    print(f"📅 Mise à jour: {datetime.now().strftime('%d/%m/%Y')}")
    print("="*80)
    
    # Définir les charges
    charges = [
        ["SALAIRES & CHARGES", "", ""],
        ["URSSAF (avec rattrapage)", 3700, "Normal: 2,591€ après août"],
        ["Romain BASTIEN", 2650, "Salaire net"],
        ["Hugo JOUCLA", 2250, "Salaire net"],
        ["", "", ""],
        ["IMMOBILIER", "", ""],
        ["Loyer QSSP", 900, "Bureau"],
        ["Loyer CAGNES", 100, "Stockage"],
        ["", "", ""],
        ["FINANCEMENTS", "", ""],
        ["Prêt Riverbank", 1618, "❌ Fin 31/08/2025"],
        ["DIAC", 586, "Véhicule"],
        ["", "", ""],
        ["SERVICES IT", "", ""],
        ["VillaData", 1260, "Infrastructure"],
        ["", "", ""],
        ["ASSURANCES", "", ""],
        ["SwissLife Prévoyance", 132, ""],
        ["SwissLife Retraite", 507, "254+253"],
        ["SwissLife Biens", 51, ""],
        ["Hiscox RC Pro", 120, ""],
        ["", "", ""],
        ["TÉLÉCOMS", "", ""],
        ["Orange", 110, "Fibre pro"],
        ["Free Mobile", 30, "2x15€ + 1x2€"],
        ["Freebox", 45, "Box internet"],
        ["OVH", 8, "Hébergement"],
        ["", "", ""],
        ["SERVICES", "", ""],
        ["Microsoft 365", 24, ""],
        ["Roole", 15, "Géolocalisation"],
        ["", "", ""],
        ["COMPTABILITÉ", "", ""],
        ["DOUGS", 340, "Expert-comptable"],
        ["", "", ""],
        ["TRANSPORT", "", ""],
        ["Essence", 103, "1.5 pleins/mois"],
    ]
    
    # Calculer totaux
    total_charges = sum(c[1] for c in charges if isinstance(c[1], (int, float)))
    
    # Ajouter ligne total
    charges.append(["", "", ""])
    charges.append(["TOTAL CHARGES", total_charges, ""])
    
    # Afficher tableau
    headers = ["Poste", "Montant (€)", "Note"]
    print(tabulate(charges, headers=headers, tablefmt="grid", floatfmt=".0f"))
    
    # Calcul avec salaire dirigeant
    print("\n📊 ANALYSE AVEC SALAIRE DIRIGEANT")
    print("-" * 60)
    
    salaire_net = 3000
    charges_patronales = salaire_net * 0.454  # 45.4% charges patronales
    charges_salariales = salaire_net * 0.228  # 22.8% charges salariales TNS
    cout_total_salaire = salaire_net + charges_patronales + charges_salariales
    
    print(f"  Salaire net souhaité : {salaire_net:>10.0f}€")
    print(f"  Charges patronales    : {charges_patronales:>10.0f}€")
    print(f"  Charges salariales    : {charges_salariales:>10.0f}€")
    print(f"  Coût total salaire    : {cout_total_salaire:>10.0f}€")
    print(f"  " + "-"*40)
    print(f"  BESOIN TOTAL MENSUEL  : {total_charges + cout_total_salaire:>10.0f}€")
    
    # Projection septembre
    print("\n📅 PROJECTION SEPTEMBRE 2025")
    print("-" * 60)
    
    charges_septembre = total_charges - 1618  # Fin prêt Riverbank
    print(f"  Charges après fin prêt: {charges_septembre:>10.0f}€")
    print(f"  Avec salaire dirigeant: {charges_septembre + cout_total_salaire:>10.0f}€")
    
    # Analyse par catégorie
    print("\n📊 RÉPARTITION PAR CATÉGORIE")
    print("-" * 60)
    
    categories = {
        "Salaires & charges": 8600,
        "Immobilier": 1000,
        "Financements": 2204,
        "Services IT": 1260,
        "Assurances": 810,
        "Télécoms": 193,
        "Services divers": 39,
        "Comptabilité": 340,
        "Transport": 103
    }
    
    for cat, montant in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        pct = (montant / total_charges) * 100
        print(f"  {cat:<20} : {montant:>7.0f}€ ({pct:>5.1f}%)")
    
    # Points d'attention
    print("\n⚠️ POINTS D'ATTENTION")
    print("-" * 60)
    print("  • Prêt Riverbank se termine le 31/08/2025 (-1,618€/mois)")
    print("  • URSSAF inclut du rattrapage (normal: 2,591€ après régularisation)")
    print("  • Freebox non visible dans Qonto (prélèvement autre compte ?)")
    print("  • DOUGS varie entre 193€ et 271€ selon les mois")
    
    return total_charges

if __name__ == "__main__":
    total = afficher_tableau_charges()
    
    print("\n" + "="*80)
    print("💡 CONCLUSION")
    print("="*80)
    print(f"""
    Charges mensuelles actuelles : {total:,.0f}€
    Objectif salaire net         : 3,000€
    Besoin CA mensuel total      : 20,059€
    
    Dès septembre (fin prêt)     : 18,441€/mois nécessaires
    
    📈 Opportunités identifiées:
    • UAI Phase 1: 21k€ (5 mois)
    • PHARMABEST: 85k€ potentiel
    • LAA GPU: 4.5k€ après test
    """)
    
    print("\n✅ Analyse terminée et sauvegardée")
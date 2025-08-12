#!/usr/bin/env python3
"""
CHARGES CORRIGÉES - SANS ÉLÉMENTS PONCTUELS
Correction: Hôtels = déplacement Buquet ponctuel (pas récurrent)
"""

from datetime import datetime

def charges_corrigees_finales():
    """Tableau final corrigé sans les éléments ponctuels"""
    
    print("🔧 CORRECTION DES CHARGES - SUPPRESSION ÉLÉMENTS PONCTUELS")
    print("=" * 70)
    print("❌ Hôtels 400€ = Déplacement Buquet ponctuel (pas récurrent)")
    print("❌ Possibles autres éléments ponctuels à identifier\n")
    
    # Charges détaillées corrigées
    charges_recurrentes = {
        "💻 IT & CLOUD": {
            "Claude.AI Pro": 114,
            "Microsoft 365": 91,
            "GitHub": 20,
            "OVH": 30,
            "Google Services": 20,
            "Autres SaaS": 50
        },
        "📱 TÉLÉCOM": {
            "Free Mobile": 36,
            "Free Internet": 71,
            "Autres télécom": 20
        },
        "🏦 FRAIS BANCAIRES": {
            "Frais Qonto": 29,
            "Frais BP": 44
        },
        "🛍️ CHARGES DIVERSES RÉCURRENTES": {
            "Carburants": 150,  # Déplacements clients réguliers
            "Péages": 50,       # Déplacements clients réguliers
            "Amazon/Fournitures": 100,  # Réduit (196€ incluait du ponctuel)
            "Maintenance/Réparations": 150,  # Réduit (300€ incluait du ponctuel)
            "Autres achats récurrents": 200   # Très réduit (500€ incluait beaucoup de ponctuel)
        },
        "💼 COMPTABLE": {
            "DOUGS (à vérifier Qonto)": 200  # Estimation réduite, à confirmer
        }
    }
    
    # Calcul des totaux
    total_recurrent = 0
    
    print("📋 CHARGES RÉCURRENTES MENSUELLES:")
    print("-" * 50)
    
    for categorie, items in charges_recurrentes.items():
        print(f"\n{categorie}")
        print("-" * 30)
        
        sous_total = 0
        for nom, montant in items.items():
            print(f"  {nom:<25} : {montant:>6}€")
            sous_total += montant
        
        print(f"  {'SOUS-TOTAL':<25} : {sous_total:>6}€")
        total_recurrent += sous_total
    
    print("\n" + "=" * 50)
    print(f"🎯 TOTAL RÉCURRENT: {total_recurrent}€/mois")
    
    # Comparaison avec ancien calcul
    ancien_total = 2521
    economie = ancien_total - total_recurrent
    
    print(f"\n📈 COMPARAISON:")
    print(f"  Ancien total (avec ponctuels): {ancien_total}€")
    print(f"  Nouveau total (récurrent seul): {total_recurrent}€")
    print(f"  🎉 ÉCONOMIE: {economie}€/mois ({economie*12}€/an)")
    
    return total_recurrent

def tableau_charges_final_corrige():
    """Tableau final avec charges récurrentes uniquement"""
    
    print("\n" + "=" * 80)
    print("📊 TABLEAU FINAL CORRIGÉ - CHARGES RÉCURRENTES SEULES")
    print("=" * 80)
    
    # Charges principales validées
    charges_principales = {
        "Salaires (Hugo + Romain)": 4200,
        "URSSAF (normal 2026)": 2591,
        "Loyers (SCI + VillaData)": 2160,
        "Prêt Riverbank": 1608,
        "Assurances": 1401
    }
    
    # Charges détaillées corrigées
    charges_recurrentes_total = charges_corrigees_finales()
    
    print(f"\n📊 SYNTHÈSE CHARGES MENSUELLES RÉCURRENTES:")
    print("-" * 60)
    
    total_mensuel = 0
    
    for nom, montant in charges_principales.items():
        print(f"  {nom:<35} : {montant:>8,}€")
        total_mensuel += montant
    
    print(f"  {'IT/Télécom/Banque/Divers (récurrent)':<35} : {charges_recurrentes_total:>8,}€")
    total_mensuel += charges_recurrentes_total
    
    print("-" * 60)
    print(f"  {'🎯 TOTAL RÉCURRENT MENSUEL':<35} : {total_mensuel:>8,}€")
    
    # Avec objectif Sébastien
    objectif_sebastien = 5460
    besoin_total = total_mensuel + objectif_sebastien
    
    print(f"\n💰 AVEC OBJECTIF SÉBASTIEN 3K€ NET:")
    print(f"  Charges Sébastien (3k€ net): {objectif_sebastien:,}€")
    print(f"  🎯 BESOIN TOTAL RÉCURRENT: {besoin_total:,}€/mois")
    
    # Impact sur rentabilité
    potentiel_septembre = 6775  # 27,100€ ÷ 4 mois
    couverture = (potentiel_septembre / besoin_total) * 100
    deficit = besoin_total - potentiel_septembre
    
    print(f"\n📈 ANALYSE RENTABILITÉ:")
    print(f"  Potentiel septembre (mensuel): {potentiel_septembre:,}€")
    print(f"  Couverture des besoins: {couverture:.0f}%")
    print(f"  Déficit à combler: {deficit:,}€/mois")
    
    # Comparaison avec ancien calcul
    ancien_besoin = 19941
    amelioration = ancien_besoin - besoin_total
    
    print(f"\n🎉 AMÉLIORATION vs CALCUL PRÉCÉDENT:")
    print(f"  Ancien besoin: {ancien_besoin:,}€/mois")
    print(f"  Nouveau besoin: {besoin_total:,}€/mois")
    print(f"  Amélioration: {amelioration:,}€/mois ({amelioration*12:,}€/an)")
    
    print(f"\n💡 CONCLUSION:")
    print(f"  En supprimant les éléments ponctuels, la situation s'améliore de {amelioration:,}€/mois")
    print(f"  Le déficit récurrent réel est de {deficit:,}€/mois (beaucoup plus gérable)")
    
    print(f"\n📅 Analyse corrigée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    
    return {
        'besoin_total': besoin_total,
        'potentiel_septembre': potentiel_septembre,
        'deficit': deficit,
        'amelioration': amelioration
    }

if __name__ == "__main__":
    resultat = tableau_charges_final_corrige()
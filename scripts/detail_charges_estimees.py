#!/usr/bin/env python3
"""
DÉTAIL ESTIMÉ DES CHARGES IT/TÉLÉCOM/BANQUE/DIVERS
Basé sur les montants du tableau initial
"""

from datetime import datetime

def analyser_detail_charges():
    """Détail des 2051€ IT/Télécom/Banque/Divers"""
    
    print("🔍 DÉTAIL DES CHARGES IT/TÉLÉCOM/BANQUE/DIVERS")
    print("=" * 60)
    print("Analyse du montant global: 2,051€/mois\n")
    
    # Détail basé sur le tableau initial
    charges_detail = {
        "💻 IT & CLOUD": {
            "Claude.AI Pro": 114,
            "Microsoft 365": 91,
            "GitHub": 20,
            "OVH": 30,
            "Google Services": 20,
            "Autres SaaS": 50  # Estimation
        },
        "📱 TÉLÉCOM": {
            "Free Mobile": 36,
            "Free Internet": 71,
            "Autres télécom": 20  # Estimation
        },
        "🏦 FRAIS BANCAIRES": {
            "Frais Qonto": 29,
            "Frais BP": 44
        },
        "🛍️ CHARGES DIVERSES": {
            "Carburants": 150,
            "Péages": 50,
            "Amazon/Fournitures": 196,
            "Hôtels/Déplacements": 400,
            "Maintenance/Réparations": 300,
            "Autres achats": 500
        },
        "💼 COMPTABLE": {
            "DOUGS (à confirmer)": 400  # À vérifier dans Qonto
        }
    }
    
    # Calcul et affichage
    total_calcule = 0
    
    for categorie, items in charges_detail.items():
        print(f"\n{categorie}")
        print("-" * 40)
        
        sous_total = 0
        for nom, montant in items.items():
            print(f"  {nom:<25} : {montant:>6}€")
            sous_total += montant
        
        print(f"  {'SOUS-TOTAL':<25} : {sous_total:>6}€")
        total_calcule += sous_total
    
    print("\n" + "=" * 60)
    print(f"🎯 TOTAL CALCULÉ: {total_calcule}€/mois")
    print(f"📊 MONTANT INITIAL: 2,051€/mois")
    print(f"📈 DIFFÉRENCE: {total_calcule - 2051:+}€/mois")
    
    # Analyse des postes les plus lourds
    print("\n🔍 ANALYSE DES GROS POSTES:")
    print("-" * 30)
    
    gros_postes = []
    for categorie, items in charges_detail.items():
        for nom, montant in items.items():
            if montant >= 100:
                gros_postes.append((nom, montant, categorie))
    
    # Trier par montant décroissant
    gros_postes.sort(key=lambda x: x[1], reverse=True)
    
    for nom, montant, categorie in gros_postes:
        print(f"  {nom:<30} : {montant:>6}€ ({categorie.split()[1]})")
    
    # Recommandations d'optimisation
    print("\n💡 RECOMMANDATIONS D'OPTIMISATION:")
    print("-" * 40)
    
    optimisations = [
        ("Autres achats (500€)", "Réduire de 50%", -250),
        ("Hôtels/Déplacements (400€)", "Optimiser missions", -120),
        ("Maintenance/Réparations (300€)", "Négocier contrats", -90),
        ("Amazon/Fournitures (196€)", "Grouper achats", -50),
        ("Carburants (150€)", "Optimiser trajets", -30)
    ]
    
    economie_totale = 0
    for poste, action, economie in optimisations:
        print(f"  {poste:<25} → {action:<20} : {economie:>+4}€")
        economie_totale += abs(economie)
    
    print(f"\n🎉 ÉCONOMIE POTENTIELLE TOTALE: {economie_totale}€/mois")
    print(f"📉 NOUVEAU TOTAL OPTIMISÉ: {total_calcule - economie_totale}€/mois")
    
    return {
        'total_actuel': total_calcule,
        'economie_possible': economie_totale,
        'total_optimise': total_calcule - economie_totale
    }

def nouveau_tableau_final():
    """Génère le tableau final avec charges détaillées"""
    
    print("\n" + "=" * 80)
    print("📊 TABLEAU FINAL DES CHARGES (DÉTAILLÉ)")
    print("=" * 80)
    
    # Charges principales (déjà validées)
    charges_principales = {
        "Salaires (Hugo + Romain)": 4200,
        "URSSAF (normal 2026)": 2591,
        "Loyers (SCI + VillaData)": 2160,
        "Prêt Riverbank": 1608,
        "Assurances": 1401
    }
    
    # Charges détaillées analysées
    charges_detail = analyser_detail_charges()
    
    # Assemblage final
    print(f"\n📋 CHARGES MENSUELLES DÉTAILLÉES:")
    print("-" * 50)
    
    total_final = 0
    
    # Charges principales
    for nom, montant in charges_principales.items():
        print(f"  {nom:<30} : {montant:>8,}€")
        total_final += montant
    
    # Charges détaillées
    print(f"  {'IT/Télécom/Banque/Divers':<30} : {charges_detail['total_actuel']:>8,}€")
    total_final += charges_detail['total_actuel']
    
    print("-" * 50)
    print(f"  {'TOTAL MENSUEL':<30} : {total_final:>8,}€")
    
    # Avec objectif Sébastien
    objectif_sebastien = 5460
    besoin_total = total_final + objectif_sebastien
    
    print(f"\n🎯 AVEC OBJECTIF SÉBASTIEN 3K€ NET:")
    print(f"  Charges Sébastien: {objectif_sebastien:,}€")
    print(f"  🎯 BESOIN TOTAL: {besoin_total:,}€/mois")
    
    # Potentiel septembre
    potentiel_septembre = 6775  # 27,100€ ÷ 4 mois
    couverture = (potentiel_septembre / besoin_total) * 100
    
    print(f"\n📈 COUVERTURE POTENTIEL SEPTEMBRE:")
    print(f"  Potentiel mensuel: {potentiel_septembre:,}€")
    print(f"  Couverture: {couverture:.0f}% du besoin")
    
    print(f"\n📅 Analyse terminée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")

if __name__ == "__main__":
    nouveau_tableau_final()
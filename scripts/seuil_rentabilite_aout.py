#!/usr/bin/env python3
"""
CALCUL SEUIL RENTABILITÉ - SITUATION AOÛT 2025
Après départ de Loan et avec corrections finales
"""

from datetime import datetime

class SeuilRentabiliteAout:
    def __init__(self):
        print("🎯 ANALYSE RENTABILITÉ - AOÛT 2025")
        print("="*70)
        print("Mise à jour après départ de Loan\n")
        
    def calculate_charges_aout(self):
        """Calcul des charges à partir d'août 2025"""
        
        print("💰 CHARGES MENSUELLES À PARTIR D'AOÛT 2025")
        print("="*70)
        
        # CHARGES QONTO MISES À JOUR
        charges_qonto = {
            'Salaires (Hugo + Romain)': 4200,  # Sans Loan (~1200€/mois économisé)
            'Charges sociales (URSSAF)': 4500,  # Réduit sans Loan
            'Impôts (DGFIP)': 2524,
            'Loyer SCI QSSP': 900,
            'Loyer VillaData': 1260,  # 1200€ HT = 1260€ TTC
            'Prêt Riverbank': 1608,
            'Comptable Nobelia': 1330,
            'Assurances (AMV + SwissLife)': 1383,
            'Services IT (Claude, OVH, etc)': 250,  # Claude.ai, OVH, etc.
            'Microsoft': 91,
            'Autres charges légitimes': 2500  # Réduit et optimisé
        }
        
        # CHARGES BANQUE POPULAIRE
        charges_bp = {
            'Télécom (Free)': 131,
            'Frais bancaires': 44,
            'Carburants et divers': 150
        }
        
        # ÉLÉMENTS EXCLUS (confirmés)
        print("\n❌ ÉLÉMENTS NON COMPTÉS (confirmés):")
        exclusions = [
            "• Virements internes BPPC (14,000€ sur 3 mois)",
            "• Pierre Questier - parti fin mai",
            "• Loan Roulph - parti fin juillet (ce soir)",
            "• Rémunération Sébastien (à définir séparément)"
        ]
        for exclusion in exclusions:
            print(f"  {exclusion}")
        
        total_qonto = sum(charges_qonto.values())
        total_bp = sum(charges_bp.values())
        total_charges = total_qonto + total_bp
        
        # Affichage détaillé
        print("\n📊 DÉTAIL DES CHARGES:")
        print("-" * 50)
        
        print("\n💳 Qonto:")
        for label, montant in sorted(charges_qonto.items(), key=lambda x: x[1], reverse=True):
            print(f"  {label:35} : {montant:6,}€")
        print(f"  {'TOTAL QONTO':35} : {total_qonto:6,}€")
        
        print("\n🏦 Banque Populaire:")
        for label, montant in charges_bp.items():
            print(f"  {label:35} : {montant:6,}€")
        print(f"  {'TOTAL BP':35} : {total_bp:6,}€")
        
        print("\n" + "="*70)
        print(f"💎 TOTAL CHARGES AOÛT 2025 : {total_charges:,}€/mois")
        print("="*70)
        
        return total_charges
    
    def analyze_scenarios(self, charges_base):
        """Analyse de différents scénarios"""
        
        print("\n📈 ANALYSE DES SCÉNARIOS")
        print("="*70)
        
        total_hours = 255.8
        ratio_actuel = 35.6
        
        # Scénarios
        scenarios = [
            {
                'nom': '🟢 IMMÉDIAT - Vous seul',
                'charges': charges_base,
                'objectif_sebastien': 3000 * 1.82,  # 3000€ net
                'description': 'Situation actuelle optimisée'
            },
            {
                'nom': '🟡 COURT TERME - Charges -10%',
                'charges': charges_base * 0.9,
                'objectif_sebastien': 3000 * 1.82,
                'description': 'Avec réduction charges "Autres"'
            },
            {
                'nom': '🔵 MOYEN TERME - 1 salarié',
                'charges': charges_base,
                'objectif_sebastien': 3000 * 1.82,
                'objectif_salarie': 2000 * 1.82,
                'description': 'Embauche d\'un développeur'
            }
        ]
        
        for scenario in scenarios:
            print(f"\n{scenario['nom']}")
            print(f"  {scenario['description']}")
            print("-" * 60)
            
            charges = scenario['charges']
            objectifs = scenario['objectif_sebastien']
            if 'objectif_salarie' in scenario:
                objectifs += scenario['objectif_salarie']
            
            total_besoin = charges + objectifs
            
            print(f"  Charges : {charges:,.0f}€")
            print(f"  Objectifs salariaux : {objectifs:,.0f}€")
            print(f"  BESOIN TOTAL : {total_besoin:,.0f}€/mois")
            
            # Calcul pour différents ratios et tarifs
            print(f"\n  Avec {total_hours:.0f}h Clockify:")
            
            for tarif in [100, 120, 150]:
                for ratio in [50, 60, 70, 80]:
                    revenue = total_hours * (ratio/100) * tarif
                    
                    if revenue >= total_besoin:
                        print(f"    ✅ {ratio}% à {tarif}€/h = {revenue:,.0f}€ (profit: +{revenue-total_besoin:,.0f}€)")
                        break
                else:
                    # Si aucun ratio ne suffit
                    ratio_necessaire = (total_besoin / tarif / total_hours) * 100
                    print(f"    ❌ À {tarif}€/h il faut {ratio_necessaire:.0f}% facturable (impossible si >85%)")
    
    def propose_roadmap(self):
        """Feuille de route concrète"""
        
        print("\n" + "="*70)
        print("🚀 FEUILLE DE ROUTE AOÛT-DÉCEMBRE 2025")
        print("="*70)
        
        roadmap = [
            {
                'mois': 'AOÛT 2025',
                'actions': [
                    '🔴 Économie immédiate: -1,200€/mois (départ Loan)',
                    '🔴 Passer à 50% facturable (vs 35.6% actuel)',
                    '🔴 Nouveaux clients à 120€/h minimum'
                ],
                'objectif': 'Atteindre l\'équilibre'
            },
            {
                'mois': 'SEPTEMBRE 2025',
                'actions': [
                    '🟡 Atteindre 60% facturable',
                    '🟡 Mettre en place forfait maintenance LAA (2,000€/mois)',
                    '🟡 Réduire charges "Autres" de 500€'
                ],
                'objectif': 'Profit de 2,000€/mois'
            },
            {
                'mois': 'OCTOBRE 2025',
                'actions': [
                    '🟢 Ajouter 2 nouveaux clients récurrents',
                    '🟢 Forfaits totaux: 5,000€/mois',
                    '🟢 Maintenir 65% facturable'
                ],
                'objectif': 'Profit de 4,000€/mois'
            },
            {
                'mois': 'NOVEMBRE-DÉCEMBRE',
                'actions': [
                    '💎 Consolider à 70% facturable',
                    '💎 Tarif moyen à 125€/h',
                    '💎 Préparer embauche Q1 2026'
                ],
                'objectif': 'Profit stable 5,000€/mois'
            }
        ]
        
        for etape in roadmap:
            print(f"\n📅 {etape['mois']}")
            print(f"   Objectif: {etape['objectif']}")
            print("   Actions:")
            for action in etape['actions']:
                print(f"     {action}")
        
        # Projection finale
        print("\n" + "="*70)
        print("💎 PROJECTION FIN 2025")
        print("="*70)
        
        # Hypothèses optimistes mais réalistes
        charges_optimisees = 20000  # Après optimisations
        ratio_fin_annee = 70
        tarif_moyen = 125
        forfaits = 5000
        
        revenue_facturation = 255.8 * (ratio_fin_annee/100) * tarif_moyen
        revenue_total = revenue_facturation + forfaits
        cout_sebastien = 3000 * 1.82
        
        profit = revenue_total - charges_optimisees - cout_sebastien
        
        print(f"\n📊 Hypothèses fin 2025:")
        print(f"  • Charges optimisées : {charges_optimisees:,}€")
        print(f"  • Ratio facturable : {ratio_fin_annee}%")
        print(f"  • Tarif moyen : {tarif_moyen}€/h")
        print(f"  • Forfaits récurrents : {forfaits:,}€")
        
        print(f"\n💰 Résultats:")
        print(f"  • Revenue total : {revenue_total:,.0f}€/mois")
        print(f"  • Charges totales : {charges_optimisees + cout_sebastien:,.0f}€/mois")
        print(f"  • Profit net : {profit:+,.0f}€/mois")
        
        if profit > 3640:
            print(f"\n  ✅ Possibilité d'embaucher un développeur !")
        else:
            print(f"\n  📈 Continuer l'optimisation pour pouvoir embaucher")

def main():
    analyzer = SeuilRentabiliteAout()
    
    # 1. Calculer charges août
    charges_aout = analyzer.calculate_charges_aout()
    
    # 2. Analyser scénarios
    analyzer.analyze_scenarios(charges_aout)
    
    # 3. Proposer roadmap
    analyzer.propose_roadmap()
    
    print("\n" + "="*70)
    print(f"📅 Analyse du {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    print("💡 Impact départ Loan: -1,200€ salaire + -500€ charges sociales")
    print("   = 1,700€/mois d'économies")
    print("="*70)

if __name__ == "__main__":
    main()
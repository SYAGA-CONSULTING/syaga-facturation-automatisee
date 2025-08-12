#!/usr/bin/env python3
"""
CALCUL FINAL SEUIL RENTABILITÉ AVEC DONNÉES CORRIGÉES
Version définitive après toutes les corrections
"""

from datetime import datetime

class AnalyseFinaleRentabilite:
    def __init__(self):
        print("💎 ANALYSE FINALE SEUIL DE RENTABILITÉ")
        print("="*70)
        print("Version corrigée avec tous les ajustements\n")
        
    def calculate_final_charges(self):
        """Calcul définitif des charges mensuelles"""
        
        print("📊 CHARGES MENSUELLES RÉELLES FINALES")
        print("="*70)
        
        # CHARGES QONTO VÉRIFIÉES
        charges_qonto = {
            'Salaires (Hugo + Romain)': 5610,
            'Charges sociales (URSSAF)': 6032,
            'Impôts (DGFIP)': 2524,
            'Loyer bureaux (SCI QSSP)': 900,
            'Loyer bureaux (VillaData)': 1260,  # 1200€ HT = 1260€ TTC confirmé
            'Prêts (Riverbank)': 2144,
            'Comptable (Nobelia)': 1330,
            'Assurances (AMV + SwissLife)': 544,  # 397 + 147
            'Autres charges légitimes': 3000  # Réduit après exclusion anomalies
        }
        
        # CHARGES BANQUE POPULAIRE
        charges_bp = {
            'Télécom (Free Mobile + Internet)': 107,
            'Frais bancaires': 44,
            'Carburants et divers': 200
        }
        
        # EXCLUSIONS CONFIRMÉES (ne pas compter)
        exclusions = [
            "Virements internes SYAGA BPPC (14,000€/3mois)",
            "Pierre Questier - parti fin mai (3,753€)",
            "Doubles comptages Sébastien (10,500€/3mois)"
        ]
        
        total_qonto = sum(charges_qonto.values())
        total_bp = sum(charges_bp.values())
        total_charges = total_qonto + total_bp
        
        # Affichage détaillé
        print("\n💳 CHARGES QONTO:")
        for label, montant in charges_qonto.items():
            print(f"  {label:35} : {montant:7,}€")
        print(f"  {'SOUS-TOTAL QONTO':35} : {total_qonto:7,}€")
        
        print("\n🏦 CHARGES BANQUE POPULAIRE:")
        for label, montant in charges_bp.items():
            print(f"  {label:35} : {montant:7,}€")
        print(f"  {'SOUS-TOTAL BP':35} : {total_bp:7,}€")
        
        print("\n❌ EXCLUSIONS (confirmées non récurrentes):")
        for exclusion in exclusions:
            print(f"  • {exclusion}")
        
        print("\n" + "="*70)
        print(f"💰 TOTAL CHARGES MENSUELLES : {total_charges:,}€")
        print("="*70)
        
        return total_charges
    
    def calculate_break_even_scenarios(self, charges_base):
        """Calcul de différents scénarios de rentabilité"""
        
        print("\n🎯 SCÉNARIOS DE RENTABILITÉ")
        print("="*70)
        
        # Constants
        total_hours_clockify = 255.8
        ratio_actuel = 35.6
        ratio_net_to_charges = 1.82
        
        # Scénarios d'objectifs
        scenarios = [
            {
                'nom': 'SURVIE (Sébastien seul)',
                'sebastien_net': 3000,
                'salaries': 0,
                'salarie_net': 0
            },
            {
                'nom': 'CONSOLIDATION (Sébastien + 1 salarié)',
                'sebastien_net': 3000,
                'salaries': 1,
                'salarie_net': 2000
            },
            {
                'nom': 'CROISSANCE (Sébastien + 2 salariés)',
                'sebastien_net': 3000,
                'salaries': 2,
                'salarie_net': 2000
            },
            {
                'nom': 'OPTIMISÉ (Charges -15%, Sébastien seul)',
                'sebastien_net': 3000,
                'salaries': 0,
                'salarie_net': 0,
                'reduction_charges': 0.15
            }
        ]
        
        for scenario in scenarios:
            print(f"\n📌 SCÉNARIO: {scenario['nom']}")
            print("-" * 50)
            
            # Calcul charges
            charges = charges_base * (1 - scenario.get('reduction_charges', 0))
            cout_sebastien = scenario['sebastien_net'] * ratio_net_to_charges
            cout_salaries = scenario['salaries'] * scenario['salarie_net'] * ratio_net_to_charges
            
            total_besoin = charges + cout_sebastien + cout_salaries
            
            print(f"  Charges base : {charges:,.0f}€")
            if scenario.get('reduction_charges'):
                print(f"  (Réduction de {scenario['reduction_charges']*100:.0f}%)")
            print(f"  Objectif Sébastien : {cout_sebastien:,.0f}€")
            if scenario['salaries'] > 0:
                print(f"  Objectif {scenario['salaries']} salarié(s) : {cout_salaries:,.0f}€")
            print(f"  TOTAL BESOIN : {total_besoin:,.0f}€/mois")
            
            # Calcul ratios nécessaires
            for tarif in [100, 120, 150]:
                heures_necessaires = total_besoin / tarif
                ratio_necessaire = (heures_necessaires / total_hours_clockify) * 100
                
                if ratio_necessaire <= 100:
                    faisabilite = "✅ RÉALISABLE" if ratio_necessaire <= 75 else "⚠️ TENDU"
                else:
                    faisabilite = "❌ IMPOSSIBLE"
                
                print(f"\n  À {tarif}€/h :")
                print(f"    Heures nécessaires : {heures_necessaires:.0f}h")
                print(f"    Ratio nécessaire : {ratio_necessaire:.0f}%")
                print(f"    Status : {faisabilite}")
    
    def propose_action_plan(self):
        """Plan d'action concret pour la rentabilité"""
        
        print("\n" + "="*70)
        print("🚀 PLAN D'ACTION IMMÉDIAT")
        print("="*70)
        
        actions = [
            {
                'priorite': '🔴 URGENT',
                'action': 'Augmenter le ratio facturable',
                'actuel': '35.6%',
                'cible': '65% minimum',
                'gain': '+8,800€/mois à 100€/h',
                'delai': '3 mois'
            },
            {
                'priorite': '🔴 URGENT',
                'action': 'Renégocier les tarifs',
                'actuel': '100€/h',
                'cible': '120€/h minimum',
                'gain': '+20% de CA',
                'delai': 'Immédiat nouveaux clients'
            },
            {
                'priorite': '🟠 IMPORTANT',
                'action': 'Réduire charges "Autres"',
                'actuel': '3,000€/mois',
                'cible': '1,500€/mois',
                'gain': '-1,500€/mois charges',
                'delai': '2 mois'
            },
            {
                'priorite': '🟠 IMPORTANT',
                'action': 'Forfaits récurrents',
                'actuel': '0€',
                'cible': '5,000€/mois',
                'gain': '+5,000€ revenus stables',
                'delai': '3-6 mois'
            },
            {
                'priorite': '🟡 MOYEN TERME',
                'action': 'Optimiser loyers',
                'actuel': '2,160€ (2 bureaux)',
                'cible': '1,200€ (1 bureau)',
                'gain': '-960€/mois',
                'delai': 'Fin de bail'
            }
        ]
        
        print("\n📋 ACTIONS PAR PRIORITÉ:\n")
        
        for action in actions:
            print(f"{action['priorite']} {action['action']}")
            print(f"   Actuel : {action['actuel']}")
            print(f"   Cible : {action['cible']}")
            print(f"   Impact : {action['gain']}")
            print(f"   Délai : {action['delai']}")
            print()
        
        # Projection si actions réalisées
        print("="*70)
        print("📈 PROJECTION AVEC ACTIONS RÉALISÉES")
        print("="*70)
        
        charges_optimisees = 23695 * 0.85  # -15% de charges
        ratio_cible = 65
        tarif_moyen = 115  # Mix 100-120€
        forfaits_recurrents = 5000
        total_hours = 255.8
        
        revenue_facturation = total_hours * (ratio_cible/100) * tarif_moyen
        revenue_total = revenue_facturation + forfaits_recurrents
        
        cout_sebastien = 3000 * 1.82
        charges_totales = charges_optimisees + cout_sebastien
        
        profit = revenue_total - charges_totales
        
        print(f"\n💰 REVENUS:")
        print(f"  Facturation ({ratio_cible}% × {tarif_moyen}€/h) : {revenue_facturation:,.0f}€")
        print(f"  Forfaits récurrents : {forfaits_recurrents:,.0f}€")
        print(f"  TOTAL REVENUS : {revenue_total:,.0f}€")
        
        print(f"\n💸 CHARGES:")
        print(f"  Charges optimisées : {charges_optimisees:,.0f}€")
        print(f"  Sébastien (3000€ net) : {cout_sebastien:,.0f}€")
        print(f"  TOTAL CHARGES : {charges_totales:,.0f}€")
        
        print(f"\n🎯 RÉSULTAT:")
        print(f"  Profit mensuel : {profit:+,.0f}€")
        
        if profit > 0:
            print(f"\n  ✅ RENTABILITÉ ATTEINTE !")
            print(f"  Possibilité d'embaucher dans {profit/3640:.0f} mois")
        else:
            print(f"\n  ⚠️ Déficit restant, actions supplémentaires nécessaires")

def main():
    """Analyse finale complète"""
    
    analyser = AnalyseFinaleRentabilite()
    
    # 1. Calculer les vraies charges
    charges_reelles = analyser.calculate_final_charges()
    
    # 2. Analyser différents scénarios
    analyser.calculate_break_even_scenarios(charges_reelles)
    
    # 3. Proposer plan d'action
    analyser.propose_action_plan()
    
    print("\n" + "="*70)
    print(f"📅 Analyse générée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    print("💡 Les loyers totaux sont : 900€ (SCI QSSP) + 1260€ (VillaData) = 2160€/mois")
    print("="*70)

if __name__ == "__main__":
    main()
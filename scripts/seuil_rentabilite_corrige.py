#!/usr/bin/env python3
"""
CALCUL SEUIL RENTABILITÉ CORRIGÉ
Après identification et correction des anomalies
"""

from datetime import datetime

class SeuilRentabiliteCorrige:
    def __init__(self):
        print("📊 CALCUL SEUIL RENTABILITÉ - VERSION CORRIGÉE")
        print("="*70)
        print("Exclusion des anomalies identifiées dans l'analyse")
        print()
        
    def calculate_real_charges(self):
        """Calcul des vraies charges après corrections"""
        
        print("💰 CHARGES RÉELLES CORRIGÉES")
        print("="*70)
        
        # CHARGES QONTO CORRIGÉES
        charges_qonto = {
            'Salaires (Hugo + Romain)': 5610,
            'Charges sociales (URSSAF)': 6032,
            'Impôts (DGFIP)': 2524,
            'Loyers (SCI QSSP)': 900,
            'Loyers bureaux (VillaData)': 840,  # 2520€ / 3 mois
            'Prêts (Riverbank)': 2144,
            'Comptable (Nobelia)': 1330,
            'Assurances': 397,  # AMV 1191€ / 3 mois
            'Autres charges légitimes': 6333  # 19000€ / 3 mois après corrections
        }
        
        # CHARGES BANQUE POPULAIRE
        charges_bp = {
            'Télécom (Free)': 107,
            'Assurances (SwissLife)': 147,
            'Frais bancaires': 44,
            'Carburants et divers': 200  # Estimation prudente
        }
        
        # ANOMALIES EXCLUES
        anomalies_exclues = {
            'Virements internes BPPC': 4667,  # 14000€ / 3 mois
            'Pierre Questier (parti)': 1251,  # 3753€ / 3 mois
            'Double comptage Sébastien': 3500,  # 10500€ / 3 mois
            'VillaData (déplacé en loyers)': 0  # Déjà compté dans loyers
        }
        
        # Calcul totaux
        total_qonto = sum(charges_qonto.values())
        total_bp = sum(charges_bp.values())
        total_anomalies = sum(anomalies_exclues.values())
        
        # Affichage détaillé
        print("\n💳 CHARGES QONTO MENSUELLES:")
        for label, montant in charges_qonto.items():
            print(f"  {label:35} : {montant:8,.0f}€")
        print(f"  {'SOUS-TOTAL QONTO':35} : {total_qonto:8,.0f}€")
        
        print("\n🏛️ CHARGES BANQUE POPULAIRE:")
        for label, montant in charges_bp.items():
            print(f"  {label:35} : {montant:8,.0f}€")
        print(f"  {'SOUS-TOTAL BP':35} : {total_bp:8,.0f}€")
        
        print("\n❌ ANOMALIES EXCLUES (non récurrentes):")
        for label, montant in anomalies_exclues.items():
            print(f"  {label:35} : {montant:8,.0f}€/mois")
        print(f"  {'TOTAL ANOMALIES':35} : {total_anomalies:8,.0f}€/mois")
        
        charges_reelles = total_qonto + total_bp
        
        print("\n" + "="*70)
        print(f"💎 TOTAL CHARGES RÉELLES MENSUELLES : {charges_reelles:,.0f}€")
        print("="*70)
        
        return charges_reelles
    
    def calculate_break_even(self, charges_reelles):
        """Calcul du seuil de rentabilité"""
        
        print("\n🎯 CALCUL SEUIL DE RENTABILITÉ")
        print("="*70)
        
        # Objectifs salariaux
        objectif_sebastien_net = 3000
        objectif_salaries_net = 2000
        nb_salaries_futurs = 2
        ratio_net_to_total = 1.82
        
        cout_sebastien = objectif_sebastien_net * ratio_net_to_total
        cout_salaries = objectif_salaries_net * nb_salaries_futurs * ratio_net_to_total
        
        print("\n👨‍💼 OBJECTIFS SALARIAUX:")
        print(f"  Sébastien (3000€ net)      : {cout_sebastien:8,.0f}€ charges")
        print(f"  2 salariés (2x2000€ net)   : {cout_salaries:8,.0f}€ charges")
        print(f"  {'TOTAL OBJECTIFS':25} : {cout_sebastien + cout_salaries:8,.0f}€")
        
        # Charges totales cibles
        charges_cibles = charges_reelles + cout_sebastien + cout_salaries
        
        print("\n🎯 BESOINS TOTAUX:")
        print(f"  Charges actuelles    : {charges_reelles:8,.0f}€")
        print(f"  Objectifs salariaux  : {cout_sebastien + cout_salaries:8,.0f}€")
        print(f"  {'TOTAL CIBLE':20} : {charges_cibles:8,.0f}€/mois")
        
        return charges_cibles
    
    def analyze_with_clockify(self, charges_cibles):
        """Analyse avec données Clockify"""
        
        print("\n📈 ANALYSE AVEC CLOCKIFY (255.8h/mois)")
        print("="*70)
        
        total_hours = 255.8
        current_billable_ratio = 35.6  # Réel juillet 2025
        
        print(f"\n🕓 Situation actuelle:")
        print(f"  Total heures Clockify : {total_hours:.1f}h")
        print(f"  Ratio facturable actuel : {current_billable_ratio}%")
        print(f"  Heures facturables actuelles : {total_hours * current_billable_ratio / 100:.1f}h")
        
        # Tableaux de simulation
        tarifs = [100, 120, 150]
        ratios = [50, 60, 70, 75, 80, 85]
        
        for tarif in tarifs:
            print(f"\n💶 AVEC TARIF {tarif}€/H:")
            print("-" * 50)
            
            seuil_found = False
            
            for ratio in ratios:
                heures_facturables = total_hours * (ratio / 100)
                revenue = heures_facturables * tarif
                profit = revenue - charges_cibles
                
                if profit >= 0 and not seuil_found:
                    status = "🎯 SEUIL"
                    seuil_found = True
                elif profit >= 0:
                    status = "✅"
                else:
                    status = "❌"
                
                print(f"  {ratio:2}% facturable : {heures_facturables:5.1f}h = {revenue:7,.0f}€ → {profit:+7,.0f}€ {status}")
            
            # Calcul précis du seuil
            seuil_hours = charges_cibles / tarif
            seuil_ratio = (seuil_hours / total_hours) * 100
            
            print(f"\n  🚨 Seuil exact à {tarif}€/h:")
            print(f"     Heures nécessaires : {seuil_hours:.1f}h")
            print(f"     Ratio nécessaire : {seuil_ratio:.1f}%")
            
            if seuil_ratio <= 80:
                print(f"     → RÉALISABLE avec effort commercial")
            else:
                print(f"     → DIFFICILE, augmenter le tarif ou réduire les charges")
    
    def recommendations(self, charges_reelles):
        """Recommandations pour atteindre la rentabilité"""
        
        print("\n" + "="*70)
        print("💡 RECOMMANDATIONS POUR LA RENTABILITÉ")
        print("="*70)
        
        print("\n🎯 ACTIONS PRIORITAIRES:")
        print("\n1️⃣ AMÉLIORER LE RATIO FACTURABLE (actuellement 35.6%):")
        print("   • Objectif court terme : 60% (gain +6,200€/mois à 100€/h)")
        print("   • Objectif moyen terme : 70% (gain +8,800€/mois à 100€/h)")
        print("   • Réduire le temps interne non facturable")
        print("   • Automatiser les tâches répétitives")
        
        print("\n2️⃣ AUGMENTER LES TARIFS:")
        print("   • LAA : passer de 100€ à 120€/h (+20%)")
        print("   • Nouveaux clients : 120-150€/h minimum")
        print("   • Expertise spécialisée : 150-200€/h")
        
        print("\n3️⃣ OPTIMISER LES CHARGES (-20% possible):")
        charges_optimisables = {
            'Autres charges': 6333 * 0.3,  # 30% réductible
            'Comptable': 1330 * 0.2,  # 20% négociable
            'Assurances': (397 + 147) * 0.15  # 15% optimisable
        }
        
        total_eco = sum(charges_optimisables.values())
        
        for label, eco in charges_optimisables.items():
            print(f"   • {label}: -{eco:.0f}€/mois")
        print(f"   → Économie potentielle : {total_eco:.0f}€/mois")
        
        print("\n4️⃣ DÉVELOPPER LES REVENUS RÉCURRENTS:")
        print("   • Forfaits maintenance : 5-10k€/mois")
        print("   • Monitoring as a Service : 3-5k€/mois")
        print("   • Support SLA premium : 2-3k€/mois")
        
        print("\n" + "="*70)
        print("🎯 SCÉNARIO OPTIMISTE ATTEIGNABLE:")
        print("="*70)
        
        # Scénario optimiste
        ratio_cible = 65
        tarif_moyen = 110
        charges_optimisees = charges_reelles * 0.9
        total_hours = 255.8  # Heures Clockify
        
        revenue_optimiste = total_hours * (ratio_cible/100) * tarif_moyen
        profit_optimiste = revenue_optimiste - charges_optimisees
        
        print(f"\n  Ratio facturable : {ratio_cible}% (vs 35.6% actuel)")
        print(f"  Tarif moyen : {tarif_moyen}€/h (vs 100€ actuel)")
        print(f"  Charges réduites : {charges_optimisees:.0f}€ (-10%)")
        print(f"  Revenue mensuel : {revenue_optimiste:.0f}€")
        print(f"  Profit net : {profit_optimiste:+.0f}€/mois")
        
        if profit_optimiste > 5000:
            print(f"\n  ✅ OBJECTIF ATTEIGNABLE avec efforts commerciaux")
        else:
            print(f"\n  ⚠️ Efforts supplémentaires nécessaires")

def main():
    """Analyse complète corrigée"""
    
    analyzer = SeuilRentabiliteCorrige()
    
    # 1. Calculer vraies charges
    charges_reelles = analyzer.calculate_real_charges()
    
    # 2. Calculer seuil de rentabilité
    charges_cibles = analyzer.calculate_break_even(charges_reelles)
    
    # 3. Analyser avec Clockify
    analyzer.analyze_with_clockify(charges_cibles)
    
    # 4. Recommandations
    analyzer.recommendations(charges_reelles)
    
    print("\n" + "="*70)
    print("📅 Date analyse: " + datetime.now().strftime("%d/%m/%Y %H:%M"))
    print("="*70)

if __name__ == "__main__":
    main()

# Variables globales pour référence
total_hours = 255.8
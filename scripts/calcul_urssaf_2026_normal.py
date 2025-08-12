#!/usr/bin/env python3
"""
CALCUL CHARGES URSSAF NORMALES 2026
Estimation des charges sociales à partir de janvier 2026 (sans rattrapage)
Basé sur les données de rémunération 2025
"""

from datetime import datetime

class CalculURSSAF2026:
    def __init__(self):
        print("\n" + "="*80)
        print("📊 CALCUL CHARGES URSSAF NORMALES 2026")
        print("="*80)
        print("Objectif: Estimer les charges mensuelles sans rattrapage\n")
        
        # Taux de charges sociales 2025-2026
        self.taux_salaries = {
            'urssaf_total': 0.4540,  # ~45.4% (sécu, retraite, famille, etc.)
            'detail': {
                'assurance_maladie': 0.1300,  # 13%
                'assurance_vieillesse': 0.1755,  # 17.55%
                'allocations_familiales': 0.0520,  # 5.2%
                'accidents_travail': 0.0105,  # ~1.05% (estimation)
                'assurance_chomage': 0.0405,  # 4.05%
                'formation_professionnelle': 0.0055,  # 0.55%
                'versement_transport': 0.0200,  # 2% (si applicable)
                'contribution_solidarite': 0.0200  # Divers contrib.
            }
        }
        
        # Taux TNS (Travailleur Non Salarié) pour le dirigeant
        self.taux_tns = {
            'urssaf_tns': 0.2280,  # ~22.8% sur revenu dirigeant
            'detail': {
                'assurance_maladie': 0.0675,  # 6.75%
                'indemnites_journalieres': 0.0085,  # 0.85%
                'assurance_vieillesse': 0.1755,  # 17.55%
                'invalidite_deces': 0.0130,  # 1.3%
                'allocations_familiales': 0.0310,  # 3.1%
                'formation_professionnelle': 0.0025  # 0.25%
            }
        }
    
    def calculer_charges_salaries(self):
        """Calcule les charges pour Hugo et Romain (2100€ chacun)"""
        
        print("🧑‍💼 CHARGES SALARIÉS (Hugo + Romain)")
        print("-" * 50)
        
        salaire_brut_mensuel = 2100  # Hypothèse: 2100€ brut chacun
        nb_salaries = 2
        
        # Calcul charges sociales employeur
        base_calcul = salaire_brut_mensuel * nb_salaries
        charges_mensuelles = base_calcul * self.taux_salaries['urssaf_total']
        
        print(f"Base de calcul: {base_calcul:,.0f}€ ({salaire_brut_mensuel:,}€ × {nb_salaries} salariés)")
        print(f"Taux charges employeur: {self.taux_salaries['urssaf_total']:.1%}")
        print(f"🎯 CHARGES MENSUELLES: {charges_mensuelles:,.0f}€/mois")
        
        # Détail par type de charge
        print(f"\n📋 Détail des charges:")
        for nom, taux in self.taux_salaries['detail'].items():
            montant = base_calcul * taux
            print(f"  • {nom.replace('_', ' ').title()}: {montant:,.0f}€ ({taux:.2%})")
        
        print(f"\n💰 CHARGES ANNUELLES: {charges_mensuelles * 12:,.0f}€")
        
        return charges_mensuelles
    
    def calculer_charges_dirigeant(self, remuneration_dirigeant=3500):
        """Calcule les charges TNS du dirigeant"""
        
        print(f"\n👨‍💼 CHARGES TNS DIRIGEANT (Sébastien)")
        print("-" * 50)
        print(f"Rémunération mensuelle dirigeant: {remuneration_dirigeant:,}€")
        
        # Les charges TNS se calculent sur la rémunération du dirigeant
        charges_tns_mensuelles = remuneration_dirigeant * self.taux_tns['urssaf_tns']
        
        print(f"Taux charges TNS: {self.taux_tns['urssaf_tns']:.1%}")
        print(f"🎯 CHARGES TNS MENSUELLES: {charges_tns_mensuelles:,.0f}€/mois")
        
        # Détail par type de charge TNS
        print(f"\n📋 Détail des charges TNS:")
        for nom, taux in self.taux_tns['detail'].items():
            montant = remuneration_dirigeant * taux
            print(f"  • {nom.replace('_', ' ').title()}: {montant:,.0f}€ ({taux:.2%})")
        
        print(f"\n💰 CHARGES ANNUELLES TNS: {charges_tns_mensuelles * 12:,.0f}€")
        
        return charges_tns_mensuelles
    
    def comparaison_2025_vs_2026(self):
        """Compare les charges actuelles (avec rattrapage) vs normales 2026"""
        
        print("\n" + "="*80)
        print("📊 COMPARAISON 2025 (RATTRAPAGE) VS 2026 (NORMAL)")
        print("="*80)
        
        # Charges actuelles (avec rattrapage)
        charges_actuelles_2025 = {
            'URSSAF PACA': 2500,
            'URSSAF Languedoc': 1200,
            'Total actuel': 3700
        }
        
        # Charges normales calculées
        charges_salaries = self.calculer_charges_salaries()
        charges_dirigeant = self.calculer_charges_dirigeant(3000)  # Objectif 3000€ net
        charges_normales_2026 = charges_salaries + charges_dirigeant
        
        print(f"\n📈 COMPARAISON:")
        print(f"  🔴 Charges actuelles 2025 (avec rattrapage): {charges_actuelles_2025['Total actuel']:,}€/mois")
        print(f"  🟢 Charges normales 2026 estimées: {charges_normales_2026:,.0f}€/mois")
        print(f"  📉 ÉCONOMIE MENSUELLE: {charges_actuelles_2025['Total actuel'] - charges_normales_2026:,.0f}€/mois")
        print(f"  💰 ÉCONOMIE ANNUELLE: {(charges_actuelles_2025['Total actuel'] - charges_normales_2026) * 12:,.0f}€")
        
        return {
            'charges_2025': charges_actuelles_2025['Total actuel'],
            'charges_2026': charges_normales_2026,
            'economie_mensuelle': charges_actuelles_2025['Total actuel'] - charges_normales_2026,
            'economie_annuelle': (charges_actuelles_2025['Total actuel'] - charges_normales_2026) * 12
        }
    
    def nouveau_tableau_charges_2026(self):
        """Génère le tableau des charges avec les nouvelles URSSAF normales"""
        
        print("\n" + "="*80)
        print("🎯 TABLEAU CHARGES CORRIGÉ 2026")
        print("="*80)
        
        comparaison = self.comparaison_2025_vs_2026()
        
        charges_2026 = {
            'Salaires (Hugo + Romain)': 4200,
            'Charges sociales NORMALES': int(comparaison['charges_2026']),
            'Impôts (DGFIP)': 2524,
            'Loyers (SCI + VillaData)': 2160,
            'Prêt Riverbank': 1608,
            'Assurances': 1401,
            'Comptable': 1330,
            'IT & Télécom': 382,
            'Frais bancaires': 73,
            'Charges variables': 1596
        }
        
        total_2026 = sum(charges_2026.values())
        
        print("📋 CHARGES MENSUELLES 2026 (SANS RATTRAPAGE):")
        print("-" * 60)
        for poste, montant in charges_2026.items():
            print(f"  {poste:<30} : {montant:>8,}€")
        
        print("-" * 60)
        print(f"  {'TOTAL 2026':<30} : {total_2026:>8,}€")
        
        print(f"\n🎯 AVEC OBJECTIF SÉBASTIEN 3,000€ NET:")
        objectif_sebastien = 5460  # 3000€ net + charges
        besoin_total_2026 = total_2026 + objectif_sebastien
        print(f"  Charges Sébastien (3000€ net): {objectif_sebastien:,}€")
        print(f"  🎯 BESOIN TOTAL 2026: {besoin_total_2026:,}€/mois")
        
        print(f"\n💡 AMÉLIORATION vs 2025:")
        ancien_besoin = 26040  # Précédent calcul
        amelioration = ancien_besoin - besoin_total_2026
        print(f"  Ancien besoin (2025): {ancien_besoin:,}€")
        print(f"  Nouveau besoin (2026): {besoin_total_2026:,}€")
        print(f"  🎉 AMÉLIORATION: {amelioration:,}€/mois ({amelioration*12:,}€/an)")
        
        return {
            'total_charges_2026': total_2026,
            'besoin_total_2026': besoin_total_2026,
            'amelioration_mensuelle': amelioration,
            'amelioration_annuelle': amelioration * 12
        }

def main():
    """Exécution du calcul complet"""
    
    calculateur = CalculURSSAF2026()
    
    # 1. Calcul détaillé des charges
    charges_salaries = calculateur.calculer_charges_salaries()
    charges_dirigeant = calculateur.calculer_charges_dirigeant(3000)
    
    # 2. Comparaison 2025 vs 2026
    comparaison = calculateur.comparaison_2025_vs_2026()
    
    # 3. Nouveau tableau 2026
    nouveau_tableau = calculateur.nouveau_tableau_charges_2026()
    
    # 4. Conclusion
    print("\n" + "="*80)
    print("🏁 CONCLUSION")
    print("="*80)
    print("Les charges URSSAF actuelles incluent probablement du rattrapage.")
    print(f"À partir de janvier 2026, économie estimée: {comparaison['economie_mensuelle']:,}€/mois")
    print(f"Nouveau seuil de rentabilité: {nouveau_tableau['besoin_total_2026']:,}€/mois")
    print("\n📅 Recommandation: Recalculer précisément en décembre 2025")
    print("avec les vrais montants URSSAF stabilisés.")
    print("="*80)
    print(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")

if __name__ == "__main__":
    main()
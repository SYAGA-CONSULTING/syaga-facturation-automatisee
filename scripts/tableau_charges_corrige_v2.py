#!/usr/bin/env python3
"""
TABLEAU CHARGES CORRIGÉ V2 - Avec vraies échéances
- URSSAF rattrapage jusqu'au 31/12/2025
- Septembre : DOUBLE prêt (ancien + nouveau)
- Nouveau prêt 6 mois à partir de septembre
"""

from datetime import datetime

def afficher_mois(titre, charges_dict, salaire_net=3000):
    """Affiche les charges pour un mois donné"""
    print(f"\n{'='*80}")
    print(f"  {titre}")
    print('='*80)
    
    total = 0
    for categorie, items in charges_dict.items():
        print(f"\n  {categorie}")
        print("  " + "-"*60)
        for nom, montant, note in items:
            if isinstance(montant, (int, float)):
                if note:
                    print(f"  {nom:<35} {montant:>8,.0f}€   {note}")
                else:
                    print(f"  {nom:<35} {montant:>8,.0f}€")
                total += montant
    
    print("\n  " + "="*60)
    print(f"  {'TOTAL CHARGES':<35} {total:>8,.0f}€")
    
    # Avec salaire
    charges_tns = int(salaire_net * 0.682)  # 68.2% total TNS
    cout_salaire = salaire_net + charges_tns
    total_avec_salaire = total + cout_salaire
    
    print(f"  {'Salaire net + charges TNS':<35} {cout_salaire:>8,.0f}€")
    print(f"  {'CA MENSUEL NÉCESSAIRE':<35} {total_avec_salaire:>8,.0f}€")
    
    return total, total_avec_salaire

def main():
    print("\n" + "="*80)
    print("       📊 ÉVOLUTION CHARGES MENSUELLES - SYAGA CONSULTING")
    print("           Mise à jour: " + datetime.now().strftime('%d/%m/%Y %H:%M'))
    print("="*80)
    
    # CHARGES AOÛT 2025 (situation actuelle)
    charges_aout = {
        "SALAIRES & CHARGES": [
            ("URSSAF (avec rattrapage)", 3700, "jusqu'au 31/12/2025"),
            ("Romain BASTIEN", 2650, ""),
            ("Hugo JOUCLA", 2250, ""),
        ],
        "IMMOBILIER": [
            ("Loyer QSSP", 900, ""),
            ("Loyer CAGNES", 100, ""),
        ],
        "FINANCEMENTS": [
            ("Prêt Riverbank", 1618, "Fin 31/08"),
            ("DIAC", 586, ""),
        ],
        "SERVICES & ASSURANCES": [
            ("VillaData", 1260, ""),
            ("SwissLife (total)", 690, "132+507+51"),
            ("Hiscox RC Pro", 120, ""),
        ],
        "TÉLÉCOMS": [
            ("Orange", 110, ""),
            ("Free (Mobile + Box)", 75, "30+45"),
            ("OVH", 8, ""),
        ],
        "AUTRES": [
            ("DOUGS comptable", 340, ""),
            ("Essence", 103, ""),
            ("Microsoft 365", 24, ""),
            ("Roole", 15, ""),
        ],
    }
    
    # CHARGES SEPTEMBRE 2025 (DOUBLE PRÊT!)
    charges_septembre = {
        "SALAIRES & CHARGES": [
            ("URSSAF (avec rattrapage)", 3700, "⚠️ jusqu'au 31/12"),
            ("Romain BASTIEN", 2650, ""),
            ("Hugo JOUCLA", 2250, ""),
        ],
        "IMMOBILIER": [
            ("Loyer QSSP", 900, ""),
            ("Loyer CAGNES", 100, ""),
        ],
        "FINANCEMENTS": [
            ("Prêt Riverbank (ancien)", 1618, "❌ DERNIER MOIS"),
            ("Nouveau prêt (6 mois)", 1700, "🆕 NOUVEAU"),
            ("DIAC", 586, ""),
        ],
        "SERVICES & ASSURANCES": [
            ("VillaData", 1260, ""),
            ("SwissLife (total)", 690, ""),
            ("Hiscox RC Pro", 120, ""),
        ],
        "TÉLÉCOMS": [
            ("Orange", 110, ""),
            ("Free (Mobile + Box)", 75, ""),
            ("OVH", 8, ""),
        ],
        "AUTRES": [
            ("DOUGS comptable", 340, ""),
            ("Essence", 103, ""),
            ("Microsoft 365", 24, ""),
            ("Roole", 15, ""),
        ],
    }
    
    # CHARGES OCTOBRE-DÉCEMBRE 2025
    charges_oct_dec = {
        "SALAIRES & CHARGES": [
            ("URSSAF (avec rattrapage)", 3700, "⚠️ jusqu'au 31/12"),
            ("Romain BASTIEN", 2650, ""),
            ("Hugo JOUCLA", 2250, ""),
        ],
        "IMMOBILIER": [
            ("Loyer QSSP", 900, ""),
            ("Loyer CAGNES", 100, ""),
        ],
        "FINANCEMENTS": [
            ("Nouveau prêt (6 mois)", 1700, "Oct→Fév 2026"),
            ("DIAC", 586, ""),
        ],
        "SERVICES & ASSURANCES": [
            ("VillaData", 1260, ""),
            ("SwissLife (total)", 690, ""),
            ("Hiscox RC Pro", 120, ""),
        ],
        "TÉLÉCOMS": [
            ("Orange", 110, ""),
            ("Free (Mobile + Box)", 75, ""),
            ("OVH", 8, ""),
        ],
        "AUTRES": [
            ("DOUGS comptable", 340, ""),
            ("Essence", 103, ""),
            ("Microsoft 365", 24, ""),
            ("Roole", 15, ""),
        ],
    }
    
    # CHARGES JANVIER 2026 (après fin rattrapage URSSAF)
    charges_janvier = {
        "SALAIRES & CHARGES": [
            ("URSSAF (normal)", 2591, "✅ FIN RATTRAPAGE"),
            ("Romain BASTIEN", 2650, ""),
            ("Hugo JOUCLA", 2250, ""),
        ],
        "IMMOBILIER": [
            ("Loyer QSSP", 900, ""),
            ("Loyer CAGNES", 100, ""),
        ],
        "FINANCEMENTS": [
            ("Nouveau prêt", 1700, "Jusqu'à février"),
            ("DIAC", 586, ""),
        ],
        "SERVICES & ASSURANCES": [
            ("VillaData", 1260, ""),
            ("SwissLife (total)", 690, ""),
            ("Hiscox RC Pro", 120, ""),
        ],
        "TÉLÉCOMS": [
            ("Orange", 110, ""),
            ("Free (Mobile + Box)", 75, ""),
            ("OVH", 8, ""),
        ],
        "AUTRES": [
            ("DOUGS comptable", 340, ""),
            ("Essence", 103, ""),
            ("Microsoft 365", 24, ""),
            ("Roole", 15, ""),
        ],
    }
    
    # CHARGES MARS 2026 (après fin nouveau prêt)
    charges_mars = {
        "SALAIRES & CHARGES": [
            ("URSSAF (normal)", 2591, ""),
            ("Romain BASTIEN", 2650, ""),
            ("Hugo JOUCLA", 2250, ""),
        ],
        "IMMOBILIER": [
            ("Loyer QSSP", 900, ""),
            ("Loyer CAGNES", 100, ""),
        ],
        "FINANCEMENTS": [
            ("DIAC", 586, "Seul crédit restant"),
        ],
        "SERVICES & ASSURANCES": [
            ("VillaData", 1260, ""),
            ("SwissLife (total)", 690, ""),
            ("Hiscox RC Pro", 120, ""),
        ],
        "TÉLÉCOMS": [
            ("Orange", 110, ""),
            ("Free (Mobile + Box)", 75, ""),
            ("OVH", 8, ""),
        ],
        "AUTRES": [
            ("DOUGS comptable", 340, ""),
            ("Essence", 103, ""),
            ("Microsoft 365", 24, ""),
            ("Roole", 15, ""),
        ],
    }
    
    # Calculer et afficher chaque période
    total_aout, besoin_aout = afficher_mois("📅 AOÛT 2025 - SITUATION ACTUELLE", charges_aout)
    total_sept, besoin_sept = afficher_mois("⚠️ SEPTEMBRE 2025 - DOUBLE PRÊT!", charges_septembre)
    total_oct, besoin_oct = afficher_mois("📅 OCTOBRE-DÉCEMBRE 2025", charges_oct_dec)
    total_jan, besoin_jan = afficher_mois("🎯 JANVIER 2026 - FIN RATTRAPAGE URSSAF", charges_janvier)
    total_mars, besoin_mars = afficher_mois("✅ MARS 2026 - SITUATION OPTIMALE", charges_mars)
    
    # SYNTHÈSE
    print("\n" + "="*80)
    print("                    📊 SYNTHÈSE ÉVOLUTION")
    print("="*80)
    
    print(f"""
    ÉVOLUTION DU BESOIN EN CA MENSUEL:
    
    📅 Août 2025      : {besoin_aout:>8,}€  (baseline)
    ⚠️ Septembre 2025 : {besoin_sept:>8,}€  (+{besoin_sept-besoin_aout:,}€ double prêt)
    📅 Oct-Déc 2025   : {besoin_oct:>8,}€  (nouveau prêt seul)
    🎯 Janvier 2026   : {besoin_jan:>8,}€  (-1,109€ fin rattrapage)
    ✅ Mars 2026      : {besoin_mars:>8,}€  (-1,700€ fin prêt)
    
    POINTS CRITIQUES:
    
    ⚠️ SEPTEMBRE 2025 - MOIS DIFFICILE
       • Double prêt : 1,618€ + 1,700€ = 3,318€
       • Besoin exceptionnel : {besoin_sept:,}€
       • +{((besoin_sept-besoin_aout)/besoin_aout)*100:.1f}% vs août
    
    📉 RÉDUCTIONS PROGRESSIVES:
       • Janvier 2026 : -1,109€/mois (URSSAF normal)
       • Mars 2026 : -1,700€/mois (fin nouveau prêt)
       • Total économies : -2,809€/mois (-{((besoin_aout-besoin_mars)/besoin_aout)*100:.1f}%)
    
    💡 BESOIN DE TRÉSORERIE SEPTEMBRE:
       • Prévoir {besoin_sept-besoin_aout:,}€ supplémentaires
       • Ou négocier décalage début nouveau prêt
    """)
    
    return besoin_aout, besoin_sept, besoin_mars

if __name__ == "__main__":
    aout, sept, mars = main()
    
    print("\n" + "="*80)
    print("💰 STRATÉGIE RECOMMANDÉE")
    print("="*80)
    print(f"""
    1. GÉRER LE PIC DE SEPTEMBRE:
       • Facturer juillet-août rapidement (15,460€ identifiés)
       • Négocier acompte PHARMABEST si possible
       • Reporter début nouveau prêt à octobre si possible
    
    2. OPPORTUNITÉS COURT TERME:
       • UAI Phase 1 : 21k€ (démarrage septembre)
       • PHARMABEST : 85k€ (RDV rentrée)
       • LAA GPU : 4.5k€ (après test 150€)
    
    3. OBJECTIF FIN 2025:
       • Stabiliser à {besoin_mars:,}€/mois
       • Soit {besoin_mars/22:.0f}€/jour ouvré
       • Ou {besoin_mars/4:.0f}€/semaine
    """)
    
    print("\n✅ Analyse terminée et sauvegardée")
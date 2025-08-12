#!/usr/bin/env python3
"""
TABLEAU CHARGES AVEC VRAIE MASSE SALARIALE
Hugo seul à 2,000€ net/mois !
ÉNORME CHANGEMENT vs analyse précédente
"""

from datetime import datetime

def main():
    print("\n" + "="*80)
    print("       🚨 CORRECTION MAJEURE - VRAIE MASSE SALARIALE")
    print("           " + datetime.now().strftime('%d/%m/%Y %H:%M'))
    print("="*80)
    
    print("\n⚠️ ERREUR PRÉCÉDENTE:")
    print("-"*60)
    print("  Je comptais Romain (2,650€) + Hugo (2,250€) = 4,900€")
    print("  MAIS Romain est PARTI !")
    
    print("\n✅ SITUATION RÉELLE:")
    print("-"*60)
    print("  Hugo SEUL à 2,000€ net/mois")
    print("  ÉCONOMIE : 2,900€ net/mois sur les salaires !")
    
    # Calculer charges Hugo avec cotisations
    salaire_hugo = 2000
    charges_patronales = salaire_hugo * 0.45  # ~45% charges patronales
    cout_total_hugo = salaire_hugo + charges_patronales
    
    print(f"\n  Détail Hugo:")
    print(f"    • Salaire net     : {salaire_hugo:>6,}€")
    print(f"    • Charges patron. : {charges_patronales:>6,.0f}€")
    print(f"    • Coût total      : {cout_total_hugo:>6,.0f}€")
    
    # NOUVEAU TABLEAU DE CHARGES
    print("\n" + "="*80)
    print("  📊 CHARGES RÉELLES SEPTEMBRE 2025 (AVEC HUGO SEUL)")
    print("="*80)
    
    charges = [
        ("MASSE SALARIALE", ""),
        ("Hugo JOUCLA", cout_total_hugo, "2,000€ net"),
        ("", ""),
        ("CHARGES DIRIGEANT", ""),
        ("URSSAF TNS (avec rattrapage)", 3700, "jusqu'au 31/12"),
        ("", ""),
        ("IMMOBILIER", ""),
        ("Loyer QSSP", 900, ""),
        ("Loyer CAGNES", 100, ""),
        ("", ""),
        ("FINANCEMENTS", ""),
        ("Nouveau prêt (6 mois)", 1700, "Sept→Fév 2026"),
        ("DIAC", 586, ""),
        ("", ""),
        ("SERVICES IT", ""),
        ("VillaData", 1260, ""),
        ("", ""),
        ("ASSURANCES", ""),
        ("SwissLife (total)", 690, "Prév+Retraite+Biens"),
        ("Hiscox RC Pro", 120, ""),
        ("", ""),
        ("TÉLÉCOMS", ""),
        ("Orange", 110, ""),
        ("Free (Mobile + Box)", 75, ""),
        ("OVH", 8, ""),
        ("", ""),
        ("AUTRES", ""),
        ("DOUGS comptable", 340, ""),
        ("Essence", 103, ""),
        ("Microsoft 365", 24, ""),
        ("Roole", 15, ""),
    ]
    
    total = 0
    for item in charges:
        if len(item) == 2:
            nom, _ = item
            if nom:
                print(f"\n  {nom}")
                print("  " + "-"*40)
        else:
            nom, montant, note = item
            if isinstance(montant, (int, float)):
                if note:
                    print(f"  {nom:<30} {montant:>8,.0f}€  {note}")
                else:
                    print(f"  {nom:<30} {montant:>8,.0f}€")
                total += montant
    
    print("\n  " + "="*60)
    print(f"  {'TOTAL CHARGES (sans salaire dirigeant)':<40} {total:>8,.0f}€")
    
    # Avec salaire dirigeant
    salaire_net_dirigeant = 3000
    charges_tns_salaire = int(salaire_net_dirigeant * 0.682)
    cout_salaire_dirigeant = salaire_net_dirigeant + charges_tns_salaire
    
    print(f"\n  {'Salaire dirigeant net':<40} {salaire_net_dirigeant:>8,}€")
    print(f"  {'Charges sociales TNS sur salaire':<40} {charges_tns_salaire:>8,}€")
    print(f"  " + "="*60)
    besoin_total = total + cout_salaire_dirigeant
    print(f"  {'💰 CA MENSUEL NÉCESSAIRE':<40} {besoin_total:>8,.0f}€")
    
    # COMPARAISON AVANT/APRÈS
    print("\n\n" + "="*80)
    print("  📊 IMPACT DE L'ÉCONOMIE SUR MASSE SALARIALE")
    print("="*80)
    
    # Ancien calcul (erroné)
    ancien_salaires = 2650 + 2250  # Romain + Hugo (ce que je calculais)
    ancien_cout = ancien_salaires * 1.45  # Avec charges
    
    # Nouveau calcul
    nouveau_cout = cout_total_hugo
    
    economie = ancien_cout - nouveau_cout
    
    print(f"\n  AVANT (calcul erroné):")
    print(f"    • Romain + Hugo : 4,900€ net")
    print(f"    • Coût total    : {ancien_cout:>8,.0f}€")
    
    print(f"\n  MAINTENANT (réel):")
    print(f"    • Hugo seul     : 2,000€ net")
    print(f"    • Coût total    : {nouveau_cout:>8,.0f}€")
    
    print(f"\n  💰 ÉCONOMIE MENSUELLE : {economie:>8,.0f}€ !")
    
    # Nouveau besoin vs ancien
    ancien_besoin = 19595  # Ce qu'on calculait avant
    nouveau_besoin = besoin_total
    difference = ancien_besoin - nouveau_besoin
    
    print(f"\n  BESOIN EN CA:")
    print(f"    • Ancien calcul  : {ancien_besoin:>8,}€/mois")
    print(f"    • Nouveau calcul : {nouveau_besoin:>8,}€/mois")
    print(f"    • RÉDUCTION     : {difference:>8,}€/mois !")
    
    # Projection sur l'année
    print("\n\n" + "="*80)
    print("  📈 PROJECTION ANNUELLE AVEC NOUVELLE STRUCTURE")
    print("="*80)
    
    besoin_annuel = nouveau_besoin * 12
    print(f"\n  Besoin annuel : {besoin_annuel:>10,}€")
    print(f"  Soit {nouveau_besoin/22:.0f}€/jour ouvré")
    print(f"  Ou {nouveau_besoin/4:.0f}€/semaine")
    
    # Comparaison avec CA 2024-2025
    ca_precedent = 230000
    marge = ca_precedent - besoin_annuel
    
    print(f"\n  Avec le CA de l'exercice précédent ({ca_precedent:,}€):")
    if marge > 0:
        print(f"  ✅ EXCÉDENT POTENTIEL : {marge:>10,}€/an")
        print(f"     Soit {marge/12:>8,.0f}€/mois de marge !")
    else:
        print(f"  ❌ Manque : {abs(marge):,}€/an")
    
    # Évolution après janvier 2026
    print("\n\n" + "="*80)
    print("  📅 ÉVOLUTION 2026")
    print("="*80)
    
    # Janvier : fin rattrapage URSSAF
    charges_janvier = total - 3700 + 2591  # URSSAF normal
    besoin_janvier = charges_janvier + cout_salaire_dirigeant
    
    # Mars : fin nouveau prêt
    charges_mars = charges_janvier - 1700
    besoin_mars = charges_mars + cout_salaire_dirigeant
    
    print(f"\n  Septembre 2025 : {nouveau_besoin:>8,}€/mois")
    print(f"  Janvier 2026   : {besoin_janvier:>8,}€/mois (-1,109€ URSSAF)")
    print(f"  Mars 2026      : {besoin_mars:>8,}€/mois (-1,700€ prêt)")
    
    print(f"\n  💡 Besoin final (mars 2026) : {besoin_mars:,}€/mois")
    print(f"     Avec CA actuel moyen (19,167€) : ")
    if besoin_mars <= 19167:
        excedent_final = 19167 - besoin_mars
        print(f"     ✅ EXCÉDENT de {excedent_final:,}€/mois !")
    else:
        manque_final = besoin_mars - 19167
        print(f"     Manque seulement {manque_final:,}€/mois")
    
    return nouveau_besoin, economie

if __name__ == "__main__":
    besoin, economie = main()
    
    print("\n\n" + "="*80)
    print("  🎯 CONCLUSION")
    print("="*80)
    print(f"""
    CHANGEMENT MAJEUR ! Avec Hugo seul à 2,000€ net :
    
    • Économie immédiate : {economie:,}€/mois sur masse salariale
    • Nouveau besoin CA : {besoin:,}€/mois (au lieu de 19,595€)
    • Vous êtes DÉJÀ proche de l'équilibre !
    
    Avec le CA moyen actuel (19,167€/mois), vous n'êtes qu'à
    {besoin - 19167:,}€/mois de l'équilibre total.
    
    C'EST EXCELLENT ! 🎉
    """)
    
    print("\n✅ Analyse corrigée terminée")
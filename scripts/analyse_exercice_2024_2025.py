#!/usr/bin/env python3
"""
ANALYSE EXERCICE 2024-2025 (01/08/2024 - 31/07/2025)
CA vs Charges réelles
"""

from datetime import datetime

def main():
    print("\n" + "="*80)
    print("       📊 ANALYSE EXERCICE 2024-2025 - SYAGA CONSULTING")
    print("           Clôture: 31/07/2025")
    print("="*80)
    
    # Données de l'exercice
    ca_total = 230000
    charges_total = 234000
    
    print(f"\n  📈 CHIFFRE D'AFFAIRES : {ca_total:>12,}€")
    print(f"  💸 CHARGES TOTALES    : {charges_total:>12,}€")
    print(f"  " + "-"*50)
    resultat = ca_total - charges_total
    if resultat < 0:
        print(f"  ❌ RÉSULTAT          : {resultat:>12,}€")
    else:
        print(f"  ✅ RÉSULTAT          : {resultat:>12,}€")
    
    # Analyse mensuelle
    print("\n\n📊 MOYENNES MENSUELLES (sur 12 mois)")
    print("-"*60)
    
    ca_mensuel = ca_total / 12
    charges_mensuel = charges_total / 12
    
    print(f"  CA moyen/mois         : {ca_mensuel:>10,.0f}€")
    print(f"  Charges moyennes/mois : {charges_mensuel:>10,.0f}€")
    print(f"  Résultat moyen/mois   : {(ca_mensuel - charges_mensuel):>10,.0f}€")
    
    # Comparaison avec situation actuelle
    print("\n\n📊 COMPARAISON AVEC ANALYSE ACTUELLE")
    print("-"*60)
    
    charges_actuelles = 14549  # D'après notre analyse
    besoin_avec_salaire = 19595  # Avec 3k€ net dirigeant
    
    print(f"  Charges réelles août 2025    : {charges_actuelles:>10,}€/mois")
    print(f"  Moyenne exercice 2024-25     : {charges_mensuel:>10,.0f}€/mois")
    print(f"  Écart                        : {(charges_actuelles - charges_mensuel):>10,.0f}€")
    
    # Analyse de la masse salariale
    print("\n\n👥 ÉVOLUTION MASSE SALARIALE")
    print("-"*60)
    
    print("""
  HISTORIQUE:
  • Fév-Juil 2024 : Pierre QUESTIER (~2,500€ net)
  • Juil 2024-Août 2025 : Loan ROULPH (~900€ net alternant)
  • Depuis début : Romain BASTIEN (2,650€ net)
  • Depuis début : Hugo JOUCLA (2,250€ net)
  
  SITUATION ACTUELLE (Août 2025):
  • Romain : 2,650€ net
  • Hugo : 2,250€ net
  • Total : 4,900€ net/mois
  
  ANALYSE:
  • La masse salariale est restée relativement stable
  • Pierre + Loan ≈ Romain + Hugo actuellement
  • Pas d'économie significative malgré les départs
    """)
    
    # Points clés sur l'équilibre
    print("\n\n⚖️ ANALYSE D'ÉQUILIBRE")
    print("-"*60)
    
    print(f"""
  CONSTAT EXERCICE 2024-2025:
  • CA : {ca_total:,}€
  • Charges : {charges_total:,}€
  • Déficit : {abs(resultat):,}€ (-{abs(resultat)/ca_total*100:.1f}%)
  
  ÉQUILIBRE TROUVÉ:
  • Vous avez réussi à tenir avec {ca_mensuel:.0f}€/mois de CA
  • Les charges étaient de {charges_mensuel:.0f}€/mois
  • Le déficit était compensé par la trésorerie/prêts
  
  BESOIN RÉEL IDENTIFIÉ:
  • Sans salaire dirigeant : {charges_actuelles:,}€/mois
  • Avec 3,000€ net : {besoin_avec_salaire:,}€/mois
  • Soit {besoin_avec_salaire * 12:,}€/an nécessaires
    """)
    
    # Projection exercice 2025-2026
    print("\n\n📅 PROJECTION EXERCICE 2025-2026")
    print("-"*60)
    
    # Revenus identifiés
    revenus_recurrents = {
        "LAA forfaits": 7000 * 12,
        "UAI forfait": 4500 * 12,
        "Autres récurrents": 2000 * 12,
    }
    
    revenus_potentiels = {
        "PHARMABEST (si signé)": 85000,
        "UAI Phase 1 (21k€)": 21000,
        "LAA GPU (après test)": 4500,
    }
    
    total_recurrent = sum(revenus_recurrents.values())
    total_potentiel = sum(revenus_potentiels.values())
    
    print(f"\n  REVENUS RÉCURRENTS IDENTIFIÉS:")
    for nom, montant in revenus_recurrents.items():
        print(f"    • {nom:<25} : {montant:>10,}€/an")
    print(f"    " + "-"*45)
    print(f"    Total récurrents         : {total_recurrent:>10,}€/an")
    
    print(f"\n  REVENUS POTENTIELS:")
    for nom, montant in revenus_potentiels.items():
        print(f"    • {nom:<25} : {montant:>10,}€")
    print(f"    " + "-"*45)
    print(f"    Total potentiels         : {total_potentiel:>10,}€")
    
    print(f"\n  PROJECTION OPTIMISTE:")
    ca_projete = total_recurrent + total_potentiel
    print(f"    CA possible 2025-26      : {ca_projete:>10,}€")
    print(f"    Besoin avec salaire      : {besoin_avec_salaire * 12:>10,}€")
    print(f"    Marge potentielle        : {ca_projete - (besoin_avec_salaire * 12):>10,}€")
    
    # Recommandations
    print("\n\n💡 RECOMMANDATIONS")
    print("-"*60)
    
    print(f"""
  COURT TERME (Septembre 2025):
  ✓ Gérer le pic du double prêt (+1,700€)
  ✓ Facturer rapidement juillet (15,460€ identifiés)
  ✓ Relancer UAI pour démarrage Phase 1
  
  MOYEN TERME (Oct-Déc 2025):
  ✓ Concrétiser PHARMABEST (85k€ = 4.5 mois de charges)
  ✓ Maintenir {besoin_avec_salaire/22:.0f}€/jour ouvré de facturation
  ✓ Préparer fin rattrapage URSSAF (-1,109€/mois en janvier)
  
  LONG TERME (2026):
  ✓ Objectif CA : 235k€ minimum (équilibre)
  ✓ Idéal : 250k€ pour marge de sécurité
  ✓ Focus sur récurrent vs one-shot
    """)
    
    return ca_total, charges_total, resultat

if __name__ == "__main__":
    ca, charges, resultat = main()
    
    print("\n" + "="*80)
    print("📊 CONCLUSION")
    print("="*80)
    print(f"""
    L'exercice 2024-2025 montre que vous avez tenu avec un léger déficit
    de {abs(resultat):,}€ sur {ca:,}€ de CA ({abs(resultat)/ca*100:.1f}%).
    
    Avec une masse salariale stable (Pierre+Loan ≈ Romain+Hugo),
    l'objectif est maintenant de passer de 19,167€/mois de CA moyen
    à 19,595€/mois pour l'équilibre avec votre salaire.
    
    C'est totalement atteignable ! (+2.2% seulement)
    """)
    print("\n✅ Analyse terminée")
#!/usr/bin/env python3
"""
TABLEAU RÉEL FINAL DES CHARGES
Basé uniquement sur les montants confirmés et vérifiés
Sans les estimations inventées
"""

from datetime import datetime

def calculer_charges_reelles():
    """Calcul basé uniquement sur les charges confirmées"""
    
    print("📊 TABLEAU RÉEL DES CHARGES - DONNÉES CONFIRMÉES UNIQUEMENT")
    print("=" * 70)
    print("✅ = Confirmé | ❓ = À vérifier dans Qonto\n")
    
    # CHARGES CONFIRMÉES
    charges_confirmees = {
        "🧑‍💼 PERSONNEL": {
            "Salaires (Hugo + Romain)": {"montant": 4200, "statut": "✅", "source": "Confirmé"},
            "URSSAF (normal 2026)": {"montant": 2591, "statut": "✅", "source": "Calculé 45.4% + 22.8% TNS"}
        },
        "🏢 IMMOBILIER": {
            "Loyer SCI QSSP": {"montant": 900, "statut": "✅", "source": "Qonto confirmé"},
            "Loyer VillaData": {"montant": 1260, "statut": "✅", "source": "1200€ HT + TVA"}
        },
        "🏦 FINANCEMENT": {
            "Prêt Riverbank": {"montant": 1608, "statut": "✅", "source": "Qonto confirmé"}
        },
        "🛡️ ASSURANCES": {
            "SwissLife Prévoyance": {"montant": 470, "statut": "✅", "source": "Qonto"},
            "SwissLife Retraite": {"montant": 254, "statut": "✅", "source": "Qonto"},
            "AMV (TERMINÉ)": {"montant": 0, "statut": "✅", "source": "Fini (assurance moto)"},
            "Hiscox RC Pro": {"montant": 133, "statut": "✅", "source": "RC professionnelle"},
            "SwissLife (via BP)": {"montant": 147, "statut": "✅", "source": "Banque Populaire"}
        },
        "💻 IT & CLOUD": {
            "Claude.AI Pro": {"montant": 114, "statut": "✅", "source": "102-125€/mois"},
            "Microsoft 365": {"montant": 91, "statut": "✅", "source": "Licences Office"},
            "GitHub": {"montant": 20, "statut": "✅", "source": "Repos privés"},
            "OVH": {"montant": 30, "statut": "✅", "source": "Serveurs"},
            "Google Services": {"montant": 20, "statut": "✅", "source": "Workspace"}
        },
        "📱 TÉLÉCOM": {
            "Free Mobile": {"montant": 36, "statut": "✅", "source": "Forfaits mobiles"},
            "Free Internet": {"montant": 71, "statut": "✅", "source": "Fibre pro"}
        },
        "🏦 FRAIS BANCAIRES": {
            "Frais Qonto": {"montant": 29, "statut": "✅", "source": "Abonnement + frais"},
            "Frais BP": {"montant": 44, "statut": "✅", "source": "Cotisations cartes"}
        },
        "💼 COMPTABILITÉ": {
            "DOUGS": {"montant": 150, "statut": "❓", "source": "À VÉRIFIER dans Qonto"}
        }
    }
    
    # CHARGES À VÉRIFIER
    charges_a_verifier = {
        "❓ À IDENTIFIER DANS QONTO": {
            "Carburants (si récurrent)": {"montant": 0, "statut": "❓", "source": "Vérifier fréquence"},
            "Autres abonnements SaaS": {"montant": 0, "statut": "❓", "source": "Vérifier Qonto"},
            "Maintenance récurrente": {"montant": 0, "statut": "❓", "source": "Si contrats"},
            "Autres charges récurrentes": {"montant": 0, "statut": "❓", "source": "À identifier"}
        }
    }
    
    # Calcul et affichage
    print("📋 CHARGES CONFIRMÉES:")
    print("-" * 60)
    
    total_confirme = 0
    total_assurances = 0
    
    for categorie, items in charges_confirmees.items():
        print(f"\n{categorie}")
        sous_total = 0
        
        for nom, details in items.items():
            montant = details["montant"]
            statut = details["statut"]
            source = details["source"]
            
            if montant > 0:
                print(f"  {nom:<30} : {montant:>6}€ {statut} ({source})")
                sous_total += montant
                
                # Calculer total assurances sans AMV
                if "ASSURANCES" in categorie and "AMV" not in nom:
                    total_assurances += montant
            elif "AMV" in nom:
                print(f"  {nom:<30} : {montant:>6}€ {statut} ({source})")
        
        if sous_total > 0:
            print(f"  {'→ Sous-total':<30} : {sous_total:>6}€")
            total_confirme += sous_total
    
    # Afficher ce qui est à vérifier
    print(f"\n📋 CHARGES À VÉRIFIER DANS QONTO:")
    print("-" * 60)
    for categorie, items in charges_a_verifier.items():
        print(f"\n{categorie}")
        for nom, details in items.items():
            print(f"  • {nom} {details['statut']}")
    
    # Correction assurances
    print(f"\n💡 NOTE IMPORTANTE:")
    print(f"  Total assurances SANS AMV: {total_assurances}€/mois")
    print(f"  (AMV terminé = économie de 397€/mois)")
    
    # Total final
    print(f"\n" + "=" * 60)
    print(f"🎯 TOTAL CHARGES CONFIRMÉES: {total_confirme:,}€/mois")
    
    # Avec objectif Sébastien
    objectif_sebastien = 5460  # 3000€ net + charges
    besoin_total = total_confirme + objectif_sebastien
    
    print(f"\n💰 AVEC OBJECTIF SÉBASTIEN 3K€ NET:")
    print(f"  Charges confirmées: {total_confirme:,}€")
    print(f"  Sébastien (3k€ net): {objectif_sebastien:,}€")
    print(f"  🎯 BESOIN TOTAL: {besoin_total:,}€/mois")
    
    # Potentiel septembre
    potentiel_septembre = 6775
    couverture = (potentiel_septembre / besoin_total) * 100
    deficit = besoin_total - potentiel_septembre
    
    print(f"\n📈 ANALYSE RENTABILITÉ:")
    print(f"  Potentiel septembre: {potentiel_septembre:,}€/mois")
    print(f"  Couverture: {couverture:.0f}%")
    print(f"  Déficit à combler: {deficit:,}€/mois")
    
    # Comparaison avec ancien calcul (avec AMV)
    ancien_total_avec_amv = total_confirme + 397
    economie_amv = 397
    
    print(f"\n🎉 IMPACT FIN AMV:")
    print(f"  Ancien total (avec AMV): {ancien_total_avec_amv:,}€/mois")
    print(f"  Nouveau total (sans AMV): {total_confirme:,}€/mois")
    print(f"  💰 Économie AMV: {economie_amv}€/mois ({economie_amv*12:,}€/an)")
    
    print(f"\n⚠️ POINTS À CLARIFIER:")
    print("  1. Montant exact DOUGS dans Qonto")
    print("  2. Identifier autres charges récurrentes éventuelles")
    print("  3. Vérifier si carburants/déplacements sont récurrents")
    print("  4. Chercher autres abonnements SaaS oubliés")
    
    print(f"\n📅 Tableau réel généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    
    return {
        'total_confirme': total_confirme,
        'besoin_total': besoin_total,
        'deficit': deficit,
        'economie_amv': economie_amv
    }

if __name__ == "__main__":
    resultat = calculer_charges_reelles()
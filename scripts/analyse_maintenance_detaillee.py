#!/usr/bin/env python3
"""
ANALYSE DÉTAILLÉE DE LA "MAINTENANCE 300€"
Qu'est-ce qui peut être réellement récurrent dans ce poste ?
"""

from datetime import datetime

def analyser_maintenance_detaillee():
    """Analyse très détaillée du poste maintenance"""
    
    print("🔧 ANALYSE DÉTAILLÉE 'MAINTENANCE/RÉPARATIONS 300€'")
    print("=" * 60)
    print("❓ QUESTION: Qu'est-ce qui peut être VRAIMENT récurrent?\n")
    
    # Analyse détaillée par secteur
    maintenance_possible = {
        "🏢 INFRASTRUCTURE BUREAU": {
            "items_possibles": [
                "Contrat maintenance photocopieuse/imprimante",
                "Contrat maintenance climatisation/chauffage", 
                "Entretien des locaux (ménage, etc.)",
                "Maintenance alarme/sécurité",
                "Contrat maintenance ascenseur (si applicable)"
            ],
            "probabilite_syaga": "FAIBLE",
            "estimation": "0-50€/mois",
            "justification": "Petite structure, pas de gros équipements"
        },
        "🚗 VÉHICULE ENTREPRISE": {
            "items_possibles": [
                "Entretien véhicule régulier (vidange, etc.)",
                "Contrôle technique annuel",
                "Assurance véhicule (déjà dans assurances?)",
                "Réparations courantes",
                "Pneumatiques"
            ],
            "probabilite_syaga": "MOYENNE",
            "estimation": "50-100€/mois",
            "justification": "Si véhicule d'entreprise, entretien nécessaire"
        },
        "💻 INFRASTRUCTURE IT": {
            "items_possibles": [
                "Support technique OVH (déjà dans IT?)",
                "Maintenance serveurs/hosting",
                "Support technique Microsoft (déjà dans M365?)",
                "Licences antivirus entreprise",
                "Support matériel informatique"
            ],
            "probabilite_syaga": "FAIBLE",
            "estimation": "0-30€/mois",
            "justification": "Déjà inclus dans autres postes IT"
        },
        "🔧 MAINTENANCE MATÉRIEL": {
            "items_possibles": [
                "Réparation ordinateurs/serveurs",
                "Remplacement composants défaillants",
                "Maintenance imprimantes",
                "Réparation équipements bureau",
                "Intervention technicien externe"
            ],
            "probabilite_syaga": "TRÈS FAIBLE",
            "estimation": "0-20€/mois récurrent",
            "justification": "Plutôt ponctuel, pas récurrent"
        },
        "🏠 MAINTENANCE IMMOBILIÈRE": {
            "items_possibles": [
                "Réparations bureaux locatifs",
                "Entretien équipements (prises, éclairage)",
                "Maintenance internet/réseau",
                "Réparations diverses immobilier"
            ],
            "probabilite_syaga": "NULLE",
            "estimation": "0€/mois",
            "justification": "Responsabilité du propriétaire (SCI/VillaData)"
        }
    }
    
    # Affichage détaillé
    total_realiste = 0
    
    for secteur, details in maintenance_possible.items():
        print(f"\n{secteur}")
        print("-" * 40)
        print(f"📊 Probabilité SYAGA: {details['probabilite_syaga']}")
        print(f"💰 Estimation: {details['estimation']}")
        print(f"💡 Justification: {details['justification']}")
        
        print(f"\n🔍 Items possibles:")
        for item in details['items_possibles']:
            print(f"  • {item}")
        
        # Extraire estimation numérique
        if "0-50€" in details['estimation']:
            estimation_max = 25  # Milieu de fourchette
        elif "50-100€" in details['estimation']:
            estimation_max = 75
        elif "0-30€" in details['estimation']:
            estimation_max = 15
        elif "0-20€" in details['estimation']:
            estimation_max = 10
        else:
            estimation_max = 0
            
        total_realiste += estimation_max
        print(f"🎯 Retenu: {estimation_max}€/mois")
    
    print(f"\n" + "=" * 60)
    print(f"📊 SYNTHÈSE MAINTENANCE RÉCURRENTE RÉALISTE")
    print("=" * 60)
    print(f"🎯 TOTAL RÉCURRENT RÉALISTE: {total_realiste}€/mois")
    print(f"📉 vs 300€ initial: -{300-total_realiste}€/mois d'économie")
    
    return total_realiste

def questions_specifiques_syaga():
    """Questions spécifiques à poser pour clarifier"""
    
    print(f"\n❓ QUESTIONS SPÉCIFIQUES POUR CLARIFIER:")
    print("=" * 50)
    
    questions = [
        "🚗 VÉHICULE: Y a-t-il un véhicule d'entreprise avec entretien régulier?",
        "🏢 BUREAUX: Contrats maintenance spécifiques (photocopieuse, clim, etc.)?", 
        "💻 IT: Support/maintenance payant au-delà des abonnements déjà listés?",
        "🔧 MATÉRIEL: Interventions technicien externes récurrentes?",
        "📄 CONTRATS: Y a-t-il des contrats maintenance signés mensuels/trimestriels?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"  {i}. {question}")
    
    print(f"\n💡 HYPOTHÈSE CONSERVATRICE:")
    print(f"  Si toutes réponses = NON → Maintenance récurrente = 0€")
    print(f"  Les 300€ sont probablement des réparations ponctuelles")

def nouveau_calcul_sans_autres_achats_maintenance():
    """Recalcul en excluant les autres achats et révisant maintenance"""
    
    print(f"\n" + "=" * 80)
    print("🎯 CALCUL FINAL - SUPPRESSION AUTRES ACHATS + RÉVISION MAINTENANCE")
    print("=" * 80)
    
    maintenance_realiste = analyser_maintenance_detaillee()
    questions_specifiques_syaga()
    
    print(f"\n📊 RÉVISIONS APPLIQUÉES:")
    print("-" * 50)
    print(f"  ❌ Autres achats: 500€ → 0€ (exclus complètement)")
    print(f"  🔧 Maintenance: 300€ → {maintenance_realiste}€ (récurrent seulement)")
    print(f"  💰 Économie totale: {500 + (300-maintenance_realiste)}€/mois")
    
    # Nouvelles charges détaillées FINALES
    charges_detail_finales = {
        "IT & Cloud": 325,      
        "Télécom": 127,         
        "Frais bancaires": 73,  
        "DOUGS comptable": 150,
        "Carburants + Péages": 200,  # Déplacements clients
        "Maintenance récurrente": maintenance_realiste,
        # Autres achats = 0€ (exclus)
    }
    
    total_detail_final = sum(charges_detail_finales.values())
    
    print(f"\n📋 CHARGES DÉTAILLÉES FINALES:")
    print("-" * 50)
    for poste, montant in charges_detail_finales.items():
        print(f"  {poste:<30} : {montant:>6}€")
    print("-" * 50)
    print(f"  {'TOTAL FINAL DÉTAILLÉ':<30} : {total_detail_final:>6}€")
    
    # Charges principales (inchangées)
    charges_principales = {
        "Salaires (Hugo + Romain)": 4200,
        "URSSAF (normal 2026)": 2591,
        "Loyers (SCI + VillaData)": 2160,
        "Prêt Riverbank": 1608,
        "Assurances": 1401
    }
    
    total_principal = sum(charges_principales.values())
    total_absolu_final = total_principal + total_detail_final
    
    print(f"\n📊 TABLEAU ABSOLU FINAL:")
    print("-" * 60)
    for nom, montant in charges_principales.items():
        print(f"  {nom:<35} : {montant:>8,}€")
    print(f"  {'IT/Télécom/Banque/Divers (final)':<35} : {total_detail_final:>8,}€")
    print("-" * 60)
    print(f"  {'🎯 TOTAL ABSOLU FINAL':<35} : {total_absolu_final:>8,}€")
    
    # Avec objectif Sébastien
    objectif_sebastien = 5460
    besoin_absolu_final = total_absolu_final + objectif_sebastien
    
    print(f"\n💰 BESOIN ABSOLU FINAL:")
    print(f"  🎯 BESOIN AVEC SÉBASTIEN 3K€: {besoin_absolu_final:,}€/mois")
    
    # Comparaisons finales
    ancien_besoin = 18795  # Premier calcul
    amelioration_totale = ancien_besoin - besoin_absolu_final
    
    potentiel_septembre = 6775
    couverture_absolue = (potentiel_septembre / besoin_absolu_final) * 100
    deficit_absolu = besoin_absolu_final - potentiel_septembre
    
    print(f"\n🎉 AMÉLIORATION TOTALE:")
    print(f"  Besoin initial: {ancien_besoin:,}€/mois")
    print(f"  Besoin absolu final: {besoin_absolu_final:,}€/mois") 
    print(f"  🎉 AMÉLIORATION TOTALE: {amelioration_totale:,}€/mois ({amelioration_totale*12:,}€/an)")
    
    print(f"\n📈 RENTABILITÉ ABSOLUE:")
    print(f"  Potentiel septembre: {potentiel_septembre:,}€/mois")
    print(f"  Couverture finale: {couverture_absolue:.0f}%")
    print(f"  Déficit final à combler: {deficit_absolu:,}€/mois")
    
    print(f"\n💡 CONCLUSION:")
    print(f"  En excluant tous les éléments ponctuels identifiés,")
    print(f"  le besoin mensuel réel passe de {ancien_besoin:,}€ à {besoin_absolu_final:,}€")
    print(f"  soit {amelioration_totale:,}€/mois d'amélioration !")
    
    print(f"\n📅 Analyse finale complète le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    
    return {
        'besoin_absolu_final': besoin_absolu_final,
        'amelioration_totale': amelioration_totale,
        'couverture_finale': couverture_absolue,
        'deficit_final': deficit_absolu
    }

if __name__ == "__main__":
    resultat = nouveau_calcul_sans_autres_achats_maintenance()
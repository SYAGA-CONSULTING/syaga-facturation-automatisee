#!/usr/bin/env python3
"""
Script de génération du fichier XML pour OXYGEN
avec les données de facturation juillet 2025
"""

import json
import sys
import os

# Ajouter le path pour importer le module
sys.path.append('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/src')

from oxygen_xml_generator import OxygenXMLGenerator

# Données Clockify juillet 2025 (basées sur notre analyse)
clockify_data = {
    "period": "2025-07",
    "extraction_date": "2025-08-11",
    "total_hours": 160.6,
    "clients": {
        "LAA": {
            "total_hours": 62.4,
            "categories": {
                "Dette technologique": 27.0,
                "Tests infrastructure": 21.5,
                "Développements": 9.0,
                "Maintenance hors forfait": 4.9
            }
        },
        "LAA MAROC": {
            "total_hours": 1.5,
            "categories": {
                "Maintenance hors forfait": 1.5
            }
        },
        "UAI": {
            "total_hours": 14.5,
            "categories": {
                "SQL Server": 9.0,
                "HardenAD": 5.5
            }
        },
        "LEFEBVRE": {
            "total_hours": 3.6,
            "categories": {
                "Conseil": 3.6
            }
        },
        "PETRAS": {
            "total_hours": 2.0,
            "categories": {
                "Support": 2.0
            }
        },
        "TOUZEAU": {
            "total_hours": 1.5,
            "categories": {
                "Support IT": 1.5
            }
        },
        "AXION": {
            "total_hours": 7.0,
            "categories": {
                "Infrastructure": 7.0
            }
        },
        "ART INFO": {
            "total_hours": 2.0,
            "categories": {
                "Maintenance": 2.0
            }
        },
        "FARBOS": {
            "total_hours": 1.5,
            "categories": {
                "Support": 1.5
            }
        },
        "PDB": {
            "total_hours": 4.0,
            "categories": {
                "HardenAD": 4.0
            }
        },
        "QUADRIMEX": {
            "total_hours": 15.0,
            "categories": {
                "Refactoring SSIS": 15.0
            }
        }
    }
}

# Configuration étendue des clients
clients_config = {
    "LAA": {
        "code": "LAA01",
        "nom_complet": "Les Artisans de l'Automobile",
        "taux_horaire": 100,
        "adresse": "Zone Industrielle Nord",
        "cp": "13100",
        "ville": "AIX-EN-PROVENCE",
        "pays": "France",
        "tel": "0442123456",
        "email": "compta@laa.fr",
        "mode_reglement": "VIR",
        "delai_paiement": 30
    },
    "LAA MAROC": {
        "code": "LAAM01",
        "nom_complet": "LAA MAROC",
        "taux_horaire": 100,
        "adresse": "Zone Industrielle",
        "cp": "20000",
        "ville": "CASABLANCA",
        "pays": "Maroc",
        "email": "compta@laa.ma",
        "mode_reglement": "VIR",
        "delai_paiement": 45
    },
    "UAI": {
        "code": "UAI01",
        "nom_complet": "Union des Assurances Immobilières",
        "taux_horaire": 850,
        "adresse": "Tour Défense",
        "adresse2": "Étage 42",
        "cp": "92000",
        "ville": "LA DEFENSE",
        "pays": "France",
        "tel": "0147123456",
        "email": "factures@uai.fr",
        "mode_reglement": "VIR",
        "delai_paiement": 45
    },
    "LEFEBVRE": {
        "code": "LEF01",
        "nom_complet": "Cabinet LEFEBVRE",
        "taux_horaire": 120,
        "adresse": "15 rue de la République",
        "cp": "13001",
        "ville": "MARSEILLE",
        "pays": "France",
        "email": "admin@lefebvre.fr",
        "mode_reglement": "VIR",
        "delai_paiement": 30
    },
    "PETRAS": {
        "code": "PET01",
        "nom_complet": "PETRAS SAS",
        "taux_horaire": 100,
        "adresse": "Chemin des Vignes",
        "cp": "83560",
        "ville": "POURRIERES",
        "pays": "France",
        "email": "contact@petras.fr",
        "mode_reglement": "CHQ",
        "delai_paiement": 30
    },
    "TOUZEAU": {
        "code": "TOU01",
        "nom_complet": "TOUZEAU",
        "taux_horaire": 100,
        "adresse": "Route de la Mer",
        "cp": "13600",
        "ville": "LA CIOTAT",
        "pays": "France",
        "mode_reglement": "VIR",
        "delai_paiement": 30
    },
    "AXION": {
        "code": "AXI01",
        "nom_complet": "AXION INFRASTRUCTURE",
        "taux_horaire": 100,
        "adresse": "Parc d'Activités",
        "cp": "13400",
        "ville": "AUBAGNE",
        "pays": "France",
        "email": "compta@axion.fr",
        "mode_reglement": "VIR",
        "delai_paiement": 30
    },
    "ART INFO": {
        "code": "ART01",
        "nom_complet": "ART INFO",
        "taux_horaire": 100,
        "adresse": "Zone Artisanale",
        "cp": "13127",
        "ville": "VITROLLES",
        "pays": "France",
        "mode_reglement": "VIR",
        "delai_paiement": 30
    },
    "FARBOS": {
        "code": "FAR01",
        "nom_complet": "FARBOS",
        "taux_horaire": 100,
        "adresse": "Avenue du Commerce",
        "cp": "13800",
        "ville": "ISTRES",
        "pays": "France",
        "mode_reglement": "CHQ",
        "delai_paiement": 30
    },
    "PDB": {
        "code": "PDB01",
        "nom_complet": "Mairie de PORT DE BOUC",
        "taux_horaire": 100,
        "adresse": "Place de l'Hôtel de Ville",
        "cp": "13110",
        "ville": "PORT DE BOUC",
        "pays": "France",
        "email": "comptabilite@portdebouc.fr",
        "mode_reglement": "MANDAT",
        "delai_paiement": 30
    },
    "QUADRIMEX": {
        "code": "QUA01",
        "nom_complet": "QUADRIMEX",
        "taux_horaire": 100,
        "adresse": "Zone Industrielle Les Paluds",
        "cp": "13400",
        "ville": "AUBAGNE",
        "pays": "France",
        "email": "finance@quadrimex.fr",
        "mode_reglement": "VIR",
        "delai_paiement": 30
    }
}

def main():
    print("🚀 GÉNÉRATION XML POUR OXYGEN - JUILLET 2025")
    print("=" * 60)
    
    # Créer le dossier de sortie
    os.makedirs('/home/sq/oxygen_export', exist_ok=True)
    
    # Sauvegarder la config des clients
    config_file = '/home/sq/oxygen_export/clients_config.json'
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(clients_config, f, indent=2, ensure_ascii=False)
    print(f"✅ Configuration clients sauvegardée: {config_file}")
    
    # Générer le XML
    generator = OxygenXMLGenerator(config_file)
    output_file = '/home/sq/oxygen_export/FACTURES_JUILLET_2025.xml'
    
    total = generator.generate_xml(clockify_data, output_file, "2025-07")
    
    print(f"\n📋 RÉSUMÉ:")
    print(f"   • {total} factures générées")
    print(f"   • Fichier XML: {output_file}")
    print(f"   • Prêt pour import dans OXYGEN")
    
    # Calculer les totaux pour vérification
    print("\n💰 MONTANTS PAR CLIENT (après arrondis):")
    print("-" * 60)
    
    total_general = 0
    for client_name, client_data in clockify_data['clients'].items():
        if client_data['total_hours'] > 0:
            config = clients_config.get(client_name, {"taux_horaire": 100})
            hours = generator.apply_intelligent_rounding(client_data['total_hours'])
            montant = hours * config['taux_horaire']
            print(f"{client_name:<20} {hours:>6.1f}h x {config['taux_horaire']:>4}€ = {montant:>8.0f}€")
            total_general += montant
    
    print("-" * 60)
    print(f"{'TOTAL HT':<32} {total_general:>8.0f}€")
    print(f"{'TVA 20%':<32} {total_general * 0.2:>8.0f}€")
    print(f"{'TOTAL TTC':<32} {total_general * 1.2:>8.0f}€")
    
    print("\n✅ Fichier XML prêt pour import dans MemSoft OXYGEN!")
    print(f"   📁 {output_file}")

if __name__ == "__main__":
    main()
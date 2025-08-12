#!/usr/bin/env python3
"""
Script de génération du fichier XML CORRIGÉ pour OXYGEN
Juillet 2025 avec :
- UAI : DEVIS (type D) et non facture
- LAA : 4 factures séparées par catégorie
- Libellés professionnels corrects
"""

import json
import sys
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from datetime import datetime

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
    # Autres clients restent identiques...
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

def apply_intelligent_rounding(hours):
    """Arrondi intelligent SYAGA"""
    if hours < 5:
        return round(hours * 2 + 0.49) / 2
    else:
        return round(hours * 2 - 0.49) / 2

def create_piece(client_name, hours, description, piece_type="F", counter=1000):
    """Crée un élément PIECE (facture ou devis)"""
    client_config = clients_config.get(client_name, clients_config.get("LAA"))
    
    piece = ET.Element('PIECE')
    
    # Informations de base
    ET.SubElement(piece, 'CLIENT_CODE').text = client_config['code']
    ET.SubElement(piece, 'TYPE').text = piece_type  # F=Facture, D=Devis
    ET.SubElement(piece, 'WEB_ID').text = f'#{counter}'
    ET.SubElement(piece, 'DESIG').text = description
    
    # Dates
    today = datetime.now().strftime('%d/%m/%Y')
    ET.SubElement(piece, 'DATE_CREATION').text = today
    ET.SubElement(piece, 'DATE_LIVRAISON').text = today
    
    # Conditions commerciales
    ET.SubElement(piece, 'TAUX_REMISE').text = '0,00'
    ET.SubElement(piece, 'TAUX_ESCOMPTE').text = '0,00'
    ET.SubElement(piece, 'GCPREG_CODE').text = client_config.get('mode_reglement', 'VIR')
    ET.SubElement(piece, 'PORT_HT').text = '0,00'
    ET.SubElement(piece, 'FRAIS_HT').text = '0,00'
    ET.SubElement(piece, 'ECOTAXE').text = '0'
    ET.SubElement(piece, 'NBRE_JOURS').text = str(client_config.get('delai_paiement', 30))
    ET.SubElement(piece, 'DECALAGE').text = '0'
    ET.SubElement(piece, 'MONNAIE').text = 'EUR'
    ET.SubElement(piece, 'VALID').text = '1'
    ET.SubElement(piece, 'ARRETE').text = 'F'
    
    # Adresse de facturation
    adresse_fact = ET.SubElement(piece, 'adresse')
    ET.SubElement(adresse_fact, 'STYPE').text = 'facturation'
    ET.SubElement(adresse_fact, 'NOM').text = client_config['nom_complet']
    ET.SubElement(adresse_fact, 'ADRESSE').text = client_config.get('adresse', '')
    if client_config.get('adresse2'):
        ET.SubElement(adresse_fact, 'ADRESSE2').text = client_config['adresse2']
    ET.SubElement(adresse_fact, 'CP').text = client_config.get('cp', '')
    ET.SubElement(adresse_fact, 'VILLE').text = client_config.get('ville', '')
    ET.SubElement(adresse_fact, 'PAYS').text = client_config.get('pays', 'France')
    if client_config.get('tel'):
        ET.SubElement(adresse_fact, 'TEL').text = client_config['tel']
    if client_config.get('email'):
        ET.SubElement(adresse_fact, 'EMAIL').text = client_config['email']
    
    # Adresse de livraison
    adresse_liv = ET.SubElement(piece, 'adresse')
    ET.SubElement(adresse_liv, 'STYPE').text = 'livraison'
    ET.SubElement(adresse_liv, 'NOM').text = client_config['nom_complet']
    ET.SubElement(adresse_liv, 'ADRESSE').text = client_config.get('adresse', '')
    ET.SubElement(adresse_liv, 'CP').text = client_config.get('cp', '')
    ET.SubElement(adresse_liv, 'VILLE').text = client_config.get('ville', '')
    ET.SubElement(adresse_liv, 'PAYS').text = client_config.get('pays', 'France')
    
    # Ligne de facturation
    hours_rounded = apply_intelligent_rounding(hours)
    ligne = ET.SubElement(piece, 'LIGNE')
    ET.SubElement(ligne, 'NUMERO').text = '1'
    ET.SubElement(ligne, 'ARTICLE_WEB_CODE').text = 'PRES-HF'
    ET.SubElement(ligne, 'DESIG').text = description
    ET.SubElement(ligne, 'QTE').text = f'{hours_rounded:.2f}'.replace('.', ',')
    ET.SubElement(ligne, 'PUHT').text = f'{client_config["taux_horaire"]},00'
    ET.SubElement(ligne, 'TAUX_REMISE').text = '0,00'
    ET.SubElement(ligne, 'GCPTVA_CODE').text = 'NORM'
    
    return piece

def main():
    print("🚀 GÉNÉRATION XML CORRIGÉ POUR OXYGEN - JUILLET 2025")
    print("=" * 60)
    
    # Créer la structure XML
    dataset = ET.Element('DataSet')
    dataset.set('xmlns', 'http://tempuri.org/')
    newdataset = ET.SubElement(dataset, 'NewDataSet')
    newdataset.set('xmlns', 'http://tempuri.org/data.xsd')
    
    counter = 1000
    total_factures = 0
    total_devis = 0
    
    # LAA - 4 FACTURES SÉPARÉES
    print("\n📄 LAA - 4 factures séparées par catégorie")
    print("-" * 40)
    
    # 1. Dette technologique (27h)
    piece = create_piece("LAA", 27.0, 
                        "Dette technologique - Migration SAGE V12 et Windows Server 2022 - Juillet 2025",
                        "F", counter)
    newdataset.append(piece)
    print(f"  F#{counter}: Dette technologique - 27h × 100€ = 2,700€")
    counter += 1
    total_factures += 1
    
    # 2. Tests infrastructure (21.5h)
    piece = create_piece("LAA", 21.5,
                        "Tests et validations infrastructure Hyper-V - Snapshots et rollback - Juillet 2025",
                        "F", counter)
    newdataset.append(piece)
    print(f"  F#{counter}: Tests infrastructure - 21.5h × 100€ = 2,150€")
    counter += 1
    total_factures += 1
    
    # 3. Développements (9h)
    piece = create_piece("LAA", 9.0,
                        "Développements SalesLogix - Nouvelles fonctionnalités demandées - Juillet 2025",
                        "F", counter)
    newdataset.append(piece)
    print(f"  F#{counter}: Développements - 9h × 100€ = 900€")
    counter += 1
    total_factures += 1
    
    # 4. Maintenance hors forfait (5h)
    piece = create_piece("LAA", 5.0,
                        "Maintenance hors forfait - Support urgences non planifiées - Juillet 2025",
                        "F", counter)
    newdataset.append(piece)
    print(f"  F#{counter}: Maintenance HF - 5h × 100€ = 500€")
    counter += 1
    total_factures += 1
    
    # LAA MAROC - 1 facture
    print("\n📄 LAA MAROC")
    print("-" * 40)
    piece = create_piece("LAA MAROC", 1.5,
                        "Maintenance hors forfait - Support à distance - Juillet 2025",
                        "F", counter)
    newdataset.append(piece)
    print(f"  F#{counter}: Maintenance HF - 1.5h × 100€ = 150€")
    counter += 1
    total_factures += 1
    
    # UAI - DEVIS (pas facture!)
    print("\n📋 UAI - DEVIS")
    print("-" * 40)
    
    # Devis SQL Server
    piece = create_piece("UAI", 9.0,
                        "Optimisation performances SQL Server - Analyse requêtes X3 - Juillet 2025",
                        "D", counter)  # D pour DEVIS
    newdataset.append(piece)
    print(f"  D#{counter}: SQL Server - 9h × 850€ = 7,650€")
    counter += 1
    total_devis += 1
    
    # Devis HardenAD
    piece = create_piece("UAI", 5.5,
                        "Audit sécurité Active Directory - Recommandations HardenAD - Juillet 2025",
                        "D", counter)  # D pour DEVIS
    newdataset.append(piece)
    print(f"  D#{counter}: HardenAD - 5.5h × 850€ = 4,675€")
    counter += 1
    total_devis += 1
    
    # AUTRES CLIENTS - Factures standard
    autres_clients = [
        ("LEFEBVRE", 4.0, "Conseil juridique informatique - Juillet 2025"),
        ("PETRAS", 2.0, "Support utilisateurs - Assistance bureautique - Juillet 2025"),
        ("TOUZEAU", 1.5, "Maintenance informatique garage - Juillet 2025"),
        ("AXION", 7.0, "Support infrastructure réseau - Juillet 2025"),
        ("ART INFO", 2.0, "Maintenance système - Juillet 2025"),
        ("FARBOS", 1.5, "Support technique - Juillet 2025"),
        ("PDB", 4.0, "Audit sécurité HardenAD mairie - Juillet 2025"),
        ("QUADRIMEX", 15.0, "Refactoring packages SSIS - Migration SQL Server - Juillet 2025")
    ]
    
    print("\n📄 Autres clients")
    print("-" * 40)
    for client, hours, description in autres_clients:
        piece = create_piece(client, hours, description, "F", counter)
        newdataset.append(piece)
        config = clients_config.get(client, {"taux_horaire": 100})
        hours_rounded = apply_intelligent_rounding(hours)
        montant = hours_rounded * config['taux_horaire']
        print(f"  F#{counter}: {client} - {hours_rounded}h × {config['taux_horaire']}€ = {montant:.0f}€")
        counter += 1
        total_factures += 1
    
    # Convertir en string avec indentation
    xml_str = ET.tostring(dataset, encoding='unicode')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="    ", encoding='UTF-8')
    
    # Sauvegarder
    output_file = '/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/oxygen/2025-07/FACTURES_JUILLET_2025_FINAL.xml'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'wb') as f:
        f.write(pretty_xml)
    
    print("\n" + "=" * 60)
    print("✅ XML CORRIGÉ GÉNÉRÉ")
    print(f"📁 Fichier: {output_file}")
    print(f"📄 {total_factures} factures")
    print(f"📋 {total_devis} devis (UAI)")
    print("\n⚠️ IMPORTANT:")
    print("  - LAA : 4 factures séparées par catégorie ✓")
    print("  - UAI : 2 DEVIS (type D) et non factures ✓")
    print("  - Libellés professionnels détaillés ✓")
    print("  - Format virgule décimale français ✓")

if __name__ == "__main__":
    main()
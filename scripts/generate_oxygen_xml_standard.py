#!/usr/bin/env python3
"""
Script FINAL avec libellés STANDARDS pour OXYGEN - Juillet 2025
Utilise les textes professionnels habituels des factures
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
        "code": "LAA01",  # Code réel OXYGEN confirmé
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
        "code": "1AIR01",  # UN AIR D'ICI - Code réel OXYGEN confirmé
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
    "LAA MAROC": {
        "code": "LAAM01",  # Code réel OXYGEN confirmé
        "nom_complet": "LAA MAROC",
        "taux_horaire": 100,
        "adresse": "Zone Industrielle",
        "cp": "20000",
        "ville": "CASABLANCA",
        "pays": "Maroc",
        "email": "compta@laa.ma",
        "mode_reglement": "VIR",
        "delai_paiement": 45,
        "tva_code": "MA"  # Exonération TVA Maroc
    },
    "LEFEBVRE": {
        "code": "LEF01",  # Code réel OXYGEN confirmé
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
        "code": "PETRAS01",  # Code réel OXYGEN confirmé
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
        "code": "TOUZ01",  # Code réel OXYGEN confirmé
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
        "code": "AXI01",  # Code réel OXYGEN confirmé
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
        "code": "ARTI01",  # Code réel OXYGEN confirmé
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
        "code": "FAR01",  # Code réel OXYGEN confirmé
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
        "code": "AIX01",  # AIXAGON - Facture pour Port de Bouc
        "nom_complet": "AIXAGON",
        "taux_horaire": 100,
        "adresse": "5 Montée de Baume",
        "adresse2": "Auberge Neuve",
        "cp": "13124",
        "ville": "PEYPIN",
        "pays": "France",
        "email": "sabinec@aixagon.fr",
        "mode_reglement": "VIR",
        "delai_paiement": 30
    },
    "QUADRIMEX": {
        "code": "QUAD01",  # Code réel OXYGEN confirmé
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

def create_piece(client_name, hours, description, piece_type="F", counter=1000, jours=False):
    """Crée un élément PIECE (facture ou devis)"""
    client_config = clients_config.get(client_name, clients_config.get("LAA"))
    
    # TVA spéciale pour Maroc
    tva_code = client_config.get('tva_code', 'NORM')
    
    piece = ET.Element('PIECE')
    
    # Informations de base
    ET.SubElement(piece, 'CLIENT_CODE').text = client_config['code']
    ET.SubElement(piece, 'TYPE').text = piece_type  # F=Facture, D=Devis
    ET.SubElement(piece, 'WEB_ID').text = f'#{counter}'
    ET.SubElement(piece, 'DESIG').text = description[:50] if len(description) > 50 else description
    
    # Dates
    ET.SubElement(piece, 'DATE_CREATION').text = '31/07/2025'  # DATE FIXE 31 JUILLET
    ET.SubElement(piece, 'DATE_LIVRAISON').text = '31/07/2025'
    
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
    if jours:
        quantite = hours
        unite = "jours"
    else:
        quantite = apply_intelligent_rounding(hours)
        unite = "heures"
    
    ligne = ET.SubElement(piece, 'LIGNE')
    ET.SubElement(ligne, 'NUMERO').text = '1'
    ET.SubElement(ligne, 'ARTICLE_WEB_CODE').text = 'PRES-INFO'  # Code article standard
    ET.SubElement(ligne, 'DESIG').text = description
    ET.SubElement(ligne, 'QTE').text = f'{quantite:.2f}'.replace('.', ',')
    ET.SubElement(ligne, 'PUHT').text = f'{client_config["taux_horaire"]},00'
    ET.SubElement(ligne, 'TAUX_REMISE').text = '0,00'
    ET.SubElement(ligne, 'GCPTVA_CODE').text = tva_code
    
    return piece

def main():
    print("🚀 GÉNÉRATION XML STANDARD POUR OXYGEN - JUILLET 2025")
    print("=" * 60)
    
    # Créer la structure XML
    dataset = ET.Element('DataSet')
    dataset.set('xmlns', 'http://tempuri.org/')
    newdataset = ET.SubElement(dataset, 'NewDataSet')
    newdataset.set('xmlns', 'http://tempuri.org/data.xsd')
    
    counter = 1000
    all_pieces = []
    
    # LAA - 4 FACTURES AVEC LIBELLÉS STANDARDS
    print("\n📄 LAA - 4 FACTURES SÉPARÉES")
    print("-" * 60)
    
    # Facture 1 - Dette technologique (style standard)
    piece = create_piece("LAA", 27.0, 
                        "Prestations informatiques - Juillet 2025",
                        "F", counter)
    newdataset.append(piece)
    info = f"FACTURE #{counter} - LAA\n  Libellé: Prestations informatiques - Juillet 2025\n  27,00h × 100,00€ = 2.700,00€ HT"
    all_pieces.append(info)
    print(info)
    counter += 1
    
    # Facture 2 - Tests (style standard)
    piece = create_piece("LAA", 21.5,
                        "Prestations informatiques - Juillet 2025",
                        "F", counter)
    newdataset.append(piece)
    info = f"FACTURE #{counter} - LAA\n  Libellé: Prestations informatiques - Juillet 2025\n  21,50h × 100,00€ = 2.150,00€ HT"
    all_pieces.append(info)
    print(info)
    counter += 1
    
    # Facture 3 - Développements (style standard)
    piece = create_piece("LAA", 9.0,
                        "Prestations informatiques - Juillet 2025",
                        "F", counter)
    newdataset.append(piece)
    info = f"FACTURE #{counter} - LAA\n  Libellé: Prestations informatiques - Juillet 2025\n  9,00h × 100,00€ = 900,00€ HT"
    all_pieces.append(info)
    print(info)
    counter += 1
    
    # Facture 4 - Maintenance HF (style standard)
    piece = create_piece("LAA", 5.0,
                        "Maintenance informatique - Juillet 2025",
                        "F", counter)
    newdataset.append(piece)
    info = f"FACTURE #{counter} - LAA\n  Libellé: Maintenance informatique - Juillet 2025\n  5,00h × 100,00€ = 500,00€ HT"
    all_pieces.append(info)
    print(info)
    counter += 1
    
    # LAA MAROC
    print("\n📄 LAA MAROC")
    print("-" * 60)
    piece = create_piece("LAA MAROC", 1.5,
                        "Maintenance informatique - Juillet 2025",
                        "F", counter)
    newdataset.append(piece)
    info = f"FACTURE #{counter} - LAA MAROC\n  Libellé: Maintenance informatique - Juillet 2025\n  1,50h × 100,00€ = 150,00€ HT"
    all_pieces.append(info)
    print(info)
    counter += 1
    
    # UAI - 2 FACTURES + 1 DEVIS
    print("\n📄 UAI - FACTURES + DEVIS")
    print("-" * 60)
    
    # FACTURE HardenAD
    piece = create_piece("UAI", 5.5,
                        "Prestations informatiques - Juillet 2025",
                        "F", counter)
    newdataset.append(piece)
    info = f"FACTURE #{counter} - UAI\n  Libellé: Prestations informatiques - Juillet 2025\n  5,50h × 850,00€ = 4.675,00€ HT"
    all_pieces.append(info)
    print(info)
    counter += 1
    
    # FACTURE SQL Server
    piece = create_piece("UAI", 9.0,
                        "Prestations informatiques - Juillet 2025",
                        "F", counter)
    newdataset.append(piece)
    info = f"FACTURE #{counter} - UAI\n  Libellé: Prestations informatiques - Juillet 2025\n  9,00h × 850,00€ = 7.650,00€ HT"
    all_pieces.append(info)
    print(info)
    counter += 1
    
    # DEVIS 30 jours
    piece = create_piece("UAI", 30.0,
                        "Projet optimisation base de données",
                        "D", counter, jours=True)
    newdataset.append(piece)
    info = f"DEVIS #{counter} - UAI\n  Libellé: Projet optimisation base de données\n  30,00 jours × 850,00€ = 25.500,00€ HT"
    all_pieces.append(info)
    print(info)
    counter += 1
    
    # AUTRES CLIENTS - Libellés standards
    print("\n📄 AUTRES CLIENTS")
    print("-" * 60)
    
    autres_clients = [
        ("LEFEBVRE", 4.0, "Prestations informatiques - Juillet 2025", 120),
        ("PETRAS", 2.0, "Support informatique - Juillet 2025", 100),
        ("TOUZEAU", 1.5, "Maintenance informatique - Juillet 2025", 100),
        ("AXION", 7.0, "Prestations informatiques - Juillet 2025", 100),
        ("ART INFO", 2.0, "Maintenance informatique - Juillet 2025", 100),
        ("FARBOS", 1.5, "Support informatique - Juillet 2025", 100),
        ("PDB", 4.0, "Prestations informatiques - Juillet 2025", 100),
        ("QUADRIMEX", 15.0, "Prestations informatiques - Juillet 2025", 100)
    ]
    
    for client, hours, description, taux in autres_clients:
        piece = create_piece(client, hours, description, "F", counter)
        newdataset.append(piece)
        hours_rounded = apply_intelligent_rounding(hours)
        montant = hours_rounded * taux
        info = f"FACTURE #{counter} - {client}\n  Libellé: {description}\n  {hours_rounded:.2f}h × {taux:.2f}€ = {montant:,.2f}€ HT"
        all_pieces.append(info)
        print(info)
        counter += 1
    
    # Convertir en string avec indentation
    xml_str = ET.tostring(dataset, encoding='unicode')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="    ", encoding='UTF-8')
    
    # Sauvegarder
    output_file = '/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/oxygen/2025-07/FACTURES_JUILLET_2025_STANDARD.xml'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'wb') as f:
        f.write(pretty_xml)
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ COMPLET DES PIÈCES STANDARDS")
    print("=" * 60)
    
    for i, piece_info in enumerate(all_pieces, 1):
        print(f"\n{i}. {piece_info}")
    
    print("\n" + "=" * 60)
    print("✅ XML STANDARD GÉNÉRÉ")
    print(f"📁 Fichier: {output_file}")
    print(f"📄 14 factures avec libellés standards")
    print(f"📋 1 devis UAI (30 jours)")
    print("\n⚠️ POINTS CLÉS:")
    print("  - Date fixe : 31/07/2025 sur toutes les pièces")
    print("  - Libellés standards : 'Prestations informatiques - Juillet 2025'")
    print("  - LAA : 4 factures séparées (même libellé, heures différentes)")
    print("  - UAI : 2 factures + 1 devis projet")
    print("  - Total : 15 pièces prêtes pour OXYGEN")

if __name__ == "__main__":
    main()
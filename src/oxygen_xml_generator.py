#!/usr/bin/env python3
"""
Générateur XML pour import dans MemSoft OXYGEN
Format XML natif pour import direct des factures
Partie 2B/5 du système de facturation automatisée
"""

import os
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import argparse
from datetime import datetime
from typing import Dict, List, Any


class OxygenXMLGenerator:
    """Génère le XML pour import direct dans OXYGEN"""
    
    def __init__(self, config_file: str = None):
        """Initialisation avec configuration des clients"""
        self.config_file = config_file or "config/clients_mapping.json"
        self.clients_config = self._load_clients_config()
        self.piece_counter = 1000  # Numéro de départ pour WEB_ID
    
    def _load_clients_config(self) -> Dict:
        """Charge la configuration des clients"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Configuration par défaut avec toutes les infos pour OXYGEN
            return {
                "LAA": {
                    "code": "LAA01",
                    "nom_complet": "Les Artisans de l'Automobile",
                    "taux_horaire": 100,
                    "adresse": "Zone Industrielle",
                    "adresse2": "",
                    "cp": "13100",
                    "ville": "AIX-EN-PROVENCE",
                    "pays": "France",
                    "tel": "0442000000",
                    "email": "comptabilite@laa.fr",
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
                    "tel": "0147000000",
                    "email": "factures@uai.fr",
                    "mode_reglement": "VIR",
                    "delai_paiement": 45
                },
                "PROVENCALE": {
                    "code": "PROV01",
                    "nom_complet": "LA PROVENCALE SA",
                    "taux_horaire": 900,
                    "adresse": "29 Avenue Frédéric MISTRAL",
                    "adresse2": "",
                    "cp": "83170",
                    "ville": "BRIGNOLES",
                    "pays": "France",
                    "tel": "0494000000",
                    "email": "comptabilite@provencale.fr",
                    "mode_reglement": "VIR",
                    "delai_paiement": 30
                },
                "PHARMABEST": {
                    "code": "PHAR01",
                    "nom_complet": "PHARMABEST",
                    "taux_horaire": 100,
                    "adresse": "Parc Technologique",
                    "adresse2": "Bâtiment Innovation",
                    "cp": "06560",
                    "ville": "SOPHIA ANTIPOLIS",
                    "pays": "France",
                    "tel": "0493000000",
                    "email": "compta@pharmabest.fr",
                    "mode_reglement": "CHQ",
                    "delai_paiement": 30
                },
                "DEFAULT": {
                    "code": "DIV01",
                    "nom_complet": "Client",
                    "taux_horaire": 100,
                    "adresse": "Adresse",
                    "cp": "00000",
                    "ville": "VILLE",
                    "pays": "France",
                    "mode_reglement": "VIR",
                    "delai_paiement": 30
                }
            }
    
    def load_clockify_data(self, input_file: str) -> Dict:
        """Charge les données extraites de Clockify"""
        with open(input_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def apply_intelligent_rounding(self, hours: float) -> float:
        """
        Applique l'arrondi intelligent SYAGA
        <5h : arrondi supérieur au 0.5
        >=5h : arrondi inférieur au 0.5
        """
        if hours < 5:
            return round(hours * 2 + 0.49) / 2
        else:
            return round(hours * 2 - 0.49) / 2
    
    def create_xml_structure(self) -> ET.Element:
        """Crée la structure XML de base"""
        # Root DataSet
        dataset = ET.Element('DataSet')
        dataset.set('xmlns', 'http://tempuri.org/')
        
        # NewDataSet
        newdataset = ET.SubElement(dataset, 'NewDataSet')
        newdataset.set('xmlns', 'http://tempuri.org/data.xsd')
        
        return dataset, newdataset
    
    def create_piece_element(self, client_name: str, client_data: Dict, 
                            period: str, newdataset: ET.Element):
        """Crée un élément PIECE (facture) pour un client"""
        
        # Récupérer la config du client
        client_config = self.clients_config.get(
            client_name,
            self.clients_config.get('DEFAULT')
        )
        
        # Créer l'élément PIECE
        piece = ET.SubElement(newdataset, 'PIECE')
        
        # Informations de base
        ET.SubElement(piece, 'CLIENT_CODE').text = client_config['code']
        ET.SubElement(piece, 'TYPE').text = 'F'  # F pour Facture
        ET.SubElement(piece, 'WEB_ID').text = f'#{self.piece_counter}'
        self.piece_counter += 1
        
        # Description générale
        ET.SubElement(piece, 'DESIG').text = f'Prestations {period}'
        
        # Dates
        today = datetime.now().strftime('%d/%m/%Y')
        ET.SubElement(piece, 'DATE_CREATION').text = today
        ET.SubElement(piece, 'DATE_LIVRAISON').text = today
        
        # Conditions commerciales
        ET.SubElement(piece, 'TAUX_REMISE').text = '0.00'
        ET.SubElement(piece, 'TAUX_ESCOMPTE').text = '0.00'
        ET.SubElement(piece, 'GCPREG_CODE').text = client_config.get('mode_reglement', 'VIR')
        ET.SubElement(piece, 'PORT_HT').text = '0.00'
        ET.SubElement(piece, 'FRAIS_HT').text = '0.00'
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
        
        # Adresse de livraison (même que facturation pour prestations de service)
        adresse_liv = ET.SubElement(piece, 'adresse')
        ET.SubElement(adresse_liv, 'STYPE').text = 'livraison'
        ET.SubElement(adresse_liv, 'NOM').text = client_config['nom_complet']
        ET.SubElement(adresse_liv, 'ADRESSE').text = client_config.get('adresse', '')
        ET.SubElement(adresse_liv, 'CP').text = client_config.get('cp', '')
        ET.SubElement(adresse_liv, 'VILLE').text = client_config.get('ville', '')
        ET.SubElement(adresse_liv, 'PAYS').text = client_config.get('pays', 'France')
        
        # Ajouter les lignes de facturation
        self._add_invoice_lines(piece, client_name, client_data, period, client_config)
        
        return piece
    
    def _add_invoice_lines(self, piece: ET.Element, client_name: str, 
                          client_data: Dict, period: str, client_config: Dict):
        """Ajoute les lignes de facturation à une PIECE"""
        
        line_number = 1
        
        # Si le client a plusieurs catégories
        if client_data.get('categories'):
            for category, hours in client_data['categories'].items():
                if hours > 0:
                    hours_rounded = self.apply_intelligent_rounding(hours)
                    
                    # Créer une ligne
                    ligne = ET.SubElement(piece, 'LIGNE')
                    ET.SubElement(ligne, 'NUMERO').text = str(line_number)
                    
                    # Code article pour prestations de service
                    if 'dette' in category.lower():
                        code_article = 'PRES-DETTE'
                        designation = f'Dette technologique - {period}'
                    elif 'test' in category.lower():
                        code_article = 'PRES-TEST'
                        designation = f'Tests infrastructure - {period}'
                    elif 'develop' in category.lower():
                        code_article = 'PRES-DEV'
                        designation = f'Développements - {period}'
                    elif 'sql' in category.lower():
                        code_article = 'PRES-SQL'
                        designation = f'Prestations SQL Server - {period}'
                    elif 'migrat' in category.lower():
                        code_article = 'PRES-MIG'
                        designation = f'Migration infrastructure - {period}'
                    else:
                        code_article = 'PRES-HF'
                        designation = f'Maintenance hors forfait - {period}'
                    
                    ET.SubElement(ligne, 'ARTICLE_WEB_CODE').text = code_article
                    ET.SubElement(ligne, 'DESIG').text = designation
                    ET.SubElement(ligne, 'QTE').text = f'{hours_rounded:.2f}'
                    ET.SubElement(ligne, 'PUHT').text = str(client_config['taux_horaire'])
                    ET.SubElement(ligne, 'TAUX_REMISE').text = '0.00'
                    ET.SubElement(ligne, 'GCPTVA_CODE').text = 'NORM'  # TVA normale 20%
                    
                    line_number += 1
        else:
            # Une seule ligne pour tout
            hours = client_data.get('total_hours', 0)
            if hours > 0:
                hours_rounded = self.apply_intelligent_rounding(hours)
                
                ligne = ET.SubElement(piece, 'LIGNE')
                ET.SubElement(ligne, 'NUMERO').text = str(line_number)
                ET.SubElement(ligne, 'ARTICLE_WEB_CODE').text = 'PRES-HF'
                ET.SubElement(ligne, 'DESIG').text = f'Prestations {period}'
                ET.SubElement(ligne, 'QTE').text = f'{hours_rounded:.2f}'
                ET.SubElement(ligne, 'PUHT').text = str(client_config['taux_horaire'])
                ET.SubElement(ligne, 'TAUX_REMISE').text = '0.00'
                ET.SubElement(ligne, 'GCPTVA_CODE').text = 'NORM'
    
    def generate_xml(self, clockify_data: Dict, output_file: str, period: str = None):
        """Génère le fichier XML pour OXYGEN"""
        
        # Déterminer la période
        if not period:
            period = clockify_data.get('period', datetime.now().strftime('%Y-%m'))
        
        # Formater la période pour l'affichage
        year, month = period.split('-')
        months_fr = {
            '01': 'Janvier', '02': 'Février', '03': 'Mars',
            '04': 'Avril', '05': 'Mai', '06': 'Juin',
            '07': 'Juillet', '08': 'Août', '09': 'Septembre',
            '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'
        }
        period_display = f"{months_fr.get(month, month)} {year}"
        
        # Créer la structure XML
        dataset, newdataset = self.create_xml_structure()
        
        # Ajouter une PIECE pour chaque client
        total_factures = 0
        total_montant = 0
        
        for client_name, client_data in clockify_data.get('clients', {}).items():
            if client_data.get('total_hours', 0) > 0:
                self.create_piece_element(client_name, client_data, period_display, newdataset)
                total_factures += 1
                
                # Calculer le montant
                client_config = self.clients_config.get(
                    client_name,
                    self.clients_config.get('DEFAULT')
                )
                hours = self.apply_intelligent_rounding(client_data['total_hours'])
                montant = hours * client_config['taux_horaire']
                total_montant += montant
        
        # Convertir en string avec indentation
        xml_str = ET.tostring(dataset, encoding='unicode')
        
        # Formatter avec minidom pour une meilleure lisibilité
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="    ", encoding='UTF-8')
        
        # Écrire dans le fichier
        with open(output_file, 'wb') as f:
            f.write(pretty_xml)
        
        print(f"✅ XML généré: {output_file}")
        print(f"   {total_factures} factures")
        print(f"   Montant total HT: {total_montant:,.0f}€")
        print(f"   TVA (20%): {total_montant * 0.2:,.0f}€")
        print(f"   Total TTC: {total_montant * 1.2:,.0f}€")
        
        # Instructions pour OXYGEN
        print("\n📝 IMPORT DANS OXYGEN:")
        print("-" * 60)
        print("1. Ouvrir MemSoft OXYGEN")
        print("2. Menu: Outils → Import → Import XML")
        print(f"3. Sélectionner: {output_file}")
        print("4. Type de document: Factures")
        print("5. Valider l'import")
        print("6. Les factures sont créées avec numérotation automatique")
        
        return total_factures


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description='Générateur XML pour import OXYGEN'
    )
    parser.add_argument('--input', type=str, required=True,
                      help='Fichier JSON Clockify en entrée')
    parser.add_argument('--output', type=str,
                      help='Fichier XML de sortie')
    parser.add_argument('--config', type=str,
                      help='Fichier de configuration clients')
    
    args = parser.parse_args()
    
    # Définir le fichier de sortie par défaut
    if not args.output:
        base_name = os.path.basename(args.input).replace('.json', '')
        args.output = f"data/oxygen/import_{base_name}.xml"
    
    # Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Générer le XML
    try:
        generator = OxygenXMLGenerator(args.config)
        clockify_data = generator.load_clockify_data(args.input)
        generator.generate_xml(clockify_data, args.output)
        return 0
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
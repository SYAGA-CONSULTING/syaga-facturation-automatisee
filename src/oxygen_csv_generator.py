#!/usr/bin/env python3
"""
Générateur de CSV pour import dans MemSoft OXYGEN
Partie 2/5 du système de facturation automatisée
"""

import os
import json
import csv
import argparse
from datetime import datetime
from typing import Dict, List, Any


class OxygenCSVGenerator:
    """Génère le CSV pour import dans OXYGEN"""
    
    def __init__(self, config_file: str = None):
        """Initialisation avec configuration des clients"""
        self.config_file = config_file or "config/clients_mapping.json"
        self.clients_config = self._load_clients_config()
        self.invoice_lines = []
    
    def _load_clients_config(self) -> Dict:
        """Charge la configuration des clients"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Configuration par défaut
            return {
                "LAA": {
                    "code": "LAA01",
                    "nom_complet": "Les Artisans de l'Automobile",
                    "taux_horaire": 100,
                    "adresse": "Zone Industrielle\n13100 AIX-EN-PROVENCE"
                },
                "UAI": {
                    "code": "UAI01", 
                    "nom_complet": "Union des Assurances Immobilières",
                    "taux_horaire": 850,
                    "adresse": "Tour Défense\n92000 LA DEFENSE"
                },
                "PROVENCALE": {
                    "code": "PROV01",
                    "nom_complet": "LA PROVENCALE SA",
                    "taux_horaire": 900,
                    "adresse": "29 Avenue Frédéric MISTRAL\n40097 BRIGNOLES"
                },
                "PHARMABEST": {
                    "code": "PHAR01",
                    "nom_complet": "PHARMABEST",
                    "taux_horaire": 100,
                    "adresse": "Parc Technologique\n06560 SOPHIA ANTIPOLIS"
                },
                "QUADRIMEX": {
                    "code": "QUAD01",
                    "nom_complet": "QUADRIMEX",
                    "taux_horaire": 100,
                    "adresse": "Zone Industrielle\n13400 AUBAGNE"
                },
                "DEFAULT": {
                    "code": "DIV01",
                    "nom_complet": "Client",
                    "taux_horaire": 100,
                    "adresse": "France"
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
            # Arrondi supérieur
            return round(hours * 2 + 0.49) / 2
        else:
            # Arrondi inférieur
            return round(hours * 2 - 0.49) / 2
    
    def process_client_data(self, client_name: str, client_data: Dict, period: str):
        """Traite les données d'un client pour générer les lignes CSV"""
        
        # Récupérer la config du client
        client_config = self.clients_config.get(
            client_name, 
            self.clients_config.get('DEFAULT')
        )
        
        # Si le client a plusieurs catégories, créer une ligne par catégorie
        if client_data.get('categories'):
            for category, hours in client_data['categories'].items():
                if hours > 0:
                    hours_rounded = self.apply_intelligent_rounding(hours)
                    
                    # Déterminer le type de prestation
                    if 'dette' in category.lower():
                        description = f"Dette technologique - {period}"
                    elif 'test' in category.lower():
                        description = f"Tests infrastructure - {period}"
                    elif 'develop' in category.lower():
                        description = f"Développements - {period}"
                    elif 'sql' in category.lower():
                        description = f"Prestations SQL Server - {period}"
                    elif 'migrat' in category.lower():
                        description = f"Migration infrastructure - {period}"
                    else:
                        description = f"Maintenance hors forfait - {period}"
                    
                    self.invoice_lines.append({
                        'code_client': client_config['code'],
                        'nom_client': client_config['nom_complet'],
                        'description': description,
                        'quantite': hours_rounded,
                        'prix_unitaire': client_config['taux_horaire'],
                        'taux_tva': 20,
                        'montant_ht': hours_rounded * client_config['taux_horaire']
                    })
        else:
            # Une seule ligne pour le client
            hours = client_data.get('total_hours', 0)
            if hours > 0:
                hours_rounded = self.apply_intelligent_rounding(hours)
                
                self.invoice_lines.append({
                    'code_client': client_config['code'],
                    'nom_client': client_config['nom_complet'],
                    'description': f"Prestations {period}",
                    'quantite': hours_rounded,
                    'prix_unitaire': client_config['taux_horaire'],
                    'taux_tva': 20,
                    'montant_ht': hours_rounded * client_config['taux_horaire']
                })
    
    def generate_csv(self, clockify_data: Dict, output_file: str, period: str = None):
        """Génère le fichier CSV pour OXYGEN"""
        
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
        
        # Traiter chaque client
        for client_name, client_data in clockify_data.get('clients', {}).items():
            self.process_client_data(client_name, client_data, period_display)
        
        # Trier par client et description
        self.invoice_lines.sort(key=lambda x: (x['nom_client'], x['description']))
        
        # Écrire le CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Code_Client', 'Nom_Client', 'Description',
                'Quantite', 'Prix_Unitaire', 'Taux_TVA'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # En-tête
            writer.writeheader()
            
            # Lignes de facture
            for line in self.invoice_lines:
                writer.writerow({
                    'Code_Client': line['code_client'],
                    'Nom_Client': line['nom_client'],
                    'Description': line['description'],
                    'Quantite': f"{line['quantite']:.1f}",
                    'Prix_Unitaire': line['prix_unitaire'],
                    'Taux_TVA': line['taux_tva']
                })
        
        print(f"✅ CSV généré: {output_file}")
        print(f"   {len(self.invoice_lines)} lignes de facturation")
        
        # Afficher le résumé
        self._display_summary()
        
        return self.invoice_lines
    
    def _display_summary(self):
        """Affiche un résumé des factures à générer"""
        print("\n📊 RÉSUMÉ DES FACTURES À GÉNÉRER:")
        print("-" * 60)
        
        # Grouper par client
        clients_summary = {}
        for line in self.invoice_lines:
            client = line['nom_client']
            if client not in clients_summary:
                clients_summary[client] = {
                    'lignes': 0,
                    'heures': 0,
                    'montant': 0
                }
            clients_summary[client]['lignes'] += 1
            clients_summary[client]['heures'] += line['quantite']
            clients_summary[client]['montant'] += line['montant_ht']
        
        # Afficher par client
        total_general = 0
        for client, data in sorted(clients_summary.items()):
            print(f"\n{client}:")
            print(f"  • {data['lignes']} ligne(s) de facturation")
            print(f"  • {data['heures']:.1f} heures")
            print(f"  • {data['montant']:,.0f}€ HT")
            total_general += data['montant']
        
        print("-" * 60)
        print(f"TOTAL GÉNÉRAL: {total_general:,.0f}€ HT")
        print(f"TVA (20%): {total_general * 0.2:,.0f}€")
        print(f"TOTAL TTC: {total_general * 1.2:,.0f}€")
        
        # Instructions pour OXYGEN
        print("\n📝 PROCHAINES ÉTAPES:")
        print("-" * 60)
        print("1. Ouvrir MemSoft OXYGEN")
        print("2. Menu: Factures → Import → CSV")
        print(f"3. Sélectionner le fichier CSV généré")
        print("4. Paramètres d'import:")
        print("   • Série: F2025")
        print("   • TVA: 20%")
        print("   • Date facturation: Date du jour")
        print("5. Générer les factures")
        print("6. Export PDF vers le dossier Factures")


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description='Générateur CSV pour import OXYGEN'
    )
    parser.add_argument('--input', type=str, required=True,
                      help='Fichier JSON Clockify en entrée')
    parser.add_argument('--output', type=str,
                      help='Fichier CSV de sortie')
    parser.add_argument('--config', type=str,
                      help='Fichier de configuration clients')
    
    args = parser.parse_args()
    
    # Définir le fichier de sortie par défaut
    if not args.output:
        # Extraire la période du nom de fichier d'entrée
        base_name = os.path.basename(args.input).replace('.json', '')
        args.output = f"data/oxygen/import_{base_name}.csv"
    
    # Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Générer le CSV
    try:
        generator = OxygenCSVGenerator(args.config)
        clockify_data = generator.load_clockify_data(args.input)
        generator.generate_csv(clockify_data, args.output)
        return 0
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
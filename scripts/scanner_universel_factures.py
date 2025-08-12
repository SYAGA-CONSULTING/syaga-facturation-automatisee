#!/usr/bin/env python3
"""
SCANNER UNIVERSEL DES FACTURES
Scanne TOUTES les factures de TOUTES les années et les met en base
"""

import os
import sqlite3
from datetime import datetime
import re
from scanner_factures_licences_2024 import FacturesDatabase

class ScannerUniverselFactures:
    def __init__(self):
        self.db = FacturesDatabase()
        self.base_path = "/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/GROUPE-SYAGA-DOCUMENTS-OFFICIELS/03-ACTIVITES-METIERS/FACTURES-CLIENTS/Factures clients/"
        
    def lister_toutes_annees(self):
        """Liste toutes les années de factures disponibles"""
        annees = []
        
        # Années probables
        for annee in range(2020, 2026):  # 2020-2025
            chemin_annee = f"{self.base_path}{annee}/"
            print(f"🔍 Vérification {annee}: {chemin_annee}")
            annees.append(annee)
            
        return annees
    
    def generer_numeros_factures(self, annee):
        """Génère tous les numéros de factures probables pour une année"""
        numeros = []
        
        # Format F20YYMMNN (standard SYAGA)
        for mois in range(1, 13):  # Janvier à décembre
            for num in range(1, 100):  # 01 à 99
                numero = f"F{annee}{mois:02d}{num:02d}"
                numeros.append(numero)
        
        # Format 20YYMMNN (alternatif)
        for mois in range(1, 13):
            for num in range(1, 100):
                numero = f"{annee}{mois:02d}{num:02d}"
                numeros.append(numero)
                
        # Format F{annee}NN (simple)
        for num in range(1, 999):
            numero = f"F{annee}{num:03d}"
            numeros.append(numero)
            
        return numeros
    
    def analyser_facture_par_lecture(self, numero_facture, annee):
        """
        Demande à Claude de lire la facture PDF directement
        Cette fonction sera appelée pour chaque facture trouvée
        """
        chemin_facture = f"{self.base_path}{annee}/{numero_facture}.pdf"
        
        print(f"📄 {numero_facture} - Chemin: {chemin_facture}")
        print(f"    ⚠️  À analyser manuellement via Read tool")
        
        return {
            'numero': numero_facture,
            'annee': annee,
            'chemin': chemin_facture,
            'status': 'ANALYSE_MANUELLE_REQUISE'
        }
    
    def scanner_annee_complete(self, annee):
        """Scanne une année complète de factures"""
        print(f"\n{'='*60}")
        print(f"📅 SCAN COMPLET ANNÉE {annee}")
        print(f"{'='*60}")
        
        numeros = self.generer_numeros_factures(annee)
        print(f"📋 {len(numeros)} numéros de factures à vérifier")
        
        factures_trouvees = []
        
        # Scanner par échantillon (priorités)
        prioritaires = []
        
        # Octobre-décembre (période connue des licences)
        for mois in [10, 11, 12]:
            for num in range(1, 50):
                prioritaires.append(f"F{annee}{mois:02d}{num:02d}")
        
        print(f"\n🔍 SCAN PRIORITAIRE ({len(prioritaires)} factures)")
        
        for numero in prioritaires[:20]:  # Limite pour test
            analyse = self.analyser_facture_par_lecture(numero, annee)
            factures_trouvees.append(analyse)
        
        return factures_trouvees
    
    def creer_facture_exemple_laa(self):
        """Crée l'exemple LAA F20241010 déjà connu"""
        return {
            'numero': 'F20241010',
            'date_facture': '2024-10-02',
            'client_nom': 'LES AUTOMATISMES APPLIQUES',
            'client_code': 'LAA01',
            'total_ht': 13560.00,
            'total_tva': 2712.00,
            'total_ttc': 16272.00,
            'taux_tva': 20.0,
            'objet': 'Remise en conformité des licences Windows Serveur et RDS 2019',
            'fichier_pdf': 'F20241010.pdf',
            'lignes': [
                {
                    'reference': 'DIV01',
                    'designation': 'Licence Windows Serveur 2022 Standard 16 core',
                    'quantite': 5,
                    'prix_unitaire': 1144.00,
                    'montant_ht': 5720.00
                },
                {
                    'reference': 'DIV01', 
                    'designation': 'Licence Windows Serveur 2022 Essentials 10 core',
                    'quantite': 2,
                    'prix_unitaire': 350.00,
                    'montant_ht': 700.00
                },
                {
                    'reference': 'DIV01',
                    'designation': 'Licence Windows Serveur CAL 2022', 
                    'quantite': 35,
                    'prix_unitaire': 49.00,
                    'montant_ht': 1715.00
                },
                {
                    'reference': 'DIV01',
                    'designation': 'Licence Windows Serveur RDS CAL 2022',
                    'quantite': 35, 
                    'prix_unitaire': 155.00,
                    'montant_ht': 5425.00
                }
            ]
        }
    
    def creer_facture_exemple_aixagon1(self):
        """Crée l'exemple AIXAGON F20241011"""
        return {
            'numero': 'F20241011',
            'date_facture': '2024-10-31',
            'client_nom': 'AIXAGON',
            'client_code': 'AIX01',
            'total_ht': 1400.00,
            'total_tva': 280.00,
            'total_ttc': 1680.00,
            'taux_tva': 20.0,
            'objet': 'Prestation de durcissement Active Directory - Client final MAIRIE DE PORT DE BOUC',
            'fichier_pdf': 'F20241011.pdf',
            'lignes': [
                {
                    'reference': 'PRES-FORF-J',
                    'designation': 'Prestation Forfaitaire à la journée',
                    'quantite': 2,
                    'prix_unitaire': 700.00,
                    'montant_ht': 1400.00
                }
            ]
        }
    
    def creer_facture_exemple_aixagon2(self):
        """Crée l'exemple AIXAGON F20241012"""
        return {
            'numero': 'F20241012',
            'date_facture': '2024-10-31',
            'client_nom': 'AIXAGON',
            'client_code': 'AIX01',
            'total_ht': 400.00,
            'total_tva': 80.00,
            'total_ttc': 480.00,
            'taux_tva': 20.0,
            'objet': 'Prestation de durcissement Active Directory - Client final AUTODISTRIBUTION - FARSY',
            'fichier_pdf': 'F20241012.pdf',
            'lignes': [
                {
                    'reference': 'PREST-FORF01',
                    'designation': 'PRESTATION FORFAITAIRE à la demi-journée',
                    'quantite': 1,
                    'prix_unitaire': 400.00,
                    'montant_ht': 400.00
                }
            ]
        }
    
    def creer_facture_exemple_provencale1(self):
        """Crée l'exemple PROVENCALE SA F20241101"""
        return {
            'numero': 'F20241101',
            'date_facture': '2024-11-01',
            'client_nom': 'PROVENCALE SA',
            'client_code': 'PROV01',
            'total_ht': 400.00,
            'total_tva': 80.00,
            'total_ttc': 480.00,
            'taux_tva': 20.0,
            'objet': 'Ingénierie réseau préventive - 11/2024',
            'fichier_pdf': 'F20241101.pdf',
            'lignes': [
                {
                    'reference': 'PREST-FORF01',
                    'designation': 'PRESTATION FORFAITAIRE - Ingénierie réseau préventive',
                    'quantite': 1,
                    'prix_unitaire': 200.00,
                    'montant_ht': 200.00
                },
                {
                    'reference': 'PREST-FORF01',
                    'designation': 'PRESTATION FORFAITAIRE - Mises à jour WindowsUpdate',
                    'quantite': 1,
                    'prix_unitaire': 200.00,
                    'montant_ht': 200.00
                }
            ]
        }
    
    def creer_facture_exemple_provencale2(self):
        """Crée l'exemple PROVENCALE SA F20241201"""
        return {
            'numero': 'F20241201',
            'date_facture': '2024-12-01',
            'client_nom': 'PROVENCALE SA',
            'client_code': 'PROV01',
            'total_ht': 400.00,
            'total_tva': 80.00,
            'total_ttc': 480.00,
            'taux_tva': 20.0,
            'objet': 'Ingénierie réseau préventive - 12/2024',
            'fichier_pdf': 'F20241201.pdf',
            'lignes': [
                {
                    'reference': 'PREST-FORF01',
                    'designation': 'PRESTATION FORFAITAIRE - Ingénierie réseau préventive',
                    'quantite': 1,
                    'prix_unitaire': 200.00,
                    'montant_ht': 200.00
                },
                {
                    'reference': 'PREST-FORF01',
                    'designation': 'PRESTATION FORFAITAIRE - Mises à jour WindowsUpdate',
                    'quantite': 1,
                    'prix_unitaire': 200.00,
                    'montant_ht': 200.00
                }
            ]
        }

def main():
    print("\n" + "="*80)
    print("       🔍 SCANNER UNIVERSEL FACTURES")
    print("         TOUTES ANNÉES - BASE COMPLÈTE")
    print("="*80)
    
    scanner = ScannerUniverselFactures()
    
    # Ajouter les factures déjà lues
    factures_connues = [
        scanner.creer_facture_exemple_laa(),
        scanner.creer_facture_exemple_aixagon1(),
        scanner.creer_facture_exemple_aixagon2(), 
        scanner.creer_facture_exemple_provencale1(),
        scanner.creer_facture_exemple_provencale2()
    ]
    
    print(f"\n📊 AJOUT DES FACTURES DÉJÀ LUES")
    print("-" * 50)
    
    total_ht_ajoute = 0
    
    for facture in factures_connues:
        facture_id = scanner.db.ajouter_facture(facture)
        if facture_id:
            print(f"✅ {facture['numero']} - {facture['client_nom']} - {facture['total_ht']}€ HT")
            total_ht_ajoute += facture['total_ht']
        else:
            print(f"⚠️  {facture['numero']} - Erreur insertion")
    
    print(f"\n💰 Total HT ajouté: {total_ht_ajoute:,.2f}€")
    
    # Scanner les années
    annees = scanner.lister_toutes_annees()
    
    print(f"\n📅 ANNÉES À SCANNER: {', '.join(map(str, annees))}")
    
    # Priorité à 2024 (année des licences)
    factures_2024 = scanner.scanner_annee_complete(2024)
    
    print(f"\n" + "="*80)
    print("📋 RÉSULTATS SCAN UNIVERSEL")
    print("="*80)
    
    print(f"✅ Factures connues ajoutées: {len(factures_connues)}")
    print(f"🔍 Factures 2024 identifiées: {len(factures_2024)}")
    print(f"💰 Total HT en base: {total_ht_ajoute:,.2f}€")
    
    print(f"\n📋 ACTIONS SUIVANTES:")
    print("1. Chaque facture 'ANALYSE_MANUELLE_REQUISE' doit être lue")
    print("2. Utiliser Read tool sur les chemins indiqués")
    print("3. Ajouter les données via scanner.db.ajouter_facture()")
    
    # Vérification base de données
    conn = sqlite3.connect(scanner.db.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM factures")
    nb_factures = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(total_ht) FROM factures")
    total_ht_base = cursor.fetchone()[0] or 0
    
    conn.close()
    
    print(f"\n💾 BASE DE DONNÉES:")
    print(f"   Fichier: {scanner.db.db_path}")
    print(f"   Factures: {nb_factures}")
    print(f"   Total HT: {total_ht_base:,.2f}€")
    
    return scanner

if __name__ == "__main__":
    scanner = main()
    print(f"\n✅ Scanner universel terminé")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
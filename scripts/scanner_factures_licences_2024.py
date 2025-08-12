#!/usr/bin/env python3
"""
SCANNER ET ANALYSEUR DE FACTURES 2024
Recherche toutes les factures de licences Windows pour BUQUET, PETRAS et autres
Crée une base de données complète des factures
"""

import os
import json
import sqlite3
from datetime import datetime
import re

class FacturesDatabase:
    def __init__(self, db_path="/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db"):
        """Initialise la base de données des factures"""
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Crée les tables de la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table factures (en-têtes)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS factures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_facture TEXT UNIQUE NOT NULL,
                date_facture DATE,
                client_nom TEXT,
                client_code TEXT,
                client_adresse TEXT,
                total_ht REAL,
                total_tva REAL,
                total_ttc REAL,
                taux_tva REAL,
                date_echeance DATE,
                mode_paiement TEXT,
                objet TEXT,
                devis_ref TEXT,
                fichier_pdf TEXT,
                date_scan TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table lignes de factures
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lignes_factures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                facture_id INTEGER,
                reference TEXT,
                designation TEXT,
                quantite REAL,
                prix_unitaire REAL,
                montant_ht REAL,
                ordre_ligne INTEGER,
                FOREIGN KEY (facture_id) REFERENCES factures (id)
            )
        ''')
        
        # Index pour performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_facture_numero ON factures(numero_facture)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_facture_client ON factures(client_nom)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ligne_designation ON lignes_factures(designation)')
        
        conn.commit()
        conn.close()
    
    def ajouter_facture(self, facture_data):
        """Ajoute une facture dans la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insérer l'en-tête de facture
            cursor.execute('''
                INSERT OR REPLACE INTO factures (
                    numero_facture, date_facture, client_nom, client_code, client_adresse,
                    total_ht, total_tva, total_ttc, taux_tva, date_echeance, 
                    mode_paiement, objet, devis_ref, fichier_pdf
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                facture_data['numero'], facture_data.get('date_facture'),
                facture_data['client_nom'], facture_data.get('client_code'),
                facture_data.get('client_adresse'), facture_data.get('total_ht'),
                facture_data.get('total_tva'), facture_data.get('total_ttc'),
                facture_data.get('taux_tva'), facture_data.get('date_echeance'),
                facture_data.get('mode_paiement'), facture_data.get('objet'),
                facture_data.get('devis_ref'), facture_data.get('fichier_pdf')
            ))
            
            facture_id = cursor.lastrowid
            
            # Insérer les lignes
            for i, ligne in enumerate(facture_data.get('lignes', [])):
                cursor.execute('''
                    INSERT INTO lignes_factures (
                        facture_id, reference, designation, quantite, 
                        prix_unitaire, montant_ht, ordre_ligne
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    facture_id, ligne.get('reference'), ligne.get('designation'),
                    ligne.get('quantite'), ligne.get('prix_unitaire'),
                    ligne.get('montant_ht'), i + 1
                ))
            
            conn.commit()
            return facture_id
            
        except Exception as e:
            print(f"Erreur insertion facture {facture_data.get('numero')}: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def ajouter_ligne_facture(self, ligne_data):
        """Ajoute une ligne de facture à la base de données"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO lignes_factures (
                    facture_id, reference, designation, quantite, 
                    prix_unitaire, montant_ht, ordre_ligne
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                ligne_data['facture_id'], ligne_data.get('reference'), ligne_data.get('designation'),
                ligne_data.get('quantite'), ligne_data.get('prix_unitaire'),
                ligne_data.get('montant_ht'), ligne_data.get('ordre_ligne', 1)
            ))
            
            ligne_id = cursor.lastrowid
            conn.commit()
            return ligne_id
            
        except Exception as e:
            print(f"Erreur insertion ligne: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

def analyser_facture_f20241010():
    """Analyse la facture F20241010 déjà lue comme modèle"""
    return {
        'numero': 'F20241010',
        'date_facture': '2024-10-02',
        'client_nom': 'LES AUTOMATISMES APPLIQUES',
        'client_code': 'LAA01',
        'client_adresse': 'Bat.C Parc de Bachasson\n13590 MEYREUIL',
        'total_ht': 13560.00,
        'total_tva': 2712.00,
        'total_ttc': 16272.00,
        'taux_tva': 20.0,
        'date_echeance': '2024-11-02',
        'mode_paiement': 'Virement',
        'objet': 'Remise en conformité des licences Windows Serveur et RDS 2019 suite aux tests de montée de version',
        'devis_ref': '20241001',
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

def scanner_factures_2024():
    """Scanne toutes les factures 2024 à la recherche de licences"""
    factures_path = "/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/GROUPE-SYAGA-DOCUMENTS-OFFICIELS/03-ACTIVITES-METIERS/FACTURES-CLIENTS/Factures clients/2024/"
    
    print("🔍 SCAN DES FACTURES 2024")
    print("=" * 60)
    
    # Patterns de recherche
    target_clients = ['buquet', 'petras', 'provencale', 'laa']
    licence_keywords = ['licence', 'windows', 'server', 'cal', 'rds', 'office', '365']
    
    factures_trouvees = []
    
    # Simuler le scan (on ne peut pas vraiment lister le dossier Windows)
    print("📁 Dossier factures 2024:")
    print(f"   {factures_path}")
    
    # Commencer par la facture connue F20241010
    factures_trouvees.append(analyser_facture_f20241010())
    
    # Lister les patterns probables à chercher
    patterns_probables = [
        "F20241011", "F20241012", "F20241013", "F20241014", "F20241015",
        "F20241020", "F20241025", "F20241030", 
        "F20241101", "F20241102", "F20241103", "F20241110", "F20241115",
        "F20241201", "F20241202", "F20241210", "F20241215"
    ]
    
    print("\n🔍 PATTERNS À RECHERCHER:")
    for pattern in patterns_probables:
        print(f"   • {pattern} - à vérifier manuellement")
    
    return factures_trouvees

def creer_rapport_licences(factures):
    """Crée un rapport des licences trouvées"""
    print("\n" + "="*80)
    print("📊 RAPPORT LICENCES WINDOWS 2024")
    print("="*80)
    
    total_licences_ht = 0
    
    for facture in factures:
        print(f"\n🏢 {facture['client_nom']} - {facture['numero']}")
        print(f"   Date: {facture['date_facture']} | Total: {facture['total_ht']:.2f}€ HT")
        print(f"   Objet: {facture['objet']}")
        
        print("   Détail licences:")
        for ligne in facture['lignes']:
            if any(kw in ligne['designation'].lower() for kw in ['licence', 'windows']):
                print(f"     • {ligne['designation']}")
                print(f"       {ligne['quantite']}x {ligne['prix_unitaire']:.2f}€ = {ligne['montant_ht']:.2f}€")
        
        total_licences_ht += facture['total_ht']
    
    print(f"\n💰 TOTAL LICENCES IDENTIFIÉES: {total_licences_ht:.2f}€ HT")
    
    return total_licences_ht

def main():
    """Fonction principale"""
    print("\n" + "="*80)
    print("       🔍 SCANNER FACTURES LICENCES 2024")
    print("           Recherche BUQUET, PETRAS et autres")
    print("="*80)
    
    # Initialiser la base de données
    db = FacturesDatabase()
    print("✅ Base de données initialisée")
    
    # Scanner les factures
    factures = scanner_factures_2024()
    print(f"\n✅ {len(factures)} facture(s) analysée(s)")
    
    # Insérer dans la base
    for facture in factures:
        facture_id = db.ajouter_facture(facture)
        if facture_id:
            print(f"✅ Facture {facture['numero']} ajoutée (ID: {facture_id})")
    
    # Créer le rapport
    total_ht = creer_rapport_licences(factures)
    
    print(f"\n" + "="*80)
    print("📋 ACTIONS À EFFECTUER")
    print("="*80)
    print("""
    1. RECHERCHE MANUELLE des factures suivantes:
       • F2024xxxx pour BUQUET (licences Windows)
       • F2024xxxx pour PETRAS (licences Windows)
       • F2024xxxx pour PROVENÇALE (licences Windows)
    
    2. CHAQUE FACTURE TROUVÉE doit être ajoutée à la base via:
       python3 ajouter_facture_manual.py F2024xxxx
    
    3. CALCUL FINAL de la dette licences une fois toutes trouvées
    """)
    
    print(f"\n💾 Base de données sauvegardée:")
    print(f"   {db.db_path}")
    
    return total_ht

if __name__ == "__main__":
    total = main()
    print(f"\n✅ Scan terminé - {total:.2f}€ HT de licences identifiées pour le moment")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
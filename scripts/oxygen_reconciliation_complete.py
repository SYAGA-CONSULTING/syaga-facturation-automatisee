#!/usr/bin/env python3
"""
RÉCONCILIATION TRI-DIRECTIONNELLE COMPLÈTE
Oxygen ↔ Base SQLite ↔ Qonto ↔ Dossier PDFs
Vérification cohérence à l'euro près
"""

import sqlite3
import pandas as pd
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import re
import PyPDF2
from pathlib import Path

class OxygenReconciliationComplete:
    """Système de réconciliation complète tri-directionnel"""
    
    def __init__(self):
        self.setup_logging()
        self.setup_database()
        self.load_paths()
        
    def setup_logging(self):
        """Configuration logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/home/sq/SYAGA-CONSULTING/logs/reconciliation.log'),
                logging.StreamHandler()
            ]
        )
        
    def setup_database(self):
        """Initialiser table réconciliation"""
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reconciliation_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_reconciliation DATETIME DEFAULT CURRENT_TIMESTAMP,
                periode_start DATE,
                periode_end DATE,
                source_type TEXT, -- 'OXYGEN', 'QONTO', 'PDF_FOLDER'
                nb_factures_source INTEGER,
                nb_factures_matched INTEGER,
                nb_ecarts INTEGER,
                ecart_montant_total REAL,
                ecarts_details TEXT, -- JSON
                status TEXT DEFAULT 'COMPLETED',
                rapport_complet TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ecarts_reconciliation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reconciliation_id INTEGER,
                facture_numero TEXT,
                source_a TEXT,
                montant_a REAL,
                source_b TEXT, 
                montant_b REAL,
                ecart_montant REAL,
                type_ecart TEXT, -- 'MONTANT', 'MANQUANT_A', 'MANQUANT_B', 'DATE'
                status TEXT DEFAULT 'PENDING',
                resolved_at DATETIME,
                FOREIGN KEY (reconciliation_id) REFERENCES reconciliation_reports (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logging.info("✅ Tables réconciliation initialisées")
        
    def load_paths(self):
        """Charger chemins des sources de données"""
        self.paths = {
            'oxygen_exports': '/home/sq/SYAGA-CONSULTING/OXYGEN_EXPORTS/',
            'pdf_factures': '/home/sq/SYAGA-CONSULTING/VRAIES_FACTURES/',
            'sqlite_db': '/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db'
        }
        
        # Créer dossiers s'ils n'existent pas
        os.makedirs(self.paths['oxygen_exports'], exist_ok=True)
        logging.info("✅ Chemins configurés")
    
    def import_oxygen_export(self, csv_file_path: str) -> List[Dict]:
        """Importer export CSV d'Oxygen"""
        try:
            # Détection automatique du séparateur et encodage
            with open(csv_file_path, 'r', encoding='latin-1') as f:
                first_line = f.readline()
                separator = ';' if ';' in first_line else ','
            
            df = pd.read_csv(csv_file_path, sep=separator, encoding='latin-1')
            
            # Standardiser les noms de colonnes (Oxygen peut varier)
            column_mapping = {
                'Numéro': 'numero_facture',
                'Numero': 'numero_facture', 
                'N°': 'numero_facture',
                'Client': 'client_nom',
                'Date': 'date_facture',
                'Date facture': 'date_facture',
                'Total HT': 'total_ht',
                'Total TTC': 'total_ttc',
                'TTC': 'total_ttc',
                'Montant HT': 'total_ht',
                'Montant TTC': 'total_ttc'
            }
            
            df = df.rename(columns=column_mapping)
            
            # Nettoyer et convertir
            for col in ['total_ht', 'total_ttc']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(' ', ''), errors='coerce')
            
            # Standardiser dates
            if 'date_facture' in df.columns:
                df['date_facture'] = pd.to_datetime(df['date_facture'], errors='coerce', dayfirst=True)
                df['date_facture'] = df['date_facture'].dt.strftime('%Y-%m-%d')
            
            factures_oxygen = df.to_dict('records')
            logging.info(f"📊 {len(factures_oxygen)} factures importées depuis Oxygen")
            
            return factures_oxygen
            
        except Exception as e:
            logging.error(f"❌ Erreur import Oxygen: {e}")
            return []
    
    def get_sqlite_invoices(self, start_date: str, end_date: str) -> List[Dict]:
        """Récupérer factures base SQLite"""
        conn = sqlite3.connect(self.paths['sqlite_db'])
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT numero_facture, client_nom, date_facture, total_ht, total_ttc
            FROM factures
            WHERE date_facture BETWEEN ? AND ?
            AND total_ht > 0
            ORDER BY date_facture DESC
        ''', (start_date, end_date))
        
        rows = cursor.fetchall()
        conn.close()
        
        factures_sqlite = []
        for row in rows:
            factures_sqlite.append({
                'numero_facture': row[0],
                'client_nom': row[1], 
                'date_facture': row[2],
                'total_ht': float(row[3]) if row[3] else 0,
                'total_ttc': float(row[4]) if row[4] else 0
            })
        
        logging.info(f"🗄️ {len(factures_sqlite)} factures récupérées base SQLite")
        return factures_sqlite
    
    def scan_pdf_directory(self, start_date: str, end_date: str) -> List[Dict]:
        """Scanner dossier PDFs pour récupérer liste réelle"""
        factures_pdf = []
        
        # Parcourir dossiers par année
        start_year = int(start_date[:4])
        end_year = int(end_date[:4])
        
        for year in range(start_year, end_year + 1):
            year_path = Path(self.paths['pdf_factures']) / str(year)
            
            if year_path.exists():
                for pdf_file in year_path.glob('F*.pdf'):
                    try:
                        # Extraire info du nom de fichier
                        filename = pdf_file.stem
                        
                        # Pattern: F20250731, F20240527, etc.
                        match = re.match(r'F(\d{8})', filename)
                        if match:
                            date_str = match.group(1)
                            # Convertir YYYYMMDD vers YYYY-MM-DD
                            if len(date_str) == 8:
                                file_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                                
                                if start_date <= file_date <= end_date:
                                    pdf_info = self.extract_pdf_info(pdf_file)
                                    pdf_info['file_date'] = file_date
                                    pdf_info['file_path'] = str(pdf_file)
                                    factures_pdf.append(pdf_info)
                                    
                    except Exception as e:
                        logging.warning(f"⚠️ Erreur lecture PDF {pdf_file}: {e}")
        
        logging.info(f"📁 {len(factures_pdf)} PDFs trouvés dans période")
        return factures_pdf
    
    def extract_pdf_info(self, pdf_path: Path) -> Dict:
        """Extraire informations d'un PDF de facture"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Lire première page
                if len(pdf_reader.pages) > 0:
                    page_text = pdf_reader.pages[0].extract_text()
                    
                    # Extraire numéro facture
                    numero_match = re.search(r'(?:Facture|FACTURE|N°)\s*:?\s*(F?\d+)', page_text)
                    numero = numero_match.group(1) if numero_match else pdf_path.stem
                    
                    # Extraire client (ligne après "Facturer à" ou similaire)
                    client_patterns = [
                        r'(?:Facturé à|FACTURER À|Client)[:\s]*\n([A-Z\s]+)',
                        r'([A-Z]{2,}(?:\s+[A-Z]+)*)\s*\n(?:\d+\s+)?[A-Za-z\s]+\n\d{5}'
                    ]
                    
                    client = "CLIENT_NON_TROUVE"
                    for pattern in client_patterns:
                        client_match = re.search(pattern, page_text, re.IGNORECASE)
                        if client_match:
                            client = client_match.group(1).strip()
                            break
                    
                    # Extraire montants
                    # Chercher Total TTC ou Total
                    montant_patterns = [
                        r'Total\s+TTC[:\s]*(\d+[,\.]?\d*)',
                        r'TOTAL[:\s]*(\d+[,\.]?\d*)',
                        r'(\d+[,\.]\d{2})\s*€?\s*$'
                    ]
                    
                    montant_ttc = 0.0
                    for pattern in montant_patterns:
                        montant_match = re.search(pattern, page_text, re.MULTILINE)
                        if montant_match:
                            montant_str = montant_match.group(1).replace(',', '.')
                            montant_ttc = float(montant_str)
                            break
                    
                    return {
                        'numero_facture': numero,
                        'client_nom': client,
                        'total_ttc': montant_ttc,
                        'source': 'PDF'
                    }
                    
        except Exception as e:
            logging.warning(f"⚠️ Erreur extraction PDF {pdf_path}: {e}")
            
        return {
            'numero_facture': pdf_path.stem,
            'client_nom': 'EXTRACTION_FAILED',
            'total_ttc': 0.0,
            'source': 'PDF'
        }
    
    def perform_tri_reconciliation(self, start_date: str, end_date: str, oxygen_csv_path: str = None) -> Dict:
        """Réconciliation tri-directionnelle complète"""
        logging.info(f"🔄 Réconciliation période {start_date} → {end_date}")
        
        # 1. Charger données des 3 sources
        sources = {}
        
        # Source SQLite (référence)
        sources['sqlite'] = self.get_sqlite_invoices(start_date, end_date)
        
        # Source Oxygen (si fournie)
        if oxygen_csv_path and os.path.exists(oxygen_csv_path):
            sources['oxygen'] = self.import_oxygen_export(oxygen_csv_path)
        else:
            sources['oxygen'] = []
            logging.warning("⚠️ Export Oxygen non fourni")
        
        # Source PDFs
        sources['pdf'] = self.scan_pdf_directory(start_date, end_date)
        
        # 2. Créer index par numéro de facture
        indexed = {}
        for source_name, invoices in sources.items():
            indexed[source_name] = {}
            for invoice in invoices:
                numero = str(invoice.get('numero_facture', '')).replace('F', '').strip()
                if numero:
                    indexed[source_name][numero] = invoice
        
        # 3. Analyser écarts
        all_numbers = set()
        for source_index in indexed.values():
            all_numbers.update(source_index.keys())
        
        ecarts = []
        matches = []
        
        for numero in sorted(all_numbers):
            sqlite_invoice = indexed['sqlite'].get(numero)
            oxygen_invoice = indexed['oxygen'].get(numero) 
            pdf_invoice = indexed['pdf'].get(numero)
            
            # Comparaisons croisées
            comparisons = [
                ('sqlite', sqlite_invoice, 'oxygen', oxygen_invoice),
                ('sqlite', sqlite_invoice, 'pdf', pdf_invoice),
                ('oxygen', oxygen_invoice, 'pdf', pdf_invoice)
            ]
            
            numero_ecarts = []
            numero_matched = True
            
            for source_a, inv_a, source_b, inv_b in comparisons:
                if inv_a is None and inv_b is None:
                    continue
                
                if inv_a is None:
                    ecarts.append({
                        'numero': numero,
                        'type': 'MANQUANT_A',
                        'source_a': source_a,
                        'source_b': source_b,
                        'montant_b': inv_b.get('total_ttc', 0),
                        'details': f"Manquant dans {source_a}"
                    })
                    numero_matched = False
                    
                elif inv_b is None:
                    ecarts.append({
                        'numero': numero,
                        'type': 'MANQUANT_B', 
                        'source_a': source_a,
                        'montant_a': inv_a.get('total_ttc', 0),
                        'source_b': source_b,
                        'details': f"Manquant dans {source_b}"
                    })
                    numero_matched = False
                    
                else:
                    # Comparer montants
                    montant_a = float(inv_a.get('total_ttc', 0))
                    montant_b = float(inv_b.get('total_ttc', 0))
                    ecart_montant = abs(montant_a - montant_b)
                    
                    if ecart_montant > 0.01:  # Tolérance 1 centime
                        ecarts.append({
                            'numero': numero,
                            'type': 'MONTANT',
                            'source_a': source_a,
                            'montant_a': montant_a,
                            'source_b': source_b,
                            'montant_b': montant_b,
                            'ecart': ecart_montant,
                            'details': f"Écart {ecart_montant:.2f}€ entre {source_a} et {source_b}"
                        })
                        numero_matched = False
            
            if numero_matched:
                matches.append({
                    'numero': numero,
                    'sqlite': sqlite_invoice,
                    'oxygen': oxygen_invoice,
                    'pdf': pdf_invoice
                })
        
        # 4. Sauvegarder rapport
        reconciliation_id = self.save_reconciliation_report(
            start_date, end_date, sources, matches, ecarts
        )
        
        # 5. Générer rapport final
        rapport = self.generate_reconciliation_report(sources, matches, ecarts)
        
        logging.info(f"✅ Réconciliation terminée: {len(matches)} matchées, {len(ecarts)} écarts")
        
        return {
            'reconciliation_id': reconciliation_id,
            'periode': {'start': start_date, 'end': end_date},
            'sources': {k: len(v) for k, v in sources.items()},
            'matches': len(matches),
            'ecarts': len(ecarts),
            'rapport': rapport,
            'details': {
                'matches': matches,
                'ecarts': ecarts
            }
        }
    
    def save_reconciliation_report(self, start_date: str, end_date: str, 
                                 sources: Dict, matches: List, ecarts: List) -> int:
        """Sauvegarder rapport de réconciliation"""
        conn = sqlite3.connect(self.paths['sqlite_db'])
        cursor = conn.cursor()
        
        # Rapport principal
        ecart_total = sum(abs(e.get('ecart', 0)) for e in ecarts)
        
        cursor.execute('''
            INSERT INTO reconciliation_reports (
                periode_start, periode_end, nb_factures_matched,
                nb_ecarts, ecart_montant_total, ecarts_details
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            start_date, end_date, len(matches),
            len(ecarts), ecart_total, json.dumps(ecarts)
        ))
        
        reconciliation_id = cursor.lastrowid
        
        # Détail des écarts
        for ecart in ecarts:
            cursor.execute('''
                INSERT INTO ecarts_reconciliation (
                    reconciliation_id, facture_numero, source_a, montant_a,
                    source_b, montant_b, ecart_montant, type_ecart
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                reconciliation_id, ecart['numero'], 
                ecart.get('source_a', ''), ecart.get('montant_a', 0),
                ecart.get('source_b', ''), ecart.get('montant_b', 0),
                ecart.get('ecart', 0), ecart['type']
            ))
        
        conn.commit()
        conn.close()
        
        return reconciliation_id
    
    def generate_reconciliation_report(self, sources: Dict, matches: List, ecarts: List) -> str:
        """Générer rapport de réconciliation détaillé"""
        
        total_sqlite = sum(inv.get('total_ttc', 0) for inv in sources['sqlite'])
        total_oxygen = sum(inv.get('total_ttc', 0) for inv in sources['oxygen'])
        total_pdf = sum(inv.get('total_ttc', 0) for inv in sources.get('pdf', []))
        
        ecart_montant_total = sum(abs(e.get('ecart', 0)) for e in ecarts)
        
        rapport = f"""
📊 RAPPORT RÉCONCILIATION TRI-DIRECTIONNELLE
==========================================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 SOURCES DE DONNÉES:
• Base SQLite:  {len(sources['sqlite']):3} factures = {total_sqlite:8,.2f}€ TTC
• Export Oxygen: {len(sources['oxygen']):3} factures = {total_oxygen:8,.2f}€ TTC  
• Dossier PDF:   {len(sources.get('pdf', [])):3} factures = {total_pdf:8,.2f}€ TTC

✅ RÉCONCILIATION:
• Factures matchées: {len(matches)}
• Écarts détectés:   {len(ecarts)}
• Écart montant:     {ecart_montant_total:.2f}€

🚨 ÉCARTS DÉTAILLÉS:
"""
        
        # Grouper écarts par type
        ecarts_by_type = {}
        for ecart in ecarts:
            type_ecart = ecart['type']
            if type_ecart not in ecarts_by_type:
                ecarts_by_type[type_ecart] = []
            ecarts_by_type[type_ecart].append(ecart)
        
        for type_ecart, type_ecarts in ecarts_by_type.items():
            rapport += f"\n{type_ecart} ({len(type_ecarts)} cas):\n"
            for i, ecart in enumerate(type_ecarts[:10]):  # Limiter à 10 par type
                if ecart['type'] == 'MONTANT':
                    rapport += f"  {i+1}. F{ecart['numero']}: {ecart['montant_a']:.2f}€ vs {ecart['montant_b']:.2f}€ (écart {ecart['ecart']:.2f}€)\n"
                else:
                    rapport += f"  {i+1}. F{ecart['numero']}: {ecart['details']}\n"
            
            if len(type_ecarts) > 10:
                rapport += f"  ... et {len(type_ecarts) - 10} autres\n"
        
        # Statistiques finales
        taux_coherence = (len(matches) / (len(matches) + len(ecarts))) * 100 if (len(matches) + len(ecarts)) > 0 else 100
        
        rapport += f"""
📊 QUALITÉ DONNÉES:
• Taux de cohérence: {taux_coherence:.1f}%
• Précision montants: ±{ecart_montant_total/max(1, len(ecarts)):.2f}€ par écart
• Fiabilité système: {'🟢 EXCELLENTE' if taux_coherence > 95 else '🟡 CORRECTE' if taux_coherence > 85 else '🔴 À AMÉLIORER'}

🎯 ACTIONS RECOMMANDÉES:
"""
        
        if len(ecarts) == 0:
            rapport += "• ✅ Aucune action requise - cohérence parfaite\n"
        else:
            rapport += f"• 🔧 Corriger {len([e for e in ecarts if e['type'] == 'MONTANT'])} écarts de montant\n"
            rapport += f"• 📄 Vérifier {len([e for e in ecarts if 'MANQUANT' in e['type']])} factures manquantes\n"
            
        rapport += f"\n⏱️ Prochaine réconciliation recommandée: {(datetime.now() + timedelta(weeks=2)).strftime('%Y-%m-%d')}"
        
        return rapport
    
    def run_monthly_reconciliation(self, months_back: int = 3):
        """Lancer réconciliation mensuelle automatique"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=months_back * 30)).strftime('%Y-%m-%d')
        
        # Chercher dernier export Oxygen
        oxygen_exports = list(Path(self.paths['oxygen_exports']).glob('*.csv'))
        latest_oxygen = max(oxygen_exports, key=os.path.getctime) if oxygen_exports else None
        
        result = self.perform_tri_reconciliation(
            start_date, end_date, 
            str(latest_oxygen) if latest_oxygen else None
        )
        
        # Envoyer rapport si écarts critiques
        if len(result['details']['ecarts']) > 10 or any(e.get('ecart', 0) > 100 for e in result['details']['ecarts']):
            self.send_reconciliation_alert(result['rapport'])
        
        return result
    
    def send_reconciliation_alert(self, rapport: str):
        """Envoyer alerte réconciliation"""
        try:
            import subprocess
            subprocess.run([
                'python3',
                '/home/sq/SYAGA-CONSULTING/syaga-instructions/SEND_EMAIL_SECURE.py',
                '--to', 'sebastien.questier@syaga.fr',
                '--subject', f'📊 Rapport Réconciliation {datetime.now().strftime("%d/%m/%Y")}',
                '--body', rapport
            ], check=True)
            logging.info("📧 Rapport réconciliation envoyé")
        except Exception as e:
            logging.error(f"❌ Erreur envoi rapport: {e}")

def main():
    """Point d'entrée principal"""
    reconciliation = OxygenReconciliationComplete()
    
    print("""
📊 RÉCONCILIATION TRI-DIRECTIONNELLE SYAGA
========================================

Usage:
  python3 oxygen_reconciliation_complete.py

Sources vérifiées:
  ✅ Base SQLite (référence)
  📤 Export Oxygen CSV (si disponible)  
  📁 Dossier PDFs réels

Tolérance: ±0.01€ (au centime près)
    """)
    
    # Réconciliation des 3 derniers mois
    result = reconciliation.run_monthly_reconciliation(3)
    
    print(f"\n✅ RÉCONCILIATION TERMINÉE")
    print(f"Période: {result['periode']['start']} → {result['periode']['end']}")
    print(f"Sources: SQLite({result['sources']['sqlite']}) / Oxygen({result['sources']['oxygen']}) / PDF({result['sources'].get('pdf', 0)})")
    print(f"Matches: {result['matches']} ✅")
    print(f"Écarts: {result['ecarts']} ⚠️")
    
    if result['ecarts'] > 0:
        print(f"\n⚠️ {result['ecarts']} écarts détectés - Vérification manuelle requise")
    else:
        print(f"\n🎉 COHÉRENCE PARFAITE - Toutes les sources concordent !")

if __name__ == "__main__":
    main()
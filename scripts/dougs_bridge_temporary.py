#!/usr/bin/env python3
"""
BRIDGE TEMPORAIRE DOUGS - EN ATTENDANT L'API OFFICIELLE
Export CSV + Import assisté + Monitoring changements
"""

import sqlite3
import csv
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
from pathlib import Path
import requests

class DougsBridgeTemporary:
    """Bridge temporaire Dougs en attendant API officielle"""
    
    def __init__(self):
        self.setup_logging()
        self.setup_database()
        self.load_dougs_config()
        
    def setup_logging(self):
        """Configuration logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/home/sq/SYAGA-CONSULTING/logs/dougs_bridge.log'),
                logging.StreamHandler()
            ]
        )
        
    def setup_database(self):
        """Initialiser table bridge Dougs"""
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dougs_exports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                export_type TEXT, -- 'FACTURES', 'PAIEMENTS', 'ECRITURES'
                periode_start DATE,
                periode_end DATE,
                nb_lignes INTEGER,
                file_path TEXT,
                status TEXT DEFAULT 'GENERATED', -- 'GENERATED', 'IMPORTED', 'VALIDATED'
                export_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                import_date DATETIME,
                dougs_validation TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dougs_monitoring (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                check_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                solde_compte REAL,
                nb_ecritures INTEGER,
                last_ecriture_date DATE,
                status_sync TEXT, -- 'SYNCED', 'PENDING', 'ERROR'
                differences_detected TEXT -- JSON
            )
        ''')
        
        conn.commit()
        conn.close()
        logging.info("✅ Tables bridge Dougs initialisées")
        
    def load_dougs_config(self):
        """Configuration bridge Dougs"""
        self.config = {
            'export_path': '/home/sq/SYAGA-CONSULTING/DOUGS_EXPORTS/',
            'qonto_dougs_sync': True,  # Utiliser intégration existante
            'csv_format': 'FEC',  # Format Fichier Écritures Comptables
            'auto_import': False,  # Import manuel pour l'instant
            'monitoring_frequency': 'daily'
        }
        
        # Créer dossier exports
        Path(self.config['export_path']).mkdir(parents=True, exist_ok=True)
        logging.info("✅ Configuration bridge Dougs chargée")
    
    def export_factures_fec_format(self, start_date: str, end_date: str) -> str:
        """Exporter factures format FEC pour Dougs"""
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        
        # Récupérer factures période
        query = '''
            SELECT 
                numero_facture, date_facture, client_nom,
                total_ht, total_tva, total_ttc,
                objet, mode_paiement
            FROM factures
            WHERE date_facture BETWEEN ? AND ?
            AND total_ht > 0
            ORDER BY date_facture, numero_facture
        '''
        
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        
        if df.empty:
            logging.warning("⚠️ Aucune facture pour la période")
            return None
        
        # Convertir en format FEC (Fichier Écritures Comptables)
        fec_data = []
        
        for _, row in df.iterrows():
            # Écriture débit client (411)
            fec_data.append({
                'JournalCode': 'VTE',  # Journal ventes
                'JournalLib': 'Journal des ventes',
                'EcritureNum': row['numero_facture'],
                'EcritureDate': row['date_facture'],
                'CompteNum': '411000',  # Clients
                'CompteLib': f"Client - {row['client_nom']}",
                'CompAuxNum': row['client_nom'][:10].upper(),
                'CompAuxLib': row['client_nom'],
                'PieceRef': row['numero_facture'],
                'PieceDate': row['date_facture'],
                'EcritureLib': row['objet'][:100],
                'Debit': row['total_ttc'],
                'Credit': 0.00,
                'EcritureLet': '',
                'DateLet': '',
                'ValidDate': row['date_facture'],
                'Montantdevise': '',
                'Idevise': ''
            })
            
            # Écriture crédit vente (701)
            fec_data.append({
                'JournalCode': 'VTE',
                'JournalLib': 'Journal des ventes',
                'EcritureNum': row['numero_facture'],
                'EcritureDate': row['date_facture'],
                'CompteNum': '706000',  # Prestations de services
                'CompteLib': 'Prestations de services',
                'CompAuxNum': '',
                'CompAuxLib': '',
                'PieceRef': row['numero_facture'],
                'PieceDate': row['date_facture'],
                'EcritureLib': row['objet'][:100],
                'Debit': 0.00,
                'Credit': row['total_ht'],
                'EcritureLet': '',
                'DateLet': '',
                'ValidDate': row['date_facture'],
                'Montantdevise': '',
                'Idevise': ''
            })
            
            # Écriture crédit TVA (445)
            if row['total_tva'] > 0:
                fec_data.append({
                    'JournalCode': 'VTE',
                    'JournalLib': 'Journal des ventes',
                    'EcritureNum': row['numero_facture'],
                    'EcritureDate': row['date_facture'],
                    'CompteNum': '445710',  # TVA collectée
                    'CompteLib': 'TVA collectée',
                    'CompAuxNum': '',
                    'CompAuxLib': '',
                    'PieceRef': row['numero_facture'],
                    'PieceDate': row['date_facture'],
                    'EcritureLib': f"TVA 20% - {row['objet'][:80]}",
                    'Debit': 0.00,
                    'Credit': row['total_tva'],
                    'EcritureLet': '',
                    'DateLet': '',
                    'ValidDate': row['date_facture'],
                    'Montantdevise': '',
                    'Idevise': ''
                })
        
        # Sauvegarder CSV FEC
        fec_df = pd.DataFrame(fec_data)
        export_filename = f"SYAGA_FEC_Factures_{start_date}_{end_date}.csv"
        export_path = Path(self.config['export_path']) / export_filename
        
        # Format FEC avec séparateur pipe |
        fec_df.to_csv(export_path, sep='|', index=False, encoding='utf-8')
        
        # Enregistrer export
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO dougs_exports (
                export_type, periode_start, periode_end, nb_lignes, file_path
            ) VALUES (?, ?, ?, ?, ?)
        ''', ('FACTURES', start_date, end_date, len(fec_data), str(export_path)))
        
        conn.commit()
        conn.close()
        
        logging.info(f"✅ Export FEC généré: {export_filename} ({len(fec_data)} lignes)")
        return str(export_path)
    
    def export_paiements_fec_format(self, start_date: str, end_date: str) -> str:
        """Exporter paiements Qonto format FEC"""
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        
        # Récupérer paiements matchés période
        query = '''
            SELECT 
                pq.transaction_id, pq.date_transaction, pq.montant,
                pq.libelle, f.numero_facture, f.client_nom
            FROM paiements_qonto pq
            JOIN factures f ON pq.facture_id = f.id
            WHERE pq.date_transaction BETWEEN ? AND ?
            AND pq.status = 'MATCHED'
            ORDER BY pq.date_transaction
        '''
        
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        
        if df.empty:
            logging.warning("⚠️ Aucun paiement pour la période")
            return None
        
        # Convertir en format FEC
        fec_data = []
        
        for _, row in df.iterrows():
            # Écriture débit banque (512)
            fec_data.append({
                'JournalCode': 'BQ1',  # Journal banque
                'JournalLib': 'Journal de banque',
                'EcritureNum': row['transaction_id'],
                'EcritureDate': row['date_transaction'],
                'CompteNum': '512000',  # Banque
                'CompteLib': 'Banque',
                'CompAuxNum': '',
                'CompAuxLib': '',
                'PieceRef': row['transaction_id'],
                'PieceDate': row['date_transaction'],
                'EcritureLib': row['libelle'][:100],
                'Debit': row['montant'],
                'Credit': 0.00,
                'EcritureLet': '',
                'DateLet': '',
                'ValidDate': row['date_transaction'],
                'Montantdevise': '',
                'Idevise': ''
            })
            
            # Écriture crédit client (411) - Lettrage
            fec_data.append({
                'JournalCode': 'BQ1',
                'JournalLib': 'Journal de banque',
                'EcritureNum': row['transaction_id'],
                'EcritureDate': row['date_transaction'],
                'CompteNum': '411000',  # Clients
                'CompteLib': f"Client - {row['client_nom']}",
                'CompAuxNum': row['client_nom'][:10].upper(),
                'CompAuxLib': row['client_nom'],
                'PieceRef': row['transaction_id'],
                'PieceDate': row['date_transaction'],
                'EcritureLib': f"Règlement {row['numero_facture']}",
                'Debit': 0.00,
                'Credit': row['montant'],
                'EcritureLet': row['numero_facture'],  # Lettrage
                'DateLet': row['date_transaction'],
                'ValidDate': row['date_transaction'],
                'Montantdevise': '',
                'Idevise': ''
            })
        
        # Sauvegarder CSV FEC
        fec_df = pd.DataFrame(fec_data)
        export_filename = f"SYAGA_FEC_Paiements_{start_date}_{end_date}.csv"
        export_path = Path(self.config['export_path']) / export_filename
        
        fec_df.to_csv(export_path, sep='|', index=False, encoding='utf-8')
        
        # Enregistrer export
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO dougs_exports (
                export_type, periode_start, periode_end, nb_lignes, file_path
            ) VALUES (?, ?, ?, ?, ?)
        ''', ('PAIEMENTS', start_date, end_date, len(fec_data), str(export_path)))
        
        conn.commit()
        conn.close()
        
        logging.info(f"✅ Export paiements FEC généré: {export_filename}")
        return str(export_path)
    
    def generate_dougs_import_instructions(self, export_files: List[str]) -> str:
        """Générer instructions import manuel Dougs"""
        instructions = f"""
📋 INSTRUCTIONS IMPORT DOUGS - {datetime.now().strftime('%Y-%m-%d')}
============================================================

📁 FICHIERS GÉNÉRÉS:
"""
        
        for file_path in export_files:
            file_name = Path(file_path).name
            file_size = Path(file_path).stat().st_size // 1024
            instructions += f"• {file_name} ({file_size} KB)\n"
        
        instructions += f"""

🔧 PROCÉDURE IMPORT DOUGS:

1. CONNEXION DOUGS
   • Se connecter à l'interface Dougs
   • Aller dans "Comptabilité" > "Import"

2. SÉLECTION FICHIER FEC
   • Choisir "Import FEC" (Fichier Écritures Comptables)
   • Format: CSV avec séparateur |
   • Encodage: UTF-8

3. VALIDATION IMPORT
   • Vérifier mapping comptes automatique
   • Contrôler équilibre débit/crédit
   • Valider périodes comptables

4. CONTRÔLES POST-IMPORT
   • Balance client (compte 411)
   • Chiffre d'affaires (compte 706)
   • TVA collectée (compte 445710)
   • Trésorerie (compte 512)

🎯 POINTS DE CONTRÔLE:

✅ Factures émises période
✅ Paiements clients reçus  
✅ Lettrage automatique
✅ TVA déclarable
✅ Balance équilibrée

📞 SUPPORT DOUGS:
En cas de problème, contacter support Dougs avec:
• Fichiers FEC générés
• Période concernée  
• Messages d'erreur éventuels

🔄 AUTOMATISATION FUTURE:
Ces exports seront automatisés dès API Dougs disponible.
"""
        
        # Sauvegarder instructions
        instructions_path = Path(self.config['export_path']) / f"Instructions_Import_Dougs_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(instructions_path, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        return str(instructions_path)
    
    def monitor_qonto_dougs_sync(self) -> Dict:
        """Monitorer synchronisation Qonto → Dougs existante"""
        # Note: Utilise l'intégration Qonto → Dougs existante
        
        monitoring_result = {
            'sync_status': 'MONITORING',
            'last_check': datetime.now().isoformat(),
            'qonto_transactions': 0,
            'dougs_sync_status': 'UNKNOWN',
            'recommendations': []
        }
        
        try:
            # Vérifier transactions Qonto récentes
            conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) FROM paiements_qonto 
                WHERE date_transaction >= DATE('now', '-7 days')
            ''')
            recent_transactions = cursor.fetchone()[0]
            monitoring_result['qonto_transactions'] = recent_transactions
            
            # Recommandations basées sur volume
            if recent_transactions == 0:
                monitoring_result['recommendations'].append("Vérifier synchronisation Qonto → Dougs")
            elif recent_transactions > 10:
                monitoring_result['recommendations'].append("Volume élevé - vérifier imports Dougs")
            
            # Enregistrer monitoring
            cursor.execute('''
                INSERT INTO dougs_monitoring (
                    nb_ecritures, status_sync, differences_detected
                ) VALUES (?, ?, ?)
            ''', (
                recent_transactions, 'MONITORED', 
                json.dumps(monitoring_result['recommendations'])
            ))
            
            conn.commit()
            conn.close()
            
            logging.info(f"📊 Monitoring Qonto-Dougs: {recent_transactions} transactions 7j")
            
        except Exception as e:
            monitoring_result['sync_status'] = 'ERROR'
            monitoring_result['error'] = str(e)
            logging.error(f"❌ Erreur monitoring: {e}")
        
        return monitoring_result
    
    def run_monthly_dougs_export(self) -> Dict:
        """Export mensuel complet pour Dougs"""
        logging.info("📊 Export mensuel Dougs")
        
        # Période mois dernier
        today = datetime.now()
        start_of_month = today.replace(day=1) - timedelta(days=1)
        start_of_month = start_of_month.replace(day=1)
        end_of_month = today.replace(day=1) - timedelta(days=1)
        
        start_date = start_of_month.strftime('%Y-%m-%d')
        end_date = end_of_month.strftime('%Y-%m-%d')
        
        results = {
            'periode': f"{start_date} → {end_date}",
            'exports': [],
            'instructions': None,
            'monitoring': {}
        }
        
        try:
            # 1. Export factures FEC
            factures_export = self.export_factures_fec_format(start_date, end_date)
            if factures_export:
                results['exports'].append(factures_export)
            
            # 2. Export paiements FEC
            paiements_export = self.export_paiements_fec_format(start_date, end_date)
            if paiements_export:
                results['exports'].append(paiements_export)
            
            # 3. Générer instructions import
            if results['exports']:
                instructions = self.generate_dougs_import_instructions(results['exports'])
                results['instructions'] = instructions
            
            # 4. Monitoring sync
            monitoring = self.monitor_qonto_dougs_sync()
            results['monitoring'] = monitoring
            
            logging.info(f"✅ Export Dougs mensuel: {len(results['exports'])} fichiers")
            
        except Exception as e:
            logging.error(f"❌ Erreur export mensuel Dougs: {e}")
            results['error'] = str(e)
        
        return results

def main():
    """Point d'entrée principal"""
    bridge = DougsBridgeTemporary()
    
    print("""
🌉 BRIDGE TEMPORAIRE DOUGS - EN ATTENDANT L'API
==============================================

Solutions déployées:
  📤 Export FEC automatisé
  📋 Instructions import détaillées  
  🔄 Monitoring Qonto→Dougs existant
  📊 Rapports mensuels

Formats supportés:
  • FEC (Fichier Écritures Comptables)
  • CSV séparateur |
  • UTF-8 encoding
  • Plan comptable français
    """)
    
    # Export mensuel
    result = bridge.run_monthly_dougs_export()
    
    print(f"\n✅ EXPORT DOUGS TERMINÉ")
    print(f"Période: {result['periode']}")
    print(f"Fichiers: {len(result['exports'])}")
    
    if result['exports']:
        print(f"📁 Fichiers générés:")
        for export_file in result['exports']:
            print(f"  • {Path(export_file).name}")
    
    if result.get('instructions'):
        print(f"📋 Instructions: {Path(result['instructions']).name}")
    
    print(f"\n💡 En attendant l'API Dougs officielle...")

if __name__ == "__main__":
    main()
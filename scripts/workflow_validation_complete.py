#!/usr/bin/env python3
"""
WORKFLOW VALIDATION COMPLET
Interface validation factures avant envoi + circuit approbation
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import subprocess

class WorkflowValidationComplete:
    """Workflow complet validation factures"""
    
    def __init__(self):
        self.setup_logging()
        self.setup_database()
        self.setup_validation_rules()
        
    def setup_logging(self):
        """Configuration logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/home/sq/SYAGA-CONSULTING/logs/workflow_validation.log'),
                logging.StreamHandler()
            ]
        )
    
    def setup_database(self):
        """Initialiser tables workflow validation"""
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        # Table workflow validation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflow_validation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                facture_id INTEGER,
                numero_facture TEXT,
                status_validation TEXT DEFAULT 'PENDING', -- 'PENDING', 'APPROVED', 'REJECTED', 'SENT'
                validateur TEXT,
                date_validation DATETIME,
                commentaires TEXT,
                modifications TEXT, -- JSON des modifications
                pdf_path TEXT,
                ready_to_send BOOLEAN DEFAULT FALSE,
                sent_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (facture_id) REFERENCES factures (id)
            )
        ''')
        
        # Table règles validation automatique
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS regles_validation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_regle TEXT,
                type_facture TEXT, -- 'FORFAIT', 'PONCTUEL', 'ALL'
                condition_json TEXT, -- JSON condition
                action TEXT, -- 'AUTO_APPROVE', 'REQUIRE_REVIEW', 'REJECT'
                active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table logs validation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs_validation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                facture_id INTEGER,
                action TEXT,
                details TEXT,
                user_action TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        self.init_default_rules()
        logging.info("✅ Tables workflow validation initialisées")
    
    def init_default_rules(self):
        """Initialiser règles de validation par défaut"""
        default_rules = [
            {
                'nom': 'Auto-approval forfaits récurrents',
                'type': 'FORFAIT',
                'condition': {'client_in': ['LAA', 'PHARMABEST', 'BUQUET', 'PETRAS'], 'montant_exact': True},
                'action': 'AUTO_APPROVE'
            },
            {
                'nom': 'Révision factures >2000€',
                'type': 'ALL',
                'condition': {'montant_ttc_gt': 2000},
                'action': 'REQUIRE_REVIEW'
            },
            {
                'nom': 'Rejet montants incohérents',
                'type': 'ALL',
                'condition': {'montant_ttc_lt': 10},
                'action': 'REJECT'
            },
            {
                'nom': 'Révision nouveaux clients',
                'type': 'ALL',
                'condition': {'client_not_in': ['LAA', 'PHARMABEST', 'BUQUET', 'PETRAS', 'PROVENCALE', 'SEXTANT', 'QUADRIMEX', 'GENLOG']},
                'action': 'REQUIRE_REVIEW'
            }
        ]
        
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        for rule in default_rules:
            cursor.execute('''
                INSERT OR IGNORE INTO regles_validation 
                (nom_regle, type_facture, condition_json, action)
                VALUES (?, ?, ?, ?)
            ''', (
                rule['nom'], rule['type'], 
                json.dumps(rule['condition']), rule['action']
            ))
        
        conn.commit()
        conn.close()
    
    def setup_validation_rules(self):
        """Charger règles de validation"""
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM regles_validation WHERE active = TRUE')
        rules = cursor.fetchall()
        
        self.validation_rules = []
        for rule in rules:
            self.validation_rules.append({
                'id': rule[0],
                'nom': rule[1],
                'type_facture': rule[2],
                'condition': json.loads(rule[3]),
                'action': rule[4]
            })
        
        conn.close()
        logging.info(f"✅ {len(self.validation_rules)} règles validation chargées")
    
    def submit_invoice_for_validation(self, facture_id: int, pdf_path: str = None) -> Dict:
        """Soumettre facture pour validation"""
        try:
            conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
            cursor = conn.cursor()
            
            # Récupérer info facture
            cursor.execute('''
                SELECT numero_facture, client_nom, total_ht, total_ttc, date_facture, objet
                FROM factures WHERE id = ?
            ''', (facture_id,))
            
            facture = cursor.fetchone()
            if not facture:
                return {'success': False, 'error': 'Facture non trouvée'}
            
            numero, client, ht, ttc, date_facture, objet = facture
            
            # Appliquer règles de validation automatique
            validation_result = self.apply_validation_rules(facture_id, {
                'numero': numero,
                'client': client,
                'montant_ht': ht,
                'montant_ttc': ttc,
                'date': date_facture,
                'objet': objet
            })
            
            # Créer entrée workflow
            cursor.execute('''
                INSERT OR REPLACE INTO workflow_validation (
                    facture_id, numero_facture, status_validation,
                    validateur, pdf_path, ready_to_send
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                facture_id, numero, validation_result['status'],
                validation_result.get('validateur', 'SYSTEM'),
                pdf_path, validation_result.get('auto_approved', False)
            ))
            
            # Log action
            cursor.execute('''
                INSERT INTO logs_validation (facture_id, action, details)
                VALUES (?, ?, ?)
            ''', (
                facture_id, 'SUBMITTED', 
                f"Soumise pour validation: {validation_result['action']}"
            ))
            
            conn.commit()
            conn.close()
            
            logging.info(f"📋 Facture {numero} soumise: {validation_result['action']}")
            
            return {
                'success': True,
                'facture_id': facture_id,
                'numero': numero,
                'status': validation_result['status'],
                'action': validation_result['action'],
                'auto_approved': validation_result.get('auto_approved', False)
            }
            
        except Exception as e:
            logging.error(f"❌ Erreur soumission validation {facture_id}: {e}")
            return {'success': False, 'error': str(e)}
    
    def apply_validation_rules(self, facture_id: int, facture_data: Dict) -> Dict:
        """Appliquer règles de validation automatique"""
        
        for rule in self.validation_rules:
            # Vérifier type facture
            if rule['type_facture'] != 'ALL':
                # Détecter type depuis objet/description
                facture_type = 'PONCTUEL'
                if 'forfait' in facture_data['objet'].lower():
                    facture_type = 'FORFAIT'
                
                if rule['type_facture'] != facture_type:
                    continue
            
            # Évaluer condition
            if self.evaluate_condition(rule['condition'], facture_data):
                action = rule['action']
                
                if action == 'AUTO_APPROVE':
                    return {
                        'status': 'APPROVED',
                        'action': f"Auto-approuvée ({rule['nom']})",
                        'validateur': 'SYSTEM_AUTO',
                        'auto_approved': True
                    }
                elif action == 'REJECT':
                    return {
                        'status': 'REJECTED',
                        'action': f"Rejetée ({rule['nom']})",
                        'validateur': 'SYSTEM_AUTO'
                    }
                elif action == 'REQUIRE_REVIEW':
                    return {
                        'status': 'PENDING',
                        'action': f"Révision requise ({rule['nom']})",
                        'validateur': None
                    }
        
        # Par défaut: révision manuelle
        return {
            'status': 'PENDING',
            'action': 'Révision manuelle standard',
            'validateur': None
        }
    
    def evaluate_condition(self, condition: Dict, facture_data: Dict) -> bool:
        """Évaluer condition de règle"""
        try:
            for key, value in condition.items():
                if key == 'client_in':
                    if not any(client in facture_data['client'].upper() for client in value):
                        return False
                        
                elif key == 'client_not_in':
                    if any(client in facture_data['client'].upper() for client in value):
                        return False
                        
                elif key == 'montant_ttc_gt':
                    if facture_data['montant_ttc'] <= value:
                        return False
                        
                elif key == 'montant_ttc_lt':
                    if facture_data['montant_ttc'] >= value:
                        return False
                        
                elif key == 'montant_exact':
                    # Vérifier si montant correspond aux forfaits standards
                    forfaits_standards = [1400, 500, 600, 400, 250, 100, 751.60]
                    if not any(abs(facture_data['montant_ttc'] - f * 1.2) < 0.01 for f in forfaits_standards):
                        return False
            
            return True
            
        except Exception as e:
            logging.warning(f"⚠️ Erreur évaluation condition: {e}")
            return False
    
    def get_pending_validations(self) -> List[Dict]:
        """Récupérer factures en attente de validation"""
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                wv.id, wv.facture_id, wv.numero_facture,
                f.client_nom, f.total_ht, f.total_ttc, f.date_facture,
                wv.pdf_path, wv.created_at
            FROM workflow_validation wv
            JOIN factures f ON wv.facture_id = f.id
            WHERE wv.status_validation = 'PENDING'
            ORDER BY wv.created_at ASC
        ''')
        
        pending = []
        for row in cursor.fetchall():
            pending.append({
                'workflow_id': row[0],
                'facture_id': row[1],
                'numero': row[2],
                'client': row[3],
                'montant_ht': row[4],
                'montant_ttc': row[5],
                'date_facture': row[6],
                'pdf_path': row[7],
                'submitted_at': row[8]
            })
        
        conn.close()
        return pending
    
    def approve_invoice(self, workflow_id: int, validateur: str, commentaires: str = "") -> bool:
        """Approuver une facture"""
        try:
            conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE workflow_validation 
                SET status_validation = 'APPROVED',
                    validateur = ?,
                    date_validation = ?,
                    commentaires = ?,
                    ready_to_send = TRUE
                WHERE id = ?
            ''', (validateur, datetime.now().isoformat(), commentaires, workflow_id))
            
            # Log action
            cursor.execute('''
                SELECT facture_id FROM workflow_validation WHERE id = ?
            ''', (workflow_id,))
            facture_id = cursor.fetchone()[0]
            
            cursor.execute('''
                INSERT INTO logs_validation (facture_id, action, details, user_action)
                VALUES (?, ?, ?, ?)
            ''', (
                facture_id, 'APPROVED', commentaires, validateur
            ))
            
            conn.commit()
            conn.close()
            
            logging.info(f"✅ Facture approuvée (workflow {workflow_id}) par {validateur}")
            return True
            
        except Exception as e:
            logging.error(f"❌ Erreur approbation: {e}")
            return False
    
    def reject_invoice(self, workflow_id: int, validateur: str, raison: str) -> bool:
        """Rejeter une facture"""
        try:
            conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE workflow_validation 
                SET status_validation = 'REJECTED',
                    validateur = ?,
                    date_validation = ?,
                    commentaires = ?
                WHERE id = ?
            ''', (validateur, datetime.now().isoformat(), raison, workflow_id))
            
            # Log action
            cursor.execute('''
                SELECT facture_id FROM workflow_validation WHERE id = ?
            ''', (workflow_id,))
            facture_id = cursor.fetchone()[0]
            
            cursor.execute('''
                INSERT INTO logs_validation (facture_id, action, details, user_action)
                VALUES (?, ?, ?, ?)
            ''', (
                facture_id, 'REJECTED', raison, validateur
            ))
            
            conn.commit()
            conn.close()
            
            logging.info(f"❌ Facture rejetée (workflow {workflow_id}) par {validateur}")
            return True
            
        except Exception as e:
            logging.error(f"❌ Erreur rejet: {e}")
            return False
    
    def get_approved_ready_to_send(self) -> List[Dict]:
        """Récupérer factures approuvées prêtes à envoyer"""
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                wv.id, wv.facture_id, wv.numero_facture,
                f.client_nom, f.total_ttc, wv.pdf_path,
                wv.date_validation, wv.validateur
            FROM workflow_validation wv
            JOIN factures f ON wv.facture_id = f.id
            WHERE wv.status_validation = 'APPROVED'
            AND wv.ready_to_send = TRUE
            AND wv.sent_at IS NULL
            ORDER BY wv.date_validation ASC
        ''')
        
        ready = []
        for row in cursor.fetchall():
            ready.append({
                'workflow_id': row[0],
                'facture_id': row[1], 
                'numero': row[2],
                'client': row[3],
                'montant_ttc': row[4],
                'pdf_path': row[5],
                'approved_at': row[6],
                'approved_by': row[7]
            })
        
        conn.close()
        return ready
    
    def mark_as_sent(self, workflow_id: int) -> bool:
        """Marquer facture comme envoyée"""
        try:
            conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE workflow_validation 
                SET status_validation = 'SENT',
                    sent_at = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), workflow_id))
            
            conn.commit()
            conn.close()
            
            logging.info(f"📤 Facture marquée envoyée (workflow {workflow_id})")
            return True
            
        except Exception as e:
            logging.error(f"❌ Erreur marquage envoi: {e}")
            return False
    
    def run_validation_batch(self, facture_ids: List[int]) -> Dict:
        """Traiter un lot de factures pour validation"""
        results = {
            'submitted': 0,
            'auto_approved': 0,
            'pending_review': 0,
            'rejected': 0,
            'errors': []
        }
        
        for facture_id in facture_ids:
            result = self.submit_invoice_for_validation(facture_id)
            
            if result['success']:
                results['submitted'] += 1
                
                if result.get('auto_approved'):
                    results['auto_approved'] += 1
                elif result['status'] == 'PENDING':
                    results['pending_review'] += 1
                elif result['status'] == 'REJECTED':
                    results['rejected'] += 1
            else:
                results['errors'].append(f"Facture {facture_id}: {result['error']}")
        
        logging.info(f"📊 Batch validation: {results['submitted']} soumises, {results['auto_approved']} auto-approuvées")
        return results
    
    def generate_validation_dashboard(self) -> str:
        """Générer dashboard validation"""
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        # Statistiques
        cursor.execute('''
            SELECT status_validation, COUNT(*) 
            FROM workflow_validation 
            GROUP BY status_validation
        ''')
        stats = dict(cursor.fetchall())
        
        # Factures en attente
        pending = self.get_pending_validations()
        ready_to_send = self.get_approved_ready_to_send()
        
        dashboard = f"""
📋 DASHBOARD WORKFLOW VALIDATION
===============================

📊 STATISTIQUES:
• En attente:     {stats.get('PENDING', 0):3} factures
• Approuvées:     {stats.get('APPROVED', 0):3} factures  
• Rejetées:       {stats.get('REJECTED', 0):3} factures
• Envoyées:       {stats.get('SENT', 0):3} factures

⏰ EN ATTENTE DE VALIDATION:
"""
        
        if pending:
            for p in pending[:10]:
                dashboard += f"• {p['numero']} - {p['client']} - {p['montant_ttc']:.2f}€ TTC\n"
        else:
            dashboard += "• Aucune facture en attente ✅\n"
        
        dashboard += f"""
✅ PRÊTES À ENVOYER:
"""
        
        if ready_to_send:
            for r in ready_to_send[:10]:
                dashboard += f"• {r['numero']} - {r['client']} - {r['montant_ttc']:.2f}€ TTC\n"
        else:
            dashboard += "• Aucune facture prête ✅\n"
        
        conn.close()
        return dashboard

def main():
    """Point d'entrée principal"""
    workflow = WorkflowValidationComplete()
    
    print("""
📋 WORKFLOW VALIDATION COMPLET SYAGA
====================================

Fonctions:
  ✅ Validation automatique (règles métier)
  👤 Interface validation manuelle
  📤 Circuit approbation
  📊 Dashboard suivi
    """)
    
    # Afficher dashboard
    dashboard = workflow.generate_validation_dashboard()
    print(dashboard)
    
    # Traiter factures en attente
    pending = workflow.get_pending_validations()
    if pending:
        print(f"\n⚠️ {len(pending)} factures en attente de validation manuelle")
    
    ready = workflow.get_approved_ready_to_send()
    if ready:
        print(f"✅ {len(ready)} factures prêtes à envoyer")

if __name__ == "__main__":
    main()
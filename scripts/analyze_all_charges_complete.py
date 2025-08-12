#!/usr/bin/env python3
"""
ANALYSE COMPLÈTE TOUTES CHARGES QONTO + BP
Extraction exhaustive pour identifier TOUTES les charges réelles
"""

import pdfplumber
import os
import re
from collections import defaultdict
from datetime import datetime

class CompleteChargesAnalyzer:
    def __init__(self):
        self.bp_dir = "/home/sq/extraits de compte BP"
        self.charges_by_category = defaultdict(list)
        
    def analyze_all_bp_pdfs(self):
        """Analyse tous les PDFs BP pour extraire TOUTES les transactions"""
        print("📄 ANALYSE EXHAUSTIVE BANQUE POPULAIRE")
        print("="*70)
        
        all_transactions = []
        
        # Analyser tous les PDFs disponibles
        pdf_files = [f for f in os.listdir(self.bp_dir) if f.endswith('.pdf') and not f.endswith('.pdf:Zone.Identifier')]
        
        for pdf_file in sorted(pdf_files):
            pdf_path = os.path.join(self.bp_dir, pdf_file)
            
            # Extraire date du nom de fichier
            date_match = re.search(r'(\d{8})\.pdf', pdf_file)
            if date_match:
                date_str = date_match.group(1)
                month = date_str[4:6]
                month_name = {
                    '03': 'Mars', '04': 'Avril', '05': 'Mai',
                    '06': 'Juin', '07': 'Juillet'
                }.get(month, month)
                
                print(f"\n📋 Analyse {month_name} 2025 ({date_str})...")
                
                try:
                    with pdfplumber.open(pdf_path) as pdf:
                        for page in pdf.pages:
                            text = page.extract_text()
                            if not text:
                                continue
                            
                            # Parser chaque ligne pour trouver TOUTES les transactions
                            lines = text.split('\n')
                            
                            for line in lines:
                                # Pattern pour débit avec montant
                                debit_match = re.search(r'(\d{2}/\d{2})\s+(.+?)\s+-\s*([\d\s]+,\d{2})\s*€', line)
                                
                                if debit_match:
                                    date = debit_match.group(1)
                                    label = debit_match.group(2).strip()
                                    amount = float(debit_match.group(3).replace(' ', '').replace(',', '.'))
                                    
                                    all_transactions.append({
                                        'month': month_name,
                                        'date': f"{date}/2025",
                                        'label': label,
                                        'amount': -amount,
                                        'type': 'debit'
                                    })
                                    
                                # Pattern pour crédit
                                credit_match = re.search(r'(\d{2}/\d{2})\s+(.+?)\s+\+?\s*([\d\s]+,\d{2})\s*€', line)
                                
                                if credit_match and not debit_match:
                                    date = credit_match.group(1)
                                    label = credit_match.group(2).strip()
                                    amount = float(credit_match.group(3).replace(' ', '').replace(',', '.'))
                                    
                                    all_transactions.append({
                                        'month': month_name,
                                        'date': f"{date}/2025",
                                        'label': label,
                                        'amount': amount,
                                        'type': 'credit'
                                    })
                                    
                except Exception as e:
                    print(f"   ❌ Erreur: {e}")
        
        print(f"\n✅ Total: {len(all_transactions)} transactions BP extraites")
        return all_transactions
    
    def categorize_all_charges(self, transactions):
        """Catégorise TOUTES les charges de manière exhaustive"""
        
        categories = {
            'remuneration_dirigeant': {
                'patterns': ['questier', 'remuneration', 'salaire dirigeant'],
                'transactions': [], 'total': 0
            },
            'salaires_employes': {
                'patterns': ['hugo joucla', 'romain bastien', 'salaire'],
                'transactions': [], 'total': 0
            },
            'charges_sociales': {
                'patterns': ['urssaf', 'rsi', 'cpam', 'charges sociales', 'cotisation'],
                'transactions': [], 'total': 0
            },
            'impots_taxes': {
                'patterns': ['dgfip', 'impot', 'taxe', 'cfe', 'cvae'],
                'transactions': [], 'total': 0
            },
            'loyers_charges_locatives': {
                'patterns': ['loyer', 'charges locatives', 'eau', 'copropriete'],
                'transactions': [], 'total': 0
            },
            'assurances_pro': {
                'patterns': ['swisslife', 'hiscox', 'assurance', 'rc pro', 'prevoyance'],
                'transactions': [], 'total': 0
            },
            'expert_comptable': {
                'patterns': ['nobelia', 'comptable', 'expert', 'fiduciaire'],
                'transactions': [], 'total': 0
            },
            'telecom_internet': {
                'patterns': ['free', 'orange', 'sfr', 'bouygues', 'mobile', 'internet'],
                'transactions': [], 'total': 0
            },
            'energie': {
                'patterns': ['edf', 'engie', 'electricite', 'gaz'],
                'transactions': [], 'total': 0
            },
            'remboursements_prets': {
                'patterns': ['riverbank', 'remboursement pret', 'echeance'],
                'transactions': [], 'total': 0
            },
            'achats_fournisseurs': {
                'patterns': ['ingram', 'lcr domiciliee', 'fournisseur'],
                'transactions': [], 'total': 0
            },
            'frais_bancaires': {
                'patterns': ['frais', 'commission', 'cotisation carte', 'agios'],
                'transactions': [], 'total': 0
            },
            'vehicule_deplacement': {
                'patterns': ['essence', 'gasoil', 'peage', 'parking', 'total market'],
                'transactions': [], 'total': 0
            },
            'virements_internes': {
                'patterns': ['vir inst syaga', 'virement interne', 'qonto'],
                'transactions': [], 'total': 0
            },
            'autres': {
                'patterns': [],
                'transactions': [], 'total': 0
            }
        }
        
        # Catégoriser chaque transaction
        for tx in transactions:
            if tx['type'] != 'debit':
                continue
                
            amount = abs(tx['amount'])
            label_lower = tx['label'].lower()
            categorized = False
            
            for cat_name, cat_info in categories.items():
                if cat_name == 'autres':
                    continue
                    
                for pattern in cat_info['patterns']:
                    if pattern in label_lower:
                        cat_info['transactions'].append(tx)
                        cat_info['total'] += amount
                        categorized = True
                        break
                
                if categorized:
                    break
            
            if not categorized and 'virements_internes' not in cat_name:
                # Vérifier si c'est un virement interne
                if any(p in label_lower for p in categories['virements_internes']['patterns']):
                    categories['virements_internes']['transactions'].append(tx)
                    categories['virements_internes']['total'] += amount
                else:
                    categories['autres']['transactions'].append(tx)
                    categories['autres']['total'] += amount
        
        return categories
    
    def display_complete_analysis(self, categories):
        """Affiche l'analyse complète avec focus sur charges fixes"""
        print("\n💰 ANALYSE COMPLÈTE DES CHARGES (Mars-Juillet 2025)")
        print("="*70)
        
        # Séparer charges fixes et ponctuelles
        charges_fixes = {}
        charges_ponctuelles = {}
        
        # Charges fixes mensuelles
        fixes = ['remuneration_dirigeant', 'salaires_employes', 'charges_sociales', 
                'impots_taxes', 'loyers_charges_locatives', 'assurances_pro',
                'expert_comptable', 'telecom_internet', 'energie', 'remboursements_prets',
                'frais_bancaires']
        
        for cat_name, cat_info in categories.items():
            if cat_name == 'virements_internes':
                continue
                
            if cat_info['total'] > 0:
                monthly_avg = cat_info['total'] / 5  # Sur 5 mois
                
                if cat_name in fixes:
                    charges_fixes[cat_name] = monthly_avg
                else:
                    charges_ponctuelles[cat_name] = monthly_avg
        
        # Afficher charges fixes
        print("\n🔒 CHARGES FIXES MENSUELLES:")
        print("-" * 50)
        total_fixes = 0
        
        for cat_name in fixes:
            if cat_name in charges_fixes:
                amount = charges_fixes[cat_name]
                total_fixes += amount
                print(f"{cat_name.replace('_', ' ').upper():30} : {amount:8,.2f}€/mois")
                
                # Afficher détails importants
                if amount > 100 and categories[cat_name]['transactions']:
                    for tx in categories[cat_name]['transactions'][:2]:
                        print(f"  → {tx['label'][:40]:40} : {abs(tx['amount']):7.2f}€")
        
        print(f"\n{'TOTAL CHARGES FIXES':30} : {total_fixes:8,.2f}€/mois")
        
        # Afficher charges ponctuelles
        print("\n📦 CHARGES PONCTUELLES/VARIABLES:")
        print("-" * 50)
        total_ponctuelles = 0
        
        for cat_name, amount in charges_ponctuelles.items():
            if cat_name != 'autres':
                total_ponctuelles += amount
                print(f"{cat_name.replace('_', ' ').upper():30} : {amount:8,.2f}€/mois (lissé)")
                
                if categories[cat_name]['transactions']:
                    for tx in categories[cat_name]['transactions'][:2]:
                        print(f"  → {tx['label'][:40]:40} : {abs(tx['amount']):7.2f}€")
        
        # Virements internes (informatif)
        if categories['virements_internes']['total'] > 0:
            print(f"\n💸 VIREMENTS INTERNES (non comptés):")
            print(f"   Total sur période : {categories['virements_internes']['total']:,.2f}€")
            for tx in categories['virements_internes']['transactions'][:3]:
                print(f"   → {tx['date']} : {abs(tx['amount']):7.2f}€")
        
        return total_fixes, total_ponctuelles
    
    def analyze_qonto_charges(self):
        """Récupère les charges Qonto déjà identifiées"""
        print("\n💳 CHARGES QONTO IDENTIFIÉES:")
        print("-" * 50)
        
        # D'après l'analyse précédente
        qonto_charges = {
            'Salaires Hugo + Romain': 4200,
            'URSSAF PACA': 3250,
            'DGFIP (impôts)': 2875,
            'Remboursement prêt Riverbank': 1600,
            'Pierre Questier (rémunération?)': 2350
        }
        
        total_qonto = 0
        for label, amount in qonto_charges.items():
            print(f"{label:30} : {amount:8,.2f}€/mois")
            total_qonto += amount
        
        print(f"\n{'TOTAL QONTO':30} : {total_qonto:8,.2f}€/mois")
        
        return total_qonto

def main():
    """Analyse exhaustive pour trouver TOUTES les charges"""
    print("🔍 RECHERCHE EXHAUSTIVE DE TOUTES LES CHARGES")
    print("="*70)
    
    analyzer = CompleteChargesAnalyzer()
    
    # 1. Analyser BP
    bp_transactions = analyzer.analyze_all_bp_pdfs()
    
    # 2. Catégoriser
    categories = analyzer.categorize_all_charges(bp_transactions)
    
    # 3. Afficher analyse complète
    charges_fixes_bp, charges_variables_bp = analyzer.display_complete_analysis(categories)
    
    # 4. Ajouter Qonto
    charges_qonto = analyzer.analyze_qonto_charges()
    
    # 5. SYNTHÈSE FINALE
    print("\n" + "="*70)
    print("💎 SYNTHÈSE CHARGES MENSUELLES RÉELLES")
    print("="*70)
    
    total_charges_fixes = charges_fixes_bp + charges_qonto
    
    print(f"\n🔒 CHARGES FIXES TOTALES:")
    print(f"   Banque Populaire : {charges_fixes_bp:8,.2f}€")
    print(f"   Qonto           : {charges_qonto:8,.2f}€")
    print(f"   TOTAL FIXES     : {total_charges_fixes:8,.2f}€/mois")
    
    print(f"\n📦 CHARGES VARIABLES:")
    print(f"   Achats ponctuels : {charges_variables_bp:8,.2f}€/mois (lissé)")
    
    # Calcul seuil rentabilité
    print("\n" + "="*70)
    print("🎯 CALCUL SEUIL DE RENTABILITÉ RÉEL")
    print("="*70)
    
    # Objectif : te payer 3000€ net
    objectif_sebastien_net = 3000
    charges_sebastien = objectif_sebastien_net * 1.82  # Estimation charges
    
    charges_totales_cibles = total_charges_fixes + charges_sebastien
    
    print(f"\nCharges actuelles    : {total_charges_fixes:8,.2f}€")
    print(f"Objectif Sébastien   : {charges_sebastien:8,.2f}€ (3000€ net)")
    print(f"TOTAL CIBLE         : {charges_totales_cibles:8,.2f}€/mois")
    
    # Avec Clockify
    total_hours = 255.8
    
    for rate in [100, 120, 150]:
        print(f"\n📊 Avec tarif {rate}€/h:")
        for ratio in [50, 60, 70, 80]:
            revenue = total_hours * (ratio/100) * rate
            profit = revenue - charges_totales_cibles
            status = "✅" if profit > 0 else "❌"
            print(f"  {ratio}% facturable : {revenue:7,.0f}€ → {profit:+7,.0f}€ {status}")

if __name__ == "__main__":
    main()
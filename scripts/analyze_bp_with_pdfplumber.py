#!/usr/bin/env python3
"""
ANALYSE EXTRAITS BANQUE POPULAIRE avec PDFPLUMBER
Extraction et catégorisation complète des charges depuis PDFs BP
"""

import os
import re
import pdfplumber
from datetime import datetime
from collections import defaultdict

class BanquePopulaireAnalyzerV2:
    def __init__(self):
        self.extracts_dir = "/home/sq/extraits de compte BP"
        
    def extract_pdf_with_plumber(self, pdf_file):
        """Extrait le texte et les tableaux d'un PDF avec pdfplumber"""
        try:
            all_text = []
            all_tables = []
            
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    # Extraire le texte
                    text = page.extract_text()
                    if text:
                        all_text.append(text)
                    
                    # Extraire les tables
                    tables = page.extract_tables()
                    if tables:
                        all_tables.extend(tables)
            
            return '\n'.join(all_text), all_tables
            
        except Exception as e:
            print(f"❌ Erreur extraction {pdf_file}: {e}")
            return "", []
    
    def parse_bp_transactions(self, text, tables, month_name):
        """Parse les transactions BP depuis le texte et tables extraits"""
        transactions = []
        
        # Pattern pour détecter les montants BP
        amount_pattern = r'([\d\s]+,\d{2})'
        
        # Patterns pour identifier les transactions
        debit_keywords = ['PAIEMENT', 'ACHAT', 'RETRAIT', 'VIREMENT', 'PRELEVEMENT', 'FRAIS', 'COTISATION']
        credit_keywords = ['VIREMENT RECU', 'REMISE', 'VERSEMENT']
        
        # Parser le texte ligne par ligne
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            # Chercher date au format JJ/MM
            date_match = re.search(r'(\d{2}/\d{2})', line)
            
            if date_match:
                date = date_match.group(1)
                
                # Récupérer contexte (ligne actuelle + suivantes)
                context = line
                if i + 1 < len(lines):
                    context += " " + lines[i + 1]
                if i + 2 < len(lines):
                    context += " " + lines[i + 2]
                
                # Chercher montants
                amounts = re.findall(amount_pattern, context)
                
                for amount_str in amounts:
                    try:
                        # Nettoyer et convertir montant
                        amount_clean = amount_str.strip().replace(' ', '').replace(',', '.')
                        amount = float(amount_clean)
                        
                        # Déterminer débit/crédit
                        is_debit = any(keyword in context.upper() for keyword in debit_keywords)
                        is_credit = any(keyword in context.upper() for keyword in credit_keywords)
                        
                        # Extraire libellé
                        label = context.replace(date, '').replace(amount_str, '').strip()
                        label = re.sub(r'\s+', ' ', label)[:150]
                        
                        # Si montant > 0 et keywords débit, c'est une charge
                        if amount > 0 and (is_debit or not is_credit):
                            transactions.append({
                                'date': f"{date}/2025",
                                'month': month_name,
                                'label': label,
                                'amount': -amount,  # Négatif pour débit
                                'type': 'debit'
                            })
                        elif amount > 0 and is_credit:
                            transactions.append({
                                'date': f"{date}/2025",
                                'month': month_name,
                                'label': label,
                                'amount': amount,
                                'type': 'credit'
                            })
                            
                    except Exception as e:
                        continue
        
        # Parser aussi les tables si présentes
        for table in tables:
            if not table:
                continue
                
            for row in table:
                if not row:
                    continue
                    
                # Chercher colonnes avec dates et montants
                row_text = ' '.join(str(cell) for cell in row if cell)
                
                date_match = re.search(r'(\d{2}/\d{2})', row_text)
                amount_matches = re.findall(amount_pattern, row_text)
                
                if date_match and amount_matches:
                    date = date_match.group(1)
                    
                    for amount_str in amount_matches:
                        try:
                            amount = float(amount_str.replace(' ', '').replace(',', '.'))
                            
                            # Créer transaction
                            label = row_text.replace(date, '').replace(amount_str, '').strip()[:150]
                            
                            transactions.append({
                                'date': f"{date}/2025",
                                'month': month_name,
                                'label': label,
                                'amount': -abs(amount) if 'DEBIT' in row_text.upper() else amount,
                                'type': 'debit' if amount < 0 else 'credit'
                            })
                            
                        except:
                            continue
        
        return transactions
    
    def categorize_bp_charges_detailed(self, transactions):
        """Catégorise les charges BP de manière très détaillée"""
        categories = {
            'loyers_immobilier': {
                'patterns': ['loyer', 'sci ', 'immobili', 'foncier', 'taxe habitation', 'taxe fonciere'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'assurances': {
                'patterns': ['hiscox', 'assurance', 'axa', 'maaf', 'allianz', 'generali', 'mutuelle', 'prevoyance', 'gan '],
                'total': 0, 'count': 0, 'transactions': []
            },
            'carburants': {
                'patterns': ['total ', 'shell', 'esso', 'carburant', 'essence', 'gasoil', 'station', 'avia', 'bp '],
                'total': 0, 'count': 0, 'transactions': []
            },
            'peages_autoroutes': {
                'patterns': ['autoroute', 'peage', 'vinci', 'asf', 'escota', 'aprr', 'cofiroute'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'telecom_internet': {
                'patterns': ['orange', 'sfr', 'bouygues', 'free', 'mobile', 'internet', 'telecom'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'energie': {
                'patterns': ['edf', 'engie', 'electricite', 'gaz', 'energie', 'enedis', 'grdf'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'restauration': {
                'patterns': ['restaurant', 'brasserie', 'cafe', 'boulang', 'mcdo', 'quick', 'burger', 'pizz'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'frais_bancaires': {
                'patterns': ['frais', 'commission', 'cotisation', 'carte', 'agios', 'interets'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'achats_equipements': {
                'patterns': ['amazon', 'fnac', 'darty', 'boulanger', 'cdiscount', 'leroy', 'castorama', 'bricorama'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'alimentation': {
                'patterns': ['carrefour', 'leclerc', 'auchan', 'intermarche', 'lidl', 'casino', 'monoprix', 'super u'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'virements_internes': {
                'patterns': ['virement interne', 'vir sepa', 'qonto', 'syaga consulting'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'autres_charges': {
                'patterns': [],
                'total': 0, 'count': 0, 'transactions': []
            }
        }
        
        for tx in transactions:
            if tx['type'] != 'debit':
                continue
                
            amount = abs(tx['amount'])
            label_lower = tx['label'].lower()
            categorized = False
            
            # Tester chaque catégorie
            for cat_name, cat_info in categories.items():
                if cat_name in ['autres_charges', 'virements_internes']:
                    continue
                    
                for pattern in cat_info['patterns']:
                    if pattern in label_lower:
                        cat_info['total'] += amount
                        cat_info['count'] += 1
                        cat_info['transactions'].append(tx)
                        categorized = True
                        break
                
                if categorized:
                    break
            
            # Si non catégorisé et pas virement interne
            if not categorized:
                # Vérifier si c'est un virement interne
                is_internal = any(p in label_lower for p in categories['virements_internes']['patterns'])
                
                if is_internal:
                    categories['virements_internes']['total'] += amount
                    categories['virements_internes']['count'] += 1
                    categories['virements_internes']['transactions'].append(tx)
                else:
                    categories['autres_charges']['total'] += amount
                    categories['autres_charges']['count'] += 1
                    categories['autres_charges']['transactions'].append(tx)
        
        return categories
    
    def analyze_all_bp_extracts(self):
        """Analyse tous les extraits BP"""
        print("📄 ANALYSE COMPLÈTE EXTRAITS BANQUE POPULAIRE")
        print("="*70)
        
        # Lister et trier les PDFs
        pdf_files = []
        months_map = {
            '20250314': 'Mars 2025',
            '20250331': 'Mars 2025',
            '20250415': 'Avril 2025',
            '20250430': 'Avril 2025',
            '20250515': 'Mai 2025',
            '20250530': 'Mai 2025',
            '20250613': 'Juin 2025',
            '20250630': 'Juin 2025',
            '20250715': 'Juillet 2025',
            '20250731': 'Juillet 2025'
        }
        
        # Focus sur les 3 derniers mois (Mai, Juin, Juillet)
        focus_months = ['20250515', '20250530', '20250613', '20250630', '20250715', '20250731']
        
        for file in os.listdir(self.extracts_dir):
            if file.endswith('.pdf') and not file.endswith('.pdf:Zone.Identifier'):
                date_match = re.search(r'(\d{8})\.pdf', file)
                if date_match:
                    date_str = date_match.group(1)
                    if date_str in focus_months:  # Focus 3 derniers mois
                        pdf_files.append({
                            'path': os.path.join(self.extracts_dir, file),
                            'date': date_str,
                            'month': months_map.get(date_str, 'Inconnu')
                        })
        
        # Analyser chaque PDF
        all_transactions = []
        
        for pdf_info in sorted(pdf_files, key=lambda x: x['date']):
            print(f"\n📋 Extraction {pdf_info['month']} ({pdf_info['date']})...")
            
            text, tables = self.extract_pdf_with_plumber(pdf_info['path'])
            
            if text:
                transactions = self.parse_bp_transactions(text, tables, pdf_info['month'])
                all_transactions.extend(transactions)
                print(f"   ✅ {len(transactions)} transactions extraites")
                
                # Afficher échantillon
                if transactions:
                    debits = [t for t in transactions if t['type'] == 'debit']
                    if debits:
                        print(f"   Exemples débits:")
                        for tx in debits[:3]:
                            print(f"     • {abs(tx['amount']):6.2f}€ - {tx['label'][:40]}")
            else:
                print(f"   ❌ Pas de texte extrait")
        
        print(f"\n✅ TOTAL: {len(all_transactions)} transactions BP extraites")
        
        # Catégoriser
        categories = self.categorize_bp_charges_detailed(all_transactions)
        
        return all_transactions, categories
    
    def display_complete_bp_analysis(self, categories):
        """Affiche l'analyse complète BP"""
        print("\n💸 ANALYSE DÉTAILLÉE CHARGES BANQUE POPULAIRE (Mai-Juillet 2025)")
        print("="*75)
        
        total_charges_bp = 0
        charges_details = {}
        
        for cat_name, cat_info in categories.items():
            # Ignorer virements internes et catégories vides
            if cat_name == 'virements_internes' or cat_info['total'] == 0:
                continue
                
            monthly_avg = cat_info['total'] / 3  # Sur 3 mois
            total_charges_bp += monthly_avg
            charges_details[cat_name] = monthly_avg
            
            print(f"\n🏷️ {cat_name.replace('_', ' ').upper()}")
            print(f"   Total 3 mois   : {cat_info['total']:8,.2f}€")
            print(f"   Moyenne/mois   : {monthly_avg:8,.2f}€")
            print(f"   Nb transactions: {cat_info['count']}")
            
            # Top 3 transactions
            if cat_info['transactions']:
                sorted_tx = sorted(cat_info['transactions'], 
                                 key=lambda x: abs(x['amount']), 
                                 reverse=True)[:3]
                print(f"   Principales dépenses:")
                for tx in sorted_tx:
                    print(f"     • {tx['month']:10} - {abs(tx['amount']):6.2f}€ - {tx['label'][:35]}")
        
        print(f"\n💎 SYNTHÈSE CHARGES BP")
        print("-" * 50)
        print(f"TOTAL CHARGES BP/MOIS : {total_charges_bp:,.2f}€")
        
        # Virements internes (informatif)
        if categories['virements_internes']['count'] > 0:
            print(f"\n📤 Virements internes (non comptés): {categories['virements_internes']['total']:,.2f}€")
        
        return total_charges_bp, charges_details

def main():
    print("🏦 ANALYSE BANQUE POPULAIRE AVEC PDFPLUMBER")
    print("="*75)
    
    analyzer = BanquePopulaireAnalyzerV2()
    
    # Analyser tous les extraits
    transactions, categories = analyzer.analyze_all_bp_extracts()
    
    # Afficher analyse complète
    charges_bp_mensuelles, details = analyzer.display_complete_bp_analysis(categories)
    
    print(f"\n🎯 RÉSULTAT FINAL BP")
    print(f"Charges BP totales/mois : {charges_bp_mensuelles:,.2f}€")
    
    return charges_bp_mensuelles, details

if __name__ == "__main__":
    main()
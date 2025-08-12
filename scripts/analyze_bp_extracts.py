#!/usr/bin/env python3
"""
ANALYSE EXTRAITS BANQUE POPULAIRE
Extraction et catégorisation des charges depuis PDFs BP
"""

import os
import subprocess
import re
from datetime import datetime
from collections import defaultdict

class BanquePopulaireAnalyzer:
    def __init__(self):
        self.extracts_dir = "/home/sq/extraits de compte BP"
        self.transactions = []
        
    def extract_pdf_text(self, pdf_file):
        """Extrait le texte d'un PDF avec pdftotext"""
        try:
            # Utiliser pdftotext pour extraire le texte
            result = subprocess.run(
                ['pdftotext', pdf_file, '-'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                # Alternative avec strings si pdftotext échoue
                result = subprocess.run(
                    ['strings', pdf_file],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return result.stdout if result.returncode == 0 else ""
                
        except Exception as e:
            print(f"❌ Erreur extraction {pdf_file}: {e}")
            return ""
    
    def parse_transactions(self, text, month_name):
        """Parse les transactions depuis le texte extrait"""
        transactions = []
        
        # Patterns pour détecter les transactions BP
        # Format typique : DATE LIBELLE DEBIT CREDIT
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            # Pattern date au début de ligne
            date_pattern = r'^\d{2}/\d{2}'
            if re.match(date_pattern, line):
                try:
                    # Extraire date
                    date_match = re.match(r'^(\d{2}/\d{2})', line)
                    if date_match:
                        date = date_match.group(1)
                        
                        # Le libellé est souvent sur la ligne suivante ou sur la même ligne
                        # Chercher montants (formats possibles : 1 234,56 ou 1234.56)
                        amount_pattern = r'[-]?\d[\d\s]*[,\.]\d{2}'
                        
                        # Combiner ligne actuelle et suivantes pour le contexte
                        full_text = line
                        if i + 1 < len(lines):
                            full_text += " " + lines[i + 1]
                        if i + 2 < len(lines):
                            full_text += " " + lines[i + 2]
                        
                        # Chercher montants
                        amounts = re.findall(amount_pattern, full_text)
                        
                        if amounts:
                            for amount_str in amounts:
                                # Nettoyer et convertir montant
                                amount_clean = amount_str.replace(' ', '').replace(',', '.')
                                amount = float(amount_clean)
                                
                                # Extraire libellé (tout ce qui n'est pas date ou montant)
                                label = full_text.replace(date, '').replace(amount_str, '').strip()
                                label = re.sub(r'\s+', ' ', label)[:100]  # Limiter longueur
                                
                                transactions.append({
                                    'date': f"{date}/2025",
                                    'month': month_name,
                                    'label': label,
                                    'amount': amount,
                                    'type': 'debit' if amount < 0 else 'credit'
                                })
                                
                except Exception as e:
                    continue
        
        return transactions
    
    def categorize_bp_charges(self, transactions):
        """Catégorise les charges BP"""
        categories = {
            'loyers_charges_immo': {
                'patterns': ['loyer', 'sci', 'immobilier', 'foncier', 'taxe habitation'],
                'total': 0, 'transactions': []
            },
            'assurances': {
                'patterns': ['hiscox', 'assurance', 'axa', 'maaf', 'allianz', 'mutuelle', 'prevoyance'],
                'total': 0, 'transactions': []
            },
            'vehicules_essence': {
                'patterns': ['total ', 'shell', 'esso', 'carburant', 'essence', 'gasoil', 'station'],
                'total': 0, 'transactions': []
            },
            'autoroutes_peages': {
                'patterns': ['autoroute', 'peage', 'vinci', 'asf', 'escota', 'aprr'],
                'total': 0, 'transactions': []
            },
            'telecom': {
                'patterns': ['orange', 'sfr', 'bouygues', 'free', 'mobile', 'internet'],
                'total': 0, 'transactions': []
            },
            'edf_energie': {
                'patterns': ['edf', 'engie', 'electricite', 'gaz', 'energie'],
                'total': 0, 'transactions': []
            },
            'repas_restauration': {
                'patterns': ['restaurant', 'brasserie', 'cafe', 'boulang', 'mcdo', 'quick'],
                'total': 0, 'transactions': []
            },
            'frais_bancaires': {
                'patterns': ['frais', 'commission', 'cotisation', 'carte', 'agios'],
                'total': 0, 'transactions': []
            },
            'achats_materiels': {
                'patterns': ['amazon', 'fnac', 'darty', 'boulanger', 'cdiscount', 'leroy', 'castorama'],
                'total': 0, 'transactions': []
            },
            'courses_alimentation': {
                'patterns': ['carrefour', 'leclerc', 'auchan', 'intermarche', 'lidl', 'casino', 'monoprix'],
                'total': 0, 'transactions': []
            },
            'autres_depenses': {
                'patterns': [],
                'total': 0, 'transactions': []
            },
            'virements_internes': {
                'patterns': ['virement', 'qonto', 'syaga'],
                'total': 0, 'transactions': []
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
                if cat_name == 'autres_depenses':
                    continue
                    
                for pattern in cat_info['patterns']:
                    if pattern in label_lower:
                        cat_info['total'] += amount
                        cat_info['transactions'].append(tx)
                        categorized = True
                        break
                
                if categorized:
                    break
            
            # Si non catégorisé
            if not categorized:
                categories['autres_depenses']['total'] += amount
                categories['autres_depenses']['transactions'].append(tx)
        
        return categories
    
    def analyze_all_extracts(self):
        """Analyse tous les extraits BP"""
        print("📄 ANALYSE EXTRAITS BANQUE POPULAIRE")
        print("="*60)
        
        # Lister les PDFs
        pdf_files = []
        months_map = {
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
        
        for file in os.listdir(self.extracts_dir):
            if file.endswith('.pdf') and not file.endswith('.pdf:Zone.Identifier'):
                pdf_path = os.path.join(self.extracts_dir, file)
                
                # Extraire date du nom de fichier
                date_match = re.search(r'(\d{8})\.pdf', file)
                if date_match:
                    date_str = date_match.group(1)
                    month_name = months_map.get(date_str, 'Inconnu')
                    
                    pdf_files.append({
                        'path': pdf_path,
                        'date': date_str,
                        'month': month_name
                    })
        
        # Analyser chaque PDF
        all_transactions = []
        
        for pdf_info in sorted(pdf_files, key=lambda x: x['date']):
            print(f"\n📋 Extraction {pdf_info['month']} ({pdf_info['date']})...")
            
            text = self.extract_pdf_text(pdf_info['path'])
            if text:
                transactions = self.parse_transactions(text, pdf_info['month'])
                all_transactions.extend(transactions)
                print(f"   ✅ {len(transactions)} transactions extraites")
            else:
                print(f"   ❌ Échec extraction")
        
        print(f"\n✅ Total: {len(all_transactions)} transactions BP extraites")
        
        # Catégoriser
        categories = self.categorize_bp_charges(all_transactions)
        
        return all_transactions, categories
    
    def display_bp_analysis(self, categories):
        """Affiche l'analyse BP"""
        print("\n💸 CHARGES BANQUE POPULAIRE (3 derniers mois)")
        print("="*65)
        
        total_charges_bp = 0
        
        for cat_name, cat_info in categories.items():
            if cat_name == 'virements_internes':
                continue
                
            if cat_info['total'] > 0:
                monthly_avg = cat_info['total'] / 3  # Sur 3 mois
                total_charges_bp += monthly_avg
                
                print(f"\n🏷️ {cat_name.replace('_', ' ').upper()}")
                print(f"   Total 3 mois  : {cat_info['total']:8,.0f}€")
                print(f"   Moyenne/mois  : {monthly_avg:8,.0f}€")
                print(f"   Transactions  : {len(cat_info['transactions'])}")
                
                # Top transactions
                if monthly_avg > 100:
                    sorted_tx = sorted(cat_info['transactions'], 
                                     key=lambda x: abs(x['amount']), 
                                     reverse=True)[:3]
                    for tx in sorted_tx:
                        print(f"     • {abs(tx['amount']):6,.0f}€ - {tx['label'][:40]}")
        
        print(f"\n💎 TOTAL CHARGES BP/MOIS : {total_charges_bp:,.0f}€")
        
        return total_charges_bp

def main():
    print("🏦 ANALYSE COMPLÈTE BANQUE POPULAIRE")
    print("="*65)
    
    # Vérifier pdftotext
    try:
        subprocess.run(['which', 'pdftotext'], check=True, capture_output=True)
        print("✅ pdftotext disponible")
    except:
        print("⚠️ pdftotext non trouvé, installation...")
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'poppler-utils'], capture_output=True)
    
    analyzer = BanquePopulaireAnalyzer()
    
    # Analyser tous les extraits
    transactions, categories = analyzer.analyze_all_extracts()
    
    # Afficher analyse
    charges_bp_mensuelles = analyzer.display_bp_analysis(categories)
    
    print(f"\n🎯 SYNTHÈSE FINALE BP")
    print(f"Charges BP mensuelles : {charges_bp_mensuelles:,.0f}€/mois")
    
    return charges_bp_mensuelles

if __name__ == "__main__":
    main()
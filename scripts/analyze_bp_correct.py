#!/usr/bin/env python3
"""
ANALYSE CORRECTE BANQUE POPULAIRE
Extraction précise des vraies transactions depuis PDFs BP
"""

import os
import re
import pdfplumber
from collections import defaultdict

class BPAnalyzerCorrect:
    def __init__(self):
        self.extracts_dir = "/home/sq/extraits de compte BP"
        
    def extract_transactions_from_pdf(self, pdf_path, month_name):
        """Extrait les vraies transactions d'un PDF BP"""
        transactions = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    lines = text.split('\n')
                    
                    # Chercher la section transactions (après SOLDE CREDITEUR AU)
                    in_transactions = False
                    
                    for line in lines:
                        # Début de la section transactions
                        if 'SOLDE CREDITEUR AU' in line and '€' in line:
                            in_transactions = True
                            continue
                        
                        # Fin de la section transactions
                        if 'TOTAL DES MOUVEMENTS' in line:
                            in_transactions = False
                            continue
                        
                        # Parser les transactions
                        if in_transactions:
                            # Pattern pour date JJ/MM au début
                            date_match = re.match(r'^(\d{2}/\d{2})\s+(.+?)\s+([\d\s]+,\d{2})\s*€', line)
                            
                            if not date_match:
                                # Alternative : montant négatif avec -
                                date_match = re.match(r'^(\d{2}/\d{2})\s+(.+?)\s+-\s*([\d\s]+,\d{2})\s*€', line)
                            
                            if date_match:
                                date = date_match.group(1)
                                label = date_match.group(2).strip()
                                amount_str = date_match.group(3).replace(' ', '').replace(',', '.')
                                
                                try:
                                    amount = float(amount_str)
                                    
                                    # Si le montant est précédé de -, c'est un débit
                                    if '-' in line:
                                        amount = -amount
                                    
                                    transactions.append({
                                        'date': f"{date}/2025",
                                        'month': month_name,
                                        'label': label,
                                        'amount': amount,
                                        'type': 'debit' if amount < 0 else 'credit'
                                    })
                                    
                                except ValueError:
                                    continue
                    
                    # Pattern alternatif pour les lignes avec montants isolés
                    # Format : 18/07 LCR DOMICILIEE 18/07 16/07 - 959,68 €
                    pattern2 = r'(\d{2}/\d{2})\s+([A-Z].+?)\s+\d{2}/\d{2}\s+\d{2}/\d{2}\s+-?\s*([\d\s]+,\d{2})\s*€'
                    
                    for match in re.finditer(pattern2, text):
                        date = match.group(1)
                        label = match.group(2).strip()
                        amount_str = match.group(3).replace(' ', '').replace(',', '.')
                        
                        try:
                            amount = -float(amount_str)  # Négatif car débit
                            
                            # Vérifier pas déjà ajouté
                            exists = any(t['date'].startswith(date) and abs(t['amount'] - amount) < 0.01 
                                       for t in transactions)
                            
                            if not exists:
                                transactions.append({
                                    'date': f"{date}/2025",
                                    'month': month_name,
                                    'label': label,
                                    'amount': amount,
                                    'type': 'debit'
                                })
                                
                        except ValueError:
                            continue
                            
        except Exception as e:
            print(f"❌ Erreur extraction {pdf_path}: {e}")
        
        return transactions
    
    def categorize_charges(self, transactions):
        """Catégorise les charges BP"""
        categories = {
            'lcr_domiciliees': {
                'patterns': ['lcr domiciliee', 'lcr domicilié'],
                'total': 0, 'transactions': []
            },
            'telecom': {
                'patterns': ['free mobile', 'orange', 'sfr', 'bouygues'],
                'total': 0, 'transactions': []
            },
            'assurances': {
                'patterns': ['swisslife', 'assurance', 'hiscox', 'axa'],
                'total': 0, 'transactions': []
            },
            'impots_taxes': {
                'patterns': ['dgfip', 'impot', 'taxe', 'tresor public'],
                'total': 0, 'transactions': []
            },
            'energie': {
                'patterns': ['edf', 'engie', 'electricite', 'gaz'],
                'total': 0, 'transactions': []
            },
            'carburants': {
                'patterns': ['total market', 'shell', 'esso', 'station'],
                'total': 0, 'transactions': []
            },
            'frais_bancaires': {
                'patterns': ['frais', 'commission', 'cotisation', 'int.parts'],
                'total': 0, 'transactions': []
            },
            'achats_cb': {
                'patterns': ['cb****', 'paiement cb', 'achat cb'],
                'total': 0, 'transactions': []
            },
            'virements': {
                'patterns': ['vir inst', 'vir sepa', 'virement'],
                'total': 0, 'transactions': []
            },
            'autres': {
                'patterns': [],
                'total': 0, 'transactions': []
            }
        }
        
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
                        cat_info['total'] += amount
                        cat_info['transactions'].append(tx)
                        categorized = True
                        break
                
                if categorized:
                    break
            
            if not categorized:
                categories['autres']['total'] += amount
                categories['autres']['transactions'].append(tx)
        
        return categories
    
    def analyze_all_bp(self):
        """Analyse tous les extraits BP"""
        print("📄 ANALYSE CORRECTE BANQUE POPULAIRE")
        print("="*60)
        
        # Focus sur Mai-Juillet 2025
        files_to_analyze = [
            ('20250515', 'Mai 2025'),
            ('20250530', 'Mai 2025'),
            ('20250613', 'Juin 2025'),
            ('20250630', 'Juin 2025'),
            ('20250715', 'Juillet 2025'),
            ('20250731', 'Juillet 2025')
        ]
        
        all_transactions = []
        
        for date_str, month_name in files_to_analyze:
            filename = f"Extrait de compte - 06021516710 - {date_str}.pdf"
            pdf_path = os.path.join(self.extracts_dir, filename)
            
            if os.path.exists(pdf_path):
                print(f"\n📋 Analyse {month_name} ({date_str})...")
                
                transactions = self.extract_transactions_from_pdf(pdf_path, month_name)
                all_transactions.extend(transactions)
                
                # Afficher échantillon
                if transactions:
                    print(f"   ✅ {len(transactions)} transactions")
                    debits = [t for t in transactions if t['type'] == 'debit']
                    for tx in debits[:3]:
                        print(f"     • {abs(tx['amount']):7.2f}€ - {tx['label'][:35]}")
        
        print(f"\n✅ TOTAL: {len(all_transactions)} transactions extraites")
        
        # Catégoriser
        categories = self.categorize_charges(all_transactions)
        
        return all_transactions, categories
    
    def display_analysis(self, categories):
        """Affiche l'analyse BP"""
        print("\n💸 CHARGES BANQUE POPULAIRE (Mai-Juillet 2025)")
        print("="*60)
        
        total_charges = 0
        
        # Ignorer virements car probablement vers Qonto
        for cat_name, cat_info in categories.items():
            if cat_name == 'virements' or cat_info['total'] == 0:
                continue
            
            monthly_avg = cat_info['total'] / 3
            total_charges += monthly_avg
            
            print(f"\n🏷️ {cat_name.replace('_', ' ').upper()}")
            print(f"   Total 3 mois : {cat_info['total']:8.2f}€")
            print(f"   Moyenne/mois : {monthly_avg:8.2f}€")
            
            # Détails
            if cat_info['transactions']:
                for tx in cat_info['transactions'][:2]:
                    print(f"     • {tx['month']} - {abs(tx['amount']):6.2f}€ - {tx['label'][:30]}")
        
        print(f"\n💎 TOTAL CHARGES BP/MOIS : {total_charges:.2f}€")
        
        return total_charges

def main():
    analyzer = BPAnalyzerCorrect()
    
    # Analyser
    transactions, categories = analyzer.analyze_all_bp()
    
    # Afficher
    charges_bp = analyzer.display_analysis(categories)
    
    # CALCUL FINAL AVEC QONTO
    print("\n" + "="*70)
    print("🎯 CALCUL FINAL SEUIL DE RENTABILITÉ")
    print("="*70)
    
    # Charges Qonto (déjà calculées)
    charges_qonto = 11875  # Salaires + URSSAF + impôts + prêt
    
    # Total charges
    charges_totales_actuelles = charges_qonto + charges_bp
    
    print(f"\n💸 CHARGES MENSUELLES RÉELLES:")
    print(f"   Qonto (salaires, URSSAF, impôts) : {charges_qonto:8,.0f}€")
    print(f"   Banque Populaire (autres charges) : {charges_bp:8,.0f}€")
    print(f"   TOTAL CHARGES ACTUELLES           : {charges_totales_actuelles:8,.0f}€")
    
    # Objectifs salariaux
    sebastien_net = 3000
    salarie_net = 2000
    nb_salaries = 2
    ratio_net_to_total = 1.82
    
    objectif_personnel = (sebastien_net + salarie_net * nb_salaries) * ratio_net_to_total
    charges_totales_cibles = charges_totales_actuelles + objectif_personnel
    
    print(f"\n👨‍💼 OBJECTIFS SALARIAUX:")
    print(f"   Sébastien (3000€ net)    : {sebastien_net * ratio_net_to_total:6,.0f}€ charges")
    print(f"   2 salariés (2000€ net)   : {salarie_net * nb_salaries * ratio_net_to_total:6,.0f}€ charges")
    print(f"   TOTAL OBJECTIF PERSONNEL : {objectif_personnel:6,.0f}€")
    
    print(f"\n🎯 CHARGES TOTALES CIBLES:")
    print(f"   Charges actuelles : {charges_totales_actuelles:6,.0f}€")
    print(f"   Objectif salaires : {objectif_personnel:6,.0f}€")
    print(f"   TOTAL CIBLE       : {charges_totales_cibles:6,.0f}€/mois")
    
    # Seuils avec Clockify
    total_hours = 255.8
    rate = 100
    
    print(f"\n📊 SEUILS RENTABILITÉ (base {total_hours:.0f}h Clockify):")
    print("-" * 60)
    
    for ratio in [50, 55, 60, 65, 70, 75, 80]:
        billable_h = total_hours * (ratio / 100)
        revenue = billable_h * rate
        profit = revenue - charges_totales_cibles
        
        status = "✅" if profit > 0 else "❌"
        print(f"  {ratio:2}% facturable : {billable_h:5.1f}h = {revenue:6,.0f}€ → {profit:+7,.0f}€ {status}")
    
    # Seuil critique
    seuil_revenue = charges_totales_cibles
    seuil_hours = seuil_revenue / rate
    seuil_ratio = (seuil_hours / total_hours) * 100
    
    print(f"\n🚨 SEUIL CRITIQUE RÉEL:")
    print(f"  Revenue minimum : {seuil_revenue:6,.0f}€/mois")
    print(f"  Heures minimum  : {seuil_hours:5.1f}h facturable")
    print(f"  Ratio minimum   : {seuil_ratio:5.1f}% facturable")
    
    # Projections Excel août+
    print(f"\n📈 PROJECTIONS EXCEL (estimations):")
    print(f"  Août 2025      : 15,000€ attendu")
    print(f"  Septembre 2025 : 18,000€ attendu")
    
    if 15000 > seuil_revenue:
        print(f"  → Août couvre le seuil de {seuil_revenue:.0f}€ ✅")
    else:
        print(f"  → Août insuffisant, manque {seuil_revenue - 15000:.0f}€ ❌")

if __name__ == "__main__":
    main()
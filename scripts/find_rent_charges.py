#!/usr/bin/env python3
"""
RECHERCHE SPÉCIFIQUE DES LOYERS DANS LES RELEVÉS BP
Recherche ciblée pour trouver les charges de loyer manquées
"""

import os
import re
import pdfplumber
from collections import defaultdict

class RentFinder:
    def __init__(self):
        self.bp_dir = "/home/sq/extraits de compte BP"
        self.rent_transactions = []
        
    def search_rent_in_pdf(self, pdf_path, filename):
        """Recherche spécifique des loyers dans un PDF"""
        print(f"\n🔍 Analyse {filename}...")
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    # Recherche patterns de loyer (insensible à la casse)
                    rent_patterns = [
                        r'loyer',
                        r'sant\s*adiol',
                        r'nimes',
                        r'nîmes',
                        r'immobili',
                        r'sci\s',
                        r'bail',
                        r'location',
                        r'locatif',
                        r'charges\s*locatives',
                        r'taxe\s*habitation',
                        r'foncier'
                    ]
                    
                    lines = text.split('\n')
                    
                    for line_num, line in enumerate(lines):
                        line_lower = line.lower()
                        
                        # Vérifier chaque pattern
                        for pattern in rent_patterns:
                            if re.search(pattern, line_lower):
                                # Extraire montant si présent
                                amount_match = re.search(r'([\d\s]+[,.]\d{2})\s*€', line)
                                
                                # Extraire date si présente
                                date_match = re.search(r'(\d{2}/\d{2})', line)
                                
                                result = {
                                    'file': filename,
                                    'page': page_num + 1,
                                    'line': line_num + 1,
                                    'text': line.strip()[:200],  # Limiter à 200 chars
                                    'pattern_found': pattern,
                                    'amount': None,
                                    'date': None
                                }
                                
                                if amount_match:
                                    amount_str = amount_match.group(1).replace(' ', '').replace(',', '.')
                                    try:
                                        result['amount'] = float(amount_str)
                                    except:
                                        pass
                                
                                if date_match:
                                    result['date'] = date_match.group(1)
                                
                                self.rent_transactions.append(result)
                                
                                # Afficher immédiatement
                                print(f"  🏠 TROUVÉ (page {page_num+1}, ligne {line_num+1}):")
                                print(f"     Pattern: '{pattern}'")
                                print(f"     Texte: {line.strip()[:100]}...")
                                if result['amount']:
                                    print(f"     Montant: {result['amount']:.2f}€")
                                if result['date']:
                                    print(f"     Date: {result['date']}")
                                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    def search_all_pdfs(self):
        """Recherche dans tous les PDFs BP"""
        print("="*70)
        print("🏠 RECHERCHE SPÉCIFIQUE DES LOYERS DANS BANQUE POPULAIRE")
        print("="*70)
        
        # Lister tous les PDFs
        pdf_files = []
        for file in os.listdir(self.bp_dir):
            if file.endswith('.pdf') and not file.endswith('.pdf:Zone.Identifier'):
                pdf_files.append(file)
        
        pdf_files.sort()
        
        print(f"\n📄 {len(pdf_files)} fichiers PDF à analyser:")
        for f in pdf_files:
            print(f"  • {f}")
        
        # Analyser chaque PDF
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.bp_dir, pdf_file)
            self.search_rent_in_pdf(pdf_path, pdf_file)
        
        return self.rent_transactions
    
    def display_results(self):
        """Affiche les résultats consolidés"""
        print("\n" + "="*70)
        print("💰 RÉSULTATS CONSOLIDÉS - CHARGES DE LOYER")
        print("="*70)
        
        if not self.rent_transactions:
            print("\n❌ AUCUNE CHARGE DE LOYER TROUVÉE")
            return 0
        
        # Grouper par montant
        by_amount = defaultdict(list)
        for tx in self.rent_transactions:
            if tx['amount']:
                by_amount[tx['amount']].append(tx)
        
        # Afficher par montant décroissant
        total_rent = 0
        unique_amounts = set()
        
        print(f"\n📊 {len(self.rent_transactions)} occurrences trouvées")
        print("\n🏠 CHARGES IDENTIFIÉES:")
        
        for amount in sorted(by_amount.keys(), reverse=True):
            items = by_amount[amount]
            print(f"\n  💶 {amount:.2f}€ ({len(items)} occurrence(s)):")
            
            # Afficher échantillon
            for item in items[:2]:  # Max 2 exemples par montant
                print(f"    • {item['file'][:30]} - {item['date'] or 'sans date'}")
                print(f"      → {item['text'][:80]}...")
            
            # Compter chaque montant unique une fois (mensuel)
            if amount not in unique_amounts:
                unique_amounts.add(amount)
                total_rent += amount
        
        # Transactions sans montant
        no_amount = [tx for tx in self.rent_transactions if not tx['amount']]
        if no_amount:
            print(f"\n⚠️ {len(no_amount)} occurrences sans montant détectable:")
            for item in no_amount[:3]:
                print(f"  • {item['file'][:30]} (p.{item['page']}, l.{item['line']}):")
                print(f"    → {item['text'][:80]}...")
        
        print(f"\n💎 TOTAL LOYERS IDENTIFIÉS: {total_rent:.2f}€")
        print(f"   (basé sur {len(unique_amounts)} montants uniques)")
        
        # Recherche spécifique Sant Adiol et Nîmes
        sant_adiol = [tx for tx in self.rent_transactions if 'sant' in tx['text'].lower() and 'adiol' in tx['text'].lower()]
        nimes = [tx for tx in self.rent_transactions if 'nimes' in tx['text'].lower() or 'nîmes' in tx['text'].lower()]
        
        if sant_adiol:
            print(f"\n🏢 SANT ADIOL trouvé ({len(sant_adiol)} fois):")
            for item in sant_adiol[:2]:
                print(f"  • {item['date'] or 'sans date'}: {item['amount']:.2f}€ si montant" if item['amount'] else f"  • {item['text'][:100]}")
        
        if nimes:
            print(f"\n🏢 NÎMES trouvé ({len(nimes)} fois):")
            for item in nimes[:2]:
                print(f"  • {item['date'] or 'sans date'}: {item['amount']:.2f}€ si montant" if item['amount'] else f"  • {item['text'][:100]}")
        
        return total_rent

def main():
    """Recherche principale des loyers"""
    finder = RentFinder()
    
    # Rechercher dans tous les PDFs
    transactions = finder.search_all_pdfs()
    
    # Afficher résultats
    total_rent = finder.display_results()
    
    # Calcul final avec loyers
    print("\n" + "="*70)
    print("🎯 MISE À JOUR CALCUL AVEC LOYERS")
    print("="*70)
    
    # Charges déjà identifiées
    charges_qonto = 11875  # Salaires, URSSAF, impôts, prêt
    charges_bp_autres = 1812  # Autres charges BP (hors loyer)
    
    charges_totales = charges_qonto + charges_bp_autres + total_rent
    
    print(f"\n💸 CHARGES MENSUELLES COMPLÈTES:")
    print(f"  Qonto (salaires, charges)  : {charges_qonto:8,.0f}€")
    print(f"  BP autres charges          : {charges_bp_autres:8,.0f}€")
    print(f"  BP loyers                  : {total_rent:8,.0f}€")
    print(f"  TOTAL CHARGES RÉELLES      : {charges_totales:8,.0f}€/mois")
    
    # Objectif salarial
    objectif_sebastien = 3000 * 1.82  # 3000€ net
    charges_cibles = charges_totales + objectif_sebastien
    
    print(f"\n👨‍💼 AVEC OBJECTIF SÉBASTIEN:")
    print(f"  Charges actuelles : {charges_totales:8,.0f}€")
    print(f"  Objectif Sébastien: {objectif_sebastien:8,.0f}€")
    print(f"  TOTAL CIBLE       : {charges_cibles:8,.0f}€/mois")
    
    # Seuil rentabilité
    total_hours = 255.8
    rate = 100
    
    seuil_hours = charges_cibles / rate
    seuil_ratio = (seuil_hours / total_hours) * 100
    
    print(f"\n🚨 SEUIL RENTABILITÉ RÉEL:")
    print(f"  Revenue minimum : {charges_cibles:6,.0f}€/mois")
    print(f"  Heures facturables : {seuil_hours:5.1f}h")
    print(f"  Ratio nécessaire : {seuil_ratio:5.1f}% facturable")
    
    print(f"\n📊 AVEC 255.8h CLOCKIFY:")
    for ratio in [60, 65, 70, 75, 80]:
        revenue = total_hours * (ratio/100) * rate
        profit = revenue - charges_cibles
        status = "✅" if profit > 0 else "❌"
        print(f"  {ratio}% facturable: {revenue:6,.0f}€ → {profit:+6,.0f}€ {status}")

if __name__ == "__main__":
    main()
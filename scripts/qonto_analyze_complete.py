#!/usr/bin/env python3
"""
ANALYSE COMPLÈTE QONTO + BP POUR TOUTES LES CHARGES
Recoupement des deux comptes bancaires
"""

import subprocess
import json
from collections import defaultdict
from datetime import datetime

class CompleteFinancialAnalyzer:
    def __init__(self):
        self.qonto_auth = "syaga-consulting-5172:06f55a4b41d0"
        self.qonto_iban = "FR7616958000018809313999064"
        
    def get_qonto_transactions(self):
        """Récupère les transactions Qonto via curl"""
        print("🔍 Récupération transactions Qonto...")
        
        cmd = [
            'curl', '-s',
            '-H', f'Authorization: {self.qonto_auth}',
            f'https://thirdparty.qonto.com/v2/transactions?status=completed&iban={self.qonto_iban}&per_page=100'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            transactions = data.get('transactions', [])
            
            # Récupérer pages suivantes si nécessaire
            total_pages = data.get('meta', {}).get('total_pages', 1)
            
            for page in range(2, min(total_pages + 1, 6)):  # Max 5 pages
                cmd_page = cmd + [f'&page={page}']
                cmd_page[4] = cmd_page[4] + f'&page={page}'
                
                result = subprocess.run(cmd[:4] + [cmd[4] + f'&page={page}'], 
                                      capture_output=True, text=True)
                page_data = json.loads(result.stdout)
                transactions.extend(page_data.get('transactions', []))
            
            print(f"✅ {len(transactions)} transactions récupérées")
            return transactions
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return []
    
    def analyze_qonto_charges(self, transactions):
        """Analyse les charges Qonto par catégorie"""
        print("\n💳 ANALYSE CHARGES QONTO")
        print("="*60)
        
        categories = {
            'salaires': {
                'patterns': ['hugo joucla', 'romain bastien', 'salaire', 'paie'],
                'total': 0, 'items': []
            },
            'dirigeant': {
                'patterns': ['sebastien questier', 'questier sebastien', 'remuneration dirigeant'],
                'total': 0, 'items': []
            },
            'charges_sociales': {
                'patterns': ['urssaf', 'rsi', 'cpam', 'charges sociales', 'cotisation sociale'],
                'total': 0, 'items': []
            },
            'impots': {
                'patterns': ['dgfip', 'impot', 'taxe', 'cfe', 'cvae', 'tresor public'],
                'total': 0, 'items': []
            },
            'loyers': {
                'patterns': ['loyer', 'sant adiol', 'nimes', 'nîmes', 'immobili', 'sci', 'location', 'bail'],
                'total': 0, 'items': []
            },
            'prets': {
                'patterns': ['riverbank', 'pret', 'emprunt', 'remboursement', 'echeance'],
                'total': 0, 'items': []
            },
            'comptable': {
                'patterns': ['nobelia', 'expert comptable', 'comptable', 'fiduciaire'],
                'total': 0, 'items': []
            },
            'autres': {
                'patterns': [],
                'total': 0, 'items': []
            }
        }
        
        # Analyser chaque transaction
        for tx in transactions:
            if tx.get('side') != 'debit':
                continue
            
            amount = abs(tx.get('amount', 0))
            label = tx.get('label', '').lower()
            date = tx.get('settled_at', '')[:10]
            
            categorized = False
            
            for cat_name, cat_info in categories.items():
                if cat_name == 'autres':
                    continue
                    
                for pattern in cat_info['patterns']:
                    if pattern in label:
                        cat_info['total'] += amount
                        cat_info['items'].append({
                            'date': date,
                            'amount': amount,
                            'label': tx.get('label', '')
                        })
                        categorized = True
                        break
                
                if categorized:
                    break
            
            if not categorized:
                categories['autres']['total'] += amount
                categories['autres']['items'].append({
                    'date': date,
                    'amount': amount,
                    'label': tx.get('label', '')
                })
        
        return categories
    
    def display_complete_analysis(self, qonto_categories):
        """Affiche l'analyse complète des charges"""
        print("\n🎯 SYNTHÈSE COMPLÈTE DES CHARGES")
        print("="*70)
        
        # Filtrer sur les 3 derniers mois
        cutoff_date = '2025-05-01'
        
        print("\n📊 CHARGES QONTO (Mai-Juillet 2025):")
        print("-" * 50)
        
        total_qonto = 0
        
        for cat_name, cat_info in qonto_categories.items():
            if cat_info['total'] == 0:
                continue
            
            # Filtrer items récents
            recent_items = [item for item in cat_info['items'] 
                          if item['date'] >= cutoff_date]
            
            if not recent_items:
                continue
            
            recent_total = sum(item['amount'] for item in recent_items)
            monthly_avg = recent_total / 3  # Sur 3 mois
            
            print(f"\n🏷️ {cat_name.replace('_', ' ').upper()}")
            print(f"  Total 3 mois: {recent_total:8,.2f}€")
            print(f"  Moyenne/mois: {monthly_avg:8,.2f}€")
            
            # Afficher échantillon
            for item in recent_items[:2]:
                print(f"    • {item['date']}: {item['amount']:6.2f}€ - {item['label'][:40]}")
            
            total_qonto += monthly_avg
        
        # Charges BP (déjà calculées)
        charges_bp = 1812  # Hors virements internes
        
        print("\n📊 CHARGES BANQUE POPULAIRE:")
        print("-" * 50)
        print(f"  LCR (achats Ingram)  : Variable")
        print(f"  Télécom/Internet     :    107€/mois")
        print(f"  Assurances           :    147€/mois")
        print(f"  Carburants           :    Variable")
        print(f"  Frais bancaires      :     44€/mois")
        print(f"  Autres               :  1,514€/mois")
        print(f"  TOTAL BP             :  1,812€/mois")
        
        # TOTAL GLOBAL
        total_charges = total_qonto + charges_bp
        
        print("\n" + "="*70)
        print("💎 TOTAL CHARGES MENSUELLES RÉELLES")
        print("="*70)
        print(f"  Qonto : {total_qonto:8,.0f}€/mois")
        print(f"  BP    : {charges_bp:8,.0f}€/mois")
        print(f"  TOTAL : {total_charges:8,.0f}€/mois")
        
        # Calcul seuil rentabilité
        print("\n🎯 SEUIL DE RENTABILITÉ")
        print("="*70)
        
        objectif_sebastien = 3000 * 1.82  # 3000€ net
        objectif_salaries = 2000 * 2 * 1.82  # 2 salariés à 2000€ net
        
        charges_cibles = total_charges + objectif_sebastien + objectif_salaries
        
        print(f"\nCharges actuelles      : {total_charges:8,.0f}€")
        print(f"Objectif Sébastien     : {objectif_sebastien:8,.0f}€ (3000€ net)")
        print(f"Objectif 2 salariés    : {objectif_salaries:8,.0f}€ (2x2000€ net)")
        print(f"TOTAL CIBLE           : {charges_cibles:8,.0f}€/mois")
        
        # Avec Clockify
        total_hours = 255.8
        
        print(f"\n📊 AVEC {total_hours:.0f}H CLOCKIFY:")
        
        for rate in [100, 120, 150]:
            print(f"\n💶 Tarif {rate}€/h:")
            for ratio in [60, 65, 70, 75, 80]:
                revenue = total_hours * (ratio/100) * rate
                profit = revenue - charges_cibles
                status = "✅" if profit > 0 else "❌"
                print(f"  {ratio}% facturable: {revenue:7,.0f}€ → {profit:+7,.0f}€ {status}")
        
        # Seuil critique
        for rate in [100, 120, 150]:
            seuil_hours = charges_cibles / rate
            seuil_ratio = (seuil_hours / total_hours) * 100
            
            print(f"\n🚨 SEUIL à {rate}€/h:")
            print(f"  Heures nécessaires: {seuil_hours:.1f}h")
            print(f"  Ratio nécessaire: {seuil_ratio:.1f}%")

def main():
    """Analyse complète Qonto + BP"""
    print("💰 ANALYSE COMPLÈTE CHARGES QONTO + BANQUE POPULAIRE")
    print("="*70)
    
    analyzer = CompleteFinancialAnalyzer()
    
    # Récupérer transactions Qonto
    qonto_transactions = analyzer.get_qonto_transactions()
    
    if not qonto_transactions:
        print("❌ Impossible de récupérer les transactions Qonto")
        return
    
    # Analyser charges Qonto
    qonto_categories = analyzer.analyze_qonto_charges(qonto_transactions)
    
    # Afficher analyse complète
    analyzer.display_complete_analysis(qonto_categories)
    
    # Message important sur les loyers
    print("\n⚠️ IMPORTANT: Si les loyers n'apparaissent pas dans Qonto,")
    print("   ils peuvent être payés autrement (chèque, virement manuel, etc.)")
    print("   Vérifier avec Sébastien le montant exact des loyers mensuels.")

if __name__ == "__main__":
    main()
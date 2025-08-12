#!/usr/bin/env python3
"""
DÉTAIL COMPLET DE TOUTES LES CHARGES
Analyse ligne par ligne pour identifier les anomalies
"""

import subprocess
import json
from collections import defaultdict
from datetime import datetime

class DetailChargesAnalyzer:
    def __init__(self):
        self.qonto_auth = "syaga-consulting-5172:06f55a4b41d0"
        self.qonto_iban = "FR7616958000018809313999064"
        
    def get_all_charges(self):
        """Récupère TOUTES les charges des 3 derniers mois"""
        print("🔍 EXTRACTION DÉTAILLÉE DE TOUTES LES CHARGES")
        print("="*70)
        print("Période : Mai-Juillet 2025\n")
        
        # Récupérer transactions Qonto
        cmd = [
            'curl', '-s',
            '-H', f'Authorization: {self.qonto_auth}',
            f'https://thirdparty.qonto.com/v2/transactions?status=completed&iban={self.qonto_iban}&per_page=100'
        ]
        
        all_transactions = []
        
        try:
            # Récupérer 3 pages (300 transactions)
            for page in range(1, 4):
                page_cmd = cmd[:4] + [cmd[4] + f'&page={page}']
                result = subprocess.run(page_cmd, capture_output=True, text=True)
                data = json.loads(result.stdout)
                all_transactions.extend(data.get('transactions', []))
            
            print(f"✅ {len(all_transactions)} transactions récupérées\n")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return []
        
        # Filtrer Mai-Juillet 2025 et débits uniquement
        charges = []
        for tx in all_transactions:
            date = tx.get('settled_at', '')
            if date >= '2025-05-01' and date < '2025-08-01' and tx.get('side') == 'debit':
                charges.append(tx)
        
        print(f"📊 {len(charges)} charges identifiées pour Mai-Juillet 2025\n")
        return charges
    
    def categorize_detailed(self, charges):
        """Catégorisation très détaillée"""
        
        categories_detail = {
            'SALAIRES_EMPLOYES': {
                'items': [],
                'patterns': ['hugo joucla', 'romain bastien', 'loan roulph']
            },
            'DIRIGEANT': {
                'items': [],
                'patterns': ['sebastien questier', 'sébastien questier']
            },
            'EX_EMPLOYE': {
                'items': [],
                'patterns': ['pierre questier']
            },
            'URSSAF': {
                'items': [],
                'patterns': ['urssaf']
            },
            'IMPOTS': {
                'items': [],
                'patterns': ['dgfip', 'impot', 'taxe']
            },
            'LOYER_SCI': {
                'items': [],
                'patterns': ['sci qssp', 'sci']
            },
            'LOYER_VILLADATA': {
                'items': [],
                'patterns': ['villadata']
            },
            'PRET_RIVERBANK': {
                'items': [],
                'patterns': ['riverbank', 'remboursement pret']
            },
            'COMPTABLE': {
                'items': [],
                'patterns': ['nobelia']
            },
            'ASSURANCES': {
                'items': [],
                'patterns': ['swisslife', 'hiscox', 'a m v', 'assurance']
            },
            'VIREMENTS_INTERNES': {
                'items': [],
                'patterns': ['syaga consulting bppc', 'virement interne']
            },
            'TELECOM': {
                'items': [],
                'patterns': ['free', 'orange', 'sfr', 'bouygues']
            },
            'MICROSOFT': {
                'items': [],
                'patterns': ['microsoft']
            },
            'SERVICES_IT': {
                'items': [],
                'patterns': ['ovh', 'google', 'claude', 'openai', 'github']
            },
            'ACHATS_DIVERS': {
                'items': [],
                'patterns': ['amazon', 'cdiscount', 'fnac']
            },
            'AUTRES': {
                'items': []
            }
        }
        
        # Catégoriser chaque charge
        for charge in charges:
            label = charge.get('label', '').lower()
            amount = abs(charge.get('amount', 0))
            date = charge.get('settled_at', '')[:10]
            
            categorized = False
            
            for cat_name, cat_data in categories_detail.items():
                if cat_name == 'AUTRES':
                    continue
                    
                for pattern in cat_data.get('patterns', []):
                    if pattern in label:
                        cat_data['items'].append({
                            'date': date,
                            'amount': amount,
                            'label': charge.get('label', '')
                        })
                        categorized = True
                        break
                
                if categorized:
                    break
            
            if not categorized:
                categories_detail['AUTRES']['items'].append({
                    'date': date,
                    'amount': amount,
                    'label': charge.get('label', '')
                })
        
        return categories_detail
    
    def display_detailed_breakdown(self, categories):
        """Affiche le détail complet par catégorie"""
        
        print("💰 DÉTAIL COMPLET DES CHARGES PAR CATÉGORIE")
        print("="*70)
        
        grand_total = 0
        summary = {}
        
        # Afficher chaque catégorie
        for cat_name, cat_data in categories.items():
            if not cat_data['items']:
                continue
            
            total = sum(item['amount'] for item in cat_data['items'])
            monthly = total / 3  # Sur 3 mois
            
            # Formater le nom de catégorie
            display_name = cat_name.replace('_', ' ')
            
            print(f"\n{'='*60}")
            print(f"📁 {display_name}")
            print(f"{'='*60}")
            print(f"Total 3 mois: {total:,.2f}€")
            print(f"Moyenne mensuelle: {monthly:,.2f}€")
            print(f"Nombre de transactions: {len(cat_data['items'])}")
            
            # Détail des transactions
            if len(cat_data['items']) <= 10:
                # Si peu de transactions, tout afficher
                print("\nDétail:")
                for item in sorted(cat_data['items'], key=lambda x: x['date']):
                    print(f"  {item['date']}: {item['amount']:8,.2f}€ - {item['label']}")
            else:
                # Si beaucoup, afficher échantillon
                print("\nÉchantillon (5 plus grosses):")
                sorted_items = sorted(cat_data['items'], key=lambda x: x['amount'], reverse=True)
                for item in sorted_items[:5]:
                    print(f"  {item['date']}: {item['amount']:8,.2f}€ - {item['label']}")
            
            summary[display_name] = monthly
            grand_total += total
        
        # Résumé final
        print("\n" + "="*70)
        print("📊 RÉSUMÉ MENSUEL")
        print("="*70)
        
        # Trier par montant décroissant
        for cat_name, monthly in sorted(summary.items(), key=lambda x: x[1], reverse=True):
            if monthly > 10:  # Ignorer les montants négligeables
                print(f"{cat_name:30} : {monthly:8,.0f}€/mois")
        
        print("-" * 50)
        print(f"{'TOTAL TOUTES CHARGES':30} : {grand_total/3:8,.0f}€/mois")
        
        # Identifier les anomalies
        print("\n" + "="*70)
        print("⚠️ ANOMALIES IDENTIFIÉES")
        print("="*70)
        
        if 'VIREMENTS INTERNES' in summary:
            print(f"❌ Virements internes comptés comme charges: {summary['VIREMENTS INTERNES']:.0f}€/mois")
        
        if 'EX EMPLOYE' in summary:
            print(f"❌ Pierre Questier (parti fin mai): {summary['EX EMPLOYE']:.0f}€/mois")
        
        if 'DIRIGEANT' in summary and summary['DIRIGEANT'] > 1000:
            print(f"⚠️ Vérifier double comptage Sébastien: {summary['DIRIGEANT']:.0f}€/mois")
        
        # Charges réelles après corrections
        charges_reelles = grand_total / 3
        
        # Soustraire les anomalies
        corrections = 0
        if 'VIREMENTS INTERNES' in summary:
            corrections += summary['VIREMENTS INTERNES']
        if 'EX EMPLOYE' in summary:
            corrections += summary['EX EMPLOYE']
        if 'DIRIGEANT' in summary:
            corrections += summary['DIRIGEANT']  # À vérifier si c'est votre salaire ou non
        
        charges_corrigees = charges_reelles - corrections
        
        print("\n" + "="*70)
        print("💎 CHARGES RÉELLES APRÈS CORRECTIONS")
        print("="*70)
        print(f"Total brut : {charges_reelles:,.0f}€/mois")
        print(f"Corrections : -{corrections:,.0f}€/mois")
        print(f"TOTAL NET : {charges_corrigees:,.0f}€/mois")
        
        return summary

def main():
    analyzer = DetailChargesAnalyzer()
    
    # Récupérer toutes les charges
    charges = analyzer.get_all_charges()
    
    if not charges:
        print("❌ Impossible de récupérer les charges")
        return
    
    # Catégoriser en détail
    categories = analyzer.categorize_detailed(charges)
    
    # Afficher le détail complet
    summary = analyzer.display_detailed_breakdown(categories)
    
    # Message final
    print("\n" + "="*70)
    print("💡 NOTES IMPORTANTES:")
    print("  • Les virements internes ne sont PAS des charges")
    print("  • Pierre Questier a quitté fin mai (paiement de sortie)")
    print("  • Vérifier si les paiements à Sébastien sont votre rémunération")
    print("  • La catégorie AUTRES nécessite une revue détaillée")
    print("="*70)

if __name__ == "__main__":
    main()
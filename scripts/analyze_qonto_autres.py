#!/usr/bin/env python3
"""
ANALYSE DÉTAILLÉE CATÉGORIE 'AUTRES' QONTO
Identifier l'anomalie des 17k€/mois
"""

import subprocess
import json
from collections import defaultdict
from datetime import datetime

class QontoAutresAnalyzer:
    def __init__(self):
        self.qonto_auth = "syaga-consulting-5172:06f55a4b41d0"
        self.qonto_iban = "FR7616958000018809313999064"
        
    def get_recent_transactions(self):
        """Récupère les transactions des 3 derniers mois"""
        print("🔍 Récupération transactions Qonto récentes...")
        
        cmd = [
            'curl', '-s',
            '-H', f'Authorization: {self.qonto_auth}',
            f'https://thirdparty.qonto.com/v2/transactions?status=completed&iban={self.qonto_iban}&per_page=100'
        ]
        
        all_transactions = []
        
        try:
            # Récupérer première page
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            all_transactions.extend(data.get('transactions', []))
            
            # Récupérer pages suivantes
            total_pages = min(data.get('meta', {}).get('total_pages', 1), 5)
            
            for page in range(2, total_pages + 1):
                page_cmd = cmd[:4] + [cmd[4] + f'&page={page}']
                result = subprocess.run(page_cmd, capture_output=True, text=True)
                page_data = json.loads(result.stdout)
                all_transactions.extend(page_data.get('transactions', []))
            
            # Filtrer sur Mai-Juillet 2025
            cutoff_date = '2025-05-01'
            recent = [tx for tx in all_transactions 
                     if tx.get('settled_at', '') >= cutoff_date and 
                        tx.get('settled_at', '') < '2025-08-01']
            
            print(f"✅ {len(recent)} transactions Mai-Juillet 2025")
            return recent
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return []
    
    def analyze_autres_category(self, transactions):
        """Analyse détaillée de ce qui tombe dans 'Autres'"""
        print("\n🔍 ANALYSE DÉTAILLÉE CATÉGORIE 'AUTRES'")
        print("="*70)
        
        # Patterns des catégories connues (pour exclure)
        known_patterns = [
            'hugo joucla', 'romain bastien', 'salaire', 'paie',
            'sebastien questier', 'questier sebastien', 'remuneration dirigeant',
            'urssaf', 'rsi', 'cpam', 'charges sociales', 'cotisation sociale',
            'dgfip', 'impot', 'taxe', 'cfe', 'cvae', 'tresor public',
            'loyer', 'sant adiol', 'nimes', 'nîmes', 'immobili', 'sci', 'location', 'bail',
            'riverbank', 'pret', 'emprunt', 'remboursement', 'echeance',
            'nobelia', 'expert comptable', 'comptable', 'fiduciaire'
        ]
        
        autres_transactions = []
        
        # Identifier transactions non catégorisées
        for tx in transactions:
            if tx.get('side') != 'debit':
                continue
            
            label = tx.get('label', '').lower()
            
            # Vérifier si c'est vraiment "autre"
            is_known = False
            for pattern in known_patterns:
                if pattern in label:
                    is_known = True
                    break
            
            if not is_known:
                autres_transactions.append(tx)
        
        # Analyser par groupes
        by_label = defaultdict(list)
        by_amount_range = defaultdict(list)
        by_category = defaultdict(list)
        
        total_autres = 0
        
        for tx in autres_transactions:
            amount = abs(tx.get('amount', 0))
            label = tx.get('label', '')
            category = tx.get('category', 'unknown')
            date = tx.get('settled_at', '')[:10]
            
            total_autres += amount
            
            # Grouper par label similaire
            label_key = label.split('#')[0].strip()[:30]
            by_label[label_key].append({
                'date': date,
                'amount': amount,
                'full_label': label
            })
            
            # Grouper par range de montant
            if amount < 100:
                range_key = '< 100€'
            elif amount < 500:
                range_key = '100-500€'
            elif amount < 1000:
                range_key = '500-1000€'
            elif amount < 5000:
                range_key = '1000-5000€'
            else:
                range_key = '> 5000€'
            
            by_amount_range[range_key].append({
                'date': date,
                'amount': amount,
                'label': label
            })
            
            # Grouper par catégorie Qonto
            by_category[category].append({
                'date': date,
                'amount': amount,
                'label': label
            })
        
        # Afficher résultats
        print(f"\n💸 TOTAL 'AUTRES': {total_autres:.2f}€ sur 3 mois")
        print(f"   Moyenne mensuelle: {total_autres/3:.2f}€")
        print(f"   Nombre de transactions: {len(autres_transactions)}")
        
        # Top 10 plus grosses transactions
        print("\n🔝 TOP 10 PLUS GROSSES TRANSACTIONS 'AUTRES':")
        print("-" * 60)
        
        sorted_tx = sorted(autres_transactions, 
                          key=lambda x: abs(x.get('amount', 0)), 
                          reverse=True)
        
        for tx in sorted_tx[:10]:
            amount = abs(tx.get('amount', 0))
            label = tx.get('label', '')
            date = tx.get('settled_at', '')[:10]
            category = tx.get('category', 'unknown')
            
            print(f"\n  {date}: {amount:8,.2f}€")
            print(f"  {label}")
            print(f"  Catégorie Qonto: {category}")
        
        # Groupement par label fréquent
        print("\n🔄 TRANSACTIONS RÉCURRENTES:")
        print("-" * 60)
        
        for label_key, items in sorted(by_label.items(), 
                                      key=lambda x: sum(i['amount'] for i in x[1]),
                                      reverse=True)[:5]:
            total = sum(item['amount'] for item in items)
            count = len(items)
            
            if count > 1:
                print(f"\n'{label_key}...' ({count} fois = {total:.2f}€ total)")
                for item in items[:2]:
                    print(f"  • {item['date']}: {item['amount']:.2f}€")
        
        # Distribution par montant
        print("\n📊 DISTRIBUTION PAR MONTANT:")
        print("-" * 60)
        
        for range_key in ['< 100€', '100-500€', '500-1000€', '1000-5000€', '> 5000€']:
            items = by_amount_range.get(range_key, [])
            if items:
                total = sum(item['amount'] for item in items)
                print(f"\n{range_key:12} : {len(items):3} tx = {total:8,.2f}€")
                # Exemple
                if items:
                    ex = items[0]
                    print(f"  Ex: {ex['label'][:50]}...")
        
        # Par catégorie Qonto
        print("\n🏷️ PAR CATÉGORIE QONTO:")
        print("-" * 60)
        
        for category, items in sorted(by_category.items(),
                                     key=lambda x: sum(i['amount'] for i in x[1]),
                                     reverse=True)[:5]:
            total = sum(item['amount'] for item in items)
            print(f"\n{category:30} : {len(items):3} tx = {total:8,.2f}€")
            # Exemple
            if items:
                ex = items[0]
                print(f"  Ex: {ex['label'][:50]}...")
        
        return total_autres

def main():
    """Analyse principale de la catégorie Autres"""
    print("🔎 INVESTIGATION ANOMALIE 17K€/MOIS")
    print("="*70)
    
    analyzer = QontoAutresAnalyzer()
    
    # Récupérer transactions récentes
    transactions = analyzer.get_recent_transactions()
    
    if not transactions:
        print("❌ Pas de transactions récupérées")
        return
    
    # Analyser catégorie Autres
    total_autres = analyzer.analyze_autres_category(transactions)
    
    # Conclusion
    print("\n" + "="*70)
    print("💡 CONCLUSION")
    print("="*70)
    
    monthly = total_autres / 3
    
    if monthly > 10000:
        print(f"\n⚠️ ALERTE: {monthly:.0f}€/mois en 'Autres' est ANORMAL")
        print("   → Vérifier les grosses transactions non catégorisées")
        print("   → Possible inclusion de virements internes ou remboursements")
        print("   → Revoir la catégorisation avec Sébastien")
    else:
        print(f"\n✅ {monthly:.0f}€/mois en 'Autres' semble normal")
        print("   (achats divers, fournitures, services ponctuels)")

if __name__ == "__main__":
    main()
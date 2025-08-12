#!/usr/bin/env python3
"""
RECHERCHE DES LOYERS DANS QONTO
Analyse des transactions Qonto pour identifier les charges de loyer
"""

import urllib.request
import urllib.parse
import json
import os
from datetime import datetime, timedelta

class QontoRentFinder:
    def __init__(self):
        # Charger config depuis fichier temporaire
        config_file = '/home/sq/.qonto_temp_config'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                lines = f.readlines()
                self.login = lines[0].strip()
                self.secret = lines[1].strip()
        else:
            # Config directe si fichier absent
            self.login = 'syaga-consulting-5172'
            self.secret = '06f55a4b41d0'
        
        self.base_url = 'https://thirdparty.qonto.com/v2'
        self.auth_header = f'{self.login}:{self.secret}'
        
    def get_transactions(self, months_back=6):
        """Récupère les transactions sur N mois"""
        print("🔍 Récupération transactions Qonto...")
        
        # Paramètres simples pour toutes les transactions
        params = {
            'status': 'completed',
            'iban': 'FR7616958000018809313999064',
            'per_page': '100'
        }
        
        all_transactions = []
        page = 1
        
        while True:
            url = f"{self.base_url}/transactions?{urllib.parse.urlencode(params)}&page={page}"
            
            try:
                request = urllib.request.Request(url)
                request.add_header('Authorization', self.auth_header)
                request.add_header('Accept', 'application/json')
                
                with urllib.request.urlopen(request) as response:
                    data = json.loads(response.read())
                    transactions = data.get('transactions', [])
                    all_transactions.extend(transactions)
                    
                    # Vérifier s'il y a d'autres pages
                    meta = data.get('meta', {})
                    if meta.get('next_page'):
                        page += 1
                        if page > 5:  # Limiter à 5 pages (500 transactions)
                            break
                    else:
                        break
                        
            except Exception as e:
                print(f"❌ Erreur API page {page}: {e}")
                break
        
        # Filtrer sur les derniers mois
        cutoff_date = (datetime.now() - timedelta(days=months_back * 30)).isoformat()
        filtered = [tx for tx in all_transactions 
                   if tx.get('settled_at', '') >= cutoff_date]
        
        return filtered
    
    def find_rent_transactions(self, transactions):
        """Identifie les transactions de loyer"""
        print("\n🏠 RECHERCHE DES LOYERS DANS QONTO")
        print("="*60)
        
        rent_keywords = [
            'loyer', 'sant adiol', 'nimes', 'nîmes', 
            'immobili', 'sci', 'location', 'bail',
            'locatif', 'habitation', 'foncier', 'rent',
            'property', 'real estate', 'lease'
        ]
        
        rent_transactions = []
        
        for tx in transactions:
            # Récupérer les infos de base
            amount = abs(tx.get('amount', 0))
            label = tx.get('label', '')
            reference = tx.get('reference', '')
            settled_at = tx.get('settled_at', '')
            side = tx.get('side', '')
            
            # Ne garder que les débits
            if side != 'debit':
                continue
            
            # Chercher mots-clés dans label et reference
            full_text = f"{label} {reference}".lower()
            
            for keyword in rent_keywords:
                if keyword in full_text:
                    # Date formatée
                    date = settled_at[:10] if settled_at else 'N/A'
                    
                    rent_transactions.append({
                        'date': date,
                        'amount': amount,
                        'label': label,
                        'reference': reference,
                        'keyword': keyword
                    })
                    
                    print(f"\n✅ TROUVÉ - Mot-clé: '{keyword}'")
                    print(f"   Date: {date}")
                    print(f"   Montant: {amount:.2f}€")
                    print(f"   Libellé: {label}")
                    if reference:
                        print(f"   Référence: {reference}")
                    break
        
        return rent_transactions
    
    def analyze_all_transactions(self, transactions):
        """Analyse complète de toutes les transactions pour patterns"""
        print("\n📊 ANALYSE COMPLÈTE DES TRANSACTIONS QONTO")
        print("="*60)
        
        # Grouper par montant pour identifier patterns récurrents
        by_amount = {}
        
        for tx in transactions:
            if tx.get('side') != 'debit':
                continue
                
            amount = abs(tx.get('amount', 0))
            label = tx.get('label', '')
            
            # Arrondir à l'euro près pour grouper
            amount_key = round(amount)
            
            if amount_key not in by_amount:
                by_amount[amount_key] = []
            
            by_amount[amount_key].append({
                'date': tx.get('settled_at', '')[:10],
                'amount': amount,
                'label': label
            })
        
        # Afficher les montants récurrents (possibles loyers)
        print("\n🔄 TRANSACTIONS RÉCURRENTES (possibles loyers):")
        
        for amount_key in sorted(by_amount.keys(), reverse=True):
            items = by_amount[amount_key]
            
            # Si montant apparaît plusieurs fois, peut être un loyer
            if len(items) >= 2 and amount_key > 500:  # Loyer probable > 500€
                print(f"\n💰 {amount_key}€ environ ({len(items)} occurrences):")
                
                # Afficher échantillon
                for item in items[:3]:
                    print(f"   • {item['date']}: {item['amount']:.2f}€")
                    print(f"     → {item['label'][:60]}...")
        
        # Afficher TOUTES les grosses transactions (>1000€)
        print("\n💸 GROSSES TRANSACTIONS (>1000€):")
        
        big_transactions = []
        for tx in transactions:
            if tx.get('side') == 'debit' and abs(tx.get('amount', 0)) > 1000:
                big_transactions.append(tx)
        
        # Trier par montant décroissant
        big_transactions.sort(key=lambda x: abs(x.get('amount', 0)), reverse=True)
        
        for tx in big_transactions[:10]:  # Top 10
            amount = abs(tx.get('amount', 0))
            label = tx.get('label', '')
            date = tx.get('settled_at', '')[:10]
            
            print(f"\n   {date}: {amount:.2f}€")
            print(f"   → {label}")

def main():
    """Recherche principale des loyers dans Qonto"""
    print("💳 ANALYSE QONTO POUR RECHERCHE LOYERS")
    print("="*70)
    
    finder = QontoRentFinder()
    
    # Récupérer transactions
    transactions = finder.get_transactions(months_back=5)
    
    if not transactions:
        print("❌ Aucune transaction récupérée")
        return
    
    print(f"✅ {len(transactions)} transactions récupérées")
    
    # Rechercher loyers par mots-clés
    rent_transactions = finder.find_rent_transactions(transactions)
    
    # Analyser toutes les transactions pour patterns
    finder.analyze_all_transactions(transactions)
    
    # Calculer total loyers
    if rent_transactions:
        print("\n" + "="*60)
        print("💎 SYNTHÈSE LOYERS IDENTIFIÉS")
        print("="*60)
        
        # Calculer moyenne mensuelle
        total = sum(tx['amount'] for tx in rent_transactions)
        monthly_avg = total / 5 if len(rent_transactions) > 0 else 0
        
        print(f"\nTotal sur période: {total:.2f}€")
        print(f"Moyenne mensuelle: {monthly_avg:.2f}€")
        
        # Mise à jour calcul avec loyers
        print("\n🎯 MISE À JOUR CALCUL SEUIL RENTABILITÉ")
        print("="*60)
        
        charges_qonto_base = 11875  # Sans loyers
        charges_bp = 1812
        charges_loyers = monthly_avg
        
        charges_totales = charges_qonto_base + charges_bp + charges_loyers
        
        print(f"\n💸 CHARGES COMPLÈTES:")
        print(f"  Qonto (salaires, charges): {charges_qonto_base:8,.0f}€")
        print(f"  Qonto (loyers)           : {charges_loyers:8,.0f}€")
        print(f"  BP (autres)              : {charges_bp:8,.0f}€")
        print(f"  TOTAL                    : {charges_totales:8,.0f}€/mois")
        
        # Calcul seuil
        objectif_sebastien = 3000 * 1.82
        charges_cibles = charges_totales + objectif_sebastien
        
        print(f"\n🎯 SEUIL RENTABILITÉ:")
        print(f"  Charges actuelles : {charges_totales:8,.0f}€")
        print(f"  Objectif Sébastien: {objectif_sebastien:8,.0f}€")
        print(f"  TOTAL CIBLE       : {charges_cibles:8,.0f}€/mois")
        
        # Ratio nécessaire
        total_hours = 255.8
        rate = 100
        seuil_ratio = (charges_cibles / rate / total_hours) * 100
        
        print(f"\n📊 Avec 255.8h Clockify:")
        print(f"  Ratio nécessaire: {seuil_ratio:.1f}% facturable")
        print(f"  Heures facturables: {charges_cibles/rate:.1f}h")

if __name__ == "__main__":
    main()
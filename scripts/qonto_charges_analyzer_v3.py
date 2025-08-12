#!/usr/bin/env python3
"""
ANALYSEUR CHARGES QONTO V3 - Selon Documentation Officielle
Authentification correcte + extraction transactions par compte
"""

import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

class QontoChargesAnalyzerV3:
    def __init__(self):
        """Initialise avec credentials selon doc officielle"""
        self.login = "syaga-consulting-5172"
        self.secret_key = "06f55a4b41d0"
        self.base_url = "https://thirdparty.qonto.com/v2"
        
        # Format auth qui fonctionne (trouvé par test)
        self.headers = {
            'Authorization': f'{self.login}:{self.secret_key}',
            'Content-Type': 'application/json'
        }
        
    def get_organization(self):
        """Récupère infos organisation et comptes"""
        try:
            response = requests.get(
                f"{self.base_url}/organization",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Organisation: {data.get('organization', {}).get('legal_name', 'Inconnue')}")
                
                # Extraire les comptes bancaires
                bank_accounts = data.get('organization', {}).get('bank_accounts', [])
                print(f"📊 {len(bank_accounts)} comptes bancaires trouvés:")
                
                for account in bank_accounts:
                    name = account.get('name', 'Sans nom')
                    balance = account.get('balance_cents', 0) / 100
                    currency = account.get('currency', 'EUR')
                    account_id = account.get('id', '')
                    iban = account.get('iban', '')
                    
                    print(f"  - {name}: {balance:,.2f} {currency} (ID: {account_id})")
                
                return data, bank_accounts
            else:
                print(f"❌ Erreur organisation: {response.status_code} - {response.text}")
                return None, []
                
        except Exception as e:
            print(f"❌ Erreur récupération organisation: {e}")
            return None, []
    
    def get_transactions_by_account(self, bank_accounts, months=3):
        """Récupère transactions pour chaque compte"""
        print(f"\n🔍 EXTRACTION TRANSACTIONS ({months} mois)")
        print("="*50)
        
        # Période
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        all_transactions = []
        
        for account in bank_accounts:
            account_id = account.get('id')
            account_name = account.get('name', 'Sans nom')
            
            if not account_id:
                continue
                
            print(f"\n📄 Compte: {account_name} (ID: {account_id})")
            
            # Paramètres avec account_id selon doc
            params = {
                'bank_account_id': account_id,
                'settled_at_from': start_date.strftime('%Y-%m-%dT00:00:00.000Z'),
                'settled_at_to': end_date.strftime('%Y-%m-%dT23:59:59.999Z'),
                'per_page': 100,
                'current_page': 1
            }
            
            page = 1
            account_transactions = []
            
            while True:
                params['current_page'] = page
                
                try:
                    response = requests.get(
                        f"{self.base_url}/transactions",
                        headers=self.headers,
                        params=params,
                        timeout=15
                    )
                    
                    if response.status_code != 200:
                        print(f"   ❌ Erreur page {page}: {response.status_code} - {response.text}")
                        break
                    
                    data = response.json()
                    transactions = data.get('transactions', [])
                    
                    if not transactions:
                        break
                    
                    account_transactions.extend(transactions)
                    print(f"   📄 Page {page}: {len(transactions)} transactions")
                    
                    # Pagination
                    meta = data.get('meta', {})
                    if page >= meta.get('total_pages', 1):
                        break
                    
                    page += 1
                    
                except Exception as e:
                    print(f"   ❌ Erreur page {page}: {e}")
                    break
            
            print(f"   ✅ Total compte {account_name}: {len(account_transactions)} transactions")
            
            # Ajouter info compte à chaque transaction
            for tx in account_transactions:
                tx['account_name'] = account_name
                tx['account_id'] = account_id
            
            all_transactions.extend(account_transactions)
        
        print(f"\n✅ TOTAL GÉNÉRAL: {len(all_transactions)} transactions récupérées")
        return all_transactions
    
    def categorize_charges(self, transactions):
        """Catégorise les charges par type"""
        print(f"\n📊 CATÉGORISATION DES CHARGES")
        print("="*50)
        
        categories = {
            'salaires_charges_sociales': {
                'keywords': ['salaire', 'paie', 'remuneration', 'urssaf', 'charges sociales', 'msa', 'pole emploi', 'retraite'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'loyers_bureaux': {
                'keywords': ['loyer', 'bail', 'location bureau', 'immobilier'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'assurances': {
                'keywords': ['assurance', 'responsabilité civile', 'mutuelle', 'prévoyance'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'telecom_internet': {
                'keywords': ['orange', 'sfr', 'bouygues', 'free', 'téléphone', 'internet', 'mobile'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'logiciels_licences': {
                'keywords': ['microsoft', 'office', 'adobe', 'saas', 'licence', 'abonnement'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'comptable_juridique': {
                'keywords': ['comptable', 'expert comptable', 'fiduciaire', 'avocat', 'notaire'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'frais_bancaires': {
                'keywords': ['commission', 'frais bancaire', 'virement', 'agios', 'carte bancaire'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'materiel_informatique': {
                'keywords': ['ordinateur', 'serveur', 'matériel', 'hardware', 'imprimante'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'transport_deplacement': {
                'keywords': ['essence', 'péage', 'train', 'avion', 'uber', 'taxi', 'parking'],
                'total': 0, 'count': 0, 'transactions': []
            },
            'autres_charges': {
                'keywords': [], 'total': 0, 'count': 0, 'transactions': []
            },
            'recettes_clients': {
                'keywords': [], 'total': 0, 'count': 0, 'transactions': []
            }
        }
        
        for transaction in transactions:
            amount_cents = transaction.get('amount_cents', 0)
            amount = amount_cents / 100
            label = transaction.get('label', '').lower()
            side = transaction.get('side', '')
            date = transaction.get('settled_at', '')[:10]
            account = transaction.get('account_name', 'Inconnu')
            
            if abs(amount) < 0.01:
                continue
            
            categorized = False
            
            # Recettes (crédit positif)
            if side == 'credit' and amount > 0:
                categories['recettes_clients']['total'] += amount
                categories['recettes_clients']['count'] += 1
                categories['recettes_clients']['transactions'].append({
                    'date': date,
                    'label': transaction.get('label', ''),
                    'amount': amount,
                    'account': account
                })
                categorized = True
            
            # Charges (débit négatif)
            elif side == 'debit' and amount < 0:
                amount = abs(amount)
                
                for category, info in categories.items():
                    if category in ['autres_charges', 'recettes_clients']:
                        continue
                        
                    for keyword in info['keywords']:
                        if keyword in label:
                            info['total'] += amount
                            info['count'] += 1
                            info['transactions'].append({
                                'date': date,
                                'label': transaction.get('label', ''),
                                'amount': amount,
                                'account': account
                            })
                            categorized = True
                            break
                    
                    if categorized:
                        break
                
                if not categorized:
                    categories['autres_charges']['total'] += amount
                    categories['autres_charges']['count'] += 1
                    categories['autres_charges']['transactions'].append({
                        'date': date,
                        'label': transaction.get('label', ''),
                        'amount': amount,
                        'account': account
                    })
        
        return categories
    
    def analyze_charges_mensuelles(self, categories):
        """Analyse charges mensuelles moyennes"""
        print(f"\n💰 ANALYSE CHARGES MENSUELLES")
        print("="*60)
        
        months = 3
        total_charges = 0
        total_recettes = 0
        
        print(f"\n🏢 CHARGES PAR CATÉGORIE (moyenne/mois sur {months} mois):")
        print("-" * 65)
        
        for category, info in categories.items():
            if category == 'recettes_clients':
                continue
                
            monthly_avg = info['total'] / months
            total_charges += monthly_avg
            
            if info['count'] > 0:
                print(f"{category.replace('_', ' ').upper():25} : {monthly_avg:8,.0f}€ ({info['count']:2} transactions)")
                
                # Détail pour catégories importantes
                if monthly_avg > 200:
                    for tx in info['transactions'][-2:]:
                        print(f"   └─ {tx['date']} - {tx['label'][:35]:35} : {tx['amount']:6,.0f}€ ({tx['account']})")
        
        monthly_recettes = categories['recettes_clients']['total'] / months
        
        print(f"\n💎 RÉSUMÉ FINANCIER MENSUEL:")
        print("-" * 40)
        print(f"💰 Recettes moyennes : {monthly_recettes:8,.0f}€/mois")
        print(f"💸 Charges moyennes  : {total_charges:8,.0f}€/mois")
        print(f"📊 Résultat moyen    : {monthly_recettes - total_charges:+8,.0f}€/mois")
        
        return {
            'charges_mensuelles_actuelles': total_charges,
            'recettes_mensuelles': monthly_recettes,
            'resultat_mensuel_actuel': monthly_recettes - total_charges,
            'categories': categories
        }
    
    def calculate_seuil_rentabilite(self, charges_actuelles):
        """Calcule seuil de rentabilité avec objectifs"""
        print(f"\n🎯 CALCUL SEUIL DE RENTABILITÉ")
        print("="*50)
        
        # Objectifs salariaux
        sebastien_net = 3000
        salarie_net = 2000
        nb_salaries = 2
        
        # Conversion net → total charges (approximation France)
        ratio_net_to_total = 1.82  # Net × 1.82 ≈ Total charges employeur
        
        sebastien_charges = sebastien_net * ratio_net_to_total
        salaries_charges = salarie_net * nb_salaries * ratio_net_to_total
        total_personnel = sebastien_charges + salaries_charges
        
        charges_totales_cible = charges_actuelles + total_personnel
        
        print(f"👨‍💼 OBJECTIFS SALARIAUX:")
        print(f"  Sébastien    : {sebastien_net:4,.0f}€ net → {sebastien_charges:6,.0f}€ total")
        print(f"  2 salariés   : {salarie_net:4,.0f}€ net × {nb_salaries} → {salaries_charges:6,.0f}€ total")
        print(f"  TOTAL ÉQUIPE : {total_personnel:6,.0f}€/mois")
        
        print(f"\n💸 CHARGES TOTALES CIBLES:")
        print(f"  Charges actuelles : {charges_actuelles:6,.0f}€/mois")
        print(f"  Charges personnel : {total_personnel:6,.0f}€/mois") 
        print(f"  TOTAL CHARGES     : {charges_totales_cible:6,.0f}€/mois")
        
        # Seuils avec Clockify
        total_hours = 255.8
        rate = 100
        
        print(f"\n📊 SEUILS RENTABILITÉ (base {total_hours}h Clockify, {rate}€/h):")
        print("-" * 65)
        
        for ratio in [50, 55, 60, 65, 70]:
            billable_h = total_hours * (ratio / 100)
            revenue = billable_h * rate
            profit = revenue - charges_totales_cible
            
            status = "✅ RENTABLE" if profit > 0 else "❌ DÉFICIT"
            print(f"  {ratio:2}% facturable : {billable_h:5.1f}h = {revenue:6,.0f}€ → {profit:+7,.0f}€ {status}")
        
        # Seuil critique exact
        seuil_revenue = charges_totales_cible
        seuil_hours = seuil_revenue / rate
        seuil_ratio = (seuil_hours / total_hours) * 100
        
        print(f"\n🚨 SEUIL CRITIQUE:")
        print(f"  Revenue minimum : {seuil_revenue:6,.0f}€/mois")
        print(f"  Heures minimum  : {seuil_hours:5.1f}h facturable/mois")
        print(f"  Ratio minimum   : {seuil_ratio:5.1f}% facturable")
        
        return {
            'charges_actuelles': charges_actuelles,
            'charges_personnel_cible': total_personnel,
            'charges_totales_cible': charges_totales_cible,
            'seuil_revenue': seuil_revenue,
            'seuil_hours': seuil_hours,
            'seuil_ratio': seuil_ratio
        }

def main():
    """Analyse complète Qonto"""
    print("🏦 ANALYSEUR CHARGES QONTO V3 - SEUIL DE RENTABILITÉ")
    print("="*65)
    
    analyzer = QontoChargesAnalyzerV3()
    
    try:
        # 1. Organisation et comptes
        org_data, bank_accounts = analyzer.get_organization()
        if not bank_accounts:
            print("❌ Aucun compte bancaire trouvé")
            return
        
        # 2. Transactions
        transactions = analyzer.get_transactions_by_account(bank_accounts, months=3)
        if not transactions:
            print("❌ Aucune transaction trouvée")
            return
        
        # 3. Catégorisation
        categories = analyzer.categorize_charges(transactions)
        
        # 4. Analyse mensuelle
        monthly_analysis = analyzer.analyze_charges_mensuelles(categories)
        
        # 5. Seuil de rentabilité
        seuil_analysis = analyzer.calculate_seuil_rentabilite(
            monthly_analysis['charges_mensuelles_actuelles']
        )
        
        # 6. Résumé final
        print(f"\n🎉 ANALYSE TERMINÉE")
        print(f"Transactions analysées : {len(transactions)}")
        print(f"Charges actuelles      : {monthly_analysis['charges_mensuelles_actuelles']:,.0f}€/mois")
        print(f"Seuil facturable       : {seuil_analysis['seuil_ratio']:.1f}%")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
ANALYSE COMPLETE QONTO + EXCEL - Toutes charges + Revenus attendus
Analyse exhaustive des dépenses + projection Excel facturation
"""

import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict
import re

class QontoCompleteAnalysis:
    def __init__(self):
        self.login = "syaga-consulting-5172"
        self.secret_key = "06f55a4b41d0"
        self.base_url = "https://thirdparty.qonto.com/v2"
        self.headers = {
            'Authorization': f'{self.login}:{self.secret_key}',
            'Content-Type': 'application/json'
        }
        
    def get_all_transactions(self, months=3):
        """Récupère toutes les transactions avec plus de détails"""
        print(f"🔍 EXTRACTION COMPLETE TRANSACTIONS ({months} mois)")
        print("="*60)
        
        # Organisation et comptes
        org_response = requests.get(f"{self.base_url}/organization", headers=self.headers)
        if org_response.status_code != 200:
            return []
            
        org_data = org_response.json()
        bank_accounts = org_data.get('organization', {}).get('bank_accounts', [])
        
        # Période
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        all_transactions = []
        
        for account in bank_accounts:
            account_id = account.get('id')
            account_name = account.get('name', 'Sans nom')
            
            params = {
                'bank_account_id': account_id,
                'settled_at_from': start_date.strftime('%Y-%m-%dT00:00:00.000Z'),
                'settled_at_to': end_date.strftime('%Y-%m-%dT23:59:59.999Z'),
                'per_page': 100,
                'current_page': 1
            }
            
            page = 1
            while True:
                params['current_page'] = page
                
                response = requests.get(f"{self.base_url}/transactions", headers=self.headers, params=params)
                if response.status_code != 200:
                    break
                
                data = response.json()
                transactions = data.get('transactions', [])
                if not transactions:
                    break
                
                for tx in transactions:
                    tx['account_name'] = account_name
                    tx['account_id'] = account_id
                
                all_transactions.extend(transactions)
                
                meta = data.get('meta', {})
                if page >= meta.get('total_pages', 1):
                    break
                page += 1
        
        print(f"✅ {len(all_transactions)} transactions récupérées")
        return all_transactions
    
    def detailed_categorization(self, transactions):
        """Catégorisation très détaillée de TOUTES les charges"""
        print(f"\n📊 CATÉGORISATION EXHAUSTIVE DES CHARGES")
        print("="*60)
        
        categories = {
            'salaires_charges_sociales': {
                'patterns': [
                    r'.*salaire.*', r'.*paie.*', r'.*remuneration.*', r'.*urssaf.*', 
                    r'.*charges\s+sociales.*', r'.*msa.*', r'.*pole\s+emploi.*', 
                    r'.*retraite.*', r'.*cpam.*', r'.*caf.*'
                ],
                'total': 0, 'transactions': []
            },
            'loyers_immobilier': {
                'patterns': [
                    r'.*loyer.*', r'.*bail.*', r'.*location.*', r'.*immobilier.*',
                    r'.*bureau.*', r'.*local.*', r'.*foncier.*'
                ],
                'total': 0, 'transactions': []
            },
            'assurances_mutuelles': {
                'patterns': [
                    r'.*assurance.*', r'.*responsabilité.*', r'.*mutuelle.*', 
                    r'.*prévoyance.*', r'.*axa.*', r'.*allianz.*', r'.*maaf.*',
                    r'.*generali.*', r'.*groupama.*'
                ],
                'total': 0, 'transactions': []
            },
            'vehicules_transport': {
                'patterns': [
                    r'.*essence.*', r'.*gasoil.*', r'.*carburant.*', r'.*péage.*',
                    r'.*autoroute.*', r'.*parking.*', r'.*voiture.*', r'.*vehicule.*',
                    r'.*total\s+.*', r'.*shell.*', r'.*esso.*', r'.*bp.*',
                    r'.*train.*', r'.*sncf.*', r'.*avion.*', r'.*uber.*', r'.*taxi.*'
                ],
                'total': 0, 'transactions': []
            },
            'telecom_internet': {
                'patterns': [
                    r'.*orange.*', r'.*sfr.*', r'.*bouygues.*', r'.*free.*',
                    r'.*téléphone.*', r'.*telephone.*', r'.*internet.*', r'.*mobile.*',
                    r'.*fibre.*', r'.*adsl.*', r'.*box.*'
                ],
                'total': 0, 'transactions': []
            },
            'logiciels_licences': {
                'patterns': [
                    r'.*microsoft.*', r'.*office.*', r'.*adobe.*', r'.*licence.*',
                    r'.*abonnement.*', r'.*saas.*', r'.*software.*', r'.*logiciel.*',
                    r'.*google.*', r'.*amazon.*', r'.*aws.*', r'.*azure.*'
                ],
                'total': 0, 'transactions': []
            },
            'comptable_juridique': {
                'patterns': [
                    r'.*comptable.*', r'.*expert.*comptable.*', r'.*fiduciaire.*',
                    r'.*avocat.*', r'.*notaire.*', r'.*juridique.*', r'.*conseil.*'
                ],
                'total': 0, 'transactions': []
            },
            'frais_bancaires': {
                'patterns': [
                    r'.*commission.*', r'.*frais.*banc.*', r'.*virement.*',
                    r'.*agios.*', r'.*carte.*banc.*', r'.*prélèvement.*'
                ],
                'total': 0, 'transactions': []
            },
            'materiel_equipement': {
                'patterns': [
                    r'.*ordinateur.*', r'.*serveur.*', r'.*matériel.*', r'.*hardware.*',
                    r'.*imprimante.*', r'.*écran.*', r'.*clavier.*', r'.*souris.*',
                    r'.*dell.*', r'.*hp.*', r'.*lenovo.*', r'.*apple.*'
                ],
                'total': 0, 'transactions': []
            },
            'energie_utilities': {
                'patterns': [
                    r'.*electricité.*', r'.*electrique.*', r'.*edf.*', r'.*engie.*',
                    r'.*gaz.*', r'.*eau.*', r'.*chauffage.*'
                ],
                'total': 0, 'transactions': []
            },
            'repas_restauration': {
                'patterns': [
                    r'.*restaurant.*', r'.*repas.*', r'.*déjeuner.*', r'.*resto.*',
                    r'.*mcdo.*', r'.*quick.*', r'.*boulang.*', r'.*café.*'
                ],
                'total': 0, 'transactions': []
            },
            'autres_charges': {
                'patterns': [],
                'total': 0, 'transactions': []
            },
            'recettes_clients': {
                'patterns': [],
                'total': 0, 'transactions': []
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
            
            tx_detail = {
                'date': date,
                'label': transaction.get('label', ''),
                'amount': abs(amount),
                'account': account,
                'side': side
            }
            
            categorized = False
            
            # Recettes (crédit)
            if side == 'credit' and amount > 0:
                categories['recettes_clients']['total'] += amount
                categories['recettes_clients']['transactions'].append(tx_detail)
                categorized = True
            
            # Charges (débit)
            elif side == 'debit' and amount < 0:
                amount = abs(amount)
                tx_detail['amount'] = amount
                
                # Test chaque catégorie avec patterns regex
                for category, info in categories.items():
                    if category in ['autres_charges', 'recettes_clients'] or categorized:
                        continue
                    
                    for pattern in info['patterns']:
                        if re.search(pattern, label, re.IGNORECASE):
                            info['total'] += amount
                            info['transactions'].append(tx_detail)
                            categorized = True
                            break
                
                # Si pas catégorisé → autres charges
                if not categorized:
                    categories['autres_charges']['total'] += amount
                    categories['autres_charges']['transactions'].append(tx_detail)
        
        return categories
    
    def display_detailed_analysis(self, categories, months=3):
        """Affichage détaillé avec exemples"""
        print(f"\n💰 ANALYSE EXHAUSTIVE CHARGES ({months} mois)")
        print("="*70)
        
        total_charges = 0
        
        # Affichage par catégorie
        for category, info in categories.items():
            if category == 'recettes_clients':
                continue
            
            monthly_avg = info['total'] / months
            total_charges += monthly_avg
            
            if info['total'] > 0:
                print(f"\n🏷️ {category.replace('_', ' ').upper()}")
                print(f"   Total {months} mois : {info['total']:8,.0f}€")
                print(f"   Moyenne/mois  : {monthly_avg:8,.0f}€")
                print(f"   Transactions  : {len(info['transactions'])}")
                
                # Afficher exemples significatifs
                if monthly_avg > 50:
                    sorted_tx = sorted(info['transactions'], key=lambda x: x['amount'], reverse=True)
                    print(f"   Exemples principaux :")
                    for tx in sorted_tx[:3]:
                        print(f"     • {tx['date']} - {tx['amount']:6,.0f}€ - {tx['label'][:45]}")
        
        # Recettes
        monthly_recettes = categories['recettes_clients']['total'] / months
        
        print(f"\n💎 SYNTHESE FINANCIERE ({months} mois):")
        print("="*50)
        print(f"💰 Recettes totales    : {categories['recettes_clients']['total']:8,.0f}€")
        print(f"💰 Recettes/mois       : {monthly_recettes:8,.0f}€")
        print(f"💸 Charges totales     : {sum(cat['total'] for cat in categories.values() if cat != categories['recettes_clients']):8,.0f}€")
        print(f"💸 Charges/mois        : {total_charges:8,.0f}€")
        print(f"📊 Résultat/mois       : {monthly_recettes - total_charges:+8,.0f}€")
        
        return {
            'charges_mensuelles_reelles': total_charges,
            'recettes_mensuelles': monthly_recettes,
            'resultat_mensuel': monthly_recettes - total_charges,
            'categories_detaillees': categories
        }
    
    def analyze_excel_projections(self):
        """Analyser les projections Excel (simulé pour l'instant)"""
        print(f"\n📊 ANALYSE EXCEL FACTURATION - PROJECTIONS AOUT+")
        print("="*60)
        
        # TODO: Charger vraies données Excel
        # Pour l'instant, estimation basée sur les données Clockify
        
        projections_mensuelles = {
            'aout_2025': {
                'facturable_attendu': 15000,  # Estimation
                'clients_confirmes': ['LAA', 'PHARMABEST', 'UAI', 'AIXAGON'],
                'opportunites': ['PETRAS', 'PROVENCALE', 'LEFEBVRE']
            },
            'septembre_2025': {
                'facturable_attendu': 18000,
                'clients_confirmes': ['LAA', 'PHARMABEST', 'UAI'],
                'opportunites': ['GUERBET', 'BUQUET']
            }
        }
        
        print("🎯 PROJECTIONS REVENUS:")
        for mois, data in projections_mensuelles.items():
            print(f"\n{mois.upper()}:")
            print(f"  Revenue attendu : {data['facturable_attendu']:6,.0f}€")
            print(f"  Clients confirmés : {', '.join(data['clients_confirmes'])}")
            print(f"  Opportunités : {', '.join(data['opportunites'])}")
        
        return projections_mensuelles
    
    def calculate_real_seuil(self, charges_reelles, projections):
        """Calcul seuil avec charges réelles + projections"""
        print(f"\n🎯 SEUIL RENTABILITE AVEC CHARGES REELLES")
        print("="*55)
        
        # Objectifs salariaux
        sebastien_net = 3000
        salarie_net = 2000
        nb_salaries = 2
        ratio_net_to_total = 1.82
        
        sebastien_charges = sebastien_net * ratio_net_to_total
        salaries_charges = salarie_net * nb_salaries * ratio_net_to_total
        total_personnel = sebastien_charges + salaries_charges
        
        charges_totales = charges_reelles + total_personnel
        
        print(f"💸 CHARGES TOTALES RÉELLES:")
        print(f"  Charges actuelles détectées : {charges_reelles:6,.0f}€/mois")
        print(f"  Objectifs personnel         : {total_personnel:6,.0f}€/mois")
        print(f"  TOTAL CHARGES MENSUELLES    : {charges_totales:6,.0f}€/mois")
        
        # Seuils
        total_hours = 255.8
        rate = 100
        
        print(f"\n📊 SEUILS AVEC CHARGES REELLES:")
        print("-" * 50)
        
        for ratio in [50, 55, 60, 65, 70]:
            billable_h = total_hours * (ratio / 100)
            revenue = billable_h * rate
            profit = revenue - charges_totales
            
            status = "✅ RENTABLE" if profit > 0 else "❌ DÉFICIT"
            print(f"  {ratio:2}% facturable : {billable_h:5.1f}h = {revenue:6,.0f}€ → {profit:+7,.0f}€ {status}")
        
        # Seuil critique
        seuil_revenue = charges_totales
        seuil_hours = seuil_revenue / rate
        seuil_ratio = (seuil_hours / total_hours) * 100
        
        print(f"\n🚨 SEUIL CRITIQUE RÉEL:")
        print(f"  Revenue minimum : {seuil_revenue:6,.0f}€/mois")
        print(f"  Heures minimum  : {seuil_hours:5.1f}h facturable/mois")
        print(f"  Ratio minimum   : {seuil_ratio:5.1f}% facturable")
        
        # Comparaison avec projections
        print(f"\n🎯 COMPARAISON PROJECTIONS:")
        for mois, data in projections.items():
            attendu = data['facturable_attendu']
            ecart = attendu - seuil_revenue
            status = "✅ OBJECTIF" if ecart >= 0 else "❌ INSUFFISANT"
            print(f"  {mois}: {attendu:6,.0f}€ → {ecart:+6,.0f}€ {status}")
        
        return charges_totales, seuil_ratio

def main():
    """Analyse complète"""
    print("🏦 ANALYSE COMPLETE QONTO + PROJECTIONS EXCEL")
    print("="*70)
    
    analyzer = QontoCompleteAnalysis()
    
    # 1. Transactions détaillées
    transactions = analyzer.get_all_transactions(months=3)
    
    # 2. Catégorisation exhaustive
    categories = analyzer.detailed_categorization(transactions)
    
    # 3. Analyse détaillée
    financial_analysis = analyzer.display_detailed_analysis(categories)
    
    # 4. Projections Excel
    projections = analyzer.analyze_excel_projections()
    
    # 5. Seuil réel
    charges_reelles = financial_analysis['charges_mensuelles_reelles']
    total_charges, seuil_ratio = analyzer.calculate_real_seuil(charges_reelles, projections)
    
    print(f"\n🎉 ANALYSE TERMINÉE")
    print(f"Charges réelles détectées : {charges_reelles:,.0f}€/mois")
    print(f"Seuil facturable réel     : {seuil_ratio:.1f}%")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
ANALYSEUR CHARGES QONTO - Calcul Seuil Rentabilité
Extraction sécurisée des transactions Qonto pour analyse charges mensuelles
"""

import requests
import json
import base64
from datetime import datetime, timedelta
from collections import defaultdict
import os

class QontoChargesAnalyzer:
    def __init__(self):
        """Initialise avec credentials temporaires"""
        self.load_temp_config()
        
    def load_temp_config(self):
        """Charge config temporaire"""
        config_file = "/home/sq/.qonto_temp_config"
        try:
            with open(config_file, 'r') as f:
                for line in f:
                    if line.startswith('QONTO_LOGIN='):
                        self.login = line.split('=')[1].strip()
                    elif line.startswith('QONTO_SECRET_KEY='):
                        self.secret_key = line.split('=')[1].strip()
                    elif line.startswith('QONTO_BASE_URL='):
                        self.base_url = line.split('=')[1].strip()
            
            # Headers pour auth
            credentials = f"{self.login}:{self.secret_key}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            self.headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/json'
            }
            
            print(f"✅ Configuration Qonto chargée pour {self.login}")
            
        except Exception as e:
            print(f"❌ Erreur chargement config: {e}")
            raise
    
    def test_connection(self):
        """Test connexion API"""
        try:
            response = requests.get(
                f"{self.base_url}/organization",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                org_data = response.json()
                print(f"✅ Connexion réussie - Organisation: {org_data.get('organization', {}).get('legal_name', 'Inconnue')}")
                return True
            else:
                print(f"❌ Erreur connexion: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur test connexion: {e}")
            return False
    
    def get_accounts(self):
        """Récupère les comptes"""
        try:
            response = requests.get(
                f"{self.base_url}/accounts",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                accounts_data = response.json()
                accounts = accounts_data.get('accounts', [])
                print(f"📊 {len(accounts)} comptes trouvés")
                
                for account in accounts:
                    name = account.get('name', 'Sans nom')
                    balance = account.get('balance_cents', 0) / 100
                    currency = account.get('currency', 'EUR')
                    print(f"  - {name}: {balance:,.2f} {currency}")
                
                return accounts
            else:
                print(f"❌ Erreur récupération comptes: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Erreur récupération comptes: {e}")
            return []
    
    def get_transactions(self, months=3):
        """Récupère transactions des derniers mois"""
        try:
            # Période d'analyse
            end_date = datetime.now()
            start_date = end_date - timedelta(days=months * 30)
            
            print(f"🔍 Extraction transactions du {start_date.strftime('%Y-%m-%d')} au {end_date.strftime('%Y-%m-%d')}")
            
            # Paramètres
            params = {
                'settled_at_from': start_date.strftime('%Y-%m-%d'),
                'settled_at_to': end_date.strftime('%Y-%m-%d'),
                'per_page': 100,
                'current_page': 1
            }
            
            all_transactions = []
            page = 1
            
            while True:
                params['current_page'] = page
                
                response = requests.get(
                    f"{self.base_url}/transactions",
                    headers=self.headers,
                    params=params,
                    timeout=15
                )
                
                if response.status_code != 200:
                    print(f"❌ Erreur page {page}: {response.status_code}")
                    break
                
                data = response.json()
                transactions = data.get('transactions', [])
                
                if not transactions:
                    break
                
                all_transactions.extend(transactions)
                print(f"📄 Page {page}: {len(transactions)} transactions")
                
                # Pagination
                meta = data.get('meta', {})
                if page >= meta.get('total_pages', 1):
                    break
                
                page += 1
            
            print(f"✅ Total: {len(all_transactions)} transactions récupérées")
            return all_transactions
            
        except Exception as e:
            print(f"❌ Erreur récupération transactions: {e}")
            return []
    
    def categorize_charges(self, transactions):
        """Catégorise les charges par type"""
        print(f"\n📊 CATÉGORISATION DES CHARGES")
        print("="*50)
        
        categories = {
            'salaires': {'keywords': ['salaire', 'paie', 'remuneration', 'urssaf', 'charges sociales'], 'total': 0, 'count': 0, 'transactions': []},
            'loyers': {'keywords': ['loyer', 'bail', 'location'], 'total': 0, 'count': 0, 'transactions': []},
            'assurances': {'keywords': ['assurance', 'responsabilité civile'], 'total': 0, 'count': 0, 'transactions': []},
            'telecom': {'keywords': ['orange', 'sfr', 'bouygues', 'free', 'téléphone', 'internet'], 'total': 0, 'count': 0, 'transactions': []},
            'logiciels': {'keywords': ['microsoft', 'office', 'adobe', 'saas', 'licence'], 'total': 0, 'count': 0, 'transactions': []},
            'comptable': {'keywords': ['comptable', 'expert comptable', 'fiduciaire'], 'total': 0, 'count': 0, 'transactions': []},
            'banque': {'keywords': ['commission', 'frais bancaire', 'virement', 'agios'], 'total': 0, 'count': 0, 'transactions': []},
            'materiel': {'keywords': ['ordinateur', 'serveur', 'matériel', 'hardware'], 'total': 0, 'count': 0, 'transactions': []},
            'transport': {'keywords': ['essence', 'péage', 'train', 'avion', 'uber'], 'total': 0, 'count': 0, 'transactions': []},
            'autres_charges': {'keywords': [], 'total': 0, 'count': 0, 'transactions': []},
            'recettes': {'keywords': [], 'total': 0, 'count': 0, 'transactions': []}
        }
        
        for transaction in transactions:
            amount_cents = transaction.get('amount_cents', 0)
            amount = amount_cents / 100
            label = transaction.get('label', '').lower()
            side = transaction.get('side', '')  # 'debit' ou 'credit'
            date = transaction.get('settled_at', '')[:10]
            
            # Ignorer transactions nulles
            if abs(amount) < 0.01:
                continue
            
            categorized = False
            
            # Si c'est un crédit (recette)
            if side == 'credit' and amount > 0:
                categories['recettes']['total'] += amount
                categories['recettes']['count'] += 1
                categories['recettes']['transactions'].append({
                    'date': date,
                    'label': transaction.get('label', ''),
                    'amount': amount
                })
                categorized = True
            
            # Si c'est un débit (charge)
            elif side == 'debit' and amount < 0:
                amount = abs(amount)  # Montant positif pour les charges
                
                # Recherche par mots-clés
                for category, info in categories.items():
                    if category in ['autres_charges', 'recettes']:
                        continue
                        
                    for keyword in info['keywords']:
                        if keyword in label:
                            info['total'] += amount
                            info['count'] += 1
                            info['transactions'].append({
                                'date': date,
                                'label': transaction.get('label', ''),
                                'amount': amount
                            })
                            categorized = True
                            break
                    
                    if categorized:
                        break
                
                # Si pas catégorisé → autres charges
                if not categorized:
                    categories['autres_charges']['total'] += amount
                    categories['autres_charges']['count'] += 1
                    categories['autres_charges']['transactions'].append({
                        'date': date,
                        'label': transaction.get('label', ''),
                        'amount': amount
                    })
        
        return categories
    
    def analyze_charges_mensuelles(self, categories):
        """Analyse et calcule charges mensuelles moyennes"""
        print(f"\n💰 ANALYSE CHARGES MENSUELLES MOYENNES")
        print("="*60)
        
        # Calcul sur 3 mois
        months = 3
        total_charges = 0
        total_recettes = 0
        
        print(f"\n🏢 CHARGES PAR CATÉGORIE (moyenne/mois sur {months} mois):")
        print("-" * 55)
        
        for category, info in categories.items():
            if category == 'recettes':
                continue
                
            monthly_avg = info['total'] / months
            total_charges += monthly_avg
            
            if info['count'] > 0:
                print(f"{category.upper():15} : {monthly_avg:8,.0f}€ ({info['count']:2} transactions)")
                
                # Afficher détail si pas trop de transactions
                if info['count'] <= 5 and monthly_avg > 100:
                    for tx in info['transactions'][-3:]:  # 3 dernières
                        print(f"   └─ {tx['date']} - {tx['label'][:40]:40} : {tx['amount']:6,.0f}€")
        
        # Recettes
        monthly_recettes = categories['recettes']['total'] / months
        total_recettes = monthly_recettes
        
        print(f"\n💎 RÉSUMÉ FINANCIER MENSUEL:")
        print("-" * 40)
        print(f"💰 Recettes moyennes : {monthly_recettes:8,.0f}€/mois")
        print(f"💸 Charges moyennes  : {total_charges:8,.0f}€/mois")
        print(f"📊 Résultat moyen    : {monthly_recettes - total_charges:+8,.0f}€/mois")
        
        return {
            'charges_mensuelles': total_charges,
            'recettes_mensuelles': monthly_recettes,
            'resultat_mensuel': monthly_recettes - total_charges,
            'categories': categories
        }
    
    def calculate_seuil_rentabilite(self, charges_mensuelles):
        """Calcule seuil de rentabilité avec objectifs salariaux"""
        print(f"\n🎯 CALCUL SEUIL DE RENTABILITÉ")
        print("="*50)
        
        # Objectifs salariaux
        sebastien_net = 3000  # €/mois
        salarie_net = 2000    # €/mois chacun
        nb_salaries = 2
        
        # Conversion net → charges totales (approximation)
        # Net → Brut (÷0.78) → Total charges (×1.42 charges patronales)
        ratio_net_to_total = 1 / 0.78 * 1.42
        
        sebastien_charges = sebastien_net * ratio_net_to_total
        salaries_charges = salarie_net * nb_salaries * ratio_net_to_total
        
        charges_personnel_objectif = sebastien_charges + salaries_charges
        charges_totales_objectif = charges_mensuelles + charges_personnel_objectif
        
        print(f"👨‍💼 OBJECTIFS SALARIAUX:")
        print(f"  Sébastien    : {sebastien_net:4,.0f}€ net → {sebastien_charges:6,.0f}€ charges totales")
        print(f"  2 salariés   : {salarie_net:4,.0f}€ net × {nb_salaries} → {salaries_charges:6,.0f}€ charges totales")
        print(f"  TOTAL ÉQUIPE : {charges_personnel_objectif:6,.0f}€/mois")
        
        print(f"\n💸 CHARGES TOTALES SOCIÉTÉ:")
        print(f"  Charges actuelles : {charges_mensuelles:6,.0f}€/mois")
        print(f"  Charges personnel : {charges_personnel_objectif:6,.0f}€/mois")
        print(f"  TOTAL CHARGES     : {charges_totales_objectif:6,.0f}€/mois")
        
        # Calcul seuils avec différents ratios facturable
        print(f"\n📊 SEUILS DE RENTABILITÉ (avec Clockify 255.8h/mois):")
        print("-" * 60)
        
        total_hours_monthly = 255.8  # Heures moyennes Clockify
        rate_per_hour = 100  # €/h moyen
        
        ratios = [50, 60, 70, 80]
        
        for ratio in ratios:
            billable_hours = total_hours_monthly * (ratio / 100)
            revenue = billable_hours * rate_per_hour
            profit = revenue - charges_totales_objectif
            
            status = "✅ RENTABLE" if profit > 0 else "❌ DÉFICITAIRE"
            
            print(f"  {ratio:2}% facturable : {billable_hours:5.1f}h = {revenue:6,.0f}€ → {profit:+7,.0f}€ {status}")
        
        # Seuil exact
        seuil_revenue = charges_totales_objectif
        seuil_hours = seuil_revenue / rate_per_hour
        seuil_ratio = (seuil_hours / total_hours_monthly) * 100
        
        print(f"\n🎯 SEUIL CRITIQUE:")
        print(f"  Heures min  : {seuil_hours:5.1f}h facturable/mois")
        print(f"  Ratio min   : {seuil_ratio:5.1f}% facturable")
        print(f"  Revenue min : {seuil_revenue:6,.0f}€/mois")
        
        return {
            'charges_totales': charges_totales_objectif,
            'seuil_hours': seuil_hours,
            'seuil_ratio': seuil_ratio,
            'seuil_revenue': seuil_revenue
        }
    
    def save_analysis(self, analysis_data):
        """Sauvegarde l'analyse"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_file = f"/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/qonto_charges_analysis_{timestamp}.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"\n✅ Analyse sauvegardée: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            return None
    
    def cleanup_temp_config(self):
        """Nettoie la config temporaire"""
        try:
            os.remove("/home/sq/.qonto_temp_config")
            print(f"🗑️ Configuration temporaire supprimée")
        except:
            pass

def main():
    """Fonction principale"""
    print("🏦 ANALYSEUR CHARGES QONTO - SEUIL DE RENTABILITÉ")
    print("="*60)
    
    analyzer = QontoChargesAnalyzer()
    
    try:
        # Test connexion
        if not analyzer.test_connection():
            print("❌ Impossible de se connecter à Qonto")
            return
        
        # Récupération comptes
        accounts = analyzer.get_accounts()
        
        # Récupération transactions
        transactions = analyzer.get_transactions(months=3)
        
        if not transactions:
            print("❌ Aucune transaction trouvée")
            return
        
        # Catégorisation
        categories = analyzer.categorize_charges(transactions)
        
        # Analyse mensuelle
        monthly_analysis = analyzer.analyze_charges_mensuelles(categories)
        
        # Calcul seuil rentabilité
        seuil_analysis = analyzer.calculate_seuil_rentabilite(monthly_analysis['charges_mensuelles'])
        
        # Données complètes
        full_analysis = {
            'timestamp': datetime.now().isoformat(),
            'accounts': accounts,
            'transaction_count': len(transactions),
            'monthly_analysis': monthly_analysis,
            'seuil_rentabilite': seuil_analysis
        }
        
        # Sauvegarde
        analyzer.save_analysis(full_analysis)
        
        print(f"\n🎉 ANALYSE TERMINÉE - Données Qonto analysées avec succès")
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Nettoyage sécurisé
        analyzer.cleanup_temp_config()

if __name__ == "__main__":
    main()
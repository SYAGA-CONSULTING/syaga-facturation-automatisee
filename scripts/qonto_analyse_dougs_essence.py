#!/usr/bin/env python3
"""
ANALYSE SPÉCIFIQUE QONTO : DOUGS + ESSENCE
Recherche dans les vraies transactions Qonto
"""

import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

class QontoAnalyseur:
    def __init__(self):
        # Credentials du script debug_transactions
        self.login = "syaga-consulting-5172"
        self.secret_key = "06f55a4b41d0"
        self.base_url = "https://thirdparty.qonto.com/v2"
        self.headers = {
            'Authorization': f'{self.login}:{self.secret_key}',
            'Content-Type': 'application/json'
        }
        
        print("🔍 ANALYSE TRANSACTIONS QONTO - DOUGS & ESSENCE")
        print("=" * 60)
        
    def get_organization_info(self):
        """Récupère les infos de l'organisation"""
        try:
            response = requests.get(f"{self.base_url}/organization", headers=self.headers)
            if response.status_code == 200:
                org_data = response.json()
                bank_accounts = org_data.get('organization', {}).get('bank_accounts', [])
                print(f"✅ Organisation trouvée: {len(bank_accounts)} compte(s)")
                return bank_accounts
            else:
                print(f"❌ Erreur organisation: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Erreur connexion: {e}")
            return []
    
    def get_all_transactions(self, months_back=6):
        """Récupère toutes les transactions"""
        bank_accounts = self.get_organization_info()
        if not bank_accounts:
            return []
        
        # Période
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months_back*30)
        
        all_transactions = []
        
        for account in bank_accounts:
            account_id = account.get('id')
            print(f"\n📁 Analyse compte: {account.get('iban', 'N/A')}")
            
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
                
                all_transactions.extend(transactions)
                
                # Check pagination
                meta = data.get('meta', {})
                if page >= meta.get('total_pages', 1):
                    break
                page += 1
            
            print(f"  → {len(all_transactions)} transactions récupérées")
        
        return all_transactions
    
    def analyser_dougs(self, transactions):
        """Analyse spécifique DOUGS"""
        print("\n💼 ANALYSE DOUGS (COMPTABLE)")
        print("-" * 50)
        
        dougs_transactions = []
        motifs_dougs = ['dougs', 'doug', 'comptable', 'accounting', 'expertise']
        
        for transaction in transactions:
            # Sortie uniquement (paiements)
            if float(transaction.get('amount_cents', 0)) >= 0:
                continue
                
            label = transaction.get('label', '').lower()
            counterparty = transaction.get('counterparty_name', '').lower() if transaction.get('counterparty_name') else ''
            reference = transaction.get('reference', '').lower() if transaction.get('reference') else ''
            
            # Chercher DOUGS
            text_to_search = f"{label} {counterparty} {reference}"
            if any(motif in text_to_search for motif in motifs_dougs):
                amount = abs(float(transaction.get('amount_cents', 0))) / 100
                dougs_transactions.append({
                    'date': transaction.get('settled_at', ''),
                    'amount': amount,
                    'label': transaction.get('label', ''),
                    'counterparty': transaction.get('counterparty_name', ''),
                    'reference': transaction.get('reference', '')
                })
        
        if dougs_transactions:
            print(f"✅ {len(dougs_transactions)} transactions DOUGS trouvées:\n")
            
            # Trier par date
            dougs_sorted = sorted(dougs_transactions, key=lambda x: x['date'], reverse=True)
            
            # Afficher toutes les transactions DOUGS
            total_dougs = 0
            for t in dougs_sorted:
                date = t['date'][:10] if t['date'] else 'N/A'
                print(f"  {date}: {t['amount']:>8.2f}€ - {t['label'][:40]}")
                if t['counterparty']:
                    print(f"            → Bénéficiaire: {t['counterparty']}")
                total_dougs += t['amount']
            
            # Calculer moyenne mensuelle
            if dougs_sorted:
                # Compter nombre de mois entre première et dernière transaction
                first_date = datetime.fromisoformat(dougs_sorted[-1]['date'][:19])
                last_date = datetime.fromisoformat(dougs_sorted[0]['date'][:19])
                months_span = max(1, (last_date - first_date).days / 30)
                
                moyenne_mensuelle = total_dougs / months_span
                
                print(f"\n📊 STATISTIQUES DOUGS:")
                print(f"  Total sur {months_span:.0f} mois: {total_dougs:.2f}€")
                print(f"  💰 Moyenne mensuelle: {moyenne_mensuelle:.2f}€/mois")
                
                # Identifier le montant récurrent
                montants_dougs = [t['amount'] for t in dougs_sorted]
                montant_frequent = max(set(montants_dougs), key=montants_dougs.count)
                print(f"  📌 Montant le plus fréquent: {montant_frequent:.2f}€")
                
                return moyenne_mensuelle
        else:
            print("❌ Aucune transaction DOUGS identifiée")
            print("💡 Recherche élargie nécessaire...")
            return 0
    
    def analyser_essence(self, transactions):
        """Analyse spécifique ESSENCE/CARBURANT"""
        print("\n⛽ ANALYSE ESSENCE/CARBURANT")
        print("-" * 50)
        
        essence_transactions = []
        motifs_essence = ['total', 'esso', 'shell', 'bp ', 'carrefour market', 'leclerc', 
                         'auchan', 'intermarche', 'super u', 'carburant', 'essence', 
                         'gasoil', 'diesel', 'station', 'avia', 'agip']
        
        for transaction in transactions:
            # Sortie uniquement
            if float(transaction.get('amount_cents', 0)) >= 0:
                continue
                
            label = transaction.get('label', '').lower()
            counterparty = transaction.get('counterparty_name', '').lower() if transaction.get('counterparty_name') else ''
            
            # Chercher essence
            text_to_search = f"{label} {counterparty}"
            if any(motif in text_to_search for motif in motifs_essence):
                amount = abs(float(transaction.get('amount_cents', 0))) / 100
                # Filtrer montants typiques essence (30-150€)
                if 25 <= amount <= 200:
                    essence_transactions.append({
                        'date': transaction.get('settled_at', ''),
                        'amount': amount,
                        'label': transaction.get('label', ''),
                        'counterparty': transaction.get('counterparty_name', '')
                    })
        
        if essence_transactions:
            print(f"✅ {len(essence_transactions)} transactions essence trouvées:\n")
            
            # Trier par date
            essence_sorted = sorted(essence_transactions, key=lambda x: x['date'], reverse=True)
            
            # Afficher les 10 dernières
            for t in essence_sorted[:10]:
                date = t['date'][:10] if t['date'] else 'N/A'
                print(f"  {date}: {t['amount']:>7.2f}€ - {t['label'][:40]}")
            
            if len(essence_sorted) > 10:
                print(f"  ... et {len(essence_sorted)-10} autres transactions")
            
            # Statistiques
            total_essence = sum(t['amount'] for t in essence_sorted)
            
            # Calculer fréquence et moyenne
            if essence_sorted:
                first_date = datetime.fromisoformat(essence_sorted[-1]['date'][:19])
                last_date = datetime.fromisoformat(essence_sorted[0]['date'][:19])
                months_span = max(1, (last_date - first_date).days / 30)
                
                moyenne_mensuelle = total_essence / months_span
                frequence = len(essence_sorted) / months_span
                
                print(f"\n📊 STATISTIQUES ESSENCE:")
                print(f"  Total sur {months_span:.0f} mois: {total_essence:.2f}€")
                print(f"  💰 Moyenne mensuelle: {moyenne_mensuelle:.2f}€/mois")
                print(f"  ⛽ Fréquence: {frequence:.1f} pleins/mois")
                print(f"  📌 Montant moyen par plein: {total_essence/len(essence_sorted):.2f}€")
                
                return moyenne_mensuelle
        else:
            print("❌ Aucune transaction essence identifiée")
            return 0
    
    def chercher_autres_recurrents(self, transactions):
        """Cherche autres charges récurrentes non identifiées"""
        print("\n🔍 RECHERCHE AUTRES CHARGES RÉCURRENTES")
        print("-" * 50)
        
        # Grouper par bénéficiaire
        beneficiaires = defaultdict(list)
        
        for transaction in transactions:
            # Sortie uniquement
            if float(transaction.get('amount_cents', 0)) >= 0:
                continue
            
            counterparty = transaction.get('counterparty_name', '')
            if counterparty:
                amount = abs(float(transaction.get('amount_cents', 0))) / 100
                beneficiaires[counterparty].append({
                    'date': transaction.get('settled_at', ''),
                    'amount': amount,
                    'label': transaction.get('label', '')
                })
        
        # Identifier récurrents (>= 3 paiements)
        recurrents = {}
        for beneficiaire, payments in beneficiaires.items():
            if len(payments) >= 3:  # Au moins 3 paiements = potentiellement récurrent
                total = sum(p['amount'] for p in payments)
                # Calculer période
                if payments:
                    dates = [datetime.fromisoformat(p['date'][:19]) for p in payments if p['date']]
                    if dates:
                        months_span = max(1, (max(dates) - min(dates)).days / 30)
                        moyenne = total / months_span
                        
                        # Filtrer les petits montants et les très gros
                        if 10 <= moyenne <= 2000:  # Entre 10€ et 2000€/mois
                            recurrents[beneficiaire] = {
                                'count': len(payments),
                                'total': total,
                                'moyenne': moyenne,
                                'dernier': max(payments, key=lambda x: x['date'])['date'][:10] if payments else 'N/A'
                            }
        
        # Exclure ceux déjà identifiés
        exclusions = ['dougs', 'urssaf', 'dgfip', 'swisslife', 'swiss life', 'hiscox', 
                     'riverbank', 'qssp', 'villadata', 'free', 'ovh', 'microsoft', 
                     'github', 'google', 'claude', 'total', 'esso', 'shell']
        
        recurrents_filtres = {}
        for beneficiaire, data in recurrents.items():
            beneficiaire_lower = beneficiaire.lower()
            if not any(exclu in beneficiaire_lower for exclu in exclusions):
                recurrents_filtres[beneficiaire] = data
        
        if recurrents_filtres:
            print("✅ Charges récurrentes potentielles identifiées:\n")
            
            # Trier par moyenne mensuelle décroissante
            sorted_recurrents = sorted(recurrents_filtres.items(), key=lambda x: x[1]['moyenne'], reverse=True)
            
            total_autres = 0
            for beneficiaire, data in sorted_recurrents[:10]:
                print(f"  • {beneficiaire[:40]}")
                print(f"    {data['count']} paiements | {data['moyenne']:.2f}€/mois | Dernier: {data['dernier']}")
                total_autres += data['moyenne']
            
            if len(sorted_recurrents) > 10:
                print(f"\n  ... et {len(sorted_recurrents)-10} autres bénéficiaires récurrents")
            
            print(f"\n💰 TOTAL AUTRES RÉCURRENTS: {total_autres:.2f}€/mois")
            return total_autres
        else:
            print("❌ Aucune autre charge récurrente significative identifiée")
            return 0

def main():
    """Analyse complète"""
    
    analyseur = QontoAnalyseur()
    
    # Récupérer toutes les transactions
    print("\n📥 Récupération des transactions...")
    transactions = analyseur.get_all_transactions(6)
    
    if not transactions:
        print("❌ Impossible de récupérer les transactions")
        print("💡 Vérifier les credentials Qonto")
        return
    
    print(f"\n✅ Total: {len(transactions)} transactions à analyser")
    
    # Analyses spécifiques
    montant_dougs = analyseur.analyser_dougs(transactions)
    montant_essence = analyseur.analyser_essence(transactions)
    montant_autres = analyseur.chercher_autres_recurrents(transactions)
    
    # Synthèse finale
    print("\n" + "=" * 60)
    print("📊 SYNTHÈSE CHARGES RÉCURRENTES IDENTIFIÉES")
    print("=" * 60)
    
    print(f"💼 DOUGS (comptable)      : {montant_dougs:>8.2f}€/mois")
    print(f"⛽ Essence/Carburant      : {montant_essence:>8.2f}€/mois")
    print(f"🔍 Autres récurrents      : {montant_autres:>8.2f}€/mois")
    print("-" * 40)
    print(f"🎯 TOTAL SUPPLÉMENTAIRE   : {montant_dougs + montant_essence + montant_autres:>8.2f}€/mois")
    
    print(f"\n📅 Analyse terminée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")

if __name__ == "__main__":
    main()
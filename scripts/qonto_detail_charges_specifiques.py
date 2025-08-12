#!/usr/bin/env python3
"""
DÉTAIL SPÉCIFIQUE CHARGES QONTO
Analyser en détail: DOUGS (comptable) + IT/Télécom/Banque/Divers
"""

import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict
import re

class QontoDetailCharges:
    def __init__(self):
        # Configuration API Qonto
        self.base_url = "https://thirdparty.qonto.com/v2"
        self.headers = {
            'Authorization': 'sebastien-questier-7:secretkey-25b9b5b1-9eff-44df-b20e-c51fdaa11e1c',
            'Accept': 'application/json'
        }
        
        # Compte principal SYAGA
        self.iban = 'FR7616958000018809313999064'
        
        print("🔍 ANALYSE DÉTAILLÉE CHARGES SPÉCIFIQUES")
        print("=" * 60)
        print("Recherche: DOUGS + IT + Télécom + Banque + Divers\n")
        
    def get_recent_transactions(self, months_back=6):
        """Récupère les transactions récentes"""
        
        try:
            params = {
                'status': 'completed',
                'iban': self.iban,
                'per_page': '200',  # Plus de transactions
                'current_page': '1'
            }
            
            response = requests.get(
                f"{self.base_url}/transactions", 
                headers=self.headers, 
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                transactions = data.get('transactions', [])
                print(f"✅ {len(transactions)} transactions récupérées")
                return transactions
            else:
                print(f"❌ Erreur API: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return []
    
    def analyser_dougs(self, transactions):
        """Analyse spécifique des paiements DOUGS"""
        
        print("\n💼 ANALYSE DOUGS (COMPTABLE)")
        print("-" * 40)
        
        dougs_transactions = []
        motifs_dougs = ['dougs', 'comptable', 'accounting']
        
        for transaction in transactions:
            label = transaction.get('label', '').lower()
            counterparty = transaction.get('counterparty_name', '').lower()
            
            # Chercher DOUGS dans label ou counterparty
            if any(motif in label or motif in counterparty for motif in motifs_dougs):
                dougs_transactions.append({
                    'date': transaction.get('emitted_at', ''),
                    'amount': abs(float(transaction.get('amount', 0))),
                    'label': transaction.get('label', ''),
                    'counterparty': transaction.get('counterparty_name', '')
                })
        
        if dougs_transactions:
            print(f"📋 {len(dougs_transactions)} transactions DOUGS trouvées:")
            for t in sorted(dougs_transactions, key=lambda x: x['date'], reverse=True)[:10]:
                date = t['date'][:10] if t['date'] else 'N/A'
                print(f"  {date}: {t['amount']:>7.0f}€ - {t['label'][:50]}")
            
            # Calculer moyenne mensuelle
            montants = [t['amount'] for t in dougs_transactions]
            if montants:
                moyenne = sum(montants) / len(montants)
                print(f"\n💰 Moyenne par transaction: {moyenne:.0f}€")
                print(f"🎯 Estimation mensuelle DOUGS: ~{moyenne:.0f}€")
        else:
            print("❌ Aucune transaction DOUGS identifiée")
            print("💡 Recherche manuelle nécessaire dans Qonto")
        
        return dougs_transactions
    
    def analyser_it_telecom(self, transactions):
        """Analyse détaillée IT/Télécom"""
        
        print("\n💻 ANALYSE IT & TÉLÉCOM")
        print("-" * 40)
        
        categories = {
            'Cloud/SaaS': ['claude', 'microsoft', 'github', 'ovh', 'google', 'azure', 'aws'],
            'Télécom': ['free', 'orange', 'sfr', 'bouygues', 'telecoms'],
            'Software': ['adobe', 'office', 'license', 'software', 'app'],
            'Hardware': ['amazon', 'ldlc', 'materiel', 'hardware']
        }
        
        it_telecom = defaultdict(list)
        
        for transaction in transactions:
            label = transaction.get('label', '').lower()
            counterparty = transaction.get('counterparty_name', '').lower()
            amount = abs(float(transaction.get('amount', 0)))
            
            # Ignorer très petits montants (< 10€)
            if amount < 10:
                continue
                
            # Catégoriser
            for categorie, motifs in categories.items():
                if any(motif in label or motif in counterparty for motif in motifs):
                    it_telecom[categorie].append({
                        'date': transaction.get('emitted_at', '')[:10],
                        'amount': amount,
                        'label': transaction.get('label', ''),
                        'counterparty': transaction.get('counterparty_name', '')
                    })
                    break
        
        # Affichage par catégorie
        total_it_telecom = 0
        for categorie, items in it_telecom.items():
            if items:
                print(f"\n📂 {categorie.upper()}:")
                category_total = 0
                for item in sorted(items, key=lambda x: x['date'], reverse=True)[:5]:
                    print(f"  {item['date']}: {item['amount']:>6.0f}€ - {item['label'][:40]}")
                    category_total += item['amount']
                
                monthly_avg = category_total / len(items)
                print(f"  💰 Moyenne mensuelle: {monthly_avg:.0f}€")
                total_it_telecom += monthly_avg
        
        print(f"\n🎯 TOTAL IT/TÉLÉCOM ESTIMÉ: {total_it_telecom:.0f}€/mois")
        return total_it_telecom
    
    def analyser_frais_bancaires(self, transactions):
        """Analyse des frais bancaires"""
        
        print("\n🏦 ANALYSE FRAIS BANCAIRES")
        print("-" * 40)
        
        frais_bancaires = []
        motifs_bancaires = ['qonto', 'frais', 'commission', 'cotisation', 'carte', 'virement']
        
        for transaction in transactions:
            label = transaction.get('label', '').lower()
            counterparty = transaction.get('counterparty_name', '').lower()
            amount = abs(float(transaction.get('amount', 0)))
            
            if any(motif in label for motif in motifs_bancaires) and amount < 200:  # Limiter aux petits montants
                frais_bancaires.append({
                    'date': transaction.get('emitted_at', '')[:10],
                    'amount': amount,
                    'label': transaction.get('label', '')
                })
        
        if frais_bancaires:
            print(f"📋 {len(frais_bancaires)} frais bancaires identifiés:")
            for f in sorted(frais_bancaires, key=lambda x: x['date'], reverse=True)[:8]:
                print(f"  {f['date']}: {f['amount']:>5.0f}€ - {f['label']}")
            
            total_frais = sum(f['amount'] for f in frais_bancaires)
            moyenne_mensuelle = total_frais / 6 if frais_bancaires else 0  # 6 mois
            print(f"\n💰 Moyenne mensuelle: {moyenne_mensuelle:.0f}€")
            return moyenne_mensuelle
        else:
            print("❌ Peu de frais bancaires identifiés")
            return 30  # Estimation
    
    def analyser_divers(self, transactions):
        """Analyse des charges diverses"""
        
        print("\n🛍️ ANALYSE CHARGES DIVERSES")
        print("-" * 40)
        
        categories_diverses = {
            'Carburant/Transport': ['total', 'esso', 'shell', 'carburant', 'essence', 'peage'],
            'Fournitures/Matériel': ['amazon', 'cdiscount', 'fnac', 'bureau', 'materiel'],
            'Déplacements/Hôtels': ['hotel', 'booking', 'airbnb', 'restaurant', 'deplacement'],
            'Maintenance/Services': ['reparation', 'maintenance', 'service', 'assistance'],
            'Autres': []
        }
        
        divers = defaultdict(list)
        
        for transaction in transactions:
            label = transaction.get('label', '').lower()
            counterparty = transaction.get('counterparty_name', '').lower()
            amount = abs(float(transaction.get('amount', 0)))
            
            # Filtrer montants trop grands (probablement pas du "divers")
            if amount > 1000:
                continue
                
            # Ignorer ce qu'on a déjà catégorisé
            skip_motifs = ['urssaf', 'dgfip', 'loyer', 'riverbank', 'assurance', 'dougs', 
                          'claude', 'microsoft', 'github', 'ovh', 'free']
            if any(motif in label or motif in counterparty for motif in skip_motifs):
                continue
            
            # Catégoriser
            categorise = False
            for categorie, motifs in categories_diverses.items():
                if motifs and any(motif in label or motif in counterparty for motif in motifs):
                    divers[categorie].append({
                        'date': transaction.get('emitted_at', '')[:10],
                        'amount': amount,
                        'label': transaction.get('label', ''),
                        'counterparty': transaction.get('counterparty_name', '')
                    })
                    categorise = True
                    break
            
            # Si pas catégorisé, mettre dans "Autres"
            if not categorise and amount > 50:  # Seulement si montant significatif
                divers['Autres'].append({
                    'date': transaction.get('emitted_at', '')[:10],
                    'amount': amount,
                    'label': transaction.get('label', ''),
                    'counterparty': transaction.get('counterparty_name', '')
                })
        
        # Affichage
        total_divers = 0
        for categorie, items in divers.items():
            if items:
                print(f"\n📂 {categorie.upper()}:")
                category_total = sum(item['amount'] for item in items)
                monthly_avg = category_total / 6 if items else 0  # 6 mois
                
                for item in sorted(items, key=lambda x: x['amount'], reverse=True)[:5]:
                    print(f"  {item['date']}: {item['amount']:>6.0f}€ - {item['label'][:40]}")
                
                print(f"  💰 Total 6 mois: {category_total:.0f}€ → {monthly_avg:.0f}€/mois")
                total_divers += monthly_avg
        
        print(f"\n🎯 TOTAL DIVERS ESTIMÉ: {total_divers:.0f}€/mois")
        return total_divers
    
    def synthese_finale(self, dougs_est, it_telecom_est, frais_bancaires_est, divers_est):
        """Synthèse finale avec nouveau total"""
        
        print("\n" + "=" * 60)
        print("📊 SYNTHÈSE DÉTAILLÉE IT/TÉLÉCOM/BANQUE/DIVERS")
        print("=" * 60)
        
        print(f"💼 DOUGS (Comptable)     : {dougs_est:>6.0f}€/mois")
        print(f"💻 IT & Télécom         : {it_telecom_est:>6.0f}€/mois")
        print(f"🏦 Frais bancaires      : {frais_bancaires_est:>6.0f}€/mois")
        print(f"🛍️ Charges diverses     : {divers_est:>6.0f}€/mois")
        print("-" * 40)
        
        total_detail = dougs_est + it_telecom_est + frais_bancaires_est + divers_est
        print(f"🎯 TOTAL DÉTAILLÉ       : {total_detail:>6.0f}€/mois")
        
        ancien_total = 2051  # Ce qu'on avait avant
        difference = ancien_total - total_detail
        
        print(f"\n📈 COMPARAISON:")
        print(f"  Ancien montant global : {ancien_total}€/mois")
        print(f"  Nouveau montant détaillé : {total_detail:.0f}€/mois")
        print(f"  {'Économie' if difference > 0 else 'Surcoût'} : {abs(difference):.0f}€/mois")
        
        return total_detail

def main():
    """Exécution de l'analyse détaillée"""
    
    analyzer = QontoDetailCharges()
    
    # 1. Récupérer les transactions
    transactions = analyzer.get_recent_transactions()
    
    if not transactions:
        print("❌ Impossible de récupérer les transactions")
        return
    
    # 2. Analyses spécifiques
    dougs_transactions = analyzer.analyser_dougs(transactions)
    dougs_est = 400 if not dougs_transactions else sum(t['amount'] for t in dougs_transactions) / len(dougs_transactions)
    
    it_telecom_est = analyzer.analyser_it_telecom(transactions)
    frais_bancaires_est = analyzer.analyser_frais_bancaires(transactions)
    divers_est = analyzer.analyser_divers(transactions)
    
    # 3. Synthèse finale
    total_final = analyzer.synthese_finale(dougs_est, it_telecom_est, frais_bancaires_est, divers_est)
    
    print(f"\n📅 Analyse terminée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    print("💡 Recommandation: Vérifier manuellement dans Qonto les montants DOUGS")

if __name__ == "__main__":
    main()
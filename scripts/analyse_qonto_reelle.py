#!/usr/bin/env python3
"""
ANALYSE RÉELLE TRANSACTIONS QONTO
Avec les vrais credentials
"""

import requests
from datetime import datetime, timedelta
from collections import defaultdict

# Credentials
login = 'syaga-consulting-5172'
secret = '06f55a4b41d0'

headers = {
    'Authorization': f'{login}:{secret}',
    'Content-Type': 'application/json'
}

print("🔍 ANALYSE TRANSACTIONS QONTO RÉELLES")
print("=" * 60)

# Test connexion
org_response = requests.get("https://thirdparty.qonto.com/v2/organization", headers=headers)
if org_response.status_code == 200:
    org = org_response.json()['organization']
    print(f"✅ Connecté: {org['name']}")
    bank_accounts = org['bank_accounts']
    
    # Récupérer transactions 6 derniers mois
    all_transactions = []
    for account in bank_accounts:
        print(f"  Compte: {account.get('iban', 'N/A')}")
        params = {
            'bank_account_id': account['id'],
            'settled_at_from': (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%dT00:00:00.000Z'),
            'settled_at_to': datetime.now().strftime('%Y-%m-%dT23:59:59.999Z'),
            'per_page': 100
        }
        
        page = 1
        while True:
            params['current_page'] = page
            response = requests.get("https://thirdparty.qonto.com/v2/transactions", headers=headers, params=params)
            if response.status_code != 200:
                break
            data = response.json()
            transactions = data.get('transactions', [])
            if not transactions:
                break
            all_transactions.extend(transactions)
            meta = data.get('meta', {})
            if page >= meta.get('total_pages', 1):
                break
            page += 1
    
    print(f"\n📊 {len(all_transactions)} transactions analysées sur 6 mois\n")
    
    # ANALYSE DOUGS
    print("💼 ANALYSE DOUGS (COMPTABLE)")
    print("-" * 50)
    dougs_trans = []
    for t in all_transactions:
        if float(t.get('amount_cents', 0)) < 0:  # Sortie d'argent
            label = t.get('label', '') or ''
            counterparty = t.get('counterparty_name', '') or ''
            combined = (label + ' ' + counterparty).lower()
            
            if 'dougs' in combined or 'doug' in combined:
                amount = abs(float(t['amount_cents'])) / 100
                dougs_trans.append({
                    'date': t['settled_at'][:10] if t.get('settled_at') else 'N/A',
                    'amount': amount,
                    'label': label,
                    'counterparty': counterparty
                })
    
    if dougs_trans:
        dougs_trans.sort(key=lambda x: x['date'], reverse=True)
        print("  Dernières transactions DOUGS:")
        for d in dougs_trans[:8]:
            print(f"    {d['date']}: {d['amount']:>7.2f}€ - {d['label'][:35]}")
            if d['counterparty']:
                print(f"              → {d['counterparty']}")
        
        total_dougs = sum(d['amount'] for d in dougs_trans)
        
        # Calculer moyenne mensuelle
        if dougs_trans:
            first_date = min(d['date'] for d in dougs_trans)
            last_date = max(d['date'] for d in dougs_trans)
            # Nombre de mois entre première et dernière transaction
            months_span = max(1, (datetime.fromisoformat(last_date) - datetime.fromisoformat(first_date)).days / 30)
            monthly_avg = total_dougs / months_span
        else:
            monthly_avg = 0
        
        print(f"\n  📊 STATISTIQUES DOUGS:")
        print(f"    • Total 6 mois: {total_dougs:.2f}€")
        print(f"    • Nombre de paiements: {len(dougs_trans)}")
        print(f"    • Moyenne par paiement: {total_dougs/len(dougs_trans):.2f}€")
        print(f"    • 💰 MOYENNE MENSUELLE: {monthly_avg:.2f}€/mois")
        
        # Identifier montant récurrent
        amounts = [d['amount'] for d in dougs_trans]
        from collections import Counter
        amount_counts = Counter(amounts)
        most_common = amount_counts.most_common(1)[0] if amount_counts else (0, 0)
        if most_common[1] > 1:
            print(f"    • 📌 Montant récurrent: {most_common[0]:.2f}€ ({most_common[1]} fois)")
    else:
        print("  ❌ Aucune transaction DOUGS trouvée")
        print("  💡 Vérifier avec d'autres mots-clés (comptable, expertise, etc.)")
    
    # ANALYSE ESSENCE
    print("\n⛽ ANALYSE ESSENCE/CARBURANT")
    print("-" * 50)
    essence_trans = []
    stations = ['total', 'esso', 'shell', 'bp ', 'carrefour', 'leclerc', 
                'intermarche', 'avia', 'station', 'carburant', 'essence', 'gasoil']
    
    for t in all_transactions:
        if float(t.get('amount_cents', 0)) < 0:
            label = t.get('label', '') or ''
            counterparty = t.get('counterparty_name', '') or ''
            combined = (label + ' ' + counterparty).lower()
            
            if any(s in combined for s in stations):
                amount = abs(float(t['amount_cents'])) / 100
                if 25 <= amount <= 200:  # Montant typique essence
                    essence_trans.append({
                        'date': t['settled_at'][:10] if t.get('settled_at') else 'N/A',
                        'amount': amount,
                        'label': label,
                        'counterparty': counterparty
                    })
    
    if essence_trans:
        essence_trans.sort(key=lambda x: x['date'], reverse=True)
        print("  Derniers pleins d'essence:")
        for e in essence_trans[:8]:
            print(f"    {e['date']}: {e['amount']:>7.2f}€ - {e['label'][:35]}")
        
        total_essence = sum(e['amount'] for e in essence_trans)
        monthly_essence = total_essence / 6  # Sur 6 mois
        
        print(f"\n  📊 STATISTIQUES ESSENCE:")
        print(f"    • Total 6 mois: {total_essence:.2f}€")
        print(f"    • Nombre de pleins: {len(essence_trans)}")
        print(f"    • Moyenne par plein: {total_essence/len(essence_trans):.2f}€")
        print(f"    • 💰 MOYENNE MENSUELLE: {monthly_essence:.2f}€/mois")
        print(f"    • ⛽ Fréquence: {len(essence_trans)/6:.1f} pleins/mois")
    else:
        print("  ❌ Aucune transaction essence identifiée")
    
    # RECHERCHE AUTRES RÉCURRENTS
    print("\n🔍 RECHERCHE AUTRES CHARGES RÉCURRENTES")
    print("-" * 50)
    
    # Grouper par bénéficiaire
    beneficiaires = defaultdict(list)
    for t in all_transactions:
        if float(t.get('amount_cents', 0)) < 0:
            counterparty = t.get('counterparty_name', '')
            if counterparty:
                amount = abs(float(t['amount_cents'])) / 100
                beneficiaires[counterparty].append({
                    'date': t['settled_at'][:10] if t.get('settled_at') else 'N/A',
                    'amount': amount,
                    'label': t.get('label', '')
                })
    
    # Identifier récurrents (>= 3 paiements)
    exclusions = ['dougs', 'urssaf', 'dgfip', 'swisslife', 'swiss life', 'hiscox', 
                  'riverbank', 'qssp', 'villadata', 'free', 'ovh', 'microsoft', 
                  'github', 'google', 'claude', 'total', 'esso', 'shell']
    
    recurrents = []
    for beneficiaire, payments in beneficiaires.items():
        if len(payments) >= 3:  # Au moins 3 paiements
            beneficiaire_lower = beneficiaire.lower()
            if not any(exclu in beneficiaire_lower for exclu in exclusions):
                total = sum(p['amount'] for p in payments)
                monthly_avg = total / 6
                if 10 <= monthly_avg <= 2000:  # Montants raisonnables
                    recurrents.append({
                        'name': beneficiaire,
                        'count': len(payments),
                        'total': total,
                        'monthly': monthly_avg,
                        'last': max(p['date'] for p in payments)
                    })
    
    if recurrents:
        recurrents.sort(key=lambda x: x['monthly'], reverse=True)
        print("  Charges récurrentes non identifiées:")
        for r in recurrents[:10]:
            print(f"    • {r['name'][:40]}")
            print(f"      {r['count']} paiements | {r['monthly']:.2f}€/mois | Dernier: {r['last']}")
        
        total_autres = sum(r['monthly'] for r in recurrents[:10])
        print(f"\n  💰 TOTAL AUTRES RÉCURRENTS: {total_autres:.2f}€/mois")
    else:
        print("  ✅ Aucune autre charge récurrente significative")
    
    # SYNTHÈSE FINALE
    print("\n" + "="*60)
    print("📊 SYNTHÈSE CHARGES RÉCURRENTES IDENTIFIÉES")
    print("="*60)
    
    dougs_monthly = monthly_avg if dougs_trans else 0
    essence_monthly = monthly_essence if essence_trans else 0
    autres_monthly = sum(r['monthly'] for r in recurrents[:10]) if recurrents else 0
    
    print(f"  💼 DOUGS (comptable)      : {dougs_monthly:>8.2f}€/mois")
    print(f"  ⛽ Essence/Carburant      : {essence_monthly:>8.2f}€/mois")
    print(f"  🔍 Autres récurrents      : {autres_monthly:>8.2f}€/mois")
    print("-" * 40)
    print(f"  🎯 TOTAL SUPPLÉMENTAIRE   : {dougs_monthly + essence_monthly + autres_monthly:>8.2f}€/mois")
    
else:
    print(f"❌ Erreur connexion Qonto: {org_response.status_code}")
    if org_response.status_code == 401:
        print("   → Vérifier les credentials dans ~/.qonto_config")

print(f"\n📅 Analyse terminée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
#!/usr/bin/env python3
"""
DEBUG TRANSACTIONS QONTO - Voir les vrais libellés
Affiche toutes les transactions pour comprendre pourquoi 0€ charges détectées
"""

import requests
import json
from datetime import datetime, timedelta

def debug_qonto_transactions():
    """Affiche toutes les transactions pour debug"""
    login = "syaga-consulting-5172"
    secret_key = "06f55a4b41d0"
    base_url = "https://thirdparty.qonto.com/v2"
    headers = {
        'Authorization': f'{login}:{secret_key}',
        'Content-Type': 'application/json'
    }
    
    # Organisation
    org_response = requests.get(f"{base_url}/organization", headers=headers)
    org_data = org_response.json()
    bank_accounts = org_data.get('organization', {}).get('bank_accounts', [])
    
    # Période
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    all_transactions = []
    
    for account in bank_accounts:
        account_id = account.get('id')
        
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
            response = requests.get(f"{base_url}/transactions", headers=headers, params=params)
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
    
    print(f"🔍 DEBUG TRANSACTIONS QONTO - {len(all_transactions)} transactions")
    print("="*80)
    
    # Séparer débits et crédits
    debits = []
    credits = []
    
    for tx in all_transactions:
        amount = tx.get('amount_cents', 0) / 100
        if tx.get('side') == 'debit':
            debits.append(tx)
        else:
            credits.append(tx)
    
    print(f"\n💸 DEBITS (CHARGES) - {len(debits)} transactions:")
    print("-" * 80)
    
    debits_sorted = sorted(debits, key=lambda x: abs(x.get('amount_cents', 0)), reverse=True)
    
    for i, tx in enumerate(debits_sorted[:20]):  # Top 20 débits
        amount = abs(tx.get('amount_cents', 0) / 100)
        date = tx.get('settled_at', '')[:10]
        label = tx.get('label', 'Sans libellé')
        
        print(f"{i+1:2d}. {date} - {amount:8,.2f}€ - {label}")
    
    print(f"\n💰 CREDITS (RECETTES) - {len(credits)} transactions:")
    print("-" * 80)
    
    credits_sorted = sorted(credits, key=lambda x: x.get('amount_cents', 0), reverse=True)
    
    for i, tx in enumerate(credits_sorted[:10]):  # Top 10 crédits
        amount = tx.get('amount_cents', 0) / 100
        date = tx.get('settled_at', '')[:10]
        label = tx.get('label', 'Sans libellé')
        
        print(f"{i+1:2d}. {date} - {amount:8,.2f}€ - {label}")
    
    # Statistiques
    total_debits = sum(abs(tx.get('amount_cents', 0)) for tx in debits) / 100
    total_credits = sum(tx.get('amount_cents', 0) for tx in credits) / 100
    
    print(f"\n📊 STATISTIQUES:")
    print(f"Total débits  : {total_debits:10,.2f}€")
    print(f"Total crédits : {total_credits:10,.2f}€")
    print(f"Solde net     : {total_credits - total_debits:+10,.2f}€")
    
    # Sauvegarder pour analyse
    with open('/home/sq/qonto_debug_transactions.json', 'w') as f:
        json.dump(all_transactions, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Transactions sauvegardées dans /home/sq/qonto_debug_transactions.json")

if __name__ == "__main__":
    debug_qonto_transactions()
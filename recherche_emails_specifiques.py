#!/usr/bin/env python3
"""
Recherche spécifique des factures dans les emails envoyés
Cherche aussi par client et par mois
"""

import sys
import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta
from pathlib import Path

# Charger configuration Azure
def load_azure_config():
    config_path = Path.home() / '.azure_config'
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration Azure AD manquante: {config_path}")
    
    config = {}
    with open(config_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                config[key] = value
    return config

config = load_azure_config()
TENANT_ID = config['TENANT_ID']
CLIENT_ID = config['CLIENT_ID']
CLIENT_SECRET = config['CLIENT_SECRET']
USER_EMAIL = config['SENDER_EMAIL']

def get_access_token():
    """Obtenir le token d'accès OAuth2"""
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    
    token_data = urllib.parse.urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials'
    }).encode('utf-8')
    
    try:
        req = urllib.request.Request(token_url, data=token_data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        with urllib.request.urlopen(req) as response:
            token_response = json.loads(response.read().decode('utf-8'))
            return token_response.get('access_token')
    except Exception as e:
        print(f"❌ Erreur token: {e}")
        return None

def search_sent_emails(search_term="", days_back=90):
    """Rechercher dans les emails envoyés"""
    access_token = get_access_token()
    if not access_token:
        return None
    
    # URL pour lire les emails envoyés
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    # Paramètres de recherche - chercher sur 90 jours
    date_filter = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Chercher dans sujet ET corps
    params_dict = {
        '$top': '200',  # Plus de résultats
        '$select': 'subject,toRecipients,sentDateTime,bodyPreview',
        '$orderby': 'sentDateTime desc'
    }
    
    # Si terme de recherche, l'ajouter
    if search_term:
        params_dict['$search'] = f'"{search_term}"'
    
    params = '?' + urllib.parse.urlencode(params_dict)
    
    try:
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('value', [])
    except Exception as e:
        print(f"❌ Erreur recherche: {e}")
        return None

def main():
    print('🔍 RECHERCHE APPROFONDIE DES FACTURES DANS LES EMAILS')
    print('='*80)
    
    # Liste des clients à chercher
    clients_a_chercher = ['BUQUET', 'LAA', 'PHARMABEST', 'SEXTANT', 'AIXAGON', 'UAI']
    
    # Recherche générale d'abord
    print('\n1️⃣ RECHERCHE GÉNÉRALE (90 derniers jours)')
    print('-'*80)
    
    all_emails = search_sent_emails("", 90)
    
    if not all_emails:
        print("❌ Impossible de lire les emails")
        return
    
    print(f"📧 {len(all_emails)} emails envoyés trouvés")
    
    # Analyser les emails
    factures_trouvees = {}
    emails_clients = {}
    
    for email in all_emails:
        subject = email.get('subject', '')
        body = email.get('bodyPreview', '')
        recipients = email.get('toRecipients', [])
        to_list = [r['emailAddress']['address'] for r in recipients]
        date = email.get('sentDateTime', '')[:10]
        
        # Chercher F2025 dans sujet ou corps
        import re
        content = subject + ' ' + body
        matches = re.findall(r'F2025\d{3,4}', content)
        
        if matches:
            for num in matches:
                if num not in factures_trouvees:
                    factures_trouvees[num] = {
                        'destinataires': to_list,
                        'date': date,
                        'sujet': subject[:80]
                    }
        
        # Chercher les clients dans les destinataires
        for client in clients_a_chercher:
            for dest in to_list:
                if client.lower() in dest.lower() or any(c.lower() in subject.lower() for c in [client, 'facture']):
                    if client not in emails_clients:
                        emails_clients[client] = []
                    emails_clients[client].append({
                        'date': date,
                        'destinataire': dest,
                        'sujet': subject[:60]
                    })
                    break
    
    # Afficher les résultats
    print('\n2️⃣ FACTURES F2025 TROUVÉES:')
    print('-'*80)
    
    if factures_trouvees:
        for num in sorted(factures_trouvees.keys()):
            info = factures_trouvees[num]
            dests = ', '.join(info['destinataires'])[:60]
            print(f"{num} → {dests} | {info['date']}")
        print(f'\n✅ Total: {len(factures_trouvees)} factures F2025')
    else:
        print("❌ Aucune facture F2025 trouvée")
    
    # Recherche spécifique BUQUET
    print('\n3️⃣ RECHERCHE SPÉCIFIQUE "BUQUET":')
    print('-'*80)
    
    buquet_found = False
    for email in all_emails:
        recipients = email.get('toRecipients', [])
        to_emails = [r['emailAddress']['address'] for r in recipients]
        subject = email.get('subject', '')
        date = email.get('sentDateTime', '')[:10]
        
        # Chercher BUQUET dans destinataires ou sujet
        if any('buquet' in dest.lower() for dest in to_emails) or 'buquet' in subject.lower():
            print(f"{date} | {', '.join(to_emails)[:40]} | {subject[:60]}")
            buquet_found = True
    
    if not buquet_found:
        print("❌ Aucun email envoyé à BUQUET trouvé")
    
    # Emails par client
    print('\n4️⃣ EMAILS PAR CLIENT (avec "facture" ou nom client):')
    print('-'*80)
    
    for client, emails in emails_clients.items():
        print(f'\n{client}: {len(emails)} emails')
        for email in emails[:3]:  # Max 3 par client
            print(f"  {email['date']} | {email['sujet']}")

if __name__ == "__main__":
    main()
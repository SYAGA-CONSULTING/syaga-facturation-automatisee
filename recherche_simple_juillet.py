#!/usr/bin/env python3
"""
Recherche simple dans TOUS les emails de juillet-août 2025
"""

import sys
import urllib.request
import urllib.parse
import json
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

def get_all_sent_emails():
    """Récupérer TOUS les emails envoyés de juillet-août 2025"""
    access_token = get_access_token()
    if not access_token:
        return None
    
    # URL pour lire les emails envoyés
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    # Filtrer uniquement juillet-août 2025
    params_dict = {
        '$filter': "sentDateTime ge 2025-07-01T00:00:00Z and sentDateTime le 2025-08-31T23:59:59Z",
        '$top': '999',  # Maximum
        '$select': 'subject,toRecipients,sentDateTime,bodyPreview',
        '$orderby': 'sentDateTime desc'
    }
    
    params = '?' + urllib.parse.urlencode(params_dict)
    
    try:
        print("🔄 Récupération des emails envoyés juillet-août 2025...")
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('value', [])
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

def main():
    print('🔍 RECHERCHE COMPLÈTE JUILLET-AOÛT 2025')
    print('='*80)
    
    emails = get_all_sent_emails()
    
    if not emails:
        print("❌ Impossible de récupérer les emails")
        return
    
    print(f"✅ {len(emails)} emails trouvés pour juillet-août 2025\n")
    
    # Chercher TOUTES les factures et mentions clients
    print('📋 EMAILS AVEC FACTURES OU CLIENTS:')
    print('-'*80)
    
    clients_importants = ['BUQUET', 'LAA', 'PHARMABEST', 'SEXTANT', 'AIXAGON', 'UAI', 'QUADRIMEX', 'PETRAS']
    
    for email in emails:
        subject = email.get('subject', '')
        body_preview = email.get('bodyPreview', '')
        recipients = email.get('toRecipients', [])
        to_list = [r['emailAddress']['address'] for r in recipients]
        date = email.get('sentDateTime', '')[:10]
        
        # Chercher F2025 ou un client
        import re
        has_f2025 = bool(re.search(r'F2025\d{3,4}', subject + ' ' + body_preview))
        has_client = any(client.lower() in (subject + ' ' + ' '.join(to_list)).lower() for client in clients_importants)
        has_facture = 'facture' in subject.lower()
        
        if has_f2025 or has_client or has_facture:
            # Extraire le numéro F2025 si présent
            f2025_nums = re.findall(r'F2025\d{3,4}', subject + ' ' + body_preview)
            nums_str = ' [' + ', '.join(f2025_nums) + ']' if f2025_nums else ''
            
            # Identifier le client
            client_found = ''
            for client in clients_importants:
                if client.lower() in (subject + ' ' + ' '.join(to_list)).lower():
                    client_found = client
                    break
            
            # Afficher
            dest_str = ', '.join(to_list)[:40]
            print(f"{date} | {client_found:<10} | {dest_str:<40} | {subject[:50]}{nums_str}")

if __name__ == "__main__":
    main()
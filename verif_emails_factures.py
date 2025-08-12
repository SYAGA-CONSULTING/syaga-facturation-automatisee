#!/usr/bin/env python3
"""
Vérification des factures dans les emails envoyés
Utilise l'API Graph directement avec les credentials Azure
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

def read_sent_emails(days_back=60):
    """Lire les emails envoyés avec factures"""
    access_token = get_access_token()
    if not access_token:
        return None
    
    # URL pour lire les emails envoyés
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    # Filtrer sur les 60 derniers jours et chercher F2025 ou facture
    date_filter = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%dT%H:%M:%SZ')
    # Encoder correctement les paramètres
    params_dict = {
        '$filter': f'sentDateTime ge {date_filter}',
        '$top': '100',
        '$select': 'subject,toRecipients,sentDateTime,hasAttachments',
        '$orderby': 'sentDateTime desc'
    }
    params = '?' + urllib.parse.urlencode(params_dict)
    
    try:
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('value', [])
    except Exception as e:
        print(f"❌ Erreur lecture emails envoyés: {e}")
        return None

def main():
    print('🔍 RECHERCHE DES FACTURES F2025 DANS LES EMAILS ENVOYÉS')
    print('='*80)
    
    emails = read_sent_emails(60)
    
    if not emails:
        print("❌ Impossible de lire les emails envoyés")
        return
    
    print(f"📧 {len(emails)} emails envoyés trouvés (60 derniers jours)")
    print('-'*80)
    
    # Chercher les factures F2025
    factures_trouvees = {}
    emails_factures = []
    
    for email in emails:
        subject = email.get('subject', '')
        
        # Chercher F2025 dans le sujet
        if 'F2025' in subject or 'facture' in subject.lower():
            recipients = email.get('toRecipients', [])
            to_list = [r['emailAddress']['address'] for r in recipients]
            date = email.get('sentDateTime', '')[:10]
            
            # Extraire numéros F2025
            import re
            matches = re.findall(r'F2025\d{3,4}', subject)
            
            if matches:
                for num in matches:
                    if num not in factures_trouvees:
                        factures_trouvees[num] = {
                            'destinataire': ', '.join(to_list),
                            'date': date,
                            'sujet': subject[:80]
                        }
            
            # Garder aussi les emails avec "facture" sans numéro
            if 'facture' in subject.lower():
                emails_factures.append({
                    'date': date,
                    'destinataire': ', '.join(to_list)[:40],
                    'sujet': subject[:60]
                })
    
    # Afficher les factures F2025 trouvées
    print('\n📋 FACTURES F2025 TROUVÉES DANS LES EMAILS:')
    print('-'*80)
    
    if factures_trouvees:
        for num in sorted(factures_trouvees.keys()):
            info = factures_trouvees[num]
            print(f"{num} → {info['destinataire'][:40]} | {info['date']}")
        
        print(f'\n✅ Total: {len(factures_trouvees)} factures F2025 envoyées')
        print(f'Numéros: {sorted(factures_trouvees.keys())}')
    else:
        print("Aucune facture F2025 trouvée dans les emails envoyés")
    
    # Afficher aussi les autres emails avec "facture"
    if emails_factures:
        print('\n📄 AUTRES EMAILS AVEC "FACTURE":')
        print('-'*80)
        for email in emails_factures[:10]:  # Limiter à 10
            print(f"{email['date']} | {email['destinataire']} | {email['sujet']}")

if __name__ == "__main__":
    main()
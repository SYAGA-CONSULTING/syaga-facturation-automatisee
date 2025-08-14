#!/usr/bin/env python3
"""
VÉRIFICATION : Quel est le dernier email envoyé ?
"""

import urllib.request
import urllib.parse
import json
from pathlib import Path

def load_azure_config():
    config_path = Path.home() / '.azure_config'
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

def main():
    print('🔍 VÉRIFICATION DU DERNIER EMAIL ENVOYÉ')
    print('='*50)
    
    access_token = get_access_token()
    if not access_token:
        return
    
    # Récupérer les 20 derniers emails envoyés
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    params_dict = {
        '$top': '500',
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
            emails = data.get('value', [])
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return
    
    if not emails:
        print("❌ Aucun email trouvé")
        return
    
    print(f"📧 {len(emails)} derniers emails envoyés:\n")
    
    for i, email in enumerate(emails, 1):
        date = email.get('sentDateTime', 'N/A')
        subject = email.get('subject', 'Sans sujet')
        recipients = email.get('toRecipients', [])
        has_attachments = email.get('hasAttachments', False)
        
        # Formater la date
        date_formatted = date[:19].replace('T', ' ') if date != 'N/A' else 'N/A'
        
        # Extraire destinataires
        to_emails = [r['emailAddress']['address'] for r in recipients]
        recipients_str = ', '.join(to_emails)[:60]
        
        # Marquer les pièces jointes
        attachment_marker = ' 📎' if has_attachments else ''
        
        print(f"{i:2}. {date_formatted}")
        print(f"    → {recipients_str}")
        print(f"    📝 {subject[:70]}{attachment_marker}")
        print()
    
    # Vérifier spécifiquement les emails de juillet/août 2025
    july_august_emails = [e for e in emails if e.get('sentDateTime', '').startswith(('2025-07', '2025-08'))]
    
    if july_august_emails:
        print('='*50)
        print(f'📅 EMAILS JUILLET/AOÛT 2025 ({len(july_august_emails)}):')
        print('-'*50)
        
        for email in july_august_emails:
            date = email.get('sentDateTime', '')[:10]
            subject = email.get('subject', '')
            recipients = email.get('toRecipients', [])
            has_attachments = email.get('hasAttachments', False)
            
            to_emails = [r['emailAddress']['address'] for r in recipients]
            att_marker = ' 📎' if has_attachments else ''
            
            print(f"📅 {date} → {', '.join(to_emails)[:40]}")
            print(f"   📝 {subject[:50]}{att_marker}")
    else:
        print('='*50)
        print('❌ AUCUN EMAIL JUILLET/AOÛT 2025 DANS LES 20 DERNIERS')

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
RECHERCHE SPÉCIFIQUE : Email 10 juillet à Anthony CIMO avec F20250706.pdf
"""

import sys
import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta
from pathlib import Path
import re

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

def search_anthony_cimo_emails():
    """Rechercher emails à Anthony CIMO autour du 10 juillet"""
    access_token = get_access_token()
    if not access_token:
        return []
    
    # Rechercher emails du 8 au 15 juillet avec Anthony CIMO
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    # Filtre pour Anthony CIMO et dates juillet
    filter_str = "toRecipients/any(r:contains(r/emailAddress/address,'cimo')) and sentDateTime ge 2025-07-08T00:00:00Z and sentDateTime le 2025-07-15T23:59:59Z"
    
    params_dict = {
        '$top': '50',
        '$select': 'subject,toRecipients,sentDateTime,hasAttachments,id',
        '$filter': filter_str,
        '$orderby': 'sentDateTime desc'
    }
    
    params = '?' + urllib.parse.urlencode(params_dict)
    
    try:
        print("🔄 Recherche emails Anthony CIMO 8-15 juillet...")
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('value', [])
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return []

def get_attachments_for_email(email_id, access_token):
    """Récupérer les pièces jointes d'un email spécifique"""
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages/{email_id}/attachments"
    
    params_dict = {
        '$select': 'name,contentType,size'
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
        print(f"❌ Erreur attachments: {e}")
        return []

def main():
    print('🎯 RECHERCHE ANTHONY CIMO - 10 JUILLET - F20250706.pdf')
    print('='*80)
    
    # Rechercher les emails à Anthony CIMO
    emails = search_anthony_cimo_emails()
    
    if not emails:
        print("❌ Aucun email trouvé pour Anthony CIMO en juillet")
        return
    
    print(f"✅ {len(emails)} email(s) trouvé(s) pour Anthony CIMO\n")
    
    access_token = get_access_token()
    
    # Analyser chaque email
    for email in emails:
        subject = email.get('subject', '')
        recipients = email.get('toRecipients', [])
        date = email.get('sentDateTime', '')
        email_id = email.get('id', '')
        has_attachments = email.get('hasAttachments', False)
        
        # Formater la date
        date_formatted = date[:10] if date else 'N/A'
        
        # Extraire les destinataires
        to_emails = [r['emailAddress']['address'] for r in recipients]
        anthony_email = [email for email in to_emails if 'cimo' in email.lower()]
        
        print(f"📧 EMAIL du {date_formatted}:")
        print(f"   Sujet: {subject}")
        print(f"   Destinataires: {', '.join(to_emails)}")
        print(f"   Anthony: {', '.join(anthony_email) if anthony_email else 'NON TROUVÉ'}")
        print(f"   Pièces jointes: {'✅ OUI' if has_attachments else '❌ NON'}")
        
        if has_attachments and access_token:
            # Récupérer les pièces jointes
            attachments = get_attachments_for_email(email_id, access_token)
            
            if attachments:
                print(f"   📎 {len(attachments)} pièce(s) jointe(s):")
                
                for attachment in attachments:
                    name = attachment.get('name', '')
                    content_type = attachment.get('contentType', '')
                    size = attachment.get('size', 0)
                    
                    # Vérifier si c'est F20250706.pdf
                    is_f20250706 = 'F20250706' in name
                    status = '🎯 F20250706.pdf TROUVÉE!' if is_f20250706 else ''
                    
                    print(f"     • {name} ({content_type}) - {size} bytes {status}")
        
        print("-" * 60)
    
    print('\n🔍 RECHERCHE ÉLARGIE - TOUS LES PDF F2025 EN JUILLET:')
    print('='*80)
    
    # Recherche élargie tous emails juillet avec pièces jointes
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    filter_str = "hasAttachments eq true and sentDateTime ge 2025-07-01T00:00:00Z and sentDateTime le 2025-07-31T23:59:59Z"
    
    params_dict = {
        '$top': '100',
        '$select': 'subject,toRecipients,sentDateTime,hasAttachments,id',
        '$filter': filter_str,
        '$orderby': 'sentDateTime desc'
    }
    
    params = '?' + urllib.parse.urlencode(params_dict)
    
    try:
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            july_emails = data.get('value', [])
    except Exception as e:
        print(f"❌ Erreur recherche juillet: {e}")
        july_emails = []
    
    print(f"📊 {len(july_emails)} emails avec pièces jointes en juillet")
    
    # Chercher les PDF F2025
    pdf_f2025_found = []
    
    for email in july_emails:
        email_id = email.get('id', '')
        date = email.get('sentDateTime', '')[:10]
        recipients = email.get('toRecipients', [])
        to_emails = [r['emailAddress']['address'] for r in recipients]
        
        attachments = get_attachments_for_email(email_id, access_token)
        
        for attachment in attachments:
            name = attachment.get('name', '')
            
            # Chercher F2025xxxx.pdf
            if re.search(r'F2025\d+\.pdf', name, re.IGNORECASE):
                pdf_f2025_found.append({
                    'date': date,
                    'filename': name,
                    'recipients': ', '.join(to_emails)[:60],
                    'subject': email.get('subject', '')[:40]
                })
    
    if pdf_f2025_found:
        print(f"\n📄 {len(pdf_f2025_found)} PDF F2025 trouvés en juillet:")
        print("-" * 80)
        for pdf in sorted(pdf_f2025_found, key=lambda x: x['date']):
            print(f"{pdf['date']} | {pdf['filename']:<15} | {pdf['recipients'][:30]}")
            if 'F20250706' in pdf['filename']:
                print("  🎯 ** C'EST NOTRE FACTURE F20250706.pdf ! **")
    else:
        print("\n❌ Aucun PDF F2025 trouvé en juillet")

if __name__ == "__main__":
    main()
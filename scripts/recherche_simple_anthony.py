#!/usr/bin/env python3
"""
RECHERCHE SIMPLE : Anthony CIMO juillet 2025
"""

import sys
import urllib.request
import urllib.parse
import json
from datetime import datetime
from pathlib import Path
import re

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
    print('🔍 RECHERCHE SIMPLE ANTHONY CIMO - JUILLET 2025')
    print('='*60)
    
    access_token = get_access_token()
    if not access_token:
        return
    
    # Recherche basique emails juillet avec pièces jointes
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    params_dict = {
        '$top': '200',
        '$select': 'subject,toRecipients,sentDateTime,hasAttachments,id',
        '$orderby': 'sentDateTime desc'
    }
    
    params = '?' + urllib.parse.urlencode(params_dict)
    
    try:
        print("📧 Récupération des emails envoyés...")
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            all_emails = data.get('value', [])
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return
    
    print(f"✅ {len(all_emails)} emails récupérés")
    
    # Filtrer emails juillet avec "cimo" et pièces jointes
    anthony_emails = []
    july_emails_with_attachments = []
    
    for email in all_emails:
        date = email.get('sentDateTime', '')
        recipients = email.get('toRecipients', [])
        has_attachments = email.get('hasAttachments', False)
        
        # Vérifier si c'est juillet 2025
        is_july = date.startswith('2025-07')
        
        if is_july and has_attachments:
            july_emails_with_attachments.append(email)
            
            # Vérifier si Anthony CIMO dans destinataires
            to_emails = [r['emailAddress']['address'].lower() for r in recipients]
            if any('cimo' in email_addr for email_addr in to_emails):
                anthony_emails.append(email)
    
    print(f"📊 {len(july_emails_with_attachments)} emails juillet avec pièces jointes")
    print(f"🎯 {len(anthony_emails)} emails à Anthony CIMO en juillet")
    
    if anthony_emails:
        print('\n' + '='*60)
        print('📧 EMAILS À ANTHONY CIMO EN JUILLET:')
        print('-'*60)
        
        for email in anthony_emails:
            date = email.get('sentDateTime', '')[:10]
            subject = email.get('subject', '')
            recipients = email.get('toRecipients', [])
            email_id = email.get('id', '')
            
            to_emails = [r['emailAddress']['address'] for r in recipients]
            anthony_addr = [addr for addr in to_emails if 'cimo' in addr.lower()]
            
            print(f"📅 {date}")
            print(f"📧 {anthony_addr[0] if anthony_addr else 'N/A'}")
            print(f"📝 {subject}")
            
            # Récupérer pièces jointes
            att_url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages/{email_id}/attachments"
            att_params = '?$select=name,contentType,size'
            
            try:
                att_req = urllib.request.Request(att_url + att_params, method='GET')
                att_req.add_header('Authorization', f'Bearer {access_token}')
                att_req.add_header('Content-Type', 'application/json')
                
                with urllib.request.urlopen(att_req) as att_response:
                    att_data = json.loads(att_response.read().decode('utf-8'))
                    attachments = att_data.get('value', [])
                
                if attachments:
                    print(f"📎 {len(attachments)} pièce(s) jointe(s):")
                    for att in attachments:
                        name = att.get('name', '')
                        size = att.get('size', 0)
                        is_f20250706 = 'F20250706' in name
                        marker = ' 🎯 TROUVÉE!' if is_f20250706 else ''
                        print(f"   • {name} ({size} bytes){marker}")
                
            except Exception as e:
                print(f"   ❌ Erreur pièces jointes: {e}")
            
            print('-' * 40)
    
    # Recherche élargie F20250706 dans TOUS les emails juillet
    print('\n' + '='*60)
    print('🔍 RECHERCHE F20250706.pdf DANS TOUS LES EMAILS JUILLET:')
    print('-'*60)
    
    f20250706_found = []
    
    for email in july_emails_with_attachments:
        email_id = email.get('id', '')
        date = email.get('sentDateTime', '')[:10]
        subject = email.get('subject', '')
        recipients = email.get('toRecipients', [])
        
        # Récupérer pièces jointes
        att_url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages/{email_id}/attachments"
        att_params = '?$select=name'
        
        try:
            att_req = urllib.request.Request(att_url + att_params, method='GET')
            att_req.add_header('Authorization', f'Bearer {access_token}')
            
            with urllib.request.urlopen(att_req) as att_response:
                att_data = json.loads(att_response.read().decode('utf-8'))
                attachments = att_data.get('value', [])
            
            for att in attachments:
                name = att.get('name', '')
                if 'F20250706' in name:
                    to_emails = [r['emailAddress']['address'] for r in recipients]
                    f20250706_found.append({
                        'date': date,
                        'filename': name,
                        'recipients': ', '.join(to_emails),
                        'subject': subject
                    })
        
        except Exception:
            continue
    
    if f20250706_found:
        print(f"🎯 F20250706.pdf trouvée dans {len(f20250706_found)} email(s):")
        for finding in f20250706_found:
            print(f"✅ {finding['date']} → {finding['recipients'][:50]}")
            print(f"   📎 {finding['filename']}")
            print(f"   📝 {finding['subject'][:50]}")
            print()
    else:
        print("❌ F20250706.pdf introuvable dans les emails juillet")

if __name__ == "__main__":
    main()
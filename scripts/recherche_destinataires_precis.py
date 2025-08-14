#!/usr/bin/env python3
"""
RECHERCHE DESTINATAIRES PRÉCIS - Analyse emails aux dates exactes
Pour identifier les vraies adresses email de destination
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
    
    req = urllib.request.Request(token_url, data=token_data, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    
    with urllib.request.urlopen(req) as response:
        token_response = json.loads(response.read().decode('utf-8'))
        return token_response.get('access_token')

def analyser_emails_dates_precises():
    """Analyser emails aux dates précises Excel pour trouver les destinataires"""
    
    print('🔍 RECHERCHE DESTINATAIRES PRÉCIS AUX DATES EXCEL')
    print('='*60)
    
    access_token = get_access_token()
    if not access_token:
        return {}
    
    # Factures à rechercher avec leurs dates Excel confirmées
    recherches = [
        {'date': '2025-07-16', 'facture': 'F20250745', 'client': 'BUQUET'},
        {'date': '2025-08-09', 'facture': 'F20250746', 'client': 'LAA'},
        {'date': '2025-08-09', 'facture': 'F20250747', 'client': 'PHARMABEST'}
    ]
    
    resultats = {}
    
    for recherche in recherches:
        date = recherche['date']
        facture = recherche['facture']
        client = recherche['client']
        
        print(f"\n📧 RECHERCHE {facture} ({client}) - Date: {date}")
        print('-' * 40)
        
        # Recherche emails avec PJ pour cette date précise
        url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
        
        params_dict = {
            '$filter': f"sentDateTime ge {date}T00:00:00Z and sentDateTime le {date}T23:59:59Z and hasAttachments eq true",
            '$select': 'subject,toRecipients,ccRecipients,sentDateTime,hasAttachments,id',
            '$orderby': 'sentDateTime desc'
        }
        
        params = '?' + urllib.parse.urlencode(params_dict)
        
        try:
            req = urllib.request.Request(url + params, method='GET')
            req.add_header('Authorization', f'Bearer {access_token}')
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                emails = data.get('value', [])
            
            print(f"  📨 {len(emails)} emails avec PJ trouvés le {date}")
            
            for email in emails:
                email_id = email.get('id', '')
                subject = email.get('subject', '')
                sent_time = email.get('sentDateTime', '')
                to_recipients = email.get('toRecipients', [])
                cc_recipients = email.get('ccRecipients', [])
                
                # Extraire adresses destinataires
                to_emails = [r['emailAddress']['address'] for r in to_recipients]
                cc_emails = [r['emailAddress']['address'] for r in cc_recipients]
                all_recipients = to_emails + cc_emails
                
                # Analyser pièces jointes
                attach_url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages/{email_id}/attachments"
                attach_params = '?$select=name'
                
                try:
                    attach_req = urllib.request.Request(attach_url + attach_params, method='GET')
                    attach_req.add_header('Authorization', f'Bearer {access_token}')
                    
                    with urllib.request.urlopen(attach_req) as attach_response:
                        attach_data = json.loads(attach_response.read().decode('utf-8'))
                        attachments = attach_data.get('value', [])
                    
                    # Rechercher notre facture
                    import re
                    for attachment in attachments:
                        name = attachment.get('name', '')
                        if facture.lower() in name.lower():
                            print(f"  ✅ TROUVÉ! {sent_time[:16]}")
                            print(f"     📝 Sujet: {subject}")
                            print(f"     📎 PJ: {name}")
                            print(f"     👥 TO: {', '.join(to_emails)}")
                            if cc_emails:
                                print(f"     📧 CC: {', '.join(cc_emails)}")
                            
                            # Identifier les clients (pas sebastien.questier@syaga.fr)
                            clients_emails = [email for email in all_recipients 
                                            if 'sebastien.questier@syaga.fr' not in email.lower()]
                            
                            if clients_emails:
                                resultats[facture] = {
                                    'destinataires': clients_emails,
                                    'date_envoi': date,
                                    'sujet': subject,
                                    'client': client
                                }
                                print(f"     🎯 CLIENTS: {', '.join(clients_emails)}")
                            
                            break
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"  ❌ Erreur recherche {date}: {e}")
    
    print("\n" + "="*60)
    print("🎯 RÉSULTATS FINAUX:")
    print("="*60)
    
    for facture, info in resultats.items():
        print(f"✅ {facture} ({info['client']}) → {', '.join(info['destinataires'])} le {info['date_envoi']}")
    
    return resultats

if __name__ == "__main__":
    analyser_emails_dates_precises()
#!/usr/bin/env python3
"""
ANALYSE DÉTAILLÉE 10 JUILLET - Vérification F20250705 + F20250706
Correction : Un email peut être envoyé AU CLIENT ET en copie à soi-même
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

def analyser_emails_10_juillet():
    """Analyse détaillée des emails du 10 juillet 2025"""
    
    print('🔍 ANALYSE DÉTAILLÉE EMAIL 10 JUILLET 2025')
    print('='*60)
    print('🎯 Objectif: Vérifier si F20250705 + F20250706 vraiment envoyées à anthony.cimo@pharmabest.com')
    print()
    
    access_token = get_access_token()
    if not access_token:
        print("❌ Impossible d'obtenir le token")
        return
    
    # Recherche emails 10 juillet 2025 avec pièces jointes
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    # Filtre spécifique 10 juillet
    params_dict = {
        '$filter': "sentDateTime ge 2025-07-10T00:00:00Z and sentDateTime le 2025-07-10T23:59:59Z and hasAttachments eq true",
        '$select': 'subject,toRecipients,ccRecipients,bccRecipients,sentDateTime,hasAttachments,id',
        '$orderby': 'sentDateTime desc'
    }
    
    params = '?' + urllib.parse.urlencode(params_dict)
    
    try:
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            emails = data.get('value', [])
        
        print(f"📧 {len(emails)} emails avec pièces jointes trouvés le 10/07/2025")
        
        for i, email in enumerate(emails):
            subject = email.get('subject', '')
            to_recipients = email.get('toRecipients', [])
            cc_recipients = email.get('ccRecipients', [])
            bcc_recipients = email.get('bccRecipients', [])
            sent_time = email.get('sentDateTime', '')
            email_id = email.get('id', '')
            
            # Extraire toutes les adresses
            to_emails = [r['emailAddress']['address'] for r in to_recipients]
            cc_emails = [r['emailAddress']['address'] for r in cc_recipients]
            bcc_emails = [r['emailAddress']['address'] for r in bcc_recipients]
            
            all_recipients = to_emails + cc_emails + bcc_emails
            
            print(f"\\n📧 EMAIL #{i+1} - {sent_time[:19]}")
            print(f"   📝 Sujet: {subject}")
            print(f"   👥 TO: {', '.join(to_emails) if to_emails else 'Aucun'}")
            if cc_emails:
                print(f"   📧 CC: {', '.join(cc_emails)}")
            if bcc_emails:
                print(f"   🔒 BCC: {', '.join(bcc_emails)}")
            
            # Analyser pièces jointes
            attach_url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages/{email_id}/attachments"
            attach_params = '?$select=name,contentType,size'
            
            try:
                attach_req = urllib.request.Request(attach_url + attach_params, method='GET')
                attach_req.add_header('Authorization', f'Bearer {access_token}')
                
                with urllib.request.urlopen(attach_req) as attach_response:
                    attach_data = json.loads(attach_response.read().decode('utf-8'))
                    attachments = attach_data.get('value', [])
                
                # Rechercher factures F2025
                import re
                factures_trouvees = []
                for att in attachments:
                    name = att.get('name', '')
                    matches = re.findall(r'F2025\\d{2,4}', name, re.IGNORECASE)
                    factures_trouvees.extend(matches)
                
                if factures_trouvees:
                    print(f"   📎 FACTURES TROUVÉES: {', '.join(set(factures_trouvees))}")
                    
                    # ANALYSE CRITIQUE DES DESTINATAIRES
                    anthony_emails = [email for email in all_recipients if 'anthony' in email.lower() or 'cimo' in email.lower()]
                    pharmabest_emails = [email for email in all_recipients if 'pharmabest' in email.lower()]
                    sebastien_emails = [email for email in all_recipients if 'sebastien.questier@syaga.fr' in email]
                    
                    client_emails = list(set(anthony_emails + pharmabest_emails))
                    
                    print(f"   🎯 ANALYSE DESTINATAIRES:")
                    if client_emails:
                        print(f"      ✅ CLIENT PHARMABEST: {', '.join(client_emails)}")
                    if sebastien_emails:
                        print(f"      📁 ARCHIVE PERSO: {', '.join(sebastien_emails)}")
                    
                    # VERDICT FINAL
                    if client_emails and sebastien_emails:
                        print(f"      🎉 VERDICT: ENVOI MIXTE - Client + Archive!")
                        print(f"      ✅ Factures vraiment envoyées au client PHARMABEST")
                    elif client_emails:
                        print(f"      ✅ VERDICT: ENVOI CLIENT SEUL")
                        print(f"      ✅ Factures vraiment envoyées au client PHARMABEST")
                    elif sebastien_emails:
                        print(f"      ⚠️  VERDICT: AUTO-ENVOI SEUL")
                        print(f"      ❌ Factures PAS envoyées au client (archive seule)")
                    else:
                        print(f"      ❓ VERDICT: DESTINATAIRES INCONNUS")
                        print(f"      ❓ Factures envoyées à: {', '.join(all_recipients[:3])}")
                else:
                    print(f"   📎 Pièces jointes: {[att['name'] for att in attachments[:3]]}")
                    
            except Exception as e:
                print(f"   ❌ Erreur analyse PJ: {e}")
    
    except Exception as e:
        print(f"❌ Erreur recherche emails: {e}")

if __name__ == "__main__":
    analyser_emails_10_juillet()
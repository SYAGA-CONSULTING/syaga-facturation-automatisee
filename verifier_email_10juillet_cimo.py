#!/usr/bin/env python3
"""
VÉRIFICATION CIBLÉE : Email 10 juillet Anthony CIMO avec pièces jointes
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
    print('🎯 VÉRIFICATION EMAIL 10 JUILLET - ANTHONY CIMO')
    print('='*60)
    
    access_token = get_access_token()
    if not access_token:
        return
    
    # Rechercher l'email exact du 10 juillet avec Anthony CIMO
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    params_dict = {
        '$top': '100',
        '$select': 'subject,toRecipients,sentDateTime,hasAttachments,id',
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
    
    # Trouver l'email du 10 juillet à Anthony CIMO
    target_email = None
    
    for email in emails:
        date = email.get('sentDateTime', '')
        recipients = email.get('toRecipients', [])
        has_attachments = email.get('hasAttachments', False)
        
        # Vérifier si c'est le 10 juillet 2025
        is_july_10 = date.startswith('2025-07-10')
        
        if is_july_10 and has_attachments:
            # Vérifier si Anthony CIMO dans destinataires
            to_emails = [r['emailAddress']['address'].lower() for r in recipients]
            if any('cimo' in email_addr for email_addr in to_emails):
                target_email = email
                break
    
    if not target_email:
        print("❌ Email du 10 juillet à Anthony CIMO introuvable")
        return
    
    # Afficher les détails de l'email trouvé
    date = target_email.get('sentDateTime', '')
    subject = target_email.get('subject', '')
    recipients = target_email.get('toRecipients', [])
    email_id = target_email.get('id', '')
    
    to_emails = [r['emailAddress']['address'] for r in recipients]
    
    print(f"✅ EMAIL TROUVÉ :")
    print(f"📅 Date: {date}")
    print(f"📧 Destinataires: {', '.join(to_emails)}")
    print(f"📝 Sujet: {subject}")
    print(f"🆔 ID: {email_id[:20]}...")
    
    # Récupérer les pièces jointes
    print(f"\n🔍 RÉCUPÉRATION DES PIÈCES JOINTES...")
    print("-" * 60)
    
    att_url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages/{email_id}/attachments"
    att_params = '?$select=name,contentType,size'
    
    try:
        att_req = urllib.request.Request(att_url + att_params, method='GET')
        att_req.add_header('Authorization', f'Bearer {access_token}')
        att_req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(att_req) as att_response:
            att_data = json.loads(att_response.read().decode('utf-8'))
            attachments = att_data.get('value', [])
    except Exception as e:
        print(f"❌ Erreur pièces jointes: {e}")
        return
    
    if not attachments:
        print("❌ Aucune pièce jointe trouvée")
        return
    
    print(f"📎 {len(attachments)} PIÈCE(S) JOINTE(S) TROUVÉE(S):")
    print("=" * 60)
    
    f20250706_found = False
    
    for i, attachment in enumerate(attachments, 1):
        name = attachment.get('name', '')
        content_type = attachment.get('contentType', '')
        size = attachment.get('size', 0)
        
        # Vérifier si c'est F20250706.pdf
        is_target_pdf = 'F20250706' in name
        
        if is_target_pdf:
            f20250706_found = True
            print(f"🎯 #{i}. {name}")
            print(f"     Type: {content_type}")
            print(f"     Taille: {size} bytes")
            print(f"     ✅ ** C'EST NOTRE FACTURE F20250706.pdf ! **")
        else:
            print(f"📄 #{i}. {name}")
            print(f"     Type: {content_type}")
            print(f"     Taille: {size} bytes")
        
        print()
    
    # Résultat final
    print("=" * 60)
    print("🏆 RÉSULTAT FINAL:")
    print("-" * 60)
    
    if f20250706_found:
        print("✅ F20250706.pdf CONFIRMÉE dans l'email du 10 juillet à Anthony CIMO !")
        print("✅ STATUT: 'Créée mais non envoyée' INCORRECT → DÉJÀ ENVOYÉE")
        print("✅ Le tableau HTML doit être mis à jour")
    else:
        print("❌ F20250706.pdf NON trouvée dans cet email")
        print("❓ Vérifier d'autres emails ou noms de fichiers")
    
    print(f"\n📊 TOTAL: {len(attachments)} pièces jointes analysées")

if __name__ == "__main__":
    main()
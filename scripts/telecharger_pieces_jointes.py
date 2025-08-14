#!/usr/bin/env python3
"""
TÉLÉCHARGEMENT : Pièces jointes des emails envoyés avec analyse des PDF F2025
"""

import urllib.request
import urllib.parse
import json
import base64
import os
from pathlib import Path
from datetime import datetime
import re

# Charger configuration Azure
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

def download_attachment(email_id, attachment_id, filename, access_token):
    """Télécharger une pièce jointe spécifique"""
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages/{email_id}/attachments/{attachment_id}"
    
    try:
        req = urllib.request.Request(url, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            att_data = json.loads(response.read().decode('utf-8'))
            
            # Récupérer le contenu en base64
            content_bytes = base64.b64decode(att_data.get('contentBytes', ''))
            
            # Créer dossier de téléchargement
            download_dir = Path('/mnt/c/temp/pieces_jointes_factures')
            download_dir.mkdir(exist_ok=True)
            
            # Sauvegarder le fichier
            file_path = download_dir / filename
            with open(file_path, 'wb') as f:
                f.write(content_bytes)
            
            print(f"✅ Téléchargé: {filename} ({len(content_bytes)} bytes)")
            return str(file_path)
            
    except Exception as e:
        print(f"❌ Erreur téléchargement {filename}: {e}")
        return None

def main():
    print('🔍 RECHERCHE ET TÉLÉCHARGEMENT DES PIÈCES JOINTES F2025')
    print('='*80)
    
    access_token = get_access_token()
    if not access_token:
        return
    
    # Rechercher emails avec pièces jointes des 2 derniers mois
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    params_dict = {
        '$top': '200',
        '$select': 'subject,toRecipients,sentDateTime,hasAttachments,id',
        '$orderby': 'sentDateTime desc'
    }
    
    params = '?' + urllib.parse.urlencode(params_dict)
    
    try:
        print("📧 Recherche des emails avec pièces jointes...")
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            emails = data.get('value', [])
    except Exception as e:
        print(f"❌ Erreur recherche emails: {e}")
        return
    
    print(f"✅ {len(emails)} emails avec pièces jointes trouvés")
    
    # Analyser chaque email pour trouver des PDF F2025
    f2025_attachments = []
    total_attachments = 0
    
    for i, email in enumerate(emails):
        email_id = email.get('id', '')
        date = email.get('sentDateTime', '')[:10]
        subject = email.get('subject', '')
        recipients = email.get('toRecipients', [])
        
        # Récupérer les pièces jointes de cet email
        att_url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages/{email_id}/attachments"
        att_params = '?$select=id,name,contentType,size'
        
        try:
            att_req = urllib.request.Request(att_url + att_params, method='GET')
            att_req.add_header('Authorization', f'Bearer {access_token}')
            
            with urllib.request.urlopen(att_req) as att_response:
                att_data = json.loads(att_response.read().decode('utf-8'))
                attachments = att_data.get('value', [])
                
                total_attachments += len(attachments)
                
                # Vérifier chaque pièce jointe
                for attachment in attachments:
                    name = attachment.get('name', '')
                    att_id = attachment.get('id', '')
                    size = attachment.get('size', 0)
                    content_type = attachment.get('contentType', '')
                    
                    # Chercher les PDF F2025
                    if re.search(r'F2025\d+\.pdf', name, re.IGNORECASE):
                        to_emails = [r['emailAddress']['address'] for r in recipients]
                        
                        f2025_attachments.append({
                            'email_id': email_id,
                            'attachment_id': att_id,
                            'filename': name,
                            'date': date,
                            'subject': subject[:50],
                            'recipients': ', '.join(to_emails)[:60],
                            'size': size,
                            'content_type': content_type
                        })
                        
                        print(f"🎯 F2025 trouvé: {name} ({date}) → {to_emails[0] if to_emails else 'N/A'}")
        
        except Exception as e:
            continue
        
        # Progress indicator
        if (i + 1) % 20 == 0:
            print(f"📊 Analysé {i + 1}/{len(emails)} emails...")
    
    # Résumé des trouvailles
    print('\n' + '='*80)
    print(f'📊 RÉSUMÉ:')
    print(f'  • {len(emails)} emails analysés')
    print(f'  • {total_attachments} pièces jointes trouvées')
    print(f'  • {len(f2025_attachments)} PDF F2025 identifiés')
    
    if not f2025_attachments:
        print("\n❌ Aucun PDF F2025 trouvé dans les pièces jointes")
        return
    
    # Afficher la liste des PDF F2025 trouvés
    print('\n🎯 PDF F2025 TROUVÉS:')
    print('-'*80)
    
    for att in sorted(f2025_attachments, key=lambda x: x['filename']):
        print(f"{att['filename']:<15} | {att['date']} | {att['recipients'][:40]}")
    
    # Demander confirmation pour téléchargement
    print('\n' + '='*80)
    print('💾 TÉLÉCHARGEMENT DES PDF F2025:')
    print('-'*80)
    
    downloaded_files = []
    
    for att in f2025_attachments:
        try:
            file_path = download_attachment(
                att['email_id'], 
                att['attachment_id'], 
                att['filename'], 
                access_token
            )
            
            if file_path:
                downloaded_files.append({
                    'filename': att['filename'],
                    'path': file_path,
                    'date': att['date'],
                    'recipients': att['recipients']
                })
        except Exception as e:
            print(f"❌ Erreur téléchargement {att['filename']}: {e}")
    
    # Résumé final
    print('\n' + '='*80)
    print(f'✅ TÉLÉCHARGEMENT TERMINÉ:')
    print(f'  • {len(downloaded_files)} PDF F2025 téléchargés')
    print(f'  • Dossier: /mnt/c/temp/pieces_jointes_factures/')
    
    if downloaded_files:
        print('\n📄 FICHIERS TÉLÉCHARGÉS:')
        for file in downloaded_files:
            print(f"  • {file['filename']} ({file['date']}) → {file['recipients'][:40]}")
        
        print('\n🔍 PROCHAINE ÉTAPE:')
        print('Utiliser le Read tool pour analyser chaque PDF téléchargé')
        
        return downloaded_files
    
    return []

if __name__ == "__main__":
    files = main()
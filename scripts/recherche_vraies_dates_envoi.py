#!/usr/bin/env python3
"""
RECHERCHE VRAIES DATES D'ENVOI : Chercher dans les éléments envoyés les dates réelles d'envoi aux clients
"""

import urllib.request
import urllib.parse
import json
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

def search_emails_by_recipient(recipient_email, access_token):
    """Chercher emails envoyés à un destinataire spécifique"""
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    params_dict = {
        '$top': '50',
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
        
        # Filtrer pour ce destinataire
        filtered_emails = []
        for email in emails:
            recipients = email.get('toRecipients', [])
            to_emails = [r['emailAddress']['address'].lower() for r in recipients]
            
            if recipient_email.lower() in to_emails:
                filtered_emails.append({
                    'date': email.get('sentDateTime', '')[:10],
                    'subject': email.get('subject', ''),
                    'has_attachments': email.get('hasAttachments', False),
                    'id': email.get('id', '')
                })
        
        return filtered_emails
        
    except Exception as e:
        print(f"❌ Erreur recherche {recipient_email}: {e}")
        return []

def get_attachments_for_email(email_id, access_token):
    """Récupérer les pièces jointes d'un email"""
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages/{email_id}/attachments"
    params = '?$select=name,contentType'
    
    try:
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            attachments = data.get('value', [])
            
        return [att.get('name', '') for att in attachments]
    except:
        return []

def main():
    print('🔍 RECHERCHE VRAIES DATES D\'ENVOI AUX CLIENTS')
    print('='*60)
    
    access_token = get_access_token()
    if not access_token:
        return
    
    # Factures à chercher avec leurs destinataires
    factures_a_chercher = {
        'F20250120': {'client': 'ANONE', 'email': 'viet.nguyen@anone.fr'},
        'F20250731': {'client': 'LAA', 'email': 'alleaume@laa.fr'},
        'F20250733': {'client': 'LAA', 'email': 'alleaume@laa.fr'},
        'F20250734': {'client': 'AXION', 'email': 'n.diaz@axion-informatique.fr'},
        'F20250735': {'client': 'ART INFO', 'email': 'h.sarda@artinformatique.net'},
        'F20250736': {'client': 'FARBOS', 'email': 'n.diaz@axion-informatique.fr'},  # Même contact AXION
        'F20250737': {'client': 'LEFEBVRE', 'email': 'mjlefebvre@selasu-mjl-avocats.com'},
        'F20250738': {'client': 'PETRAS', 'email': 'lauriane.petras@petras.fr'},
        'F20250744': {'client': 'TOUZEAU', 'email': 'commercial.diaboliqbike@gmail.com'}
    }
    
    vraies_dates_trouvees = {}
    
    print(f"🔍 Recherche en cours pour {len(factures_a_chercher)} factures...")
    
    # Chercher pour chaque client
    clients_deja_cherches = set()
    
    for numero_facture, info in factures_a_chercher.items():
        client_email = info['email']
        client_nom = info['client']
        
        if client_email not in clients_deja_cherches:
            print(f"\n📧 Recherche emails à {client_nom} ({client_email})...")
            emails = search_emails_by_recipient(client_email, access_token)
            clients_deja_cherches.add(client_email)
            
            if emails:
                print(f"   ✅ {len(emails)} emails trouvés")
                
                # Chercher emails avec pièces jointes contenant des PDF F2025
                for email in emails:
                    if email['has_attachments']:
                        attachments = get_attachments_for_email(email['id'], access_token)
                        
                        # Chercher les PDF F2025 dans les pièces jointes
                        pdf_f2025 = [att for att in attachments if re.search(r'F2025\d+\.pdf', att, re.IGNORECASE)]
                        
                        if pdf_f2025:
                            print(f"   📎 {email['date']} : {email['subject'][:50]}")
                            for pdf in pdf_f2025:
                                print(f"     • {pdf}")
                                
                                # Extraire le numéro de facture
                                match = re.search(r'F2025\d+', pdf)
                                if match:
                                    num_facture = match.group()
                                    if num_facture in factures_a_chercher:
                                        vraies_dates_trouvees[num_facture] = email['date']
                                        print(f"     🎯 TROUVÉ: {num_facture} envoyé le {email['date']}")
            else:
                print(f"   ❌ Aucun email trouvé pour {client_nom}")
    
    # Résumé des dates trouvées
    print('\n' + '='*60)
    print('📅 VRAIES DATES D\'ENVOI TROUVÉES:')
    print('-'*60)
    
    if vraies_dates_trouvees:
        for numero, date in vraies_dates_trouvees.items():
            client = factures_a_chercher[numero]['client']
            print(f"✅ {numero} - {client:<12} : {date}")
    else:
        print("❌ Aucune date d'envoi trouvée automatiquement")
        print("💡 Les factures peuvent être dans des emails groupés")
        print("💡 Ou avec des noms de fichiers différents")
    
    # Factures non trouvées
    non_trouvees = set(factures_a_chercher.keys()) - set(vraies_dates_trouvees.keys())
    if non_trouvees:
        print(f"\n⚠️  FACTURES NON TROUVÉES ({len(non_trouvees)}):")
        for numero in non_trouvees:
            client = factures_a_chercher[numero]['client']
            email = factures_a_chercher[numero]['email']
            print(f"   • {numero} - {client} → {email}")
    
    print(f"\n💡 SUGGESTIONS:")
    print("   • Vérifier si factures groupées dans un seul email")
    print("   • Chercher avec des mots-clés dans les sujets")
    print("   • Vérifier noms de fichiers alternatifs")
    
    return vraies_dates_trouvees

if __name__ == "__main__":
    dates_trouvees = main()
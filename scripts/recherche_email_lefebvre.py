#!/usr/bin/env python3
"""
RECHERCHE EMAIL LEFEBVRE - Analyse 6 mois d'emails
Pour trouver l'adresse email de l'avocate LEFEBVRE
"""

import urllib.request
import urllib.parse
import json
from pathlib import Path
from datetime import datetime, timedelta

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

def rechercher_emails_lefebvre():
    """Rechercher tous les emails contenant LEFEBVRE dans les 6 derniers mois"""
    
    print('🔍 RECHERCHE EMAIL AVOCATE LEFEBVRE - 6 MOIS')
    print('='*50)
    
    access_token = get_access_token()
    if not access_token:
        return []
    
    # Date de début : 6 mois avant aujourd'hui
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=180)  # 6 mois
    
    print(f"📅 Période: {date_debut.strftime('%Y-%m-%d')} → {date_fin.strftime('%Y-%m-%d')}")
    
    # Recherche dans les éléments ENVOYÉS avec LEFEBVRE
    print("\n📧 RECHERCHE DANS LES ÉLÉMENTS ENVOYÉS...")
    emails_envoyes = rechercher_dans_dossier('sentitems', date_debut, date_fin, access_token)
    
    # Recherche dans les éléments REÇUS avec LEFEBVRE
    print("\n📧 RECHERCHE DANS LES ÉLÉMENTS REÇUS...")
    emails_recus = rechercher_dans_dossier('inbox', date_debut, date_fin, access_token)
    
    tous_emails = emails_envoyes + emails_recus
    
    print(f"\n🎯 TOTAL: {len(tous_emails)} emails trouvés avec LEFEBVRE")
    
    # Analyser tous les emails pour extraire les adresses
    adresses_lefebvre = set()
    
    for email in tous_emails:
        to_recipients = email.get('toRecipients', [])
        from_email = email.get('from', {}).get('emailAddress', {}).get('address', '')
        cc_recipients = email.get('ccRecipients', [])
        
        # Extraire toutes les adresses
        all_addresses = []
        
        if from_email and 'lefebvre' in from_email.lower():
            all_addresses.append(from_email)
            
        for recipient in to_recipients:
            addr = recipient.get('emailAddress', {}).get('address', '')
            if addr and 'lefebvre' in addr.lower():
                all_addresses.append(addr)
                
        for recipient in cc_recipients:
            addr = recipient.get('emailAddress', {}).get('address', '')
            if addr and 'lefebvre' in addr.lower():
                all_addresses.append(addr)
        
        if all_addresses:
            adresses_lefebvre.update(all_addresses)
            print(f"  📝 {email.get('sentDateTime', email.get('receivedDateTime', ''))[:10]} - {email.get('subject', '')[:50]}")
            print(f"     📧 Adresses: {', '.join(all_addresses)}")
    
    print("\n" + "="*50)
    print("🎯 ADRESSES EMAIL LEFEBVRE TROUVÉES:")
    print("="*50)
    
    if adresses_lefebvre:
        for adresse in sorted(adresses_lefebvre):
            print(f"✅ {adresse}")
    else:
        print("❌ Aucune adresse email LEFEBVRE trouvée")
    
    return list(adresses_lefebvre)

def rechercher_dans_dossier(dossier, date_debut, date_fin, access_token):
    """Rechercher emails dans un dossier spécifique"""
    
    emails = []
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/{dossier}/messages"
    
    # Recherche avec plusieurs termes LEFEBVRE
    termes_recherche = ['lefebvre', 'LEFEBVRE', 'Lefebvre', 'mjlefebvre', 'selasu']
    
    for terme in termes_recherche:
        print(f"  🔍 Recherche terme: {terme}")
        
        params_dict = {
            '$filter': f"receivedDateTime ge {date_debut.strftime('%Y-%m-%d')}T00:00:00Z and receivedDateTime le {date_fin.strftime('%Y-%m-%d')}T23:59:59Z",
            '$search': f'"{terme}"',
            '$select': 'subject,toRecipients,ccRecipients,from,sentDateTime,receivedDateTime,id',
            '$top': 50
        }
        
        params = '?' + urllib.parse.urlencode(params_dict)
        
        try:
            req = urllib.request.Request(url + params, method='GET')
            req.add_header('Authorization', f'Bearer {access_token}')
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                nouveaux_emails = data.get('value', [])
                emails.extend(nouveaux_emails)
                print(f"    📨 {len(nouveaux_emails)} emails trouvés pour '{terme}'")
                
        except Exception as e:
            print(f"    ❌ Erreur recherche '{terme}': {e}")
    
    # Supprimer doublons par ID
    emails_uniques = {}
    for email in emails:
        email_id = email.get('id')
        if email_id not in emails_uniques:
            emails_uniques[email_id] = email
    
    print(f"  📊 Total unique dans {dossier}: {len(emails_uniques)} emails")
    return list(emails_uniques.values())

if __name__ == "__main__":
    adresses = rechercher_emails_lefebvre()
    
    if adresses:
        print(f"\n🎯 RÉSULTAT: {len(adresses)} adresse(s) email LEFEBVRE trouvée(s)")
        for adresse in adresses:
            print(f"📧 {adresse}")
    else:
        print("\n❌ Aucune adresse email LEFEBVRE trouvée dans les 6 derniers mois")
#!/usr/bin/env python3
"""
RECHERCHE EMAIL LEFEBVRE V2 - Sans $search, avec $filter sur sujet/corps
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

def rechercher_emails_lefebvre_v2():
    """Rechercher emails LEFEBVRE avec approche différente - récupérer TOUS les emails et filtrer"""
    
    print('🔍 RECHERCHE EMAIL AVOCATE LEFEBVRE V2 - 6 MOIS')
    print('='*55)
    
    access_token = get_access_token()
    if not access_token:
        return []
    
    # Date de début : 6 mois avant aujourd'hui
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(days=180)  # 6 mois
    
    print(f"📅 Période: {date_debut.strftime('%Y-%m-%d')} → {date_fin.strftime('%Y-%m-%d')}")
    
    adresses_lefebvre = set()
    
    # Recherche dans plusieurs dossiers
    dossiers = ['sentitems', 'inbox']
    
    for dossier in dossiers:
        print(f"\n📧 ANALYSE DOSSIER: {dossier.upper()}")
        print("-" * 40)
        
        # Récupérer emails par batch de 50 avec pagination
        skip = 0
        total_analysed = 0
        
        while skip < 1000:  # Limite à 1000 emails par dossier
            url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/{dossier}/messages"
            
            params_dict = {
                '$filter': f"receivedDateTime ge {date_debut.strftime('%Y-%m-%d')}T00:00:00Z and receivedDateTime le {date_fin.strftime('%Y-%m-%d')}T23:59:59Z",
                '$select': 'subject,toRecipients,ccRecipients,from,sentDateTime,receivedDateTime,id',
                '$orderby': 'receivedDateTime desc',
                '$top': 50,
                '$skip': skip
            }
            
            params = '?' + urllib.parse.urlencode(params_dict)
            
            try:
                req = urllib.request.Request(url + params, method='GET')
                req.add_header('Authorization', f'Bearer {access_token}')
                
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    emails = data.get('value', [])
                
                if not emails:
                    break
                
                print(f"  📨 Batch {skip//50 + 1}: {len(emails)} emails récupérés")
                
                # Analyser chaque email pour LEFEBVRE
                for email in emails:
                    total_analysed += 1
                    
                    # Vérifier sujet
                    subject = email.get('subject', '').lower()
                    
                    # Vérifier expéditeur
                    from_email = email.get('from', {})
                    if from_email:
                        from_addr = from_email.get('emailAddress', {}).get('address', '').lower()
                        from_name = from_email.get('emailAddress', {}).get('name', '').lower()
                    else:
                        from_addr = ''
                        from_name = ''
                    
                    # Vérifier destinataires
                    to_recipients = email.get('toRecipients', [])
                    cc_recipients = email.get('ccRecipients', [])
                    
                    # Recherche LEFEBVRE dans tous les champs
                    lefebvre_trouve = False
                    adresses_email = []
                    
                    # Vérifier si LEFEBVRE dans sujet
                    if 'lefebvre' in subject:
                        lefebvre_trouve = True
                    
                    # Vérifier expéditeur
                    if 'lefebvre' in from_addr or 'lefebvre' in from_name:
                        lefebvre_trouve = True
                        adresses_email.append(from_addr)
                    
                    # Vérifier destinataires TO
                    for recipient in to_recipients:
                        addr = recipient.get('emailAddress', {}).get('address', '').lower()
                        name = recipient.get('emailAddress', {}).get('name', '').lower()
                        
                        if 'lefebvre' in addr or 'lefebvre' in name:
                            lefebvre_trouve = True
                            adresses_email.append(addr)
                    
                    # Vérifier destinataires CC
                    for recipient in cc_recipients:
                        addr = recipient.get('emailAddress', {}).get('address', '').lower()
                        name = recipient.get('emailAddress', {}).get('name', '').lower()
                        
                        if 'lefebvre' in addr or 'lefebvre' in name:
                            lefebvre_trouve = True
                            adresses_email.append(addr)
                    
                    if lefebvre_trouve:
                        date_email = email.get('receivedDateTime', email.get('sentDateTime', ''))[:10]
                        print(f"    ✅ {date_email} - {email.get('subject', '')[:50]}")
                        
                        if adresses_email:
                            for addr in adresses_email:
                                if addr and 'lefebvre' in addr:
                                    adresses_lefebvre.add(addr)
                                    print(f"       📧 {addr}")
                
                skip += 50
                
            except Exception as e:
                print(f"    ❌ Erreur batch {skip//50 + 1}: {e}")
                break
        
        print(f"  📊 Total analysé dans {dossier}: {total_analysed} emails")
    
    print("\n" + "="*55)
    print("🎯 ADRESSES EMAIL LEFEBVRE TROUVÉES:")
    print("="*55)
    
    if adresses_lefebvre:
        for adresse in sorted(adresses_lefebvre):
            print(f"✅ {adresse}")
    else:
        print("❌ Aucune adresse email LEFEBVRE trouvée")
    
    return list(adresses_lefebvre)

if __name__ == "__main__":
    adresses = rechercher_emails_lefebvre_v2()
    
    if adresses:
        print(f"\n🎯 RÉSULTAT: {len(adresses)} adresse(s) email LEFEBVRE trouvée(s)")
        for adresse in adresses:
            print(f"📧 {adresse}")
    else:
        print("\n❌ Aucune adresse email LEFEBVRE trouvée dans les 6 derniers mois")
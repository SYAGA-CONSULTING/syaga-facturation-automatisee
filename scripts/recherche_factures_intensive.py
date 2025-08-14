#!/usr/bin/env python3
"""
RECHERCHE INTENSIVE : Trouver TOUTES les factures F2025 dans TOUS les emails envoyés
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

def get_attachments_for_email(email_id, access_token):
    """Récupérer les pièces jointes d'un email avec plus de détails"""
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages/{email_id}/attachments"
    params = '?$select=name,contentType,size'
    
    try:
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            attachments = data.get('value', [])
            
        return attachments
    except Exception as e:
        return []

def main():
    print('🔍 RECHERCHE INTENSIVE - TOUTES LES FACTURES F2025')
    print('='*70)
    
    access_token = get_access_token()
    if not access_token:
        return
    
    # Les 9 factures qu'on DOIT trouver
    factures_cibles = ['F20250120', 'F20250731', 'F20250733', 'F20250734', 
                      'F20250735', 'F20250736', 'F20250737', 'F20250738', 'F20250744']
    
    # Récupérer TOUS les emails avec pièces jointes (plus large)
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    params_dict = {
        '$top': '500',  # Augmenté à 500
        '$select': 'subject,toRecipients,sentDateTime,hasAttachments,id',
        '$orderby': 'sentDateTime desc'
    }
    
    params = '?' + urllib.parse.urlencode(params_dict)
    
    print("📧 Récupération de TOUS les emails avec pièces jointes...")
    
    try:
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            emails = data.get('value', [])
    except Exception as e:
        print(f"❌ Erreur récupération emails: {e}")
        return
    
    print(f"✅ {len(emails)} emails récupérés")
    
    # Filtrer seulement ceux avec pièces jointes
    emails_avec_pj = [email for email in emails if email.get('hasAttachments', False)]
    print(f"📎 {len(emails_avec_pj)} emails avec pièces jointes")
    
    # Recherche intensive
    factures_trouvees = {}
    emails_avec_f2025 = []
    
    print(f"\n🔍 ANALYSE INTENSIVE DES PIÈCES JOINTES...")
    
    for i, email in enumerate(emails_avec_pj):
        email_id = email.get('id', '')
        date = email.get('sentDateTime', '')[:10]
        subject = email.get('subject', '')
        recipients = email.get('toRecipients', [])
        
        # Récupérer les pièces jointes
        attachments = get_attachments_for_email(email_id, access_token)
        
        if attachments:
            # Chercher les PDF F2025
            pdf_f2025_dans_cet_email = []
            
            for attachment in attachments:
                name = attachment.get('name', '')
                
                # Recherche flexible des factures F2025
                matches = re.findall(r'F2025\d{2,4}', name, re.IGNORECASE)
                
                for match in matches:
                    pdf_f2025_dans_cet_email.append(match.upper())
            
            # Si cet email contient des PDF F2025
            if pdf_f2025_dans_cet_email:
                to_emails = [r['emailAddress']['address'] for r in recipients]
                
                email_info = {
                    'date': date,
                    'subject': subject,
                    'recipients': to_emails,
                    'factures': pdf_f2025_dans_cet_email,
                    'total_attachments': len(attachments)
                }
                
                emails_avec_f2025.append(email_info)
                
                # Enregistrer chaque facture trouvée
                for facture in pdf_f2025_dans_cet_email:
                    if facture not in factures_trouvees:
                        factures_trouvees[facture] = []
                    factures_trouvees[facture].append(email_info)
                
                print(f"📎 {date} | {len(pdf_f2025_dans_cet_email)} F2025 | → {', '.join(to_emails)[:50]}")
                for facture in pdf_f2025_dans_cet_email:
                    if facture in factures_cibles:
                        print(f"   🎯 {facture} TROUVÉ !")
        
        # Progress
        if (i + 1) % 50 == 0:
            print(f"   📊 Analysé {i + 1}/{len(emails_avec_pj)} emails...")
    
    # RÉSULTATS
    print('\n' + '='*70)
    print('🎯 RÉSULTATS DE LA RECHERCHE INTENSIVE:')
    print('='*70)
    
    print(f"\n📊 STATISTIQUES:")
    print(f"  • {len(emails_avec_pj)} emails avec pièces jointes analysés")
    print(f"  • {len(emails_avec_f2025)} emails contenant des PDF F2025")
    print(f"  • {len(factures_trouvees)} factures F2025 uniques trouvées")
    
    # Vérification des 9 factures cibles
    print(f"\n🎯 VÉRIFICATION DES 9 FACTURES CIBLES:")
    print('-'*50)
    
    factures_cibles_trouvees = []
    factures_cibles_manquantes = []
    
    for facture in factures_cibles:
        if facture in factures_trouvees:
            factures_cibles_trouvees.append(facture)
            envois = factures_trouvees[facture]
            print(f"✅ {facture} trouvé dans {len(envois)} email(s):")
            
            for envoi in envois:
                recipients_str = ', '.join(envoi['recipients'])[:60]
                print(f"   📅 {envoi['date']} → {recipients_str}")
                if len(envoi['subject']) > 0:
                    print(f"      📝 {envoi['subject'][:50]}")
        else:
            factures_cibles_manquantes.append(facture)
            print(f"❌ {facture} NON TROUVÉ")
    
    print(f"\n📈 RÉSUMÉ FINAL:")
    print(f"✅ {len(factures_cibles_trouvees)}/{len(factures_cibles)} factures cibles trouvées")
    print(f"❌ {len(factures_cibles_manquantes)} factures cibles manquantes")
    
    if factures_cibles_manquantes:
        print(f"\n⚠️  FACTURES MANQUANTES:")
        for facture in factures_cibles_manquantes:
            print(f"  • {facture}")
    
    # Dates d'envoi les plus probables
    if factures_cibles_trouvees:
        print(f"\n📅 DATES D'ENVOI PROBABLES:")
        dates_par_facture = {}
        
        for facture in factures_cibles_trouvees:
            dates = [envoi['date'] for envoi in factures_trouvees[facture]]
            # Prendre la date la plus ancienne (premier envoi)
            date_envoi = min(dates)
            dates_par_facture[facture] = date_envoi
            
            recipients = factures_trouvees[facture][0]['recipients']
            print(f"  {facture}: {date_envoi} → {', '.join(recipients)[:50]}")
        
        return dates_par_facture
    
    return {}

if __name__ == "__main__":
    dates = main()
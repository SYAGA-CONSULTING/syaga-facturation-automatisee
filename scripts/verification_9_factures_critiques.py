#!/usr/bin/env python3
"""
VÉRIFICATION CRITIQUE : Les 9 factures F2025 sans date ont-elles été envoyées ?
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

def search_all_emails():
    """Récupérer TOUS les emails pertinents (envoyés + reçus)"""
    access_token = get_access_token()
    if not access_token:
        return [], []
    
    sent_emails = []
    received_emails = []
    
    # 1. EMAILS ENVOYÉS
    url_sent = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    params_dict = {
        '$top': '999',
        '$select': 'subject,toRecipients,sentDateTime,bodyPreview,hasAttachments',
        '$orderby': 'sentDateTime desc'
    }
    params = '?' + urllib.parse.urlencode(params_dict)
    
    try:
        req = urllib.request.Request(url_sent + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            sent_emails = data.get('value', [])
    except:
        pass
    
    # 2. EMAILS REÇUS (pour voir les confirmations d'envoi)
    url_inbox = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages"
    params_dict = {
        '$top': '999',
        '$select': 'subject,from,receivedDateTime,bodyPreview',
        '$orderby': 'receivedDateTime desc'
    }
    params = '?' + urllib.parse.urlencode(params_dict)
    
    try:
        req = urllib.request.Request(url_inbox + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            received_emails = data.get('value', [])
    except:
        pass
    
    return sent_emails, received_emails

def main():
    print('🔍 VÉRIFICATION CRITIQUE - 9 FACTURES F2025 SANS DATE D\'ENVOI')
    print('='*80)
    
    # Les 9 factures à vérifier
    factures_a_verifier = {
        'F20250120': {'client': 'ANONE', 'montant': 300, 'email': 'viet.nguyen@anone.fr'},
        'F20250731': {'client': 'LAA', 'montant': 1800, 'email': 'alleaume@laa.fr'},
        'F20250733': {'client': 'LAA', 'montant': 700, 'email': 'alleaume@laa.fr'},
        'F20250734': {'client': 'AXION', 'montant': 700, 'email': 'n.diaz@axion-informatique.fr'},
        'F20250735': {'client': 'ART INFO', 'montant': 200, 'email': 'h.sarda@artinformatique.net'},
        'F20250736': {'client': 'FARBOS', 'montant': 150, 'email': 'n.diaz@axion-informatique.fr'},
        'F20250737': {'client': 'LEFEBVRE', 'montant': 360, 'email': 'mjlefebvre@selasu-mjl-avocats.com'},
        'F20250738': {'client': 'PETRAS', 'montant': 600, 'email': 'lauriane.petras@petras.fr'},
        'F20250744': {'client': 'TOUZEAU', 'montant': 150, 'email': 'commercial.diaboliqbike@gmail.com'}
    }
    
    print('📋 FACTURES À VÉRIFIER :')
    for num, info in factures_a_verifier.items():
        print(f'  • {num} - {info["client"]:<15} {info["montant"]:>6}€ → {info["email"]}')
    
    # Rechercher dans les emails
    print('\n🔄 Recherche dans les emails...')
    sent_emails, received_emails = search_all_emails()
    
    print(f'  • {len(sent_emails)} emails envoyés analysés')
    print(f'  • {len(received_emails)} emails reçus analysés')
    
    # Analyser chaque facture
    print('\n📊 RÉSULTATS DE LA RECHERCHE :')
    print('-'*80)
    
    factures_trouvees = {}
    factures_non_trouvees = []
    
    for num_facture, info in factures_a_verifier.items():
        trouvee = False
        details = []
        
        # Chercher dans les emails envoyés
        for email in sent_emails:
            subject = email.get('subject', '')
            body = email.get('bodyPreview', '')
            recipients = email.get('toRecipients', [])
            date = email.get('sentDateTime', '')[:10]
            
            # Chercher le numéro de facture
            if (subject and num_facture in subject) or (body and num_facture in body):
                # Vérifier si envoyé au bon destinataire
                to_emails = [r['emailAddress']['address'] for r in recipients]
                
                if info['email'] in to_emails:
                    trouvee = True
                    details.append({
                        'type': 'ENVOYÉ AU CLIENT',
                        'date': date,
                        'sujet': subject[:60],
                        'destinataire': info['email']
                    })
                elif USER_EMAIL in to_emails:
                    details.append({
                        'type': 'ENVOYÉ À SOI-MÊME',
                        'date': date,
                        'sujet': subject[:60]
                    })
                else:
                    other_dest = ', '.join(to_emails)[:40]
                    details.append({
                        'type': 'ENVOYÉ AILLEURS',
                        'date': date,
                        'destinataire': other_dest
                    })
        
        # Chercher dans les emails reçus (confirmations, etc.)
        for email in received_emails:
            subject = email.get('subject', '')
            body = email.get('bodyPreview', '')
            sender = email.get('from', {}).get('emailAddress', {}).get('address', '')
            date = email.get('receivedDateTime', '')[:10]
            
            if num_facture in subject or num_facture in body:
                # Accusé de réception ?
                if 'lu' in subject.lower() or 'reçu' in subject.lower() or 'reception' in subject.lower():
                    details.append({
                        'type': 'ACCUSÉ RÉCEPTION',
                        'date': date,
                        'de': sender
                    })
        
        # Afficher résultat pour cette facture
        print(f'\n{num_facture} - {info["client"]} ({info["montant"]}€) :')
        
        if trouvee:
            print(f'  ✅ TROUVÉE - Facture envoyée')
            factures_trouvees[num_facture] = details
        else:
            if details:
                print(f'  ⚠️ DOUTE - Trouvée mais pas envoyée au client')
            else:
                print(f'  ❌ NON TROUVÉE - Jamais envoyée')
                factures_non_trouvees.append(num_facture)
        
        for detail in details:
            if detail['type'] == 'ENVOYÉ AU CLIENT':
                print(f'    • {detail["date"]} : Envoyé à {detail["destinataire"]}')
            elif detail['type'] == 'ENVOYÉ À SOI-MÊME':
                print(f'    • {detail["date"]} : Envoyé à soi-même (test?)')
            elif detail['type'] == 'ENVOYÉ AILLEURS':
                print(f'    • {detail["date"]} : Envoyé à {detail["destinataire"]}')
            elif detail['type'] == 'ACCUSÉ RÉCEPTION':
                print(f'    • {detail["date"]} : Accusé réception de {detail["de"]}')
    
    # RÉSUMÉ FINAL
    print('\n' + '='*80)
    print('🎯 CONCLUSION DÉFINITIVE :')
    print('-'*80)
    
    if factures_trouvees:
        print(f'✅ FACTURES ENVOYÉES ({len(factures_trouvees)}) :')
        for num in factures_trouvees:
            print(f'  • {num} - {factures_a_verifier[num]["client"]}')
    
    if factures_non_trouvees:
        print(f'\n❌ FACTURES JAMAIS ENVOYÉES ({len(factures_non_trouvees)}) - À ENVOYER :')
        total = 0
        for num in factures_non_trouvees:
            info = factures_a_verifier[num]
            print(f'  • {num} - {info["client"]:<15} {info["montant"]:>6}€ → {info["email"]}')
            total += info['montant']
        print(f'\n  TOTAL À FACTURER : {total}€ HT')
    
    print('\n💡 RECOMMANDATION :')
    if factures_non_trouvees:
        print(f'  → Envoyer les {len(factures_non_trouvees)} factures non trouvées')
        print(f'  → Mettre à jour l\'Excel avec les dates d\'envoi')
    else:
        print(f'  → Toutes les factures ont été envoyées !')

if __name__ == "__main__":
    main()
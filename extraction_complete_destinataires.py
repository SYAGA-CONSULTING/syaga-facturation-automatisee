#!/usr/bin/env python3
"""
Extraction COMPLÈTE et FIABLE des destinataires depuis les emails envoyés
Recherche approfondie pour TOUS les clients
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

def get_all_sent_emails(months_back=6):
    """Récupérer TOUS les emails envoyés sur X mois"""
    access_token = get_access_token()
    if not access_token:
        return []
    
    all_emails = []
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    # Date de début (6 mois en arrière)
    date_start = (datetime.now() - timedelta(days=months_back*30)).strftime('%Y-%m-%dT00:00:00Z')
    
    # Paramètres initiaux
    params_dict = {
        '$filter': f"sentDateTime ge {date_start}",
        '$top': '100',
        '$select': 'subject,toRecipients,sentDateTime,bodyPreview',
        '$orderby': 'sentDateTime desc'
    }
    
    next_link = url + '?' + urllib.parse.urlencode(params_dict)
    
    print(f"🔄 Récupération des emails envoyés ({months_back} derniers mois)...")
    
    # Pagination pour récupérer TOUS les emails
    while next_link:
        try:
            req = urllib.request.Request(next_link, method='GET')
            req.add_header('Authorization', f'Bearer {access_token}')
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                emails = data.get('value', [])
                all_emails.extend(emails)
                
                # Vérifier s'il y a une page suivante
                next_link = data.get('@odata.nextLink')
                
                print(f"  • {len(all_emails)} emails récupérés...", end='\r')
                
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            break
    
    print(f"\n✅ Total: {len(all_emails)} emails récupérés")
    return all_emails

def extract_client_emails(emails):
    """Extraire les adresses email par client"""
    
    # Dictionnaire des clients connus (avec variantes possibles)
    clients = {
        'LAA': ['laa.fr', 'LAA', 'LES AUTOMATISMES'],
        'BUQUET': ['buquet', 'BUQUET'],
        'PHARMABEST': ['pharmabest', 'PHARMABEST', 'belfonte'],
        'SEXTANT': ['sextant', 'SEXTANT'],
        'UAI': ['unairdici', 'UAI', "UN AIR D'ICI"],
        'AIXAGON': ['aixagon', 'AIXAGON'],
        'QUADRIMEX': ['quadrimex', 'QUADRIMEX'],
        'GENLOG': ['genlog', 'GENLOG'],
        'PETRAS': ['petras', 'PETRAS'],
        'AXION': ['axion', 'AXION'],
        'ANONE': ['anone', 'ANONE'],
        'FARBOS': ['farbos', 'FARBOS'],
        'ART INFO': ['art-info', 'ART INFO', 'ART INFORMATIQUE'],
        'LEFEBVRE': ['lefebvre', 'LEFEBVRE', 'MARIE-JOSE'],
        'TOUZEAU': ['touzeau', 'TOUZEAU', 'garage'],
        'PROVENCALE': ['provencale', 'PROVENÇALE'],
        'PDB': ['port-de-bouc', 'PDB', 'PORT DE BOUC'],
        'FARSY': ['farsy', 'FARSY'],
        'CRAU': ['crau', 'CRAU']
    }
    
    client_contacts = {}
    
    for email in emails:
        subject = email.get('subject', '')
        body = email.get('bodyPreview', '')
        recipients = email.get('toRecipients', [])
        date = email.get('sentDateTime', '')[:10]
        
        # Ignorer les emails à soi-même
        to_list = []
        for r in recipients:
            addr = r['emailAddress']['address']
            if addr != USER_EMAIL:
                to_list.append({
                    'email': addr,
                    'name': r['emailAddress'].get('name', '')
                })
        
        if not to_list:  # Skip si seulement envoyé à soi-même
            continue
        
        # Chercher quel client est concerné
        content = (subject + ' ' + body + ' ' + str(to_list)).upper()
        
        for client_name, keywords in clients.items():
            for keyword in keywords:
                if keyword.upper() in content:
                    # Trouvé un client !
                    if client_name not in client_contacts:
                        client_contacts[client_name] = {}
                    
                    # Ajouter les destinataires
                    for recipient in to_list:
                        email_addr = recipient['email']
                        if email_addr not in client_contacts[client_name]:
                            client_contacts[client_name][email_addr] = {
                                'name': recipient['name'],
                                'last_contact': date,
                                'subjects': []
                            }
                        
                        # Mettre à jour la date si plus récente
                        if date > client_contacts[client_name][email_addr]['last_contact']:
                            client_contacts[client_name][email_addr]['last_contact'] = date
                        
                        # Ajouter le sujet si pertinent
                        if 'facture' in subject.lower() or 'F2025' in subject:
                            client_contacts[client_name][email_addr]['subjects'].append(subject[:50])
                    
                    break  # Un client trouvé, passer au prochain email
    
    return client_contacts

def main():
    print('📧 EXTRACTION COMPLÈTE DES DESTINATAIRES CLIENTS')
    print('='*80)
    
    # Récupérer tous les emails sur 6 mois
    emails = get_all_sent_emails(6)
    
    if not emails:
        print("❌ Aucun email trouvé")
        return
    
    # Extraire les contacts clients
    client_contacts = extract_client_emails(emails)
    
    # Afficher les résultats organisés
    print('\n📋 CONTACTS CLIENTS EXTRAITS DES EMAILS ENVOYÉS:')
    print('='*80)
    
    clients_avec_factures = ['ANONE', 'LAA', 'AXION', 'FARBOS', 'ART INFO', 
                             'LEFEBVRE', 'PETRAS', 'TOUZEAU', 'FARSY', 'PDB',
                             'UAI', 'QUADRIMEX', 'BUQUET', 'PHARMABEST', 'SEXTANT',
                             'PROVENCALE', 'GENLOG']
    
    for client in clients_avec_factures:
        print(f'\n🏢 {client}:')
        print('-'*60)
        
        if client in client_contacts:
            for email_addr, info in client_contacts[client].items():
                name = info['name'] if info['name'] else 'N/A'
                last_contact = info['last_contact']
                print(f'  • {name:<25} → {email_addr:<40} (dernier: {last_contact})')
                
                # Afficher si des factures ont été envoyées
                facture_subjects = [s for s in info['subjects'] if 'F2025' in s or 'facture' in s.lower()]
                if facture_subjects:
                    for subj in facture_subjects[:2]:  # Max 2 exemples
                        print(f'    └─ {subj}')
        else:
            print('  ❓ Aucun contact trouvé dans les emails récents')
    
    # Résumé
    print('\n' + '='*80)
    print('📊 RÉSUMÉ:')
    found = sum(1 for c in clients_avec_factures if c in client_contacts)
    print(f'• Clients avec contacts trouvés: {found}/{len(clients_avec_factures)}')
    
    # Sauvegarder dans un fichier
    print('\n💾 Sauvegarde des contacts...')
    with open('CONTACTS_CLIENTS_FACTURES.txt', 'w', encoding='utf-8') as f:
        f.write('CONTACTS CLIENTS POUR FACTURES\n')
        f.write('='*60 + '\n\n')
        
        for client in clients_avec_factures:
            f.write(f'{client}:\n')
            if client in client_contacts:
                for email_addr, info in client_contacts[client].items():
                    f.write(f'  • {info["name"]}: {email_addr}\n')
            else:
                f.write('  • À RECHERCHER\n')
            f.write('\n')
    
    print('✅ Contacts sauvegardés dans CONTACTS_CLIENTS_FACTURES.txt')

if __name__ == "__main__":
    main()
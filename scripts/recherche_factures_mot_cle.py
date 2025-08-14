#!/usr/bin/env python3
"""
Recherche des emails avec "facture" ou "facturation" dans l'objet
et vérification des pièces jointes
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

def search_emails_with_facture():
    """Rechercher les emails avec 'facture' ou 'facturation' dans le sujet"""
    access_token = get_access_token()
    if not access_token:
        return []
    
    # URL des emails envoyés
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    # Recherche sur les 6 derniers mois
    date_filter = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%dT00:00:00Z')
    
    # Paramètres de recherche
    params_dict = {
        '$filter': f"sentDateTime ge {date_filter} and hasAttachments eq true",
        '$top': '999',
        '$select': 'id,subject,toRecipients,sentDateTime,hasAttachments',
        '$orderby': 'sentDateTime desc'
    }
    
    params = '?' + urllib.parse.urlencode(params_dict)
    
    all_emails = []
    
    try:
        print("🔄 Recherche des emails avec pièces jointes...")
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            emails = data.get('value', [])
            
            # Filtrer ceux qui ont "factur" dans le sujet
            for email in emails:
                subject = email.get('subject', '').lower()
                if 'factur' in subject or 'invoice' in subject:
                    all_emails.append(email)
            
            return all_emails
    except Exception as e:
        print(f"❌ Erreur recherche: {e}")
        return []

def get_attachments(email_id, access_token):
    """Récupérer les pièces jointes d'un email spécifique"""
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages/{email_id}/attachments"
    
    try:
        req = urllib.request.Request(url, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('value', [])
    except:
        return []

def main():
    print('🔍 RECHERCHE DES FACTURES DANS LES EMAILS AVEC "FACTUR*" DANS L\'OBJET')
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
    
    # Rechercher les emails
    emails = search_emails_with_facture()
    
    if not emails:
        print("❌ Aucun email avec 'factur' trouvé")
        return
    
    print(f"✅ {len(emails)} emails avec 'factur*' dans l'objet trouvés\n")
    
    # Obtenir le token pour les requêtes suivantes
    access_token = get_access_token()
    
    # Analyser chaque email
    print('📎 ANALYSE DES EMAILS AVEC FACTURES:')
    print('-'*80)
    
    factures_trouvees = {}
    emails_avec_f2025 = []
    
    for email in emails[:50]:  # Limiter aux 50 plus récents
        email_id = email.get('id')
        subject = email.get('subject', '')
        recipients = email.get('toRecipients', [])
        date = email.get('sentDateTime', '')[:10]
        
        # Extraire les destinataires
        to_emails = [r['emailAddress']['address'] for r in recipients]
        
        # Ignorer les emails à soi-même
        if len(to_emails) == 1 and to_emails[0] == USER_EMAIL:
            continue
        
        # Récupérer les pièces jointes
        attachments = get_attachments(email_id, access_token)
        
        # Chercher les PDF F2025
        for attachment in attachments:
            name = attachment.get('name', '')
            
            # Vérifier si c'est un PDF avec F2025
            if name.lower().endswith('.pdf'):
                matches = re.findall(r'F2025\d{3,4}', name)
                
                if matches:
                    for num_facture in matches:
                        if num_facture not in factures_trouvees:
                            factures_trouvees[num_facture] = []
                        
                        factures_trouvees[num_facture].append({
                            'date': date,
                            'destinataires': to_emails,
                            'sujet': subject[:60],
                            'fichier': name
                        })
                        
                        # Afficher immédiatement
                        dest_str = ', '.join(to_emails)[:40]
                        print(f"{date} | {num_facture} | {dest_str} | {name}")
    
    # Vérifier les 9 factures spécifiques
    print('\n' + '='*80)
    print('🎯 VÉRIFICATION DES 9 FACTURES F2025 SANS DATE D\'ENVOI:')
    print('-'*80)
    
    factures_envoyees = []
    factures_non_envoyees = []
    
    for num_facture, info in factures_a_verifier.items():
        if num_facture in factures_trouvees:
            # Vérifier si envoyée au bon client
            envoyee_au_client = False
            for envoi in factures_trouvees[num_facture]:
                if info['email'] in envoi['destinataires']:
                    envoyee_au_client = True
                    print(f"✅ {num_facture} - {info['client']} - ENVOYÉE le {envoi['date']}")
                    factures_envoyees.append(num_facture)
                    break
            
            if not envoyee_au_client:
                print(f"⚠️ {num_facture} - {info['client']} - Trouvée mais pas au bon destinataire")
                factures_non_envoyees.append(num_facture)
        else:
            print(f"❌ {num_facture} - {info['client']} - JAMAIS ENVOYÉE")
            factures_non_envoyees.append(num_facture)
    
    # RÉSUMÉ FINAL
    print('\n' + '='*80)
    print('📊 RÉSUMÉ DÉFINITIF:')
    print('-'*80)
    
    if factures_envoyees:
        print(f'\n✅ FACTURES DÉJÀ ENVOYÉES ({len(factures_envoyees)}):')
        total_envoye = 0
        for num in factures_envoyees:
            info = factures_a_verifier[num]
            print(f'  • {num} - {info["client"]} - {info["montant"]}€')
            total_envoye += info['montant']
        print(f'  Total: {total_envoye}€')
    
    if factures_non_envoyees:
        print(f'\n❌ FACTURES À ENVOYER ({len(factures_non_envoyees)}):')
        total_a_envoyer = 0
        for num in factures_non_envoyees:
            info = factures_a_verifier[num]
            print(f'  • {num} - {info["client"]:<15} {info["montant"]:>6}€ → {info["email"]}')
            total_a_envoyer += info['montant']
        print(f'\n  TOTAL À FACTURER: {total_a_envoyer}€ HT')
        
        # Total avec les autres factures
        print('\n💰 CALCUL TOTAL AVEC TOUTES LES FACTURES:')
        print(f'  • {len(factures_non_envoyees)} F2025 non envoyées: {total_a_envoyer}€')
        print(f'  • 16 factures juillet sans numéro: 15 610€')
        print(f'  • 8 factures août récurrentes: 4 150€')
        total_general = total_a_envoyer + 15610 + 4150
        print(f'\n  TOTAL GÉNÉRAL: {total_general}€ HT ({total_general * 1.2:.0f}€ TTC)')

if __name__ == "__main__":
    main()
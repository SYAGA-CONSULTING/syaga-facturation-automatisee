#!/usr/bin/env python3
"""
RECHERCHE DES VRAIES FACTURES : Emails avec PDF F2025xxxx.pdf en pièce jointe
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

def get_emails_with_attachments():
    """Récupérer UNIQUEMENT les emails envoyés avec pièces jointes"""
    access_token = get_access_token()
    if not access_token:
        return []
    
    # Rechercher les emails envoyés avec pièces jointes
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    # Paramètres étendus pour inclure les pièces jointes
    params_dict = {
        '$top': '500',
        '$select': 'subject,toRecipients,sentDateTime,hasAttachments',
        '$expand': 'attachments',
        '$orderby': 'sentDateTime desc'
    }
    
    params = '?' + urllib.parse.urlencode(params_dict)
    
    try:
        print("🔄 Récupération des emails avec pièces jointes...")
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('value', [])
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return []

def main():
    print('🔍 RECHERCHE DES FACTURES PDF F2025 DANS LES PIÈCES JOINTES')
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
    
    # Récupérer les emails avec pièces jointes
    emails = get_emails_with_attachments()
    
    if not emails:
        print("❌ Aucun email avec pièces jointes trouvé")
        return
    
    print(f"✅ {len(emails)} emails avec pièces jointes trouvés\n")
    
    # Analyser les pièces jointes
    print('📎 ANALYSE DES PIÈCES JOINTES PDF:')
    print('-'*80)
    
    factures_pdf_trouvees = {}
    tous_pdf_f2025 = []
    
    for email in emails:
        subject = email.get('subject', '')
        recipients = email.get('toRecipients', [])
        date = email.get('sentDateTime', '')[:10]
        attachments = email.get('attachments', [])
        
        # Extraire les destinataires
        to_emails = [r['emailAddress']['address'] for r in recipients]
        
        # Chercher les PDF F2025
        for attachment in attachments:
            name = attachment.get('name', '')
            content_type = attachment.get('contentType', '')
            
            # Vérifier si c'est un PDF F2025
            if 'pdf' in content_type.lower() or name.lower().endswith('.pdf'):
                # Extraire le numéro F2025 du nom de fichier
                matches = re.findall(r'F2025\d{3,4}', name)
                
                if matches:
                    for num_facture in matches:
                        # Enregistrer cette facture PDF
                        if num_facture not in factures_pdf_trouvees:
                            factures_pdf_trouvees[num_facture] = []
                        
                        factures_pdf_trouvees[num_facture].append({
                            'date': date,
                            'destinataires': to_emails,
                            'sujet': subject[:60],
                            'fichier': name
                        })
                        
                        tous_pdf_f2025.append({
                            'numero': num_facture,
                            'date': date,
                            'destinataires': ', '.join(to_emails)[:60],
                            'fichier': name
                        })
    
    # Afficher tous les PDF F2025 trouvés
    if tous_pdf_f2025:
        print('\n📄 TOUS LES PDF F2025 TROUVÉS:')
        print('-'*80)
        for pdf in sorted(tous_pdf_f2025, key=lambda x: x['numero']):
            print(f"{pdf['numero']} | {pdf['date']} | {pdf['destinataires'][:40]} | {pdf['fichier']}")
    
    # Vérifier les 9 factures spécifiques
    print('\n' + '='*80)
    print('🎯 VÉRIFICATION DES 9 FACTURES SANS DATE D\'ENVOI:')
    print('-'*80)
    
    factures_envoyees = []
    factures_non_envoyees = []
    
    for num_facture, info in factures_a_verifier.items():
        print(f'\n{num_facture} - {info["client"]} ({info["montant"]}€):')
        
        if num_facture in factures_pdf_trouvees:
            # Facture trouvée !
            envois = factures_pdf_trouvees[num_facture]
            
            # Vérifier si envoyée au bon client
            envoyee_au_client = False
            for envoi in envois:
                if info['email'] in envoi['destinataires']:
                    envoyee_au_client = True
                    print(f'  ✅ ENVOYÉE le {envoi["date"]} à {info["email"]}')
                    print(f'     Fichier: {envoi["fichier"]}')
                    break
            
            if envoyee_au_client:
                factures_envoyees.append(num_facture)
            else:
                # Envoyée mais pas au bon destinataire
                print(f'  ⚠️ PDF trouvé mais pas envoyé au client attendu')
                for envoi in envois:
                    dest = ', '.join(envoi['destinataires'])[:60]
                    print(f'     {envoi["date"]} → {dest}')
                factures_non_envoyees.append(num_facture)
        else:
            # Facture jamais envoyée
            print(f'  ❌ JAMAIS ENVOYÉE (aucun PDF trouvé)')
            factures_non_envoyees.append(num_facture)
    
    # RÉSUMÉ FINAL
    print('\n' + '='*80)
    print('📊 RÉSUMÉ DÉFINITIF:')
    print('-'*80)
    
    if factures_envoyees:
        print(f'\n✅ FACTURES DÉJÀ ENVOYÉES ({len(factures_envoyees)}):')
        for num in factures_envoyees:
            info = factures_a_verifier[num]
            print(f'  • {num} - {info["client"]} - {info["montant"]}€')
    
    if factures_non_envoyees:
        print(f'\n❌ FACTURES À ENVOYER ({len(factures_non_envoyees)}):')
        total = 0
        for num in factures_non_envoyees:
            info = factures_a_verifier[num]
            print(f'  • {num} - {info["client"]:<15} {info["montant"]:>6}€ → {info["email"]}')
            total += info['montant']
        print(f'\nTOTAL À FACTURER: {total}€ HT')
    
    # Calculer le total général avec les 16 juillet + 8 août
    print('\n' + '='*80)
    print('💰 CALCUL FINAL AVEC TOUTES LES FACTURES:')
    print(f'  • {len(factures_non_envoyees)} factures F2025 non envoyées: {sum(factures_a_verifier[n]["montant"] for n in factures_non_envoyees)}€')
    print(f'  • 16 factures juillet sans numéro: 15 610€')
    print(f'  • 8 factures août récurrentes: 4 150€')
    total_general = sum(factures_a_verifier[n]["montant"] for n in factures_non_envoyees) + 15610 + 4150
    print(f'\n  TOTAL GÉNÉRAL: {total_general}€ HT ({total_general * 1.2:.0f}€ TTC)')

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
VÉRIFICATION VRAIS DESTINATAIRES - Distinction client final vs auto-envoi
Correction majeure : PDF trouvé ≠ envoyé au client !
"""

import urllib.request
import urllib.parse
import json
import sqlite3
import datetime
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
USER_EMAIL = config['SENDER_EMAIL']  # sebastien.questier@syaga.fr

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
    """Récupérer les pièces jointes d'un email"""
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

def analyser_vrais_destinataires():
    """Analyser les emails pour identifier les VRAIS destinataires clients"""
    
    print('🔍 VÉRIFICATION VRAIS DESTINATAIRES - CLIENTS vs AUTO-ENVOI')
    print('='*70)
    
    access_token = get_access_token()
    if not access_token:
        return {}
    
    # Factures à vérifier
    factures_cibles = ['F20250120', 'F20250731', 'F20250733', 'F20250734', 
                      'F20250735', 'F20250736', 'F20250737', 'F20250738', 'F20250744',
                      'F20250705', 'F20250706']  # Ajout des PHARMABEST
    
    # Adresses clients légitimes (PAS sebastien.questier@syaga.fr)
    adresses_clients = {
        'anthony.cimo@pharmabest.com': 'PHARMABEST',
        'alleaume@laa.fr': 'LAA', 
        'viet.nguyen@anone.fr': 'ANONE',
        'n.diaz@axion-informatique.fr': 'AXION',
        'h.sarda@artinformatique.net': 'ART INFO',
        'mjlefebvre@selasu-mjl-avocats.com': 'LEFEBVRE',
        'lauriane.petras@petras.fr': 'PETRAS',
        'commercial.diaboliqbike@gmail.com': 'TOUZEAU'
    }
    
    print(f"📧 Recherche dans emails envoyés (500+ emails)...")
    
    # Récupérer emails avec pièces jointes
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/sentitems/messages"
    
    params_dict = {
        '$top': '500',
        '$select': 'subject,toRecipients,sentDateTime,hasAttachments,id',
        '$orderby': 'sentDateTime desc'
    }
    
    params = '?' + urllib.parse.urlencode(params_dict)
    
    try:
        req = urllib.request.Request(url + params, method='GET')
        req.add_header('Authorization', f'Bearer {access_token}')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            emails = data.get('value', [])
    except Exception as e:
        print(f"❌ Erreur récupération emails: {e}")
        return {}
    
    print(f"✅ {len(emails)} emails récupérés")
    
    # Filtrer emails avec pièces jointes
    emails_avec_pj = [email for email in emails if email.get('hasAttachments', False)]
    print(f"📎 {len(emails_avec_pj)} emails avec pièces jointes")
    
    # Analyse des destinataires RÉELS
    factures_clients_confirmes = {}
    auto_envois_detectes = {}
    
    print(f"\n🔍 ANALYSE DES VRAIS DESTINATAIRES...")
    
    for i, email in enumerate(emails_avec_pj):
        email_id = email.get('id', '')
        date = email.get('sentDateTime', '')[:10]
        subject = email.get('subject', '')
        recipients = email.get('toRecipients', [])
        
        # Extraire adresses destinataires
        to_emails = [r['emailAddress']['address'].lower() for r in recipients]
        
        # Vérifier pièces jointes pour factures F2025
        attachments = get_attachments_for_email(email_id, access_token)
        
        if attachments:
            import re
            for attachment in attachments:
                name = attachment.get('name', '')
                matches = re.findall(r'F2025\d{2,4}', name, re.IGNORECASE)
                
                for facture_num in matches:
                    facture_num = facture_num.upper()
                    if facture_num in factures_cibles:
                        
                        # DISTINCTION CRUCIALE : Client vs Auto-envoi
                        clients_dans_destinataires = []
                        auto_envoi = False
                        
                        for email_dest in to_emails:
                            if email_dest == USER_EMAIL.lower():  # sebastien.questier@syaga.fr
                                auto_envoi = True
                            elif email_dest in adresses_clients:
                                clients_dans_destinataires.append({
                                    'email': email_dest,
                                    'client': adresses_clients[email_dest]
                                })
                        
                        if clients_dans_destinataires:
                            # VRAIE facture envoyée au client
                            for client_info in clients_dans_destinataires:
                                factures_clients_confirmes[facture_num] = {
                                    'date_envoi': date,
                                    'destinataire_client': client_info['email'],
                                    'client_nom': client_info['client'],
                                    'sujet_email': subject,
                                    'statut': 'CLIENT_CONFIRME'
                                }
                                print(f"✅ {facture_num} → CLIENT {client_info['client']} ({client_info['email']}) - {date}")
                        
                        elif auto_envoi and not clients_dans_destinataires:
                            # Auto-envoi détecté (probablement archivage/test)
                            auto_envois_detectes[facture_num] = {
                                'date_envoi': date,
                                'destinataire_reel': USER_EMAIL,
                                'sujet_email': subject,
                                'statut': 'AUTO_ENVOI_ARCHIVE'
                            }
                            print(f"⚠️  {facture_num} → AUTO-ENVOI (sebastien.questier@syaga.fr) - {date}")
        
        if (i + 1) % 100 == 0:
            print(f"   📊 Analysé {i + 1}/{len(emails_avec_pj)} emails...")
    
    # RÉSULTATS FINAL
    print('\n' + '='*70)
    print('🎯 RÉSULTATS ANALYSE VRAIS DESTINATAIRES')
    print('='*70)
    
    print(f"\n✅ FACTURES VRAIMENT ENVOYÉES AUX CLIENTS ({len(factures_clients_confirmes)}):")
    for facture, info in factures_clients_confirmes.items():
        print(f"   {facture} → {info['client_nom']} ({info['destinataire_client']}) - {info['date_envoi']}")
    
    print(f"\n⚠️  AUTO-ENVOIS DÉTECTÉS (PAS AUX CLIENTS) ({len(auto_envois_detectes)}):")
    for facture, info in auto_envois_detectes.items():
        print(f"   {facture} → Archive personnelle - {info['date_envoi']}")
    
    # Factures non trouvées
    toutes_factures = set(factures_cibles)
    factures_trouvees = set(factures_clients_confirmes.keys()) | set(auto_envois_detectes.keys())
    factures_manquantes = toutes_factures - factures_trouvees
    
    if factures_manquantes:
        print(f"\n❌ FACTURES NON TROUVÉES ({len(factures_manquantes)}):")
        for facture in factures_manquantes:
            print(f"   {facture} → Aucune trace dans emails")
    
    print(f"\n📊 BILAN FINAL:")
    print(f"   ✅ Envoyées clients: {len(factures_clients_confirmes)}")
    print(f"   ⚠️  Auto-envois: {len(auto_envois_detectes)}")
    print(f"   ❌ Non trouvées: {len(factures_manquantes)}")
    
    return {
        'clients_confirmes': factures_clients_confirmes,
        'auto_envois': auto_envois_detectes,
        'manquantes': factures_manquantes
    }

def mettre_a_jour_base_sqlite(resultats_analyse):
    """Mettre à jour la base SQLite avec les VRAIS statuts"""
    
    db_path = '/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n🗃️  MISE À JOUR BASE SQLITE AVEC VRAIS DESTINATAIRES")
        print('-'*60)
        
        # Ajouter nouvelles colonnes si nécessaires
        nouvelles_colonnes = [
            ('destinataire_client_final', 'TEXT'),  # Email client réel
            ('statut_envoi_reel', 'TEXT'),          # CLIENT_CONFIRME / AUTO_ENVOI_ARCHIVE / NON_ENVOYE
            ('type_destinataire', 'TEXT')           # CLIENT / AUTO / INCONNU
        ]
        
        for col_name, col_type in nouvelles_colonnes:
            try:
                cursor.execute(f"ALTER TABLE factures ADD COLUMN {col_name} {col_type};")
                print(f"  ✅ Colonne ajoutée: {col_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"  ℹ️  Colonne existe déjà: {col_name}")
                else:
                    print(f"  ❌ Erreur {col_name}: {e}")
        
        # Mise à jour avec résultats analyse
        date_verification = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. Factures vraiment envoyées aux clients
        for facture, info in resultats_analyse['clients_confirmes'].items():
            cursor.execute("""
                UPDATE factures 
                SET destinataire_client_final = ?,
                    statut_envoi_reel = 'CLIENT_CONFIRME',
                    type_destinataire = 'CLIENT',
                    date_envoi_reel = ?,
                    destinataire_reel = ?,
                    statut_pdf_confirme = 'OUI',
                    date_verification_pdf = ?,
                    methode_verification = 'Analyse destinataires emails'
                WHERE numero_facture = ? OR numero_facture LIKE ?
            """, (
                info['destinataire_client'],
                info['date_envoi'],
                info['destinataire_client'],
                date_verification,
                facture,
                f"%{facture}%"
            ))
            
            if cursor.rowcount > 0:
                print(f"  ✅ {facture} → CLIENT {info['client_nom']} confirmé")
            else:
                print(f"  ⚠️  {facture} → Facture non trouvée en base")
        
        # 2. Auto-envois (PAS aux clients)
        for facture, info in resultats_analyse['auto_envois'].items():
            cursor.execute("""
                UPDATE factures 
                SET destinataire_client_final = NULL,
                    statut_envoi_reel = 'AUTO_ENVOI_ARCHIVE',
                    type_destinataire = 'AUTO',
                    date_envoi_reel = ?,
                    destinataire_reel = ?,
                    statut_pdf_confirme = 'NON_CLIENT',
                    date_verification_pdf = ?,
                    methode_verification = 'Analyse destinataires emails'
                WHERE numero_facture = ? OR numero_facture LIKE ?
            """, (
                info['date_envoi'],
                info['destinataire_reel'],
                date_verification,
                facture,
                f"%{facture}%"
            ))
            
            if cursor.rowcount > 0:
                print(f"  ⚠️  {facture} → AUTO-ENVOI (pas client) détecté")
        
        # 3. Factures non trouvées = vraiment non envoyées
        for facture in resultats_analyse['manquantes']:
            cursor.execute("""
                UPDATE factures 
                SET destinataire_client_final = NULL,
                    statut_envoi_reel = 'NON_ENVOYE',
                    type_destinataire = 'INCONNU',
                    date_envoi_reel = NULL,
                    destinataire_reel = NULL,
                    statut_pdf_confirme = 'NON',
                    date_verification_pdf = ?,
                    methode_verification = 'Analyse destinataires emails'
                WHERE numero_facture = ? OR numero_facture LIKE ?
            """, (
                date_verification,
                facture,
                f"%{facture}%"
            ))
            
            if cursor.rowcount > 0:
                print(f"  ❌ {facture} → VRAIMENT non envoyé confirmé")
        
        conn.commit()
        
        # Vérification finale
        cursor.execute("""
            SELECT COUNT(*) FROM factures 
            WHERE statut_envoi_reel = 'CLIENT_CONFIRME'
        """)
        nb_clients_confirmes = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM factures 
            WHERE statut_envoi_reel = 'AUTO_ENVOI_ARCHIVE'
        """)
        nb_auto_envois = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM factures 
            WHERE statut_envoi_reel = 'NON_ENVOYE'
        """)
        nb_non_envoyes = cursor.fetchone()[0]
        
        print(f"\n📊 ÉTAT FINAL BASE SQLITE:")
        print(f"  ✅ Factures clients confirmées: {nb_clients_confirmes}")
        print(f"  ⚠️  Auto-envois détectés: {nb_auto_envois}")
        print(f"  ❌ Vraiment non envoyées: {nb_non_envoyes}")
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur mise à jour base: {e}")
        return False

def main():
    print('🔍 VÉRIFICATION VRAIS DESTINATAIRES - CORRECTION MAJEURE')
    print('='*70)
    print('⚠️  IMPORTANT: PDF trouvé ≠ envoyé au client !')
    print('🎯 Distinction: Client final vs auto-envoi archive')
    print('='*70)
    
    # 1. Analyser vrais destinataires
    resultats = analyser_vrais_destinataires()
    
    if not resultats:
        print("❌ Impossible d'analyser les destinataires")
        return
    
    # 2. Mettre à jour base SQLite
    if mettre_a_jour_base_sqlite(resultats):
        print("\n🎉 CORRECTION TERMINÉE!")
        print("✅ Base SQLite mise à jour avec vrais statuts destinataires")
        print("🔍 Distinction claire: clients vs auto-envois")
    else:
        print("\n❌ Erreur mise à jour base SQLite")

if __name__ == "__main__":
    main()
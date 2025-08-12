#!/usr/bin/env python3
"""
SURVEILLANCE EMAIL COMPLÈTE - ENVOI & MONITORING
Envoi factures + surveillance réponses + détection litiges
"""

import imaplib
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re
import os
from pathlib import Path

class EmailSurveillanceComplete:
    """Système complet envoi/surveillance email facturation"""
    
    def __init__(self):
        self.setup_logging()
        self.load_email_config()
        self.setup_database()
        
    def setup_logging(self):
        """Configuration logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/home/sq/SYAGA-CONSULTING/logs/email_surveillance.log'),
                logging.StreamHandler()
            ]
        )
        
    def load_email_config(self):
        """Charger configuration email sécurisée"""
        try:
            with open('/home/sq/.email_config', 'r') as f:
                self.email_config = {}
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        self.email_config[key] = value
            
            logging.info("✅ Configuration email chargée")
        except FileNotFoundError:
            # Configuration par défaut pour développement
            self.email_config = {
                'SMTP_HOST': 'smtp.office365.com',
                'SMTP_PORT': '587',
                'IMAP_HOST': 'outlook.office365.com', 
                'IMAP_PORT': '993',
                'EMAIL_USER': 'sebastien.questier@syaga.fr',
                'EMAIL_PASSWORD': 'demo_password'
            }
            logging.warning("⚠️ Configuration email par défaut (dev)")
    
    def setup_database(self):
        """Initialiser tables surveillance email"""
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        # Table envois email
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS envois_email (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                facture_id INTEGER,
                numero_facture TEXT,
                client_nom TEXT,
                client_email TEXT,
                subject TEXT,
                date_envoi DATETIME DEFAULT CURRENT_TIMESTAMP,
                message_id TEXT,
                status TEXT DEFAULT 'SENT', -- 'SENT', 'DELIVERED', 'READ', 'REPLIED'
                tracking_data TEXT, -- JSON
                FOREIGN KEY (facture_id) REFERENCES factures (id)
            )
        ''')
        
        # Table surveillance réponses
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS surveillance_reponses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                envoi_id INTEGER,
                date_reponse DATETIME,
                sender_email TEXT,
                subject TEXT,
                body_text TEXT,
                sentiment_score REAL, -- -1 (négatif) à +1 (positif)
                type_reponse TEXT, -- 'ACK', 'QUESTION', 'LITIGE', 'PAIEMENT'
                urgence INTEGER DEFAULT 0, -- 0-5
                traited BOOLEAN DEFAULT FALSE,
                action_requise TEXT,
                FOREIGN KEY (envoi_id) REFERENCES envois_email (id)
            )
        ''')
        
        # Table modèles email
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS templates_email (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_template TEXT,
                type_facture TEXT, -- 'FORFAIT', 'PONCTUEL', 'RELANCE'
                subject_template TEXT,
                body_template TEXT,
                active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Initialiser templates par défaut
        self.init_default_templates()
        logging.info("✅ Tables surveillance email initialisées")
    
    def init_default_templates(self):
        """Initialiser templates email par défaut"""
        templates = [
            {
                'nom': 'facture_forfait',
                'type': 'FORFAIT',
                'subject': 'Facture forfait {client} - {periode} - {numero}',
                'body': '''Bonjour,

Veuillez trouver ci-joint la facture de forfait pour la période de {periode}.

Numéro de facture : {numero}
Montant HT : {montant_ht}€
Montant TTC : {montant_ttc}€
Échéance : {echeance}

Le règlement peut être effectué par virement sur notre compte :
IBAN : FR76 1234 5678 9012 3456 789A BIC : TESTFRPP

Merci de votre confiance.

Cordialement,
SYAGA CONSULTING'''
            },
            {
                'nom': 'facture_ponctuelle',
                'type': 'PONCTUEL', 
                'subject': 'Facture prestation {client} - {description} - {numero}',
                'body': '''Bonjour,

Veuillez trouver ci-joint la facture pour les prestations réalisées.

Détails :
{description}
Période : {periode}
Temps passé : {heures}h

Numéro de facture : {numero}
Montant HT : {montant_ht}€
Montant TTC : {montant_ttc}€

Merci de votre confiance.

Cordialement,
SYAGA CONSULTING'''
            },
            {
                'nom': 'relance_j15',
                'type': 'RELANCE',
                'subject': 'Rappel facture {numero} - Échéance dépassée',
                'body': '''Bonjour,

Nous nous permettons de vous rappeler que la facture {numero} d'un montant de {montant_ttc}€ TTC était échue le {echeance}.

Si le règlement a déjà été effectué, merci de ne pas tenir compte de ce message.

Dans le cas contraire, nous vous remercions de bien vouloir procéder au règlement dans les meilleurs délais.

Cordialement,
SYAGA CONSULTING'''
            }
        ]
        
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        for template in templates:
            cursor.execute('''
                INSERT OR IGNORE INTO templates_email 
                (nom_template, type_facture, subject_template, body_template)
                VALUES (?, ?, ?, ?)
            ''', (
                template['nom'], template['type'], 
                template['subject'], template['body']
            ))
        
        conn.commit()
        conn.close()
    
    def get_client_emails(self) -> Dict[str, str]:
        """Récupérer emails clients depuis config ou base"""
        # Pour l'instant, mapping statique - à terme depuis CRM
        client_emails = {
            'LAA': 'bm@laa.fr',
            'PHARMABEST': 'david-abenhaim@pharmacie-prado-mermoz.fr',
            'BUQUET': 'm.hinault@buquet-sas.fr',
            'PETRAS': 'contact@petras.fr',
            'PROVENCALE': 'christophe.marteau@provencale.com',
            'SEXTANT': 'contact@sextant-consulting.fr',
            'QUADRIMEX': 'shuon@quadrimex.com',
            'GENLOG': 'contact@genlog.fr',
            'UAI': 'f.beaute@unairici.fr',
            'AXION': 'n.diaz@axion-informatique.fr'
        }
        return client_emails
    
    def send_invoice_email(self, facture_id: int, pdf_path: str = None, 
                          template_type: str = 'FORFAIT') -> bool:
        """Envoyer email avec facture PDF"""
        try:
            # Récupérer infos facture
            conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT numero_facture, client_nom, date_facture, 
                       total_ht, total_ttc, date_echeance, objet
                FROM factures WHERE id = ?
            ''', (facture_id,))
            
            facture = cursor.fetchone()
            if not facture:
                logging.error(f"❌ Facture {facture_id} non trouvée")
                return False
            
            numero, client, date_facture, ht, ttc, echeance, description = facture
            
            # Récupérer template
            cursor.execute('''
                SELECT subject_template, body_template 
                FROM templates_email 
                WHERE type_facture = ? AND active = TRUE
                LIMIT 1
            ''', (template_type,))
            
            template = cursor.fetchone()
            if not template:
                logging.error(f"❌ Template {template_type} non trouvé")
                return False
            
            subject_template, body_template = template
            
            # Email client
            client_emails = self.get_client_emails()
            client_key = client.upper().split()[0]  # Premier mot du nom client
            client_email = client_emails.get(client_key, f'contact@{client_key.lower()}.fr')
            
            # Variables pour templates
            variables = {
                'client': client,
                'numero': numero,
                'montant_ht': f'{ht:.2f}',
                'montant_ttc': f'{ttc:.2f}',
                'echeance': echeance,
                'periode': datetime.strptime(date_facture, '%Y-%m-%d').strftime('%B %Y'),
                'description': description or 'Prestations réalisées',
                'heures': '0'  # À calculer depuis Clockify si nécessaire
            }
            
            # Générer email
            subject = subject_template.format(**variables)
            body = body_template.format(**variables)
            
            # Envoyer email
            success = self.send_smtp_email(
                to_email=client_email,
                subject=subject,
                body=body,
                pdf_attachment=pdf_path
            )
            
            if success:
                # Enregistrer envoi
                cursor.execute('''
                    INSERT INTO envois_email (
                        facture_id, numero_facture, client_nom, client_email,
                        subject, message_id, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    facture_id, numero, client, client_email,
                    subject, f'msg_{datetime.now().timestamp()}', 'SENT'
                ))
                
                conn.commit()
                logging.info(f"✅ Email envoyé: {numero} → {client_email}")
            
            conn.close()
            return success
            
        except Exception as e:
            logging.error(f"❌ Erreur envoi email facture {facture_id}: {e}")
            return False
    
    def send_smtp_email(self, to_email: str, subject: str, body: str, 
                       pdf_attachment: str = None) -> bool:
        """Envoyer email SMTP avec pièce jointe"""
        try:
            # Créer message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['EMAIL_USER']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Corps du message
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Pièce jointe PDF
            if pdf_attachment and os.path.exists(pdf_attachment):
                with open(pdf_attachment, 'rb') as f:
                    pdf_data = f.read()
                
                pdf_part = MIMEApplication(pdf_data, _subtype='pdf')
                pdf_part.add_header(
                    'Content-Disposition', 
                    'attachment', 
                    filename=os.path.basename(pdf_attachment)
                )
                msg.attach(pdf_part)
            
            # Connexion SMTP
            server = smtplib.SMTP(
                self.email_config['SMTP_HOST'],
                int(self.email_config['SMTP_PORT'])
            )
            server.starttls()
            server.login(
                self.email_config['EMAIL_USER'],
                self.email_config['EMAIL_PASSWORD']
            )
            
            # Envoi
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Erreur SMTP: {e}")
            return False
    
    def monitor_email_responses(self) -> List[Dict]:
        """Surveiller boîte de réception pour réponses"""
        try:
            # Connexion IMAP
            mail = imaplib.IMAP4_SSL(
                self.email_config['IMAP_HOST'],
                int(self.email_config['IMAP_PORT'])
            )
            mail.login(
                self.email_config['EMAIL_USER'], 
                self.email_config['EMAIL_PASSWORD']
            )
            mail.select('INBOX')
            
            # Chercher emails récents (7 derniers jours)
            depuis = (datetime.now() - timedelta(days=7)).strftime('%d-%b-%Y')
            status, messages = mail.search(None, f'SINCE {depuis}')
            
            if status != 'OK':
                logging.error("❌ Erreur recherche emails")
                return []
            
            nouvelles_reponses = []
            
            for msg_num in messages[0].split()[-20:]:  # 20 plus récents
                try:
                    status, data = mail.fetch(msg_num, '(RFC822)')
                    if status != 'OK':
                        continue
                    
                    email_message = email.message_from_bytes(data[0][1])
                    
                    # Analyser email
                    sender = email_message['From']
                    subject = email_message['Subject'] or ''
                    date_str = email_message['Date']
                    
                    # Extraire corps
                    body_text = self.extract_email_body(email_message)
                    
                    # Détecter si lié à facturation
                    if self.is_invoice_related(subject, body_text):
                        # Analyser sentiment et type
                        analysis = self.analyze_email_content(subject, body_text)
                        
                        response = {
                            'sender': sender,
                            'subject': subject,
                            'date': date_str,
                            'body': body_text,
                            'sentiment': analysis['sentiment'],
                            'type_reponse': analysis['type'],
                            'urgence': analysis['urgence'],
                            'facture_numero': analysis.get('facture_numero')
                        }
                        
                        nouvelles_reponses.append(response)
                        
                        # Sauvegarder en base
                        self.save_email_response(response)
                        
                except Exception as e:
                    logging.warning(f"⚠️ Erreur traitement email {msg_num}: {e}")
            
            mail.close()
            mail.logout()
            
            logging.info(f"📧 {len(nouvelles_reponses)} réponses facturation détectées")
            return nouvelles_reponses
            
        except Exception as e:
            logging.error(f"❌ Erreur surveillance email: {e}")
            return []
    
    def extract_email_body(self, email_message) -> str:
        """Extraire corps de l'email"""
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            body = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        return body.strip()
    
    def is_invoice_related(self, subject: str, body: str) -> bool:
        """Détecter si email lié à facturation"""
        facture_keywords = [
            'facture', 'invoice', 'paiement', 'payment', 'règlement',
            'F20', 'montant', 'échéance', 'virement', 'syaga'
        ]
        
        text = (subject + ' ' + body).lower()
        return any(keyword in text for keyword in facture_keywords)
    
    def analyze_email_content(self, subject: str, body: str) -> Dict:
        """Analyser contenu email (sentiment, type, urgence)"""
        text = (subject + ' ' + body).lower()
        
        # Détection type
        type_reponse = 'ACK'  # Par défaut
        
        if any(word in text for word in ['merci', 'reçu', 'parfait', 'ok', 'bien reçu']):
            type_reponse = 'ACK'
        elif any(word in text for word in ['question', 'précision', 'détail', 'expliquer']):
            type_reponse = 'QUESTION'
        elif any(word in text for word in ['payé', 'virement', 'règlement', 'effectué']):
            type_reponse = 'PAIEMENT'
        elif any(word in text for word in ['erreur', 'conteste', 'incorrect', 'problème', 'litige']):
            type_reponse = 'LITIGE'
        
        # Score sentiment (-1 à +1)
        sentiment = 0.0
        
        positive_words = ['merci', 'parfait', 'excellent', 'satisfait', 'content']
        negative_words = ['problème', 'erreur', 'mécontent', 'litige', 'incorrect']
        
        for word in positive_words:
            if word in text:
                sentiment += 0.2
                
        for word in negative_words:
            if word in text:
                sentiment -= 0.3
        
        sentiment = max(-1.0, min(1.0, sentiment))
        
        # Urgence (0-5)
        urgence = 0
        if type_reponse == 'LITIGE':
            urgence = 4
        elif type_reponse == 'QUESTION':
            urgence = 2
        elif sentiment < -0.3:
            urgence = 3
        
        # Détecter numéro facture
        facture_match = re.search(r'F?(\d{8,10})', subject + ' ' + body)
        facture_numero = facture_match.group(1) if facture_match else None
        
        return {
            'type': type_reponse,
            'sentiment': sentiment,
            'urgence': urgence,
            'facture_numero': facture_numero
        }
    
    def save_email_response(self, response: Dict):
        """Sauvegarder réponse email en base"""
        conn = sqlite3.connect('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO surveillance_reponses (
                    date_reponse, sender_email, subject, body_text,
                    sentiment_score, type_reponse, urgence
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                response['sender'],
                response['subject'],
                response['body'],
                response['sentiment'],
                response['type_reponse'],
                response['urgence']
            ))
            
            conn.commit()
            
        except Exception as e:
            logging.error(f"❌ Erreur sauvegarde réponse: {e}")
        
        conn.close()
    
    def run_daily_surveillance(self) -> Dict:
        """Surveillance quotidienne complète"""
        logging.info("🕵️ Démarrage surveillance email quotidienne")
        
        # 1. Surveiller réponses
        nouvelles_reponses = self.monitor_email_responses()
        
        # 2. Analyser réponses critiques
        critiques = [r for r in nouvelles_reponses if r['urgence'] >= 3]
        
        # 3. Générer rapport
        rapport = f"""
📧 SURVEILLANCE EMAIL QUOTIDIENNE {datetime.now().strftime('%d/%m/%Y')}
===============================================================

📨 ACTIVITÉ:
• Nouvelles réponses: {len(nouvelles_reponses)}
• Réponses critiques: {len(critiques)}

🚨 RÉPONSES CRITIQUES:
"""
        
        for i, reponse in enumerate(critiques[:5], 1):
            rapport += f"{i}. {reponse['type_reponse']} - {reponse['sender']}\n"
            rapport += f"   Sujet: {reponse['subject'][:60]}...\n"
            rapport += f"   Urgence: {reponse['urgence']}/5\n\n"
        
        rapport += f"""
📊 RÉPARTITION PAR TYPE:
"""
        
        types_count = {}
        for r in nouvelles_reponses:
            types_count[r['type_reponse']] = types_count.get(r['type_reponse'], 0) + 1
        
        for type_r, count in types_count.items():
            rapport += f"• {type_r}: {count}\n"
        
        logging.info(rapport)
        
        # Envoyer alerte si critiques
        if len(critiques) > 0:
            self.send_surveillance_alert(rapport)
        
        return {
            'nouvelles_reponses': len(nouvelles_reponses),
            'critiques': len(critiques),
            'types': types_count,
            'rapport': rapport
        }
    
    def send_surveillance_alert(self, rapport: str):
        """Envoyer alerte surveillance critique"""
        try:
            import subprocess
            subprocess.run([
                'python3',
                '/home/sq/SYAGA-CONSULTING/syaga-instructions/SEND_EMAIL_SECURE.py',
                '--to', 'sebastien.questier@syaga.fr',
                '--subject', f'🚨 Surveillance Email - Réponses Critiques {datetime.now().strftime("%d/%m/%Y")}',
                '--body', rapport
            ], check=True)
            logging.info("📧 Alerte surveillance envoyée")
        except Exception as e:
            logging.error(f"❌ Erreur envoi alerte: {e}")

def main():
    """Point d'entrée principal"""
    surveillance = EmailSurveillanceComplete()
    
    print("""
📧 SURVEILLANCE EMAIL COMPLÈTE SYAGA
=====================================

Fonctions:
  📤 Envoi factures automatique
  👁️ Surveillance réponses clients
  🚨 Détection litiges/contestations
  📊 Analyse sentiment/urgence
    """)
    
    # Surveillance quotidienne
    result = surveillance.run_daily_surveillance()
    
    print(f"\n✅ SURVEILLANCE TERMINÉE")
    print(f"Réponses: {result['nouvelles_reponses']} nouvelles")
    print(f"Critiques: {result['critiques']} à traiter")
    print(f"Types: {result['types']}")
    
    if result['critiques'] > 0:
        print(f"\n⚠️ {result['critiques']} réponses critiques détectées")

if __name__ == "__main__":
    main()
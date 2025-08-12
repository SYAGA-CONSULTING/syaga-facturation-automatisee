#!/usr/bin/env python3
"""
ANALYSE SÉCURISÉE QONTO - Sans tokens dans le code
Les credentials doivent être dans ~/.qonto_config
"""

import os
import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

class QontoAnalyseurSecure:
    def __init__(self):
        print("🔍 ANALYSE SÉCURISÉE TRANSACTIONS QONTO")
        print("=" * 60)
        
        # Charger credentials depuis fichier sécurisé
        self.load_credentials()
        
        if not self.login or not self.secret_key:
            print("\n⚠️ CONFIGURATION REQUISE:")
            print("1. Connectez-vous à votre compte Qonto")
            print("2. Allez dans Paramètres > Intégrations > API")
            print("3. Récupérez votre login et clé secrète")
            print("4. Créez le fichier ~/.qonto_config avec:")
            print("   QONTO_LOGIN='votre-login'")
            print("   QONTO_SECRET='votre-clé-secrète'")
            print("5. Sécurisez le fichier: chmod 600 ~/.qonto_config")
            return
        
        self.base_url = "https://thirdparty.qonto.com/v2"
        self.headers = {
            'Authorization': f'{self.login}:{self.secret_key}',
            'Content-Type': 'application/json'
        }
        
    def load_credentials(self):
        """Charge les credentials depuis fichier sécurisé"""
        config_file = os.path.expanduser('~/.qonto_config')
        self.login = None
        self.secret_key = None
        
        if not os.path.exists(config_file):
            print(f"❌ Fichier {config_file} non trouvé")
            return
        
        # Vérifier permissions
        stat_info = os.stat(config_file)
        mode = oct(stat_info.st_mode)[-3:]
        if mode != '600':
            print(f"⚠️ Permissions incorrectes sur {config_file}: {mode}")
            print("   Correction: chmod 600 ~/.qonto_config")
        
        # Lire le fichier
        try:
            with open(config_file, 'r') as f:
                for line in f:
                    if 'QONTO_LOGIN=' in line:
                        self.login = line.split('=')[1].strip().strip("'\"")
                    elif 'QONTO_SECRET=' in line:
                        self.secret_key = line.split('=')[1].strip().strip("'\"")
            
            if self.login and self.secret_key:
                if 'RÉCUPÉRER' in self.login or 'RÉCUPÉRER' in self.secret_key:
                    print("⚠️ Credentials de démo détectés")
                    self.login = None
                    self.secret_key = None
                else:
                    print(f"✅ Credentials chargés depuis {config_file}")
        except Exception as e:
            print(f"❌ Erreur lecture config: {e}")
    
    def test_connection(self):
        """Test la connexion à l'API Qonto"""
        if not self.login or not self.secret_key:
            return False
            
        try:
            response = requests.get(f"{self.base_url}/organization", headers=self.headers)
            if response.status_code == 200:
                org_data = response.json()
                org_name = org_data.get('organization', {}).get('name', 'N/A')
                print(f"✅ Connexion réussie - Organisation: {org_name}")
                return True
            else:
                print(f"❌ Erreur connexion: {response.status_code}")
                if response.status_code == 401:
                    print("   → Credentials invalides")
                return False
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False

def instructions_recuperation_token():
    """Affiche instructions pour récupérer token Qonto"""
    print("\n" + "="*60)
    print("📋 INSTRUCTIONS POUR RÉCUPÉRER VOS CREDENTIALS QONTO")
    print("="*60)
    
    print("""
1. CONNEXION À QONTO:
   → https://app.qonto.com
   → Connectez-vous avec vos identifiants

2. ACCÈS AUX PARAMÈTRES API:
   → Cliquez sur votre nom en haut à droite
   → Allez dans "Paramètres" 
   → Section "Intégrations" > "API"
   
3. RÉCUPÉRATION DES CREDENTIALS:
   → Login API: quelque chose comme "syaga-consulting-XXXX"
   → Clé secrète: une chaîne de caractères aléatoires
   
4. CRÉATION DU FICHIER CONFIG:
   → Exécutez ces commandes dans le terminal:
   
   cat > ~/.qonto_config << EOF
   QONTO_LOGIN='votre-login-ici'
   QONTO_SECRET='votre-secret-ici'
   EOF
   
   chmod 600 ~/.qonto_config
   
5. VÉRIFICATION:
   → Relancez ce script pour tester la connexion

⚠️ SÉCURITÉ:
   • NE JAMAIS commiter ces credentials dans Git
   • NE JAMAIS partager le fichier ~/.qonto_config
   • Garder les permissions à 600 (lecture owner uniquement)
""")

def main():
    """Test et instructions"""
    
    analyseur = QontoAnalyseurSecure()
    
    if analyseur.login and analyseur.secret_key:
        # Tester la connexion
        if analyseur.test_connection():
            print("\n✅ Prêt pour l'analyse des transactions!")
            print("💡 Relancez le script qonto_analyse_dougs_essence.py")
            print("   après avoir mis à jour les credentials dans ce script")
        else:
            print("\n❌ Connexion échouée")
            instructions_recuperation_token()
    else:
        instructions_recuperation_token()

if __name__ == "__main__":
    main()
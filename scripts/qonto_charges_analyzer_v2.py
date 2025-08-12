#!/usr/bin/env python3
"""
ANALYSEUR CHARGES QONTO V2 - Format Auth Correct
Test différents formats d'authentification Qonto
"""

import requests
import json
from datetime import datetime
import base64

class QontoChargesAnalyzerV2:
    def __init__(self):
        """Initialise avec credentials"""
        self.login = "syaga-consulting-5172"
        self.secret_key = "06f55a4b41d0"
        self.base_url = "https://thirdparty.qonto.com/v2"
        
    def test_auth_methods(self):
        """Test différents formats d'authentification"""
        print("🔐 TEST MÉTHODES D'AUTHENTIFICATION QONTO")
        print("="*50)
        
        # Méthode 1: Basic Auth avec login:secret
        print("\n1️⃣ Test Basic Auth (login:secret)")
        try:
            credentials = f"{self.login}:{self.secret_key}"
            encoded = base64.b64encode(credentials.encode()).decode()
            headers = {
                'Authorization': f'Basic {encoded}',
                'Content-Type': 'application/json'
            }
            response = requests.get(f"{self.base_url}/organization", headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            if response.status_code != 200:
                print(f"   Erreur: {response.text}")
        except Exception as e:
            print(f"   Exception: {e}")
        
        # Méthode 2: Bearer Token
        print("\n2️⃣ Test Bearer Token")
        try:
            headers = {
                'Authorization': f'Bearer {self.secret_key}',
                'Content-Type': 'application/json'
            }
            response = requests.get(f"{self.base_url}/organization", headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            if response.status_code != 200:
                print(f"   Erreur: {response.text}")
        except Exception as e:
            print(f"   Exception: {e}")
        
        # Méthode 3: API Key header
        print("\n3️⃣ Test API Key Header")
        try:
            headers = {
                'Authorization': f'{self.login}:{self.secret_key}',
                'Content-Type': 'application/json'
            }
            response = requests.get(f"{self.base_url}/organization", headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            if response.status_code != 200:
                print(f"   Erreur: {response.text}")
        except Exception as e:
            print(f"   Exception: {e}")
        
        # Méthode 4: Custom format
        print("\n4️⃣ Test Format Custom")
        try:
            headers = {
                'Authorization': f'{self.secret_key}',
                'Content-Type': 'application/json'
            }
            response = requests.get(f"{self.base_url}/organization", headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            if response.status_code != 200:
                print(f"   Erreur: {response.text}")
        except Exception as e:
            print(f"   Exception: {e}")
        
        # Méthode 5: URL avec credentials
        print("\n5️⃣ Test URL avec credentials")
        try:
            auth_url = f"https://{self.login}:{self.secret_key}@thirdparty.qonto.com/v2/organization"
            response = requests.get(auth_url, timeout=10)
            print(f"   Status: {response.status_code}")
            if response.status_code != 200:
                print(f"   Erreur: {response.text}")
        except Exception as e:
            print(f"   Exception: {e}")
        
        # Test endpoint de base
        print("\n6️⃣ Test endpoint racine sans auth")
        try:
            response = requests.get("https://thirdparty.qonto.com/v2", timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
        except Exception as e:
            print(f"   Exception: {e}")

def main():
    print("🔐 DIAGNOSTIC AUTHENTIFICATION QONTO")
    print("Credentials reçues:")
    print("- Login:", "syaga-consulting-5172")
    print("- Secret:", "06f55a4b41d0")
    
    analyzer = QontoChargesAnalyzerV2()
    analyzer.test_auth_methods()

if __name__ == "__main__":
    main()
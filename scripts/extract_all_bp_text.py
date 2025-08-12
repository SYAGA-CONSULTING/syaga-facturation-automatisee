#!/usr/bin/env python3
"""
EXTRACTION COMPLÈTE DU TEXTE DES PDFs BP
Pour analyse manuelle et recherche des loyers
"""

import os
import re
import pdfplumber

class BPTextExtractor:
    def __init__(self):
        self.bp_dir = "/home/sq/extraits de compte BP"
        
    def extract_all_text(self):
        """Extrait tout le texte de tous les PDFs"""
        print("="*70)
        print("📄 EXTRACTION TEXTE COMPLET BANQUE POPULAIRE")
        print("="*70)
        
        # Focus sur les 3 derniers mois
        focus_files = [
            'Extrait de compte - 06021516710 - 20250515.pdf',  # Mai
            'Extrait de compte - 06021516710 - 20250530.pdf',  # Mai
            'Extrait de compte - 06021516710 - 20250613.pdf',  # Juin
            'Extrait de compte - 06021516710 - 20250630.pdf',  # Juin
            'Extrait de compte - 06021516710 - 20250715.pdf',  # Juillet
            'Extrait de compte - 06021516710 - 20250731.pdf'   # Juillet
        ]
        
        for filename in focus_files:
            pdf_path = os.path.join(self.bp_dir, filename)
            
            if not os.path.exists(pdf_path):
                continue
                
            print(f"\n🔍 {filename}:")
            print("-" * 60)
            
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if not text:
                            continue
                        
                        print(f"\n--- PAGE {page_num + 1} ---")
                        
                        # Afficher ligne par ligne pour recherche manuelle
                        lines = text.split('\n')
                        for i, line in enumerate(lines):
                            # Filtrer les lignes avec montants (débits probables)
                            if re.search(r'\d+[,.]\d{2}\s*€', line):
                                # Vérifier si c'est un débit (montant négatif ou contexte débit)
                                if '-' in line or any(keyword in line.upper() for keyword in ['PAIEMENT', 'VIREMENT', 'PRELEVEMENT', 'ACHAT', 'RETRAIT']):
                                    print(f"  L{i+1:3}: {line}")
                            # Ou si ligne contient des mots-clés intéressants
                            elif any(word in line.lower() for word in ['loyer', 'sant', 'adiol', 'nimes', 'nîmes', 'immobil', 'sci', 'location', 'bail']):
                                print(f"  L{i+1:3} [KEYWORD]: {line}")
                                
            except Exception as e:
                print(f"❌ Erreur: {e}")

def main():
    extractor = BPTextExtractor()
    extractor.extract_all_text()

if __name__ == "__main__":
    main()
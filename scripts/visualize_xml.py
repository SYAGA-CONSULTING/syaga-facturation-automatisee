#!/usr/bin/env python3
"""
Visualise le contenu du XML OXYGEN de manière claire
"""

import xml.etree.ElementTree as ET
import sys

# Parser le XML
xml_file = sys.argv[1] if len(sys.argv) > 1 else 'data/oxygen/2025-07/FACTURES_JUILLET_2025_CORRECT.xml'
tree = ET.parse(xml_file)
root = tree.getroot()

print('📊 FACTURES JUILLET 2025 - IMPORT OXYGEN')
print('=' * 70)

total_global = 0
facture_num = 1

# Définir les namespaces
ns = {'ns': 'http://tempuri.org/data.xsd'}

# Parcourir chaque PIECE (facture)
for piece in root.findall('.//ns:PIECE', ns):
    # Récupérer les infos de base
    client_code = piece.find('ns:CLIENT_CODE', ns)
    client_code = client_code.text if client_code is not None else 'N/A'
    
    # Récupérer nom client depuis l'adresse de facturation
    nom_client = client_code
    for adresse in piece.findall('ns:adresse', ns):
        stype = adresse.find('ns:STYPE', ns)
        if stype is not None and stype.text == 'facturation':
            nom = adresse.find('ns:NOM', ns)
            if nom is not None:
                nom_client = nom.text
                break
    
    print(f'\n📄 Facture #{facture_num} - {nom_client} ({client_code})')
    print('-' * 50)
    
    total_facture = 0
    
    # Parcourir chaque ligne
    for ligne in piece.findall('ns:LIGNE', ns):
        desig_elem = ligne.find('ns:DESIG', ns)
        qte_elem = ligne.find('ns:QTE', ns)
        puht_elem = ligne.find('ns:PUHT', ns)
        
        if desig_elem is not None and qte_elem is not None and puht_elem is not None:
            desig = desig_elem.text
            qte = qte_elem.text.replace(',', '.')
            puht = puht_elem.text.replace(',', '.')
            
            montant = float(qte) * float(puht)
            total_facture += montant
            
            print(f'  • {desig}')
            print(f'    {qte}h × {puht}€ = {montant:,.0f}€')
    
    print(f'  → Total HT: {total_facture:,.0f}€')
    print(f'  → TVA 20%: {total_facture * 0.2:,.0f}€')
    print(f'  → Total TTC: {total_facture * 1.2:,.0f}€')
    
    total_global += total_facture
    facture_num += 1

print('\n' + '=' * 70)
print(f'💰 TOTAL GLOBAL: {total_global:,.0f}€ HT')
print(f'💰 TVA TOTALE: {total_global * 0.2:,.0f}€')
print(f'💰 TOTAL TTC: {total_global * 1.2:,.0f}€')
print(f'📝 Nombre de factures: {facture_num - 1}')
print('=' * 70)
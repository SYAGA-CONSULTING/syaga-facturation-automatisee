#!/usr/bin/env python3
"""
Corrige le format XML pour OXYGEN :
- Remplace les points par des virgules dans les montants
- Ajoute les virgules aux montants entiers
"""

import re

# Lire le fichier XML
with open('/home/sq/oxygen_export/FACTURES_JUILLET_2025.xml', 'r', encoding='utf-8') as f:
    xml_content = f.read()

# Corriger les formats de montants
# 1. Remplacer les points par des virgules dans les décimales
xml_content = re.sub(r'<QTE>(\d+)\.(\d+)</QTE>', r'<QTE>\1,\2</QTE>', xml_content)
xml_content = re.sub(r'<TAUX_REMISE>(\d+)\.(\d+)</TAUX_REMISE>', r'<TAUX_REMISE>\1,\2</TAUX_REMISE>', xml_content)
xml_content = re.sub(r'<TAUX_ESCOMPTE>(\d+)\.(\d+)</TAUX_ESCOMPTE>', r'<TAUX_ESCOMPTE>\1,\2</TAUX_ESCOMPTE>', xml_content)
xml_content = re.sub(r'<PORT_HT>(\d+)\.(\d+)</PORT_HT>', r'<PORT_HT>\1,\2</PORT_HT>', xml_content)
xml_content = re.sub(r'<FRAIS_HT>(\d+)\.(\d+)</FRAIS_HT>', r'<FRAIS_HT>\1,\2</FRAIS_HT>', xml_content)

# 2. Ajouter des virgules aux montants PUHT qui sont des entiers
xml_content = re.sub(r'<PUHT>(\d+)</PUHT>', r'<PUHT>\1,00</PUHT>', xml_content)

# Sauvegarder le fichier corrigé
with open('/home/sq/oxygen_export/FACTURES_JUILLET_2025_CORRECT.xml', 'w', encoding='utf-8') as f:
    f.write(xml_content)

print("✅ XML corrigé avec le format virgule pour OXYGEN")
print("📁 Fichier: /home/sq/oxygen_export/FACTURES_JUILLET_2025_CORRECT.xml")
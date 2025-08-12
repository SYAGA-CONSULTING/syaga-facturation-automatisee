#!/usr/bin/env python3
"""
Génération de tous les PDF avec le module SYAGA_PDF correct
"""

import sys
import os
sys.path.append('/home/sq/SYAGA-CONSULTING/syaga-instructions')

# Importer le bon module
from SYAGA_PDF_V3_3_TECHNICAL import generate_and_send_technical_pdf

# Importer le module d'envoi email
from SEND_EMAIL_SECURE import send_email

from datetime import datetime
import json

def generate_clockify_pdf(client, hours_data, output_path):
    """Génère un PDF de rapport Clockify"""
    
    if isinstance(hours_data, dict):
        total = hours_data.get('TOTAL', sum(v for k,v in hours_data.items() if k != 'TOTAL'))
        details_html = "<table border='1' style='width: 100%; border-collapse: collapse;'>"
        details_html += "<tr style='background: #f0f0f0;'><th>Tâche</th><th>Heures</th><th>%</th></tr>"
        
        for task, hours in hours_data.items():
            if task != 'TOTAL':
                percentage = (hours/total*100) if total > 0 else 0
                details_html += f"<tr><td>{task}</td><td>{hours:.2f}h</td><td>{percentage:.1f}%</td></tr>"
        
        details_html += f"<tr style='background: #e8f4f8; font-weight: bold;'><td>TOTAL</td><td>{total:.2f}h</td><td>100%</td></tr>"
        details_html += "</table>"
    else:
        total = hours_data
        details_html = f"<p>Total : {total:.2f} heures</p>"
    
    sections = [
        {
            'title': 'Rapport Clockify',
            'content': f"""
            <h2 style='color: #667eea;'>{client} - Juillet 2025</h2>
            <div style='background: #f8f9fa; padding: 15px; margin: 20px 0;'>
                <p><strong>Total heures :</strong> {total:.2f}h</p>
                <p><strong>Équivalent jours :</strong> {total/7:.1f}j (base 7h)</p>
                <p><strong>Période :</strong> 01/07/2025 - 31/07/2025</p>
            </div>
            <h3>Détail des heures</h3>
            {details_html}
            """
        }
    ]
    
    # Sauvegarder comme HTML pour conversion ultérieure
    with open(output_path.replace('.pdf', '.html'), 'w', encoding='utf-8') as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Clockify - {client}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h2 {{ color: #667eea; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #667eea; color: white; padding: 10px; }}
        td {{ padding: 8px; border: 1px solid #ddd; }}
    </style>
</head>
<body>
    {sections[0]['content']}
</body>
</html>
        """)
    
    print(f"  ✅ HTML créé : {output_path.replace('.pdf', '.html')}")
    return True

def generate_invoice_pdf(invoice_data, output_path):
    """Génère un PDF de facture"""
    
    tva_rate = invoice_data.get('tva_rate', 0.20)
    # Nettoyer le montant : supprimer espaces, €, puis remplacer , par . et supprimer points de milliers
    total_ht_str = invoice_data['total_ht'].replace('€', '').replace(' ', '').strip()
    if ',' in total_ht_str:
        # Format français : 2.700,00 -> 2700.00
        total_ht_str = total_ht_str.replace('.', '').replace(',', '.')
    total_ht_val = float(total_ht_str)
    tva_montant = total_ht_val * tva_rate
    total_ttc = total_ht_val * (1 + tva_rate)
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Facture {invoice_data['numero']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ border-bottom: 3px solid #333; padding-bottom: 20px; margin-bottom: 30px; }}
        .logo {{ font-size: 24pt; font-weight: bold; color: #667eea; }}
        .invoice-number {{ color: #e74c3c; font-weight: bold; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 20px 0; }}
        .section {{ background: #f8f9fa; padding: 15px; border-radius: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #e9ecef; padding: 10px; text-align: left; }}
        td {{ padding: 10px; border: 1px solid #dee2e6; }}
        .total-section {{ background: #e8f4f8; padding: 15px; margin-top: 20px; border: 2px solid #3498db; }}
        .total-line {{ margin: 5px 0; }}
        .total-final {{ font-size: 14pt; font-weight: bold; border-top: 2px solid #3498db; padding-top: 10px; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">SYAGA CONSULTING</div>
        <h1>FACTURE <span class="invoice-number">{invoice_data['numero']}</span></h1>
        <p>Date : 31/07/2025</p>
    </div>
    
    <div class="grid">
        <div class="section">
            <h3>ÉMETTEUR</h3>
            <strong>SYAGA CONSULTING</strong><br>
            Sébastien QUESTIER<br>
            [Adresse à compléter]<br>
            SIRET : [À compléter]
        </div>
        <div class="section">
            <h3>CLIENT</h3>
            <strong>{invoice_data['client_nom']}</strong><br>
            Code OXYGEN : <strong>{invoice_data['code_oxygen']}</strong><br>
            {invoice_data['adresse'].replace(chr(10), '<br>')}
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Désignation</th>
                <th>Quantité</th>
                <th>Prix Unit. HT</th>
                <th>Total HT</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{invoice_data['designation']}</td>
                <td>{invoice_data['quantite']}</td>
                <td>{invoice_data['prix_unit']}</td>
                <td>{invoice_data['total_ht']}</td>
            </tr>
        </tbody>
    </table>
    
    <div class="total-section">
        <div class="total-line">Total HT : <strong>{invoice_data['total_ht']}</strong></div>
        <div class="total-line">TVA {invoice_data.get('tva_label', '20%')} : <strong>{tva_montant:.2f} €</strong></div>
        <div class="total-line total-final">TOTAL TTC : <strong>{total_ttc:.2f} €</strong></div>
    </div>
    
    <p style="margin-top: 30px;">
        <strong>Conditions :</strong> Paiement à 30 jours par virement<br>
        {invoice_data.get('mention_legale', '')}
    </p>
</body>
</html>
    """
    
    # Sauvegarder comme HTML
    with open(output_path.replace('.pdf', '.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  ✅ HTML créé : {output_path.replace('.pdf', '.html')}")
    return True

def main():
    print("🚀 GÉNÉRATION DES PDF - JUILLET 2025")
    print("="*60)
    
    base_dir = "/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee"
    pdf_dir = f"{base_dir}/reports/pdf/2025-07"
    os.makedirs(f"{pdf_dir}/clockify", exist_ok=True)
    os.makedirs(f"{pdf_dir}/factures", exist_ok=True)
    
    # 1. GÉNÉRER LES RAPPORTS CLOCKIFY
    print("\n📊 Génération des rapports Clockify...")
    
    clients_hours = {
        "LAA": {"Dette technologique": 27.0, "Tests": 21.5, "Développements": 9.0, "Maintenance HF": 5.0, "TOTAL": 62.5},
        "LAA_MAROC": 1.5,
        "UAI": {"HardenAD": 5.5, "SQL Server": 9.0, "TOTAL": 14.5},
        "LEFEBVRE": 4.0,
        "PETRAS": 2.0,
        "TOUZEAU": 1.5,
        "AXION": 7.0,
        "ART_INFO": 2.0,
        "FARBOS": 1.5,
        "PORT_DE_BOUC": 4.0,
        "QUADRIMEX": 15.0
    }
    
    for client, hours in clients_hours.items():
        output_path = f"{pdf_dir}/clockify/Clockify_{client}_Juillet_2025.pdf"
        generate_clockify_pdf(client, hours, output_path)
    
    # 2. GÉNÉRER LES FACTURES MOCKUP
    print("\n📄 Génération des factures mockup...")
    
    factures = [
        {
            'numero': 'F20250001',
            'client_nom': 'LES AUTOMATISMES APPLIQUES',
            'code_oxygen': 'LAA01',
            'adresse': 'Bat.C Parc de Bachasson\n13590 MEYREUIL',
            'designation': 'Prestations informatiques - Juillet 2025',
            'quantite': '27,00 heures',
            'prix_unit': '100,00 €',
            'total_ht': '2.700,00 €',
            'tva_rate': 0.20,
            'tva_label': '20%'
        },
        {
            'numero': 'F20250002',
            'client_nom': 'LAA MAROC',
            'code_oxygen': 'LAAM01',
            'adresse': 'TFZ, Centre Affaires\n90000 TANGER - MAROC',
            'designation': 'Maintenance informatique - Juillet 2025',
            'quantite': '1,50 heures',
            'prix_unit': '100,00 €',
            'total_ht': '150,00 €',
            'tva_rate': 0,
            'tva_label': '0% (Exonération)',
            'mention_legale': 'Exonération TVA art. 259 B CGI'
        },
        {
            'numero': 'F20250003',
            'client_nom': 'UN AIR D\'ICI',
            'code_oxygen': '1AIR01',
            'adresse': '850 chemin de Villefranche\n84200 CARPENTRAS',
            'designation': 'Prestations informatiques - Juillet 2025',
            'quantite': '5,50 heures',
            'prix_unit': '850,00 €',
            'total_ht': '4.675,00 €',
            'tva_rate': 0.20,
            'tva_label': '20%'
        },
        {
            'numero': 'F20250004',
            'client_nom': 'AIXAGON',
            'code_oxygen': 'AIX01',
            'adresse': '5 Montée de Baume\n13124 PEYPIN',
            'designation': 'Prestations informatiques - Juillet 2025',
            'quantite': '4,00 heures',
            'prix_unit': '100,00 €',
            'total_ht': '400,00 €',
            'tva_rate': 0.20,
            'tva_label': '20%'
        }
    ]
    
    for facture in factures:
        output_path = f"{pdf_dir}/factures/{facture['numero']}_{facture['code_oxygen']}.pdf"
        generate_invoice_pdf(facture, output_path)
    
    # 3. CRÉER L'EMAIL AVEC TOUS LES LIENS
    print("\n📧 Préparation de l'email...")
    
    html_body = f"""
    <h2>📊 Package Complet Facturation Juillet 2025</h2>
    
    <h3>✅ Fichiers générés :</h3>
    
    <h4>📈 Rapports Clockify (11 fichiers)</h4>
    <ul>
        <li>LAA : 62,5h (4 catégories)</li>
        <li>LAA Maroc : 1,5h (TVA 0%)</li>
        <li>UAI : 14,5h (2 catégories)</li>
        <li>+ 8 autres clients</li>
    </ul>
    
    <h4>📄 Factures Mockup (4 exemples)</h4>
    <ul>
        <li>LAA (LAA01) : 2.700€</li>
        <li>LAA Maroc (LAAM01) : 150€ (TVA 0%)</li>
        <li>UAI (1AIR01) : 4.675€</li>
        <li>AIXAGON (AIX01) : 400€ (pour Port de Bouc)</li>
    </ul>
    
    <h4>📊 Excel LAA</h4>
    <p>Fichier CSV avec détail des 4 catégories : {base_dir}/reports/excel/2025-07/LAA_detail_juillet_2025.csv</p>
    
    <h4>📁 XML OXYGEN</h4>
    <p>Prêt pour import : {base_dir}/data/oxygen/2025-07/FACTURES_JUILLET_2025_STANDARD.xml</p>
    
    <h3>⚠️ Points de validation :</h3>
    <ul style='background: #fff3cd; padding: 15px;'>
        <li><strong>UAI = 1AIR01</strong> (pas UAI01)</li>
        <li><strong>Port de Bouc = AIX01</strong> (via AIXAGON)</li>
        <li><strong>LAA Maroc = TVA 0%</strong> (code MA)</li>
        <li><strong>Total : 115,50h</strong> = cohérent Clockify</li>
    </ul>
    
    <p><strong>📁 Tous les fichiers dans :</strong><br>
    <code>{pdf_dir}/</code></p>
    
    <p><em>Note : Les PDF sont générés en HTML pour visualisation. 
    Conversion PDF finale avec wkhtmltopdf ou impression navigateur.</em></p>
    """
    
    # Envoyer l'email
    result = send_email(
        to_email="sebastien.questier@syaga.fr",
        subject="📊 PACKAGE COMPLET - Rapports Clockify + Factures + Excel - Juillet 2025",
        html_body=html_body
    )
    
    if result:
        print("\n✅ Email envoyé avec succès!")
    else:
        print("\n❌ Erreur envoi email")
    
    print("\n" + "="*60)
    print("✅ GÉNÉRATION TERMINÉE")
    print(f"📁 Fichiers dans : {pdf_dir}")
    print("  - /clockify/ : 11 rapports HTML")
    print("  - /factures/ : 4 factures HTML")
    print("  - Excel CSV disponible")
    print("  - XML OXYGEN prêt")
    print("\n💡 Pour convertir en PDF :")
    print("  - Ouvrir les HTML dans un navigateur")
    print("  - Imprimer en PDF (Ctrl+P)")
    print("  - Ou utiliser wkhtmltopdf")

if __name__ == "__main__":
    main()
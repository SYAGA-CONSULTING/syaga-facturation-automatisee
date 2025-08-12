#!/usr/bin/env python3
"""Génère les 14 factures juillet 2025 en HTML"""

import os
from datetime import datetime

FACTURES_DATA = [
    {"num": "F2025-1000", "client": "LES AUTOMATISMES APPLIQUÉS", "adresse": "Parc de Bachasson Bât.C", "cp_ville": "13590 MEYREUIL", "contact": "Bruno MEUNIER", "desc": "Dette technologique - Migration SAGE V12 et Windows Server 2022 - Juillet 2025", "qty": "27.00 h", "pu": "100.00", "ht": "2700.00"},
    {"num": "F2025-1001", "client": "LES AUTOMATISMES APPLIQUÉS", "adresse": "Parc de Bachasson Bât.C", "cp_ville": "13590 MEYREUIL", "contact": "Bruno MEUNIER", "desc": "Tests et validations infrastructure Hyper-V - Snapshots et rollback - Juillet 2025", "qty": "21.50 h", "pu": "100.00", "ht": "2150.00"},
    {"num": "F2025-1002", "client": "LES AUTOMATISMES APPLIQUÉS", "adresse": "Parc de Bachasson Bât.C", "cp_ville": "13590 MEYREUIL", "contact": "Bruno MEUNIER", "desc": "Support technique niveau 3 - Juillet 2025", "qty": "7.00 h", "pu": "100.00", "ht": "700.00"},
    {"num": "F2025-1003", "client": "LES AUTOMATISMES APPLIQUÉS", "adresse": "Parc de Bachasson Bât.C", "cp_ville": "13590 MEYREUIL", "contact": "Bruno MEUNIER", "desc": "Maintenance préventive serveurs - Juillet 2025", "qty": "7.00 h", "pu": "100.00", "ht": "700.00"},
    {"num": "F2025-1004", "client": "LAA MAROC", "adresse": "Zone Industrielle", "cp_ville": "TANGER - MAROC", "contact": "Bruno DELICATA", "desc": "Support à distance infrastructure - Juillet 2025", "qty": "1.50 h", "pu": "100.00", "ht": "150.00"},
    {"num": "F2025-1005", "client": "UN AIR D'ICI", "adresse": "850 Chemin de Villefranche", "cp_ville": "84200 CARPENTRAS", "contact": "Frédéric BEAUTE", "desc": "Optimisation base de données SQL Server X3 - Phase 1 - Juillet 2025", "qty": "113.25 h", "pu": "100.00", "ht": "11325.00"},
    {"num": "F2025-1006", "client": "UN AIR D'ICI", "adresse": "850 Chemin de Villefranche", "cp_ville": "84200 CARPENTRAS", "contact": "Frédéric BEAUTE", "desc": "Support technique et maintenance - Juillet 2025", "qty": "10.00 h", "pu": "100.00", "ht": "1000.00"},
    {"num": "F2025-1007", "client": "SELAS MARIE-JOSE LEFEBVRE", "adresse": "75 Avenue des Champs-Élysées", "cp_ville": "75008 PARIS", "contact": "Marie-José LEFEBVRE", "desc": "Conseil et expertise informatique - Juillet 2025", "qty": "4.80 h", "pu": "100.00", "ht": "480.00"},
    {"num": "F2025-1008", "client": "PETRAS SAS", "adresse": "Route de Rians", "cp_ville": "83910 POURRIÈRES", "contact": "Dominique PETRAS", "desc": "Maintenance infrastructure IT - Juillet 2025", "qty": "2.00 h", "pu": "100.00", "ht": "200.00"},
    {"num": "F2025-1009", "client": "GARAGE TOUZEAU", "adresse": "15 Rue de la République", "cp_ville": "78120 RAMBOUILLET", "contact": "Direction", "desc": "Support technique - Juillet 2025", "qty": "1.50 h", "pu": "100.00", "ht": "150.00"},
    {"num": "F2025-1010", "client": "AXION INFORMATIQUE", "adresse": "Zone d'Activités", "cp_ville": "13100 AIX-EN-PROVENCE", "contact": "Nicolas DIAZ", "desc": "Infogérance serveurs clients - Juillet 2025", "qty": "7.00 h", "pu": "100.00", "ht": "700.00"},
    {"num": "F2025-1011", "client": "ART INFORMATIQUE", "adresse": "Parc Technologique", "cp_ville": "31000 TOULOUSE", "contact": "Serge SENEGAS", "desc": "Support et conseil - Juillet 2025", "qty": "2.00 h", "pu": "100.00", "ht": "200.00"},
    {"num": "F2025-1012", "client": "FARBOS SAS", "adresse": "Zone Industrielle", "cp_ville": "33000 BORDEAUX", "contact": "Jean-Philippe BRIAL", "desc": "Maintenance systèmes - Juillet 2025", "qty": "1.50 h", "pu": "100.00", "ht": "150.00"},
    {"num": "F2025-1013", "client": "MAIRIE DE PORT DE BOUC", "adresse": "Cours Landrivon", "cp_ville": "13110 PORT DE BOUC", "contact": "Service Informatique", "desc": "Support infrastructure municipale - Juillet 2025", "qty": "4.00 h", "pu": "100.00", "ht": "400.00"},
    {"num": "F2025-1014", "client": "QUADRIMEX", "adresse": "Parc d'Activités", "cp_ville": "13400 AUBAGNE", "contact": "Philippe STEPHAN", "desc": "Développement spécifique et intégration - Juillet 2025", "qty": "15.00 h", "pu": "100.00", "ht": "1500.00"},
]

TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facture {num}</title>
    <style>
        @page {{ size: A4; margin: 20mm; }}
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #000; background: white; }}
        .invoice-container {{ max-width: 800px; margin: 0 auto; background: white; }}
        .header {{ text-align: center; margin-bottom: 40px; }}
        .company-name {{ font-size: 28px; font-weight: bold; color: #003d7a; margin-bottom: 10px; }}
        .company-info {{ font-size: 12px; line-height: 1.5; color: #333; }}
        .invoice-title {{ text-align: center; font-size: 24px; font-weight: bold; color: #c00; margin: 30px 0; }}
        .invoice-date {{ font-size: 14px; margin-bottom: 30px; }}
        .client-section {{ border: 2px solid #003d7a; margin-bottom: 30px; background: #e8f0f7; }}
        .client-header {{ background: #d4e3f0; padding: 8px 15px; font-weight: bold; border-bottom: 1px solid #003d7a; }}
        .client-info {{ padding: 15px; line-height: 1.6; }}
        .items-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
        .items-table th {{ background: #003d7a; color: white; padding: 10px; text-align: left; font-size: 14px; }}
        .items-table th:last-child, .items-table td:last-child {{ text-align: right; }}
        .items-table td {{ padding: 10px; border-bottom: 1px solid #ddd; font-size: 13px; }}
        .totals-section {{ margin-left: auto; width: 300px; margin-bottom: 40px; }}
        .totals-section table {{ width: 100%; border-collapse: collapse; }}
        .totals-section td {{ padding: 8px; font-size: 14px; }}
        .totals-section .total-row {{ font-weight: bold; font-size: 16px; border-top: 2px solid #003d7a; }}
        .payment-info {{ margin-top: 40px; font-size: 13px; line-height: 1.6; }}
        .payment-info strong {{ font-weight: bold; }}
    </style>
</head>
<body>
    <div class="invoice-container">
        <div class="header">
            <div class="company-name">SYAGA CONSULTING</div>
            <div class="company-info">
                15 Rue des Pêcheurs - 13270 FOS-SUR-MER<br>
                Tél: 06 61 28 33 76 - Email: sebastien.questier@syaga.fr<br>
                SIRET: 799 332 507 00018 - TVA: FR 62 799332507
            </div>
        </div>
        
        <div class="invoice-title">FACTURE {num}</div>
        <div class="invoice-date">Date: 31/07/2025</div>
        
        <div class="client-section">
            <div class="client-header">CLIENT</div>
            <div class="client-info">
                <strong>{client}</strong><br>
                {adresse}<br>
                {cp_ville}<br>
                À l'attention de: {contact}
            </div>
        </div>
        
        <table class="items-table">
            <thead>
                <tr>
                    <th style="width: 50%;">Description</th>
                    <th style="width: 15%;">Quantité</th>
                    <th style="width: 15%;">Prix Unit.</th>
                    <th style="width: 20%;">Total HT</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{desc}</td>
                    <td>{qty}</td>
                    <td>{pu} €</td>
                    <td>{ht} €</td>
                </tr>
            </tbody>
        </table>
        
        <div class="totals-section">
            <table>
                <tr>
                    <td style="text-align: right;">Total HT:</td>
                    <td style="text-align: right; font-weight: bold;">{ht} €</td>
                </tr>
                <tr>
                    <td style="text-align: right;">TVA 20%:</td>
                    <td style="text-align: right;">{tva:.2f} €</td>
                </tr>
                <tr class="total-row">
                    <td style="text-align: right;">Total TTC:</td>
                    <td style="text-align: right;">{ttc:.2f} €</td>
                </tr>
            </table>
        </div>
        
        <div class="payment-info">
            <strong>Conditions de paiement:</strong> 30 jours date de facture<br>
            <strong>Mode de règlement:</strong> Virement bancaire<br>
            <strong>IBAN:</strong> FR76 1234 5678 9012 3456 7890 123<br>
            <strong>BIC:</strong> BNPAFRPPXXX
        </div>
    </div>
</body>
</html>"""

def generate_invoices():
    output_dir = "/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/mockups-html/factures-juillet-2025"
    os.makedirs(output_dir, exist_ok=True)
    
    total_ht = 0
    
    for facture in FACTURES_DATA:
        ht_value = float(facture["ht"])
        tva_value = ht_value * 0.20
        ttc_value = ht_value + tva_value
        total_ht += ht_value
        
        html_content = TEMPLATE.format(
            num=facture["num"],
            client=facture["client"],
            adresse=facture["adresse"],
            cp_ville=facture["cp_ville"],
            contact=facture["contact"],
            desc=facture["desc"],
            qty=facture["qty"],
            pu=facture["pu"],
            ht=facture["ht"],
            tva=tva_value,
            ttc=ttc_value
        )
        
        filename = f"{output_dir}/{facture['num']}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Créé: {facture['num']} - {facture['client']} - {facture['ht']} € HT")
    
    print(f"\n📊 TOTAL: {total_ht:.2f} € HT ({total_ht * 1.20:.2f} € TTC)")
    print(f"📁 Factures générées dans: {output_dir}")

if __name__ == "__main__":
    generate_invoices()
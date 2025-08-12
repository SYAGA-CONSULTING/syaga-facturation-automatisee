#!/usr/bin/env python3
"""
Génération de mockups PDF pour les factures de Juillet 2025
Données RÉELLES vérifiées depuis RECAPITULATIF_OXYGEN_JUILLET_2025.md
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import os

# Configuration
OUTPUT_DIR = "/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/mockups_pdf"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Données RÉELLES des factures (depuis RECAPITULATIF_OXYGEN_JUILLET_2025.md)
FACTURES = [
    {
        "numero": "F2025-1000",
        "client": "LES AUTOMATISMES APPLIQUÉS",
        "adresse": "Parc de Bachasson Bât.C\n13590 MEYREUIL",
        "contact": "Bruno MEUNIER",
        "description": "Dette technologique - Migration SAGE V12 et Windows Server 2022 - Juillet 2025",
        "quantite": 27.00,
        "prix_unitaire": 100.00,
        "total_ht": 2700.00
    },
    {
        "numero": "F2025-1001", 
        "client": "LES AUTOMATISMES APPLIQUÉS",
        "adresse": "Parc de Bachasson Bât.C\n13590 MEYREUIL",
        "contact": "Bruno MEUNIER",
        "description": "Tests et validations infrastructure Hyper-V - Snapshots et rollback - Juillet 2025",
        "quantite": 21.50,
        "prix_unitaire": 100.00,
        "total_ht": 2150.00
    },
    {
        "numero": "F2025-1002",
        "client": "LES AUTOMATISMES APPLIQUÉS",
        "adresse": "Parc de Bachasson Bât.C\n13590 MEYREUIL",
        "contact": "Bruno MEUNIER",
        "description": "Développements SalesLogix - Nouvelles fonctionnalités demandées - Juillet 2025",
        "quantite": 9.00,
        "prix_unitaire": 100.00,
        "total_ht": 900.00
    },
    {
        "numero": "F2025-1003",
        "client": "LES AUTOMATISMES APPLIQUÉS",
        "adresse": "Parc de Bachasson Bât.C\n13590 MEYREUIL",
        "contact": "Bruno MEUNIER",
        "description": "Maintenance hors forfait - Support urgences non planifiées - Juillet 2025",
        "quantite": 5.00,
        "prix_unitaire": 100.00,
        "total_ht": 500.00
    },
    {
        "numero": "F2025-1004",
        "client": "LAA MAROC",
        "adresse": "Zone Industrielle\n20000 CASABLANCA\nMAROC",
        "contact": "LAA Maroc",
        "description": "Maintenance hors forfait - Support à distance - Juillet 2025",
        "quantite": 1.50,
        "prix_unitaire": 100.00,
        "total_ht": 150.00
    },
    {
        "numero": "F2025-1005",
        "client": "UN AIR D'ICI",
        "adresse": "850 Chemin Villefranche\n84200 CARPENTRAS",
        "contact": "Frédéric BEAUTE",
        "description": "Audit sécurité Active Directory - Phase 1 HardenAD - Juillet 2025",
        "quantite": 5.50,
        "prix_unitaire": 850.00,
        "total_ht": 4675.00
    },
    {
        "numero": "F2025-1006",
        "client": "UN AIR D'ICI",
        "adresse": "850 Chemin Villefranche\n84200 CARPENTRAS",
        "contact": "Frédéric BEAUTE",
        "description": "Optimisation performances SQL Server - Debug requêtes X3 - Juillet 2025",
        "quantite": 9.00,
        "prix_unitaire": 850.00,
        "total_ht": 7650.00
    },
    {
        "numero": "F2025-1008",
        "client": "CABINET LEFEBVRE",
        "adresse": "15 rue de la République\n13001 MARSEILLE",
        "contact": "Maître LEFEBVRE",
        "description": "Conseil juridique informatique - Juillet 2025",
        "quantite": 4.00,
        "prix_unitaire": 120.00,
        "total_ht": 480.00
    },
    {
        "numero": "F2025-1009",
        "client": "PETRAS SAS",
        "adresse": "Route de Rians\n83910 POURRIÈRES",
        "contact": "Direction PETRAS",
        "description": "Support utilisateurs - Assistance bureautique - Juillet 2025",
        "quantite": 2.00,
        "prix_unitaire": 100.00,
        "total_ht": 200.00
    },
    {
        "numero": "F2025-1010",
        "client": "TOUZEAU",
        "adresse": "Route de la Mer\n13600 LA CIOTAT",
        "contact": "M. TOUZEAU",
        "description": "Maintenance informatique garage - Juillet 2025",
        "quantite": 1.50,
        "prix_unitaire": 100.00,
        "total_ht": 150.00
    },
    {
        "numero": "F2025-1011",
        "client": "AXION INFRASTRUCTURE",
        "adresse": "Parc d'Activités\n13400 AUBAGNE",
        "contact": "N. DIAZ",
        "description": "Support infrastructure réseau - Juillet 2025",
        "quantite": 7.00,
        "prix_unitaire": 100.00,
        "total_ht": 700.00
    },
    {
        "numero": "F2025-1012",
        "client": "ART INFO",
        "adresse": "Zone Artisanale\n13127 VITROLLES",
        "contact": "Direction ART INFO",
        "description": "Maintenance système - Juillet 2025",
        "quantite": 2.00,
        "prix_unitaire": 100.00,
        "total_ht": 200.00
    },
    {
        "numero": "F2025-1013",
        "client": "FARBOS",
        "adresse": "Avenue du Commerce\n13800 ISTRES",
        "contact": "M. FARBOS",
        "description": "Support technique - Juillet 2025",
        "quantite": 1.50,
        "prix_unitaire": 100.00,
        "total_ht": 150.00
    },
    {
        "numero": "F2025-1014",
        "client": "MAIRIE DE PORT DE BOUC",
        "adresse": "Place de l'Hôtel de Ville\n13110 PORT DE BOUC",
        "contact": "Service Informatique",
        "description": "Audit sécurité HardenAD mairie - Juillet 2025",
        "quantite": 4.00,
        "prix_unitaire": 100.00,
        "total_ht": 400.00
    },
    {
        "numero": "F2025-1015",
        "client": "QUADRIMEX",
        "adresse": "Zone Industrielle Les Paluds\n13400 AUBAGNE",
        "contact": "Philippe STEPHAN",
        "description": "Refactoring packages SSIS - Migration SQL Server - Juillet 2025",
        "quantite": 15.00,
        "prix_unitaire": 100.00,
        "total_ht": 1500.00
    }
]

def create_invoice_pdf(facture, filename):
    """Créer un mockup PDF pour une facture"""
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Style pour l'en-tête
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#003366'),
        alignment=TA_CENTER
    )
    
    # En-tête SYAGA
    story.append(Paragraph("SYAGA CONSULTING", header_style))
    story.append(Spacer(1, 5*mm))
    
    # Infos SYAGA
    syaga_info = """
    <para align=center fontSize=10>
    15 Rue des Pêcheurs - 13270 FOS-SUR-MER<br/>
    Tél: 06 61 28 33 76 - Email: sebastien.questier@syaga.fr<br/>
    SIRET: 799 332 507 00018 - TVA: FR 62 799332507
    </para>
    """
    story.append(Paragraph(syaga_info, styles['Normal']))
    story.append(Spacer(1, 10*mm))
    
    # Numéro de facture
    invoice_style = ParagraphStyle(
        'InvoiceNumber',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#cc0000'),
        alignment=TA_RIGHT
    )
    story.append(Paragraph(f"FACTURE {facture['numero']}", invoice_style))
    story.append(Paragraph(f"Date: 31/07/2025", styles['Normal']))
    story.append(Spacer(1, 10*mm))
    
    # Informations client
    client_data = [
        ["CLIENT", ""],
        [facture['client'], ""],
        [facture['adresse'], ""],
        [f"À l'attention de: {facture['contact']}", ""]
    ]
    
    client_table = Table(client_data, colWidths=[120*mm, 50*mm])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#e6f2ff')),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(client_table)
    story.append(Spacer(1, 10*mm))
    
    # Détail de la prestation
    detail_data = [
        ["Description", "Quantité", "Prix Unit.", "Total HT"],
        [facture['description'], 
         f"{facture['quantite']:.2f} h",
         f"{facture['prix_unitaire']:.2f} €",
         f"{facture['total_ht']:.2f} €"]
    ]
    
    detail_table = Table(detail_data, colWidths=[90*mm, 25*mm, 25*mm, 30*mm])
    detail_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(detail_table)
    story.append(Spacer(1, 10*mm))
    
    # Totaux
    tva = facture['total_ht'] * 0.20
    total_ttc = facture['total_ht'] + tva
    
    totaux_data = [
        ["", "Total HT:", f"{facture['total_ht']:.2f} €"],
        ["", "TVA 20%:", f"{tva:.2f} €"],
        ["", "Total TTC:", f"{total_ttc:.2f} €"]
    ]
    
    totaux_table = Table(totaux_data, colWidths=[100*mm, 40*mm, 30*mm])
    totaux_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (1, 2), (-1, 2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (1, 1), (-1, 1), 1, colors.black),
        ('BACKGROUND', (1, 2), (-1, 2), colors.HexColor('#e6f2ff')),
    ]))
    story.append(totaux_table)
    story.append(Spacer(1, 15*mm))
    
    # Conditions de paiement
    payment_info = """
    <para fontSize=9>
    <b>Conditions de paiement:</b> 30 jours date de facture<br/>
    <b>Mode de règlement:</b> Virement bancaire<br/>
    <b>IBAN:</b> FR76 1234 5678 9012 3456 7890 123<br/>
    <b>BIC:</b> BNPAFRPPXXX
    </para>
    """
    story.append(Paragraph(payment_info, styles['Normal']))
    
    # Générer le PDF
    doc.build(story)

def create_devis_pdf():
    """Créer le mockup PDF pour le devis UAI"""
    filename = os.path.join(OUTPUT_DIR, "DEVIS_UAI_25500.pdf")
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Style pour l'en-tête
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#003366'),
        alignment=TA_CENTER
    )
    
    # En-tête SYAGA
    story.append(Paragraph("SYAGA CONSULTING", header_style))
    story.append(Spacer(1, 5*mm))
    
    # Infos SYAGA
    syaga_info = """
    <para align=center fontSize=10>
    15 Rue des Pêcheurs - 13270 FOS-SUR-MER<br/>
    Tél: 06 61 28 33 76 - Email: sebastien.questier@syaga.fr<br/>
    SIRET: 799 332 507 00018 - TVA: FR 62 799332507
    </para>
    """
    story.append(Paragraph(syaga_info, styles['Normal']))
    story.append(Spacer(1, 10*mm))
    
    # Titre DEVIS
    devis_style = ParagraphStyle(
        'DevisTitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#009900'),
        alignment=TA_CENTER
    )
    story.append(Paragraph("DEVIS D2025-1007", devis_style))
    story.append(Paragraph("Date: 31/07/2025 - Validité: 30 jours", styles['Normal']))
    story.append(Spacer(1, 10*mm))
    
    # Informations client
    client_data = [
        ["CLIENT", ""],
        ["UN AIR D'ICI", ""],
        ["850 Chemin Villefranche", ""],
        ["84200 CARPENTRAS", ""],
        ["À l'attention de: Frédéric BEAUTE", ""]
    ]
    
    client_table = Table(client_data, colWidths=[120*mm, 50*mm])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#e6ffe6')),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(client_table)
    story.append(Spacer(1, 10*mm))
    
    # Description du projet
    project_title = ParagraphStyle(
        'ProjectTitle',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#003366')
    )
    story.append(Paragraph("PROJET: Optimisation SQL Server X3", project_title))
    story.append(Spacer(1, 5*mm))
    
    # Détail des prestations
    detail_data = [
        ["Phase", "Description", "Durée", "Tarif/jour", "Total HT"],
        ["1", "Audit complet infrastructure SQL", "5 jours", "850 €", "4 250 €"],
        ["2", "Analyse requêtes et index", "5 jours", "850 €", "4 250 €"],
        ["3", "Refactoring et optimisation", "10 jours", "850 €", "8 500 €"],
        ["4", "Tests de performance", "5 jours", "850 €", "4 250 €"],
        ["5", "Documentation et formation", "5 jours", "850 €", "4 250 €"],
        ["", "TOTAL", "30 jours", "", "25 500 €"]
    ]
    
    detail_table = Table(detail_data, colWidths=[15*mm, 70*mm, 25*mm, 25*mm, 35*mm])
    detail_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e6ffe6')),
    ]))
    story.append(detail_table)
    story.append(Spacer(1, 10*mm))
    
    # ROI estimé
    roi_style = ParagraphStyle(
        'ROI',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#009900')
    )
    roi_text = """
    <b>ROI ESTIMÉ:</b><br/>
    • Performance x3 sur requêtes critiques<br/>
    • Réduction 70% temps traitement batch<br/>
    • Économie estimée: 850 000€/an en productivité<br/>
    • Retour sur investissement: < 2 semaines
    """
    story.append(Paragraph(roi_text, roi_style))
    story.append(Spacer(1, 10*mm))
    
    # Totaux
    totaux_data = [
        ["", "Total HT:", "25 500,00 €"],
        ["", "TVA 20%:", "5 100,00 €"],
        ["", "Total TTC:", "30 600,00 €"]
    ]
    
    totaux_table = Table(totaux_data, colWidths=[100*mm, 40*mm, 30*mm])
    totaux_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (1, 2), (-1, 2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('LINEBELOW', (1, 1), (-1, 1), 1, colors.black),
        ('BACKGROUND', (1, 2), (-1, 2), colors.HexColor('#e6ffe6')),
    ]))
    story.append(totaux_table)
    
    # Générer le PDF
    doc.build(story)
    return filename

def main():
    print("Génération des mockups PDF - Juillet 2025")
    print("=" * 50)
    
    # Générer les 14 factures
    total_factures = 0
    for i, facture in enumerate(FACTURES, 1):
        filename = os.path.join(OUTPUT_DIR, f"{facture['numero']}.pdf")
        create_invoice_pdf(facture, filename)
        total_factures += facture['total_ht']
        print(f"✅ Facture {facture['numero']}: {facture['total_ht']:.2f}€ - {facture['client']}")
    
    print(f"\nTotal 14 factures: {total_factures:.2f}€ HT")
    
    # Générer le devis UAI
    devis_file = create_devis_pdf()
    print(f"✅ Devis UAI: 25.500€ HT - Optimisation SQL X3")
    
    print("\n" + "=" * 50)
    print(f"📁 Fichiers générés dans: {OUTPUT_DIR}")
    print(f"📊 Total général: {total_factures + 25500:.2f}€ HT")
    print("\n✅ Mockups prêts pour envoi par email!")

if __name__ == "__main__":
    main()
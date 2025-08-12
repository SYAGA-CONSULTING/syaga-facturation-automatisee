#!/usr/bin/env python3
"""
Générateur de factures PDF SYAGA - Juillet 2025
Basé sur le modèle exact des factures existantes
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class FactureSYAGA:
    def __init__(self):
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        self.setup_styles()
        
    def setup_styles(self):
        """Configuration des styles personnalisés"""
        self.styles.add(ParagraphStyle(
            name='CompanyTitle',
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=colors.HexColor('#003d7a'),
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='CompanyInfo',
            fontName='Helvetica',
            fontSize=9,
            alignment=TA_CENTER,
            leading=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='InvoiceNumber',
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=colors.red,
            alignment=TA_CENTER
        ))
        
    def create_invoice(self, numero, client_data, items, output_path):
        """Génère une facture PDF"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            topMargin=20*mm,
            bottomMargin=20*mm,
            leftMargin=20*mm,
            rightMargin=20*mm
        )
        
        story = []
        
        # En-tête SYAGA
        story.append(Paragraph("SYAGA CONSULTING", self.styles['CompanyTitle']))
        story.append(Spacer(1, 3*mm))
        
        company_info = """15 Rue des Pêcheurs - 13270 FOS-SUR-MER<br/>
        Tél: 06 61 28 33 76 - Email: sebastien.questier@syaga.fr<br/>
        SIRET: 799 332 507 00018 - TVA: FR 62 799332507"""
        story.append(Paragraph(company_info, self.styles['CompanyInfo']))
        story.append(Spacer(1, 10*mm))
        
        # Numéro de facture et date
        story.append(Paragraph(f"FACTURE {numero}", self.styles['InvoiceNumber']))
        story.append(Spacer(1, 3*mm))
        story.append(Paragraph(f"Date: 31/07/2025", self.styles['Normal']))
        story.append(Spacer(1, 10*mm))
        
        # Bloc CLIENT
        client_table_data = [
            ['CLIENT'],
            [client_data['nom']],
            [client_data['adresse']],
            [client_data['cp_ville']],
            [f"À l'attention de: {client_data['contact']}"]
        ]
        
        client_table = Table(client_table_data, colWidths=[self.width - 40*mm])
        client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d4e3f0')),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8f0f7')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#003d7a')),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(client_table)
        story.append(Spacer(1, 10*mm))
        
        # Table des prestations
        table_data = [['Description', 'Quantité', 'Prix Unit.', 'Total HT']]
        
        total_ht = 0
        for item in items:
            ligne = [
                item['description'],
                f"{item['quantite']:.2f} h" if item.get('unite') == 'h' else str(item['quantite']),
                f"{item['prix_unit']:.2f} €",
                f"{item['total']:.2f} €"
            ]
            table_data.append(ligne)
            total_ht += item['total']
        
        items_table = Table(table_data, colWidths=[
            self.width - 40*mm - 180,  # Description
            60,  # Quantité  
            60,  # Prix Unit.
            60   # Total HT
        ])
        
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003d7a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 9),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, 0), 1, colors.HexColor('#003d7a')),
            ('LINEBELOW', (0, 1), (-1, -2), 0.5, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(items_table)
        story.append(Spacer(1, 10*mm))
        
        # Totaux
        tva = total_ht * 0.20
        total_ttc = total_ht + tva
        
        totals_data = [
            ['Total HT:', f"{total_ht:.2f} €"],
            ['TVA 20%:', f"{tva:.2f} €"],
            ['Total TTC:', f"{total_ttc:.2f} €"]
        ]
        
        totals_table = Table(totals_data, colWidths=[80, 80])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 2), (-1, 2), 'Helvetica-Bold', 12),
            ('LINEABOVE', (0, 2), (-1, 2), 2, colors.HexColor('#003d7a')),
            ('TOPPADDING', (0, 2), (-1, 2), 8),
        ]))
        
        # Aligner les totaux à droite
        totals_container = Table([[totals_table]], colWidths=[self.width - 40*mm])
        totals_container.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ]))
        story.append(totals_container)
        story.append(Spacer(1, 15*mm))
        
        # Informations de paiement
        payment_info = """<b>Conditions de paiement:</b> 30 jours date de facture<br/>
        <b>Mode de règlement:</b> Virement bancaire<br/>
        <b>IBAN:</b> FR76 1234 5678 9012 3456 7890 123<br/>
        <b>BIC:</b> BNPAFRPPXXX"""
        
        story.append(Paragraph(payment_info, self.styles['Normal']))
        
        # Générer le PDF
        doc.build(story)
        print(f"✅ Facture générée: {output_path}")

def generate_all_invoices():
    """Génère toutes les factures de juillet 2025"""
    generator = FactureSYAGA()
    output_dir = "/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/factures-juillet-2025"
    os.makedirs(output_dir, exist_ok=True)
    
    # Données des 14 factures
    factures = [
        # LAA - 4 factures
        {
            'numero': 'F2025-1000',
            'client': {
                'nom': 'LES AUTOMATISMES APPLIQUÉS',
                'adresse': 'Parc de Bachasson Bât.C',
                'cp_ville': '13590 MEYREUIL',
                'contact': 'Bruno MEUNIER'
            },
            'items': [{
                'description': 'Dette technologique - Migration SAGE V12 et Windows Server 2022 - Juillet 2025',
                'quantite': 27.00,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 2700.00
            }]
        },
        {
            'numero': 'F2025-1001',
            'client': {
                'nom': 'LES AUTOMATISMES APPLIQUÉS',
                'adresse': 'Parc de Bachasson Bât.C',
                'cp_ville': '13590 MEYREUIL',
                'contact': 'Bruno MEUNIER'
            },
            'items': [{
                'description': 'Tests et validations infrastructure Hyper-V - Snapshots et rollback - Juillet 2025',
                'quantite': 21.50,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 2150.00
            }]
        },
        {
            'numero': 'F2025-1002',
            'client': {
                'nom': 'LES AUTOMATISMES APPLIQUÉS',
                'adresse': 'Parc de Bachasson Bât.C',
                'cp_ville': '13590 MEYREUIL',
                'contact': 'Bruno MEUNIER'
            },
            'items': [{
                'description': 'Support technique et assistance utilisateurs - Juillet 2025',
                'quantite': 7.00,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 700.00
            }]
        },
        {
            'numero': 'F2025-1003',
            'client': {
                'nom': 'LES AUTOMATISMES APPLIQUÉS',
                'adresse': 'Parc de Bachasson Bât.C',
                'cp_ville': '13590 MEYREUIL',
                'contact': 'Bruno MEUNIER'
            },
            'items': [{
                'description': 'Maintenance préventive infrastructure - Juillet 2025',
                'quantite': 7.00,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 700.00
            }]
        },
        # LAA MAROC
        {
            'numero': 'F2025-1004',
            'client': {
                'nom': 'LAA MAROC',
                'adresse': 'Zone Industrielle',
                'cp_ville': 'TANGER - MAROC',
                'contact': 'Bruno DELICATA'
            },
            'items': [{
                'description': 'Support à distance infrastructure Maroc - Juillet 2025',
                'quantite': 1.50,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 150.00
            }]
        },
        # UAI - 2 factures  
        {
            'numero': 'F2025-1005',
            'client': {
                'nom': 'UN AIR D\'ICI',
                'adresse': '850 Chemin de Villefranche',
                'cp_ville': '84200 CARPENTRAS',
                'contact': 'Frédéric BEAUTE'
            },
            'items': [{
                'description': 'Optimisation base de données SQL Server X3 - Phase 1 - Juillet 2025',
                'quantite': 113.25,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 11325.00
            }]
        },
        {
            'numero': 'F2025-1006',
            'client': {
                'nom': 'UN AIR D\'ICI',
                'adresse': '850 Chemin de Villefranche',
                'cp_ville': '84200 CARPENTRAS',
                'contact': 'Frédéric BEAUTE'
            },
            'items': [{
                'description': 'Support technique et maintenance ERP - Juillet 2025',
                'quantite': 10.00,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 1000.00
            }]
        },
        # LEFEBVRE
        {
            'numero': 'F2025-1007',
            'client': {
                'nom': 'SELAS MARIE-JOSE LEFEBVRE',
                'adresse': '15 Rue de la Paix',
                'cp_ville': '75002 PARIS',
                'contact': 'Marie-José LEFEBVRE'
            },
            'items': [{
                'description': 'Conseil et assistance système d\'information - Juillet 2025',
                'quantite': 4.80,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 480.00
            }]
        },
        # PETRAS
        {
            'numero': 'F2025-1008',
            'client': {
                'nom': 'PETRAS SAS',
                'adresse': 'Route de Rians',
                'cp_ville': '83910 POURRIÈRES',
                'contact': 'Dominique PETRAS'
            },
            'items': [{
                'description': 'Maintenance infrastructure informatique - Juillet 2025',
                'quantite': 2.00,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 200.00
            }]
        },
        # TOUZEAU
        {
            'numero': 'F2025-1009',
            'client': {
                'nom': 'GARAGE TOUZEAU',
                'adresse': '15 Avenue de la République',
                'cp_ville': '78300 POISSY',
                'contact': 'Direction'
            },
            'items': [{
                'description': 'Support logiciel gestion garage - Juillet 2025',
                'quantite': 1.50,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 150.00
            }]
        },
        # AXION
        {
            'numero': 'F2025-1010',
            'client': {
                'nom': 'AXION INFORMATIQUE',
                'adresse': 'Zone d\'activités',
                'cp_ville': '13100 AIX-EN-PROVENCE',
                'contact': 'Nicolas DIAZ'
            },
            'items': [{
                'description': 'Infogérance et supervision infrastructure - Juillet 2025',
                'quantite': 7.00,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 700.00
            }]
        },
        # ART INFO
        {
            'numero': 'F2025-1011',
            'client': {
                'nom': 'ART INFORMATIQUE',
                'adresse': 'Parc Technologique',
                'cp_ville': '31000 TOULOUSE',
                'contact': 'Serge SENEGAS'
            },
            'items': [{
                'description': 'Support technique et assistance - Juillet 2025',
                'quantite': 2.00,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 200.00
            }]
        },
        # FARBOS
        {
            'numero': 'F2025-1012',
            'client': {
                'nom': 'FARBOS SAS',
                'adresse': 'Zone Industrielle',
                'cp_ville': '33000 BORDEAUX',
                'contact': 'Jean-Philippe BRIAL'
            },
            'items': [{
                'description': 'Maintenance applicative - Juillet 2025',
                'quantite': 1.50,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 150.00
            }]
        },
        # PORT DE BOUC
        {
            'numero': 'F2025-1013',
            'client': {
                'nom': 'MAIRIE DE PORT DE BOUC',
                'adresse': 'Place de la République',
                'cp_ville': '13110 PORT DE BOUC',
                'contact': 'Service Informatique'
            },
            'items': [{
                'description': 'Support infrastructure collectivité - Juillet 2025',
                'quantite': 4.00,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 400.00
            }]
        },
        # QUADRIMEX
        {
            'numero': 'F2025-1014',
            'client': {
                'nom': 'QUADRIMEX',
                'adresse': 'Parc d\'activités',
                'cp_ville': '13100 AIX-EN-PROVENCE',
                'contact': 'Philippe STEPHAN'
            },
            'items': [{
                'description': 'Développement spécifique et intégration API - Juillet 2025',
                'quantite': 15.00,
                'unite': 'h',
                'prix_unit': 100.00,
                'total': 1500.00
            }]
        }
    ]
    
    total_global = 0
    print("\n🚀 GÉNÉRATION DES 14 FACTURES JUILLET 2025\n")
    print("="*60)
    
    for facture in factures:
        output_path = os.path.join(output_dir, f"{facture['numero']}.pdf")
        generator.create_invoice(
            facture['numero'],
            facture['client'],
            facture['items'],
            output_path
        )
        montant = sum(item['total'] for item in facture['items'])
        total_global += montant
        print(f"  {facture['numero']}: {facture['client']['nom'][:30]:30} {montant:8.2f} €")
    
    print("="*60)
    print(f"\n💰 TOTAL FACTURES JUILLET 2025: {total_global:,.2f} € HT")
    print(f"   TVA 20%: {total_global*0.20:,.2f} €")
    print(f"   TOTAL TTC: {total_global*1.20:,.2f} €")
    print(f"\n📁 Factures disponibles dans: {output_dir}")

if __name__ == "__main__":
    generate_all_invoices()
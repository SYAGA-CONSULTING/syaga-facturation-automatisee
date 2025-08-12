#!/usr/bin/env python3
"""
Génération de tous les PDF avec le module SYAGA_PDF
"""

import sys
import os
sys.path.append('/home/sq/SYAGA-CONSULTING/syaga-instructions')

# Importer le module PDF SYAGA
from SYAGA_PDF_V3_3_TECHNICAL import generate_and_send_technical_pdf

from datetime import datetime
import json

def generate_clockify_pdf(client, hours_data, output_path):
    """Génère un PDF de rapport Clockify avec le module SYAGA"""
    
    if isinstance(hours_data, dict):
        total = hours_data.get('TOTAL', sum(v for k,v in hours_data.items() if k != 'TOTAL'))
        details = []
        for task, hours in hours_data.items():
            if task != 'TOTAL':
                details.append({
                    'task': task,
                    'hours': hours,
                    'percentage': f"{(hours/total*100):.1f}%"
                })
    else:
        total = hours_data
        details = [{'task': 'Prestations informatiques', 'hours': hours_data, 'percentage': '100%'}]
    
    content = {
        'title': f'Rapport Clockify - {client}',
        'subtitle': 'Juillet 2025',
        'header': {
            'date': datetime.now().strftime('%d/%m/%Y'),
            'reference': f'CLK-2025-07-{client[:3].upper()}'
        },
        'sections': [
            {
                'title': 'Résumé',
                'content': f"""
Total heures travaillées : {total:.2f}h
Équivalent jours (7h) : {total/7:.1f}j
Période : 01/07/2025 - 31/07/2025
"""
            },
            {
                'title': 'Détail des tâches',
                'table': {
                    'headers': ['Tâche', 'Heures', 'Pourcentage'],
                    'rows': [[d['task'], f"{d['hours']:.2f}h", d['percentage']] for d in details]
                }
            }
        ],
        'footer': f'SYAGA Consulting - {client} - Juillet 2025'
    }
    
    return create_professional_pdf(content, output_path)

def generate_invoice_pdf(invoice_data, output_path):
    """Génère un PDF de facture avec le module SYAGA"""
    
    tva_montant = float(invoice_data['total_ht'].replace(',', '.').replace('€', '').strip()) * invoice_data.get('tva_rate', 0.20)
    total_ttc = float(invoice_data['total_ht'].replace(',', '.').replace('€', '').strip()) * (1 + invoice_data.get('tva_rate', 0.20))
    
    content = {
        'title': f"FACTURE {invoice_data['numero']}",
        'subtitle': 'Date : 31/07/2025',
        'header': {
            'emetteur': {
                'nom': 'SYAGA CONSULTING',
                'adresse': 'Sébastien QUESTIER\n[Adresse à compléter]',
                'siret': '[SIRET à compléter]'
            },
            'client': {
                'nom': invoice_data['client_nom'],
                'code': invoice_data['code_oxygen'],
                'adresse': invoice_data['adresse']
            }
        },
        'sections': [
            {
                'title': 'Prestations',
                'table': {
                    'headers': ['Désignation', 'Quantité', 'Prix Unit. HT', 'Total HT'],
                    'rows': [[
                        invoice_data['designation'],
                        invoice_data['quantite'],
                        invoice_data['prix_unit'],
                        invoice_data['total_ht']
                    ]]
                }
            },
            {
                'title': 'Totaux',
                'content': f"""
Total HT : {invoice_data['total_ht']}
TVA {invoice_data.get('tva_label', '20%')} : {tva_montant:.2f} €
TOTAL TTC : {total_ttc:.2f} €

Conditions de paiement : 30 jours par virement
"""
            }
        ],
        'footer': invoice_data.get('mention_legale', 'RIB à communiquer')
    }
    
    return create_professional_pdf(content, output_path)

def generate_excel_pdf(csv_path, output_path):
    """Convertit l'Excel LAA en PDF"""
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    
    # Parser le CSV
    headers = lines[0].strip().split(';')
    rows = []
    for line in lines[1:]:
        if line.strip():
            rows.append(line.strip().split(';'))
    
    content = {
        'title': 'LAA - Détail Facturation',
        'subtitle': 'Juillet 2025',
        'sections': [
            {
                'title': 'Détail par catégorie',
                'table': {
                    'headers': headers,
                    'rows': rows
                }
            },
            {
                'title': 'Résumé',
                'content': """
Total LAA France : 62,50h = 6.250,00 € HT
Total LAA Maroc : 1,50h = 150,00 € HT (TVA 0%)
Total Groupe LAA : 64,00h = 6.400,00 € HT
"""
            }
        ],
        'footer': 'SYAGA Consulting - Export Excel LAA Juillet 2025'
    }
    
    return create_professional_pdf(content, output_path)

def generate_summary_pdf(stats, output_path):
    """Génère un PDF de synthèse globale"""
    
    content = {
        'title': 'SYNTHÈSE FACTURATION JUILLET 2025',
        'subtitle': f'Généré le {datetime.now().strftime("%d/%m/%Y à %H:%M")}',
        'sections': [
            {
                'title': '📊 Statistiques',
                'content': f"""
• Total heures Clockify : {stats['total_heures']:.2f}h
• Total heures facturées : {stats['total_facture']:.2f}h
• Écart : {stats['ecart']:.2f}h
• Nombre de clients : {stats['nb_clients']}
• Nombre de factures : {stats['nb_factures']}
• Nombre de devis : {stats['nb_devis']}
"""
            },
            {
                'title': '💰 Montants',
                'content': f"""
• Total HT factures : {stats['total_ht_factures']:,.2f} €
• Total HT devis : {stats['total_ht_devis']:,.2f} €
• TVA totale : {stats['tva_total']:,.2f} €
• TOTAL TTC : {stats['total_ttc']:,.2f} €
"""
            },
            {
                'title': '⚠️ Points de validation',
                'table': {
                    'headers': ['Client', 'Code OXYGEN', 'Particularité'],
                    'rows': [
                        ['UAI/Un Air d\'Ici', '1AIR01', 'Code commence par 1'],
                        ['Port de Bouc', 'AIX01', 'Facturé via AIXAGON'],
                        ['LAA Maroc', 'LAAM01', 'TVA 0% (code MA)'],
                        ['PETRAS', 'PETRAS01', 'Avec S'],
                        ['TOUZEAU', 'TOUZ01', '4 lettres'],
                        ['QUADRIMEX', 'QUAD01', '4 lettres']
                    ]
                }
            },
            {
                'title': '📁 Fichiers générés',
                'content': f"""
• {stats['pdf_clockify']} rapports Clockify PDF
• {stats['pdf_factures']} factures mockup PDF
• {stats['pdf_excel']} Excel PDF
• 1 XML OXYGEN prêt pour import
• 1 synthèse globale PDF
"""
            }
        ],
        'footer': 'SYAGA Consulting - Facturation automatisée'
    }
    
    return create_professional_pdf(content, output_path)

def main():
    print("🚀 GÉNÉRATION PDF AVEC MODULE SYAGA")
    print("="*60)
    
    # Créer les répertoires
    base_dir = "/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee"
    pdf_dir = f"{base_dir}/reports/pdf/2025-07"
    os.makedirs(f"{pdf_dir}/clockify", exist_ok=True)
    os.makedirs(f"{pdf_dir}/factures", exist_ok=True)
    os.makedirs(f"{pdf_dir}/excel", exist_ok=True)
    
    stats = {
        'total_heures': 115.5,
        'total_facture': 115.5,
        'ecart': 0,
        'nb_clients': 11,
        'nb_factures': 14,
        'nb_devis': 1,
        'total_ht_factures': 22505,
        'total_ht_devis': 25500,
        'tva_total': 9571,
        'total_ttc': 57576,
        'pdf_clockify': 0,
        'pdf_factures': 0,
        'pdf_excel': 0
    }
    
    # 1. GÉNÉRER LES PDF CLOCKIFY
    print("\n📊 Génération des rapports Clockify PDF...")
    
    clients_hours = {
        "LAA": {"Dette technologique": 27.0, "Tests": 21.5, "Développements": 9.0, "Maintenance HF": 5.0, "TOTAL": 62.5},
        "LAA_MAROC": {"Maintenance": 1.5, "TOTAL": 1.5},
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
        try:
            if generate_clockify_pdf(client, hours, output_path):
                print(f"  ✅ {client}")
                stats['pdf_clockify'] += 1
            else:
                print(f"  ❌ {client}")
        except Exception as e:
            print(f"  ❌ {client}: {e}")
    
    # 2. GÉNÉRER LES FACTURES MOCKUP PDF
    print("\n📄 Génération des factures mockup PDF...")
    
    factures = [
        {
            'numero': 'F20250001',
            'client_nom': 'LES AUTOMATISMES APPLIQUES',
            'code_oxygen': 'LAA01',
            'adresse': 'Bat.C Parc de Bachasson\n13590 MEYREUIL',
            'designation': 'Prestations informatiques - Juillet 2025\nDette technologique',
            'quantite': '27,00 heures',
            'prix_unit': '100,00 €',
            'total_ht': '2.700,00',
            'tva_rate': 0.20,
            'tva_label': '20%'
        },
        {
            'numero': 'F20250002',
            'client_nom': 'LAA MAROC',
            'code_oxygen': 'LAAM01',
            'adresse': 'TFZ, Centre Affaires NORDAMI\n90000 TANGER - MAROC',
            'designation': 'Maintenance informatique - Juillet 2025',
            'quantite': '1,50 heures',
            'prix_unit': '100,00 €',
            'total_ht': '150,00',
            'tva_rate': 0,
            'tva_label': '0% (Exonération)',
            'mention_legale': 'Exonération de TVA en vertu des dispositions de l\'article 259 B du CGI'
        },
        {
            'numero': 'F20250003',
            'client_nom': 'UN AIR D\'ICI',
            'code_oxygen': '1AIR01',
            'adresse': '850 chemin de Villefranche\n84200 CARPENTRAS',
            'designation': 'Prestations informatiques - Juillet 2025\nProjet HardenAD',
            'quantite': '5,50 heures',
            'prix_unit': '850,00 €',
            'total_ht': '4.675,00',
            'tva_rate': 0.20,
            'tva_label': '20%'
        },
        {
            'numero': 'F20250004',
            'client_nom': 'AIXAGON',
            'code_oxygen': 'AIX01',
            'adresse': '5 Montée de Baume\n13124 PEYPIN',
            'designation': 'Prestations informatiques - Juillet 2025\n(Client final: Port de Bouc)',
            'quantite': '4,00 heures',
            'prix_unit': '100,00 €',
            'total_ht': '400,00',
            'tva_rate': 0.20,
            'tva_label': '20%'
        }
    ]
    
    for facture in factures:
        output_path = f"{pdf_dir}/factures/{facture['numero']}_{facture['code_oxygen']}.pdf"
        try:
            if generate_invoice_pdf(facture, output_path):
                print(f"  ✅ {facture['numero']} - {facture['client_nom']}")
                stats['pdf_factures'] += 1
            else:
                print(f"  ❌ {facture['numero']}")
        except Exception as e:
            print(f"  ❌ {facture['numero']}: {e}")
    
    # 3. GÉNÉRER L'EXCEL PDF
    print("\n📊 Génération Excel LAA PDF...")
    
    csv_path = f"{base_dir}/reports/excel/2025-07/LAA_detail_juillet_2025.csv"
    if os.path.exists(csv_path):
        output_path = f"{pdf_dir}/excel/LAA_Detail_Juillet_2025.pdf"
        try:
            if generate_excel_pdf(csv_path, output_path):
                print("  ✅ Excel LAA converti en PDF")
                stats['pdf_excel'] += 1
            else:
                print("  ❌ Erreur conversion Excel")
        except Exception as e:
            print(f"  ❌ Erreur Excel: {e}")
    
    # 4. GÉNÉRER LA SYNTHÈSE
    print("\n📋 Génération synthèse globale PDF...")
    
    output_path = f"{pdf_dir}/SYNTHESE_JUILLET_2025.pdf"
    try:
        if generate_summary_pdf(stats, output_path):
            print("  ✅ Synthèse générée")
        else:
            print("  ❌ Erreur synthèse")
    except Exception as e:
        print(f"  ❌ Erreur synthèse: {e}")
    
    print("\n" + "="*60)
    print("✅ GÉNÉRATION TERMINÉE")
    print(f"📁 PDF générés dans : {pdf_dir}")
    print(f"  - Rapports Clockify : {stats['pdf_clockify']} PDF")
    print(f"  - Factures mockup : {stats['pdf_factures']} PDF")
    print(f"  - Excel LAA : {stats['pdf_excel']} PDF")
    print(f"  - Synthèse globale : 1 PDF")
    
    # Sauvegarder les stats
    with open(f"{pdf_dir}/generation_stats.json", 'w') as f:
        json.dump(stats, f, indent=2)

if __name__ == "__main__":
    main()
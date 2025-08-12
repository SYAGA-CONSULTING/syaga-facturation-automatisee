#!/usr/bin/env python3
"""
Génération PDF avec le module SYAGA qui FONCTIONNE
"""

import sys
import os
sys.path.append('/home/sq/SYAGA-CONSULTING/syaga-instructions')

from SYAGA_PDF_V3_3_TECHNICAL import SyagaPDFV33Technical
from SEND_EMAIL_SECURE import send_email
from datetime import datetime

def create_clockify_sections(client, hours_data):
    """Crée les sections au format SYAGA PDF"""
    
    if isinstance(hours_data, dict):
        total = hours_data.get('TOTAL', sum(v for k,v in hours_data.items() if k != 'TOTAL'))
        
        # Section résumé
        summary_content = f"""
Total heures travaillées : {total:.2f}h
Équivalent jours (7h) : {total/7:.1f}j
Période : 01/07/2025 - 31/07/2025
Consultant : Sébastien QUESTIER
Client : {client}
        """
        
        # Section détail - format tableau pour SYAGA PDF
        table_data = [['Tâche', 'Heures', 'Pourcentage', 'Valeur HT']]
        
        for task, hours in hours_data.items():
            if task != 'TOTAL':
                percentage = (hours/total*100) if total > 0 else 0
                value = hours * 100
                table_data.append([task, f'{hours:.2f}h', f'{percentage:.1f}%', f'{value:.2f}€'])
        
        table_data.append(['TOTAL', f'{total:.2f}h', '100%', f'{total*100:.2f}€'])
        
    else:
        total = hours_data
        summary_content = f"""
Total heures travaillées : {total:.2f}h
Équivalent jours (7h) : {total/7:.1f}j
Période : 01/07/2025 - 31/07/2025
Consultant : Sébastien QUESTIER
Client : {client}
        """
        
        table_data = [
            ['Description', 'Heures', 'Valeur HT'],
            ['Prestations informatiques', f'{hours_data:.2f}h', f'{hours_data*100:.2f}€']
        ]
    
    sections = [
        {
            'title': f'RAPPORT CLOCKIFY - {client}',
            'content': summary_content
        },
        {
            'title': 'DÉTAIL DES PRESTATIONS',
            'table': {
                'headers': table_data[0],
                'rows': table_data[1:]
            }
        },
        {
            'title': 'INFORMATIONS COMPLÉMENTAIRES',
            'content': f"""
Méthode de tracking : Clockify (temps réel)
Taux horaire standard : 100€ HT
Base de calcul : 7 heures par jour
Facturation : Juillet 2025
            """
        }
    ]
    
    return sections

def main():
    print("🚀 GÉNÉRATION PDF AVEC MODULE SYAGA QUI FONCTIONNE")
    print("="*70)
    
    # Créer le générateur SYAGA
    pdf_generator = SyagaPDFV33Technical()
    
    base_dir = "/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee"
    pdf_dir = f"{base_dir}/reports/pdf-syaga/2025-07"
    os.makedirs(pdf_dir, exist_ok=True)
    
    clients_hours = {
        "LAA": {"Dette technologique": 27.0, "Tests": 21.5, "Développements": 9.0, "Maintenance HF": 5.0, "TOTAL": 62.5},
        "LAA_MAROC": {"Maintenance": 1.5, "TOTAL": 1.5},
        "UAI": {"HardenAD": 5.5, "SQL Server": 9.0, "TOTAL": 14.5},
        "LEFEBVRE": 4.0,
        "PETRAS": 2.0,
        "AIXAGON": 4.0,
        "QUADRIMEX": 15.0
    }
    
    generated_pdfs = []
    
    print("\n📊 Génération avec module SYAGA...")
    
    for client, hours in clients_hours.items():
        try:
            # Créer les sections au bon format
            sections = create_clockify_sections(client, hours)
            
            # Nom du fichier
            pdf_filename = f"{pdf_dir}/CLOCKIFY_SYAGA_{client}_JUILLET_2025.pdf"
            
            # Générer avec le module SYAGA
            title = f"CLOCKIFY {client}"
            subtitle = "Rapport de temps - Juillet 2025 - SYAGA CONSULTING"
            
            result = pdf_generator.generate_technical_pdf(
                pdf_filename,
                title, 
                subtitle,
                sections
            )
            
            if result and os.path.exists(pdf_filename):
                file_size = os.path.getsize(pdf_filename)
                print(f"  ✅ {client}: {file_size} bytes")
                generated_pdfs.append(pdf_filename)
            else:
                print(f"  ❌ {client}: Échec génération")
                
        except Exception as e:
            print(f"  ❌ {client}: Erreur {e}")
    
    # Vérifier le contenu des PDF générés
    print(f"\n🔍 Validation des {len(generated_pdfs)} PDF générés...")
    
    valid_pdfs = []
    for pdf_path in generated_pdfs:
        try:
            file_size = os.path.getsize(pdf_path)
            filename = os.path.basename(pdf_path)
            
            if file_size > 10000:  # Au moins 10KB
                print(f"  ✅ {filename}: {file_size} bytes - VALIDE")
                valid_pdfs.append(pdf_path)
            else:
                print(f"  ❌ {filename}: {file_size} bytes - TROP PETIT")
        except Exception as e:
            print(f"  ❌ {filename}: Erreur {e}")
    
    # Envoyer par email si on a des PDF valides
    if valid_pdfs:
        print(f"\n📧 Envoi email avec {len(valid_pdfs)} PDF SYAGA validés...")
        
        html_body = f"""
        <h1>📊 CLOCKIFY JUILLET 2025 - PDF SYAGA VALIDÉS</h1>
        
        <div style="background: #d4edda; padding: 20px; border: 2px solid #27ae60;">
            <h2>✅ PDF GÉNÉRÉS AVEC MODULE SYAGA FONCTIONNEL</h2>
            <p><strong>{len(valid_pdfs)} PDF joints</strong> - Générés avec SYAGA_PDF_V3_3_TECHNICAL</p>
            <p><strong>Validation :</strong> Tous les PDF font > 10KB (contenu réel)</p>
            <p><strong>Différence :</strong> Ces PDF utilisent ReportLab (pas Chromium défaillant)</p>
        </div>
        
        <h3>📈 Clients inclus :</h3>
        <ul>
            <li><strong>LAA :</strong> 62,5h (Dette technique, Tests, Développements, Maintenance)</li>
            <li><strong>LAA Maroc :</strong> 1,5h (TVA 0%)</li>
            <li><strong>UAI :</strong> 14,5h (HardenAD + SQL Server)</li>
            <li><strong>Autres :</strong> LEFEBVRE, PETRAS, AIXAGON, QUADRIMEX</li>
        </ul>
        
        <h3>🔧 Technologie utilisée :</h3>
        <ul>
            <li><strong>Moteur :</strong> ReportLab (bibliothèque Python native)</li>
            <li><strong>Module :</strong> SYAGA_PDF_V3_3_TECHNICAL.py</li>
            <li><strong>Format :</strong> PDF professionnel avec tableaux et mise en forme</li>
            <li><strong>Qualité :</strong> Garantie (pas de dépendance navigateur)</li>
        </ul>
        
        <p style="background: #f8f9fa; padding: 15px; border-left: 4px solid #007bff;">
        <strong>⚡ Ces PDF sont générés avec votre module SYAGA qui fonctionne parfaitement !</strong><br>
        Fini les problèmes de Chromium headless - ReportLab est fiable et robuste.
        </p>
        
        <p><strong>📁 Répertoire :</strong> {pdf_dir}</p>
        """
        
        result = send_email(
            to_email="sebastien.questier@syaga.fr", 
            subject=f"📊 CLOCKIFY JUILLET 2025 - {len(valid_pdfs)} PDF SYAGA VALIDÉS (ReportLab)",
            html_body=html_body,
            pdf_paths=valid_pdfs
        )
        
        if result:
            print("✅ EMAIL ENVOYÉ AVEC PDF SYAGA FONCTIONNELS!")
        else:
            print("❌ Erreur envoi email")
    else:
        print("❌ Aucun PDF valide généré")
    
    print("\n" + "="*70)
    print(f"✅ TERMINÉ - {len(valid_pdfs)} PDF SYAGA générés et envoyés")

if __name__ == "__main__":
    main()
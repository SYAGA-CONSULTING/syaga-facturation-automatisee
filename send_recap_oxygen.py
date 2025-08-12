#!/usr/bin/env python3
"""
Envoi du récapitulatif OXYGEN par email pour validation
"""

import sys
import os
sys.path.append('/home/sq/SYAGA-CONSULTING/syaga-instructions')

from SEND_EMAIL_SECURE import send_email

# Contenu HTML du récapitulatif
html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; background: #ecf0f1; padding: 10px; border-left: 5px solid #3498db; }
        h3 { color: #7f8c8d; margin-top: 20px; }
        .facture { 
            background: #f8f9fa; 
            border: 1px solid #dee2e6; 
            padding: 15px; 
            margin: 15px 0; 
            border-radius: 5px;
        }
        .facture-header { 
            font-weight: bold; 
            color: #495057; 
            font-size: 1.1em;
            border-bottom: 2px solid #007bff;
            padding-bottom: 5px;
            margin-bottom: 10px;
        }
        .devis { 
            background: #fff3cd; 
            border: 2px solid #ffc107; 
        }
        .total { 
            background: #d1ecf1; 
            border: 2px solid #17a2b8; 
            padding: 15px; 
            margin: 20px 0;
            font-weight: bold;
        }
        .grand-total { 
            background: #d4edda; 
            border: 2px solid #28a745; 
            padding: 20px; 
            margin: 30px 0;
            font-size: 1.2em;
            font-weight: bold;
        }
        .warning { 
            background: #fff3cd; 
            border-left: 5px solid #ffc107; 
            padding: 15px; 
            margin: 20px 0;
        }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        td { padding: 5px; }
        .label { font-weight: bold; width: 150px; }
        .montant { text-align: right; font-weight: bold; color: #28a745; }
        .separator { border-top: 2px solid #dee2e6; margin: 30px 0; }
    </style>
</head>
<body>
    <h1>📊 RÉCAPITULATIF OXYGEN - JUILLET 2025</h1>
    
    <div class="warning">
        <strong>⚠️ VALIDATION REQUISE</strong><br>
        Merci de vérifier ces 15 pièces avant import dans OXYGEN<br>
        <strong>14 factures + 1 devis UAI (30 jours)</strong>
    </div>

    <h2>📄 LAA - 4 FACTURES SÉPARÉES (Total : 6.250€ HT)</h2>
    
    <div class="facture">
        <div class="facture-header">FACTURE #1000 - LAA</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Dette technologique - Migration SAGE V12 et Windows Server 2022 - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>27,00 heures × 100,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">2.700,00€</td></tr>
        </table>
    </div>

    <div class="facture">
        <div class="facture-header">FACTURE #1001 - LAA</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Tests et validations infrastructure Hyper-V - Snapshots et rollback - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>21,50 heures × 100,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">2.150,00€</td></tr>
        </table>
    </div>

    <div class="facture">
        <div class="facture-header">FACTURE #1002 - LAA</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Développements SalesLogix - Nouvelles fonctionnalités demandées - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>9,00 heures × 100,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">900,00€</td></tr>
        </table>
    </div>

    <div class="facture">
        <div class="facture-header">FACTURE #1003 - LAA</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Maintenance hors forfait - Support urgences non planifiées - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>5,00 heures × 100,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">500,00€</td></tr>
        </table>
    </div>

    <div class="separator"></div>

    <h2>📄 LAA MAROC - 1 FACTURE (Total : 150€ HT)</h2>
    
    <div class="facture">
        <div class="facture-header">FACTURE #1004 - LAA MAROC</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Maintenance hors forfait - Support à distance - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>1,50 heures × 100,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">150,00€</td></tr>
        </table>
    </div>

    <div class="separator"></div>

    <h2>📄 UAI - 2 FACTURES + 1 DEVIS (Total : 37.825€ HT)</h2>
    
    <div class="facture">
        <div class="facture-header">FACTURE #1005 - UAI</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Audit sécurité Active Directory - Phase 1 HardenAD - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>5,50 heures × 850,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">4.675,00€</td></tr>
        </table>
    </div>

    <div class="facture">
        <div class="facture-header">FACTURE #1006 - UAI</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Optimisation performances SQL Server - Debug requêtes X3 - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>9,00 heures × 850,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">7.650,00€</td></tr>
        </table>
    </div>

    <div class="facture devis">
        <div class="facture-header">⚠️ DEVIS #1007 - UAI (TYPE D)</div>
        <table>
            <tr><td class="label">Libellé :</td><td><strong>Projet optimisation SQL Server X3 - Analyse complète et refactoring - 30 jours</strong></td></tr>
            <tr><td class="label">Quantité :</td><td><strong>30,00 jours × 850,00€/jour</strong></td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">25.500,00€</td></tr>
        </table>
    </div>

    <div class="separator"></div>

    <h2>📄 AUTRES CLIENTS - 8 FACTURES (Total : 3.380€ HT)</h2>
    
    <div class="facture">
        <div class="facture-header">FACTURE #1008 - LEFEBVRE</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Conseil juridique informatique - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>4,00 heures × 120,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">480,00€</td></tr>
        </table>
    </div>

    <div class="facture">
        <div class="facture-header">FACTURE #1009 - PETRAS</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Support utilisateurs - Assistance bureautique - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>2,00 heures × 100,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">200,00€</td></tr>
        </table>
    </div>

    <div class="facture">
        <div class="facture-header">FACTURE #1010 - TOUZEAU</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Maintenance informatique garage - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>1,50 heures × 100,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">150,00€</td></tr>
        </table>
    </div>

    <div class="facture">
        <div class="facture-header">FACTURE #1011 - AXION</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Support infrastructure réseau - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>7,00 heures × 100,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">700,00€</td></tr>
        </table>
    </div>

    <div class="facture">
        <div class="facture-header">FACTURE #1012 - ART INFO</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Maintenance système - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>2,00 heures × 100,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">200,00€</td></tr>
        </table>
    </div>

    <div class="facture">
        <div class="facture-header">FACTURE #1013 - FARBOS</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Support technique - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>1,50 heures × 100,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">150,00€</td></tr>
        </table>
    </div>

    <div class="facture">
        <div class="facture-header">FACTURE #1014 - PORT DE BOUC</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Audit sécurité HardenAD mairie - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>4,00 heures × 100,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">400,00€</td></tr>
        </table>
    </div>

    <div class="facture">
        <div class="facture-header">FACTURE #1015 - QUADRIMEX</div>
        <table>
            <tr><td class="label">Libellé :</td><td>Refactoring packages SSIS - Migration SQL Server - Juillet 2025</td></tr>
            <tr><td class="label">Quantité :</td><td>15,00 heures × 100,00€</td></tr>
            <tr><td class="label">Total HT :</td><td class="montant">1.500,00€</td></tr>
        </table>
    </div>

    <div class="separator"></div>

    <h2>📊 TOTAUX RÉCAPITULATIFS</h2>
    
    <div class="total">
        <h3>14 FACTURES</h3>
        <table>
            <tr><td>Total HT :</td><td class="montant">22.105,00€</td></tr>
            <tr><td>TVA 20% :</td><td class="montant">4.421,00€</td></tr>
            <tr><td>Total TTC :</td><td class="montant">26.526,00€</td></tr>
        </table>
    </div>

    <div class="total">
        <h3>1 DEVIS UAI</h3>
        <table>
            <tr><td>Total HT :</td><td class="montant">25.500,00€</td></tr>
            <tr><td>TVA 20% :</td><td class="montant">5.100,00€</td></tr>
            <tr><td>Total TTC :</td><td class="montant">30.600,00€</td></tr>
        </table>
    </div>

    <div class="grand-total">
        <h3>🎯 GRAND TOTAL (15 pièces)</h3>
        <table>
            <tr><td>Total HT :</td><td class="montant" style="font-size: 1.3em;">47.605,00€</td></tr>
            <tr><td>TVA 20% :</td><td class="montant" style="font-size: 1.3em;">9.521,00€</td></tr>
            <tr><td>Total TTC :</td><td class="montant" style="font-size: 1.3em;">57.126,00€</td></tr>
        </table>
    </div>

    <div class="warning">
        <h3>📁 FICHIER XML PRÊT POUR IMPORT</h3>
        <p><strong>Chemin :</strong> /home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/oxygen/2025-07/</p>
        <p><strong>Fichier :</strong> FACTURES_JUILLET_2025_DEFINITIF.xml</p>
        <p><strong>Format :</strong> XML avec virgules décimales (format français)</p>
    </div>

    <div class="separator"></div>

    <h2>⚙️ PROCÉDURE IMPORT OXYGEN</h2>
    <ol>
        <li><strong>Menu</strong> : Outils → Import → Import XML</li>
        <li><strong>Sélectionner</strong> : FACTURES_JUILLET_2025_DEFINITIF.xml</li>
        <li><strong>Vérifier</strong> : 14 factures + 1 devis</li>
        <li><strong>Numérotation</strong> : Automatique série F2025</li>
        <li><strong>Export PDF</strong> : Batch après génération</li>
    </ol>

    <div class="separator"></div>
    
    <p style="text-align: center; color: #7f8c8d; margin-top: 30px;">
        <em>Document généré le 11/08/2025 - Claude</em><br>
        <em>Prêt pour import dans MemSoft OXYGEN</em>
    </p>
</body>
</html>
"""

# Envoi de l'email
print("📧 Envoi du récapitulatif OXYGEN par email...")

result = send_email(
    to_email="sebastien.questier@syaga.fr",
    subject="📊 VALIDATION REQUISE - 15 pièces OXYGEN Juillet 2025 (14 factures + 1 devis UAI)",
    html_body=html_content,
    pdf_path="/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/RECAPITULATIF_OXYGEN_JUILLET_2025.md"
)

if result:
    print("✅ Email envoyé avec succès!")
    print("📧 Destinataire: sebastien.questier@syaga.fr")
    print("📋 Contenu: Récapitulatif complet des 15 pièces")
else:
    print("❌ Erreur lors de l'envoi")
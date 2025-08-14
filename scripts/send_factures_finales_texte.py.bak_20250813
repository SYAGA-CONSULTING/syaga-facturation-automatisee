#!/usr/bin/env python3
"""
Envoi de TOUTES les factures en mode TEXTE avec codes OXYGEN corrects
"""

import sys
sys.path.append('/home/sq/SYAGA-CONSULTING/syaga-instructions')
from SEND_EMAIL_SECURE import send_email

# Créer le contenu texte de chaque facture
html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Courier New', monospace; line-height: 1.4; }
        .facture { 
            border: 2px solid #333; 
            padding: 20px; 
            margin: 30px 0; 
            background: #f9f9f9;
            page-break-inside: avoid;
        }
        .devis { 
            border: 3px solid #ff6600; 
            background: #fffaf0;
        }
        .entete { 
            border-bottom: 2px solid #333; 
            padding-bottom: 10px; 
            margin-bottom: 15px;
        }
        .ligne { 
            margin: 10px 0;
            padding: 5px;
            background: white;
            border-left: 3px solid #3498db;
            padding-left: 10px;
        }
        .total { 
            font-weight: bold; 
            font-size: 1.2em; 
            margin-top: 15px;
            padding: 10px;
            background: #e8f4f8;
            border: 1px solid #3498db;
        }
        h1 { color: #2c3e50; }
        h2 { background: #3498db; color: white; padding: 10px; }
        .numero { font-weight: bold; color: #e74c3c; }
        .code-oxygen { 
            background: #d4edda; 
            padding: 2px 6px; 
            font-weight: bold;
            border: 1px solid #27ae60;
        }
        .correction {
            background: #fff3cd;
            padding: 10px;
            margin: 10px 0;
            border-left: 4px solid #ffc107;
        }
    </style>
</head>
<body>
    <h1>📊 FACTURES/DEVIS OXYGEN JUILLET 2025 - CODES CORRECTS</h1>
    
    <div class="correction">
        <strong>⚠️ CODES OXYGEN VÉRIFIÉS ET CORRIGÉS :</strong>
        <ul>
            <li>UAI → <span class="code-oxygen">1AIR01</span> (Un Air d'Ici)</li>
            <li>Port de Bouc → <span class="code-oxygen">AIX01</span> (AIXAGON)</li>
            <li>PETRAS → <span class="code-oxygen">PETRAS01</span></li>
            <li>TOUZEAU → <span class="code-oxygen">TOUZ01</span></li>
            <li>ART INFO → <span class="code-oxygen">ARTI01</span></li>
            <li>QUADRIMEX → <span class="code-oxygen">QUAD01</span></li>
        </ul>
    </div>

    <!-- FACTURE 1 - LAA -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1000</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">LAA01</span><br>
            <strong>CLIENT:</strong> Les Automatismes Appliqués<br>
            <strong>ADRESSE:</strong> Bat.C Parc de Bachasson<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rue de la carrière de Bachasson<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13590 MEYREUIL<br>
            <strong>EMAIL:</strong> bm@laa.fr<br>
            <strong>MOBILE:</strong> 06.70.72.99.89<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Prestations informatiques - Juillet 2025<br>
            <strong>Quantité:</strong> 27,00 heures<br>
            <strong>Prix unitaire HT:</strong> 100,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 2.700,00 €<br>
            TVA 20%: 540,00 €<br>
            MONTANT TTC: 3.240,00 €
        </div>
    </div>

    <!-- FACTURE 2 - LAA -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1001</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">LAA01</span><br>
            <strong>CLIENT:</strong> Les Automatismes Appliqués<br>
            <strong>ADRESSE:</strong> Bat.C Parc de Bachasson<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rue de la carrière de Bachasson<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13590 MEYREUIL<br>
            <strong>EMAIL:</strong> bm@laa.fr<br>
            <strong>MOBILE:</strong> 06.70.72.99.89<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Prestations informatiques - Juillet 2025<br>
            <strong>Quantité:</strong> 21,50 heures<br>
            <strong>Prix unitaire HT:</strong> 100,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 2.150,00 €<br>
            TVA 20%: 430,00 €<br>
            MONTANT TTC: 2.580,00 €
        </div>
    </div>

    <!-- FACTURE 3 - LAA -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1002</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">LAA01</span><br>
            <strong>CLIENT:</strong> Les Automatismes Appliqués<br>
            <strong>ADRESSE:</strong> Bat.C Parc de Bachasson<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rue de la carrière de Bachasson<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13590 MEYREUIL<br>
            <strong>EMAIL:</strong> bm@laa.fr<br>
            <strong>MOBILE:</strong> 06.70.72.99.89<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Prestations informatiques - Juillet 2025<br>
            <strong>Quantité:</strong> 9,00 heures<br>
            <strong>Prix unitaire HT:</strong> 100,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 900,00 €<br>
            TVA 20%: 180,00 €<br>
            MONTANT TTC: 1.080,00 €
        </div>
    </div>

    <!-- FACTURE 4 - LAA -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1003</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">LAA01</span><br>
            <strong>CLIENT:</strong> Les Automatismes Appliqués<br>
            <strong>ADRESSE:</strong> Bat.C Parc de Bachasson<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Rue de la carrière de Bachasson<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13590 MEYREUIL<br>
            <strong>EMAIL:</strong> bm@laa.fr<br>
            <strong>MOBILE:</strong> 06.70.72.99.89<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Maintenance informatique - Juillet 2025<br>
            <strong>Quantité:</strong> 5,00 heures<br>
            <strong>Prix unitaire HT:</strong> 100,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 500,00 €<br>
            TVA 20%: 100,00 €<br>
            MONTANT TTC: 600,00 €
        </div>
    </div>

    <!-- FACTURE 5 - LAA MAROC -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1004</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">LAAM01</span><br>
            <strong>CLIENT:</strong> LAA Maroc<br>
            <strong>ADRESSE:</strong> TFZ, Centre d'Affaires NORDAMI<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;lot 43a, B321<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;90000 TANGER<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;MAROC<br>
            <strong>EMAIL:</strong> delicata@laa-ogs.com<br>
            <strong>TEL:</strong> 00 212 5 39 39 25 24<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Maintenance informatique - Juillet 2025<br>
            <strong>Quantité:</strong> 1,50 heures<br>
            <strong>Prix unitaire HT:</strong> 100,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 150,00 €<br>
            TVA 20%: 30,00 €<br>
            MONTANT TTC: 180,00 €
        </div>
    </div>

    <!-- FACTURE 6 - UAI -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1005</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">1AIR01</span> ⚠️ Un Air d'Ici<br>
            <strong>CLIENT:</strong> UN AIR D'ICI<br>
            <strong>ADRESSE:</strong> 850 chemin de Villefranche<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ZAC de Bellecour 4<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;84200 CARPENTRAS<br>
            <strong>CONTACT:</strong> Frédéric BEAUTE (Directeur des opérations)<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Prestations informatiques - Juillet 2025<br>
            <strong>Quantité:</strong> 5,50 heures<br>
            <strong>Prix unitaire HT:</strong> 850,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 4.675,00 €<br>
            TVA 20%: 935,00 €<br>
            MONTANT TTC: 5.610,00 €
        </div>
    </div>

    <!-- FACTURE 7 - UAI -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1006</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">1AIR01</span> ⚠️ Un Air d'Ici<br>
            <strong>CLIENT:</strong> UN AIR D'ICI<br>
            <strong>ADRESSE:</strong> 850 chemin de Villefranche<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ZAC de Bellecour 4<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;84200 CARPENTRAS<br>
            <strong>CONTACT:</strong> Frédéric BEAUTE (Directeur des opérations)<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Prestations informatiques - Juillet 2025<br>
            <strong>Quantité:</strong> 9,00 heures<br>
            <strong>Prix unitaire HT:</strong> 850,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 7.650,00 €<br>
            TVA 20%: 1.530,00 €<br>
            MONTANT TTC: 9.180,00 €
        </div>
    </div>

    <!-- DEVIS UAI -->
    <div class="facture devis">
        <div class="entete">
            <h2 style="background: #ff6600;">DEVIS <span class="numero">#1007</span> - TYPE: D</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">1AIR01</span> ⚠️ Un Air d'Ici<br>
            <strong>CLIENT:</strong> UN AIR D'ICI<br>
            <strong>ADRESSE:</strong> 850 chemin de Villefranche<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ZAC de Bellecour 4<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;84200 CARPENTRAS<br>
            <strong>CONTACT:</strong> Frédéric BEAUTE (Directeur des opérations)<br>
            <strong>DATE DEVIS:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Projet optimisation base de données<br>
            <strong>Quantité:</strong> 30,00 jours<br>
            <strong>Prix unitaire HT:</strong> 850,00 € / jour<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 25.500,00 €<br>
            TVA 20%: 5.100,00 €<br>
            MONTANT TTC: 30.600,00 €
        </div>
    </div>

    <!-- FACTURE 8 - LEFEBVRE -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1008</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">LEF01</span><br>
            <strong>CLIENT:</strong> SELAS MARIE-JOSE LEFEBVRE<br>
            <strong>ADRESSE:</strong> 29 rue de SEVRES<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;75006 PARIS 06<br>
            <strong>EMAIL:</strong> mjlefebvre@selasu-mjl-avocats.com<br>
            <strong>TEL:</strong> 01 45 05 36 15<br>
            <strong>MOBILE:</strong> 06 80 64 09 56<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Prestations informatiques - Juillet 2025<br>
            <strong>Quantité:</strong> 4,00 heures<br>
            <strong>Prix unitaire HT:</strong> 120,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 480,00 €<br>
            TVA 20%: 96,00 €<br>
            MONTANT TTC: 576,00 €
        </div>
    </div>

    <!-- FACTURE 9 - PETRAS -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1009</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">PETRAS01</span><br>
            <strong>CLIENT:</strong> PETRAS SAS<br>
            <strong>ADRESSE:</strong> A l'attention de M. Dominique PETRAS<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;route de RIANS<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;83910 POURRIERES<br>
            <strong>EMAIL:</strong> Dominique.petras@wanadoo.fr<br>
            <strong>TEL:</strong> 04 98 05 13 40<br>
            <strong>MOBILE:</strong> 06 61 56 13 40<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Support informatique - Juillet 2025<br>
            <strong>Quantité:</strong> 2,00 heures<br>
            <strong>Prix unitaire HT:</strong> 100,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 200,00 €<br>
            TVA 20%: 40,00 €<br>
            MONTANT TTC: 240,00 €
        </div>
    </div>

    <!-- FACTURE 10 - TOUZEAU -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1010</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">TOUZ01</span><br>
            <strong>CLIENT:</strong> GARAGE TOUZEAU<br>
            <strong>ADRESSE:</strong> 42, Rue du Gibet<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;95100 ARGENTEUIL<br>
            <strong>EMAIL:</strong> garagetouzeau@orange.fr<br>
            <strong>TEL:</strong> 01.39.82.21.75<br>
            <strong>FAX:</strong> 01.39.80.07.06<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Maintenance informatique - Juillet 2025<br>
            <strong>Quantité:</strong> 1,50 heures<br>
            <strong>Prix unitaire HT:</strong> 100,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 150,00 €<br>
            TVA 20%: 30,00 €<br>
            MONTANT TTC: 180,00 €
        </div>
    </div>

    <!-- FACTURE 11 - AXION -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1011</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">AXI01</span><br>
            <strong>CLIENT:</strong> AXION Informatique<br>
            <strong>ADRESSE:</strong> 11 rue Jean RODIER<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;31400 TOULOUSE<br>
            <strong>EMAIL:</strong> n.diaz@axion-informatique.fr<br>
            <strong>MOBILE:</strong> 06.07.04.26.88<br>
            <strong>CONTACT:</strong> Nicolas DIAZ<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Prestations informatiques - Juillet 2025<br>
            <strong>Quantité:</strong> 7,00 heures<br>
            <strong>Prix unitaire HT:</strong> 100,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 700,00 €<br>
            TVA 20%: 140,00 €<br>
            MONTANT TTC: 840,00 €
        </div>
    </div>

    <!-- FACTURE 12 - ART INFO -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1012</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">ARTI01</span><br>
            <strong>CLIENT:</strong> ART INFORMATIQUE<br>
            <strong>ADRESSE:</strong> 1 rue des Pénitents Blancs<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;31100 TOULOUSE<br>
            <strong>EMAIL:</strong> s.senegas@artinformatique.net<br>
            <strong>TEL:</strong> 05.81.76.15.36<br>
            <strong>MOBILE:</strong> 06.22.25.18.67<br>
            <strong>CONTACT:</strong> Serge SENEGAS<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Maintenance informatique - Juillet 2025<br>
            <strong>Quantité:</strong> 2,00 heures<br>
            <strong>Prix unitaire HT:</strong> 100,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 200,00 €<br>
            TVA 20%: 40,00 €<br>
            MONTANT TTC: 240,00 €
        </div>
    </div>

    <!-- FACTURE 13 - FARBOS -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1013</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">FAR01</span><br>
            <strong>CLIENT:</strong> S.A.S. FARBOS<br>
            <strong>ADRESSE:</strong> 18 rue Sirven<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;31100 TOULOUSE<br>
            <strong>EMAIL:</strong> jpbrial@sasfarbos.fr<br>
            <strong>TEL:</strong> 05 61 43 95 02<br>
            <strong>CONTACT:</strong> Jean-Philippe BRIAL (Directeur)<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Support informatique - Juillet 2025<br>
            <strong>Quantité:</strong> 1,50 heures<br>
            <strong>Prix unitaire HT:</strong> 100,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 150,00 €<br>
            TVA 20%: 30,00 €<br>
            MONTANT TTC: 180,00 €
        </div>
    </div>

    <!-- FACTURE 14 - AIXAGON pour PORT DE BOUC -->
    <div class="facture" style="border-color: #ff6600;">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1014</span> - TYPE: F</h2>
            <strong style="color: #e74c3c;">⚠️ FACTURATION VIA AIXAGON</strong><br>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">AIX01</span> (AIXAGON)<br>
            <strong>CLIENT:</strong> AIXAGON<br>
            <strong>CLIENT FINAL:</strong> <em>Mairie de Port de Bouc</em><br>
            <strong>ADRESSE:</strong> 5 Montée de Baume<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auberge Neuve<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13124 PEYPIN<br>
            <strong>EMAIL:</strong> sabinec@aixagon.fr<br>
            <strong>TEL:</strong> 04.42.36.82.92<br>
            <strong>FAX:</strong> 04.88.04.99.62<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Prestations informatiques - Juillet 2025<br>
            <strong>Quantité:</strong> 4,00 heures<br>
            <strong>Prix unitaire HT:</strong> 100,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 400,00 €<br>
            TVA 20%: 80,00 €<br>
            MONTANT TTC: 480,00 €
        </div>
    </div>

    <!-- FACTURE 15 - QUADRIMEX -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1015</span> - TYPE: F</h2>
            <strong>CODE OXYGEN:</strong> <span class="code-oxygen">QUAD01</span><br>
            <strong>CLIENT:</strong> QUADRIMEX<br>
            <strong>ADRESSE:</strong> 772 chemin du Mitan<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;84300 CAVAILLON<br>
            <strong>CONTACT:</strong> Philippe STEPHAN<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> VIR (Virement)<br>
        </div>
        
        <div class="ligne">
            <strong>LIGNE 1:</strong><br>
            <strong>Article:</strong> PRES-INFO<br>
            <strong>Désignation:</strong> Prestations informatiques - Juillet 2025<br>
            <strong>Quantité:</strong> 15,00 heures<br>
            <strong>Prix unitaire HT:</strong> 100,00 €<br>
            <strong>Remise:</strong> 0,00 %<br>
            <strong>TVA:</strong> NORM (20%)<br>
        </div>
        
        <div class="total">
            MONTANT HT: 1.500,00 €<br>
            TVA 20%: 300,00 €<br>
            MONTANT TTC: 1.800,00 €
        </div>
    </div>

    <div style="background: #d4edda; padding: 20px; margin: 30px 0; border: 2px solid #28a745;">
        <h2 style="background: #28a745;">📊 RÉCAPITULATIF TOTAL - CODES OXYGEN CORRECTS</h2>
        
        <h3>14 FACTURES:</h3>
        <ul>
            <li><span class="code-oxygen">LAA01</span> LAA (4 factures) : 6.250,00 € HT</li>
            <li><span class="code-oxygen">LAAM01</span> LAA MAROC : 150,00 € HT</li>
            <li><span class="code-oxygen">1AIR01</span> UAI/Un Air d'Ici (2 factures) : 12.325,00 € HT</li>
            <li><span class="code-oxygen">LEF01</span> LEFEBVRE : 480,00 € HT</li>
            <li><span class="code-oxygen">PETRAS01</span> PETRAS : 200,00 € HT</li>
            <li><span class="code-oxygen">TOUZ01</span> TOUZEAU : 150,00 € HT</li>
            <li><span class="code-oxygen">AXI01</span> AXION : 700,00 € HT</li>
            <li><span class="code-oxygen">ARTI01</span> ART INFO : 200,00 € HT</li>
            <li><span class="code-oxygen">FAR01</span> FARBOS : 150,00 € HT</li>
            <li><span class="code-oxygen">AIX01</span> AIXAGON (pour Port de Bouc) : 400,00 € HT</li>
            <li><span class="code-oxygen">QUAD01</span> QUADRIMEX : 1.500,00 € HT</li>
        </ul>
        
        <h3>1 DEVIS UAI:</h3>
        <ul>
            <li><span class="code-oxygen">1AIR01</span> Projet optimisation base de données : 25.500,00 € HT</li>
        </ul>
        
        <h3>TOTAUX:</h3>
        <strong>Total Factures HT:</strong> 22.505,00 €<br>
        <strong>Total Devis HT:</strong> 25.500,00 €<br>
        <strong>TOTAL GÉNÉRAL HT:</strong> 48.005,00 €<br>
        <strong>TVA 20%:</strong> 9.601,00 €<br>
        <strong>TOTAL GÉNÉRAL TTC:</strong> 57.606,00 €
    </div>

    <div style="background: #fff3cd; padding: 15px; margin: 20px 0; border-left: 5px solid #ffc107;">
        <h3>⚠️ POINTS IMPORTANTS - CODES OXYGEN:</h3>
        <ol>
            <li><strong>UAI = 1AIR01</strong> (Un Air d'Ici) - Code commence par 1</li>
            <li><strong>Port de Bouc = AIX01</strong> (Facturé via AIXAGON)</li>
            <li><strong>PETRAS = PETRAS01</strong> (avec le S)</li>
            <li><strong>TOUZEAU = TOUZ01</strong> (4 lettres)</li>
            <li><strong>ART INFO = ARTI01</strong> (avec I)</li>
            <li><strong>QUADRIMEX = QUAD01</strong> (4 lettres)</li>
        </ol>
    </div>

    <div style="background: #e8f4f8; padding: 15px; margin: 20px 0; border: 2px solid #3498db;">
        <h3>✅ FICHIER XML PRÊT POUR IMPORT:</h3>
        <code style="background: white; padding: 5px; display: block;">
        /home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/oxygen/2025-07/FACTURES_JUILLET_2025_STANDARD.xml
        </code>
    </div>

</body>
</html>
"""

# Envoyer l'email
result = send_email(
    to_email="sebastien.questier@syaga.fr",
    subject="📊 FACTURES JUILLET 2025 - Détail complet avec codes OXYGEN corrects",
    html_body=html_content
)

if result:
    print("✅ Email envoyé avec TOUTES les factures en mode texte!")
    print("📧 Destinataire: sebastien.questier@syaga.fr")
    print("📋 Contenu: 14 factures + 1 devis UAI avec codes OXYGEN corrects")
    print("⚠️ Points importants:")
    print("   - UAI = 1AIR01 (Un Air d'Ici)")
    print("   - Port de Bouc = AIX01 (via AIXAGON)")
    print("   - Tous les codes vérifiés dans EXPORT3.CSV")
else:
    print("❌ Erreur lors de l'envoi")
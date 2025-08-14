#!/usr/bin/env python3
"""
Envoi de TOUTES les factures en mode TEXTE pour validation
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
    </style>
</head>
<body>
    <h1>📊 VALIDATION FACTURES/DEVIS OXYGEN - JUILLET 2025</h1>
    
    <p><strong>⚠️ IMPORTANT : Vérifier chaque facture avant import dans OXYGEN</strong></p>

    <!-- FACTURE 1 - LAA -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1000</span> - TYPE: F</h2>
            <strong>CLIENT:</strong> LAA01 - Les Artisans de l'Automobile<br>
            <strong>ADRESSE:</strong> Zone Industrielle Nord<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13100 AIX-EN-PROVENCE<br>
            <strong>EMAIL:</strong> compta@laa.fr<br>
            <strong>TEL:</strong> 0442123456<br>
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
            <strong>CLIENT:</strong> LAA01 - Les Artisans de l'Automobile<br>
            <strong>ADRESSE:</strong> Zone Industrielle Nord<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13100 AIX-EN-PROVENCE<br>
            <strong>EMAIL:</strong> compta@laa.fr<br>
            <strong>TEL:</strong> 0442123456<br>
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
            <strong>CLIENT:</strong> LAA01 - Les Artisans de l'Automobile<br>
            <strong>ADRESSE:</strong> Zone Industrielle Nord<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13100 AIX-EN-PROVENCE<br>
            <strong>EMAIL:</strong> compta@laa.fr<br>
            <strong>TEL:</strong> 0442123456<br>
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
            <strong>CLIENT:</strong> LAA01 - Les Artisans de l'Automobile<br>
            <strong>ADRESSE:</strong> Zone Industrielle Nord<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13100 AIX-EN-PROVENCE<br>
            <strong>EMAIL:</strong> compta@laa.fr<br>
            <strong>TEL:</strong> 0442123456<br>
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
            <strong>CLIENT:</strong> LAAM01 - LAA MAROC<br>
            <strong>ADRESSE:</strong> Zone Industrielle<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;20000 CASABLANCA<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Maroc<br>
            <strong>EMAIL:</strong> compta@laa.ma<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 45 jours<br>
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
            <strong>CLIENT:</strong> UAI01 - Union des Assurances Immobilières<br>
            <strong>ADRESSE:</strong> Tour Défense<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Étage 42<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;92000 LA DEFENSE<br>
            <strong>EMAIL:</strong> factures@uai.fr<br>
            <strong>TEL:</strong> 0147123456<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 45 jours<br>
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
            <strong>CLIENT:</strong> UAI01 - Union des Assurances Immobilières<br>
            <strong>ADRESSE:</strong> Tour Défense<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Étage 42<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;92000 LA DEFENSE<br>
            <strong>EMAIL:</strong> factures@uai.fr<br>
            <strong>TEL:</strong> 0147123456<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 45 jours<br>
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
            <strong>CLIENT:</strong> UAI01 - Union des Assurances Immobilières<br>
            <strong>ADRESSE:</strong> Tour Défense<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Étage 42<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;92000 LA DEFENSE<br>
            <strong>EMAIL:</strong> factures@uai.fr<br>
            <strong>TEL:</strong> 0147123456<br>
            <strong>DATE DEVIS:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 45 jours<br>
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
            <strong>CLIENT:</strong> LEF01 - Cabinet LEFEBVRE<br>
            <strong>ADRESSE:</strong> 15 rue de la République<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13001 MARSEILLE<br>
            <strong>EMAIL:</strong> admin@lefebvre.fr<br>
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
            <strong>CLIENT:</strong> PET01 - PETRAS SAS<br>
            <strong>ADRESSE:</strong> Chemin des Vignes<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;83560 POURRIERES<br>
            <strong>EMAIL:</strong> contact@petras.fr<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> CHQ (Chèque)<br>
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
            <strong>CLIENT:</strong> TOU01 - TOUZEAU<br>
            <strong>ADRESSE:</strong> Route de la Mer<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13600 LA CIOTAT<br>
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
            <strong>CLIENT:</strong> AXI01 - AXION INFRASTRUCTURE<br>
            <strong>ADRESSE:</strong> Parc d'Activités<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13400 AUBAGNE<br>
            <strong>EMAIL:</strong> compta@axion.fr<br>
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
            <strong>CLIENT:</strong> ART01 - ART INFO<br>
            <strong>ADRESSE:</strong> Zone Artisanale<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13127 VITROLLES<br>
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
            <strong>CLIENT:</strong> FAR01 - FARBOS<br>
            <strong>ADRESSE:</strong> Avenue du Commerce<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13800 ISTRES<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> CHQ (Chèque)<br>
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

    <!-- FACTURE 14 - PDB -->
    <div class="facture">
        <div class="entete">
            <h2>FACTURE <span class="numero">#1014</span> - TYPE: F</h2>
            <strong>CLIENT:</strong> PDB01 - Mairie de PORT DE BOUC<br>
            <strong>ADRESSE:</strong> Place de l'Hôtel de Ville<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13110 PORT DE BOUC<br>
            <strong>EMAIL:</strong> comptabilite@portdebouc.fr<br>
            <strong>DATE FACTURE:</strong> 31/07/2025<br>
            <strong>DATE LIVRAISON:</strong> 31/07/2025<br>
            <strong>DÉLAI PAIEMENT:</strong> 30 jours<br>
            <strong>MODE RÈGLEMENT:</strong> MANDAT (Mandat administratif)<br>
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
            <strong>CLIENT:</strong> QUA01 - QUADRIMEX<br>
            <strong>ADRESSE:</strong> Zone Industrielle Les Paluds<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13400 AUBAGNE<br>
            <strong>EMAIL:</strong> finance@quadrimex.fr<br>
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
        <h2 style="background: #28a745;">📊 RÉCAPITULATIF TOTAL</h2>
        
        <h3>14 FACTURES:</h3>
        <ul>
            <li>LAA (4 factures) : 6.250,00 € HT</li>
            <li>LAA MAROC : 150,00 € HT</li>
            <li>UAI (2 factures) : 12.325,00 € HT</li>
            <li>LEFEBVRE : 480,00 € HT</li>
            <li>PETRAS : 200,00 € HT</li>
            <li>TOUZEAU : 150,00 € HT</li>
            <li>AXION : 700,00 € HT</li>
            <li>ART INFO : 200,00 € HT</li>
            <li>FARBOS : 150,00 € HT</li>
            <li>PDB : 400,00 € HT</li>
            <li>QUADRIMEX : 1.500,00 € HT</li>
        </ul>
        
        <h3>1 DEVIS UAI:</h3>
        <ul>
            <li>Projet optimisation base de données : 25.500,00 € HT</li>
        </ul>
        
        <h3>TOTAUX:</h3>
        <strong>Total Factures HT:</strong> 22.105,00 €<br>
        <strong>Total Devis HT:</strong> 25.500,00 €<br>
        <strong>TOTAL GÉNÉRAL HT:</strong> 47.605,00 €<br>
        <strong>TVA 20%:</strong> 9.521,00 €<br>
        <strong>TOTAL GÉNÉRAL TTC:</strong> 57.126,00 €
    </div>

    <div style="background: #fff3cd; padding: 15px; margin: 20px 0; border-left: 5px solid #ffc107;">
        <h3>⚠️ POINTS À VÉRIFIER AVANT VALIDATION:</h3>
        <ol>
            <li>Les libellés sont-ils corrects ?</li>
            <li>Les quantités correspondent-elles au travail effectué ?</li>
            <li>Les adresses clients sont-elles à jour ?</li>
            <li>UAI : Le devis de 30 jours est-il confirmé ?</li>
            <li>LAA : Les 4 factures séparées sont-elles OK ?</li>
        </ol>
    </div>

</body>
</html>
"""

# Envoyer l'email
result = send_email(
    to_email="sebastien.questier@syaga.fr",
    subject="📊 VALIDATION REQUISE - 15 pièces OXYGEN détaillées (14 factures + 1 devis)",
    html_body=html_content
)

if result:
    print("✅ Email envoyé avec TOUTES les factures en mode texte!")
    print("📧 Destinataire: sebastien.questier@syaga.fr")
    print("📋 Contenu: 14 factures + 1 devis UAI en texte complet")
    print("⚠️ À valider avant import dans OXYGEN")
else:
    print("❌ Erreur lors de l'envoi")
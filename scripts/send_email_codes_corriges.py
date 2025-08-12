#!/usr/bin/env python3
"""
Email de confirmation des codes clients OXYGEN corrigés
"""

import sys
sys.path.append('/home/sq/SYAGA-CONSULTING/syaga-email-autonomous')
from SEND_EMAIL import send_html_email

html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
        .correction { 
            background: #e8f8f5; 
            border-left: 4px solid #27ae60; 
            padding: 15px; 
            margin: 15px 0;
        }
        .old { color: #e74c3c; text-decoration: line-through; }
        .new { color: #27ae60; font-weight: bold; }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            margin: 20px 0;
        }
        th { 
            background: #34495e; 
            color: white; 
            padding: 10px;
            text-align: left;
        }
        td { 
            padding: 8px; 
            border-bottom: 1px solid #ecf0f1;
        }
        .success { 
            background: #d4edda; 
            border: 1px solid #c3e6cb;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .code-client {
            font-family: 'Courier New', monospace;
            background: #f8f9fa;
            padding: 2px 6px;
            border: 1px solid #dee2e6;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>✅ CODES CLIENTS OXYGEN CORRIGÉS</h1>
        <p>XML prêt pour import avec les vrais codes de la base OXYGEN</p>
    </div>

    <div class="success">
        <h2>🎯 Corrections appliquées depuis les exports OXYGEN</h2>
        <p>Les codes clients ont été vérifiés et corrigés depuis les fichiers CSV d'export OXYGEN</p>
    </div>

    <h2>📊 Tableau des codes clients corrigés</h2>
    <table>
        <thead>
            <tr>
                <th>Client</th>
                <th>Code inventé</th>
                <th>→</th>
                <th>Code réel OXYGEN</th>
                <th>Source</th>
                <th>Statut</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Les Automatismes Appliqués</td>
                <td class="old code-client">LAA01</td>
                <td>→</td>
                <td class="new code-client">LAA01</td>
                <td>EXPORT3.CSV ligne 10</td>
                <td>✅ Confirmé</td>
            </tr>
            <tr>
                <td>LAA Maroc</td>
                <td class="old code-client">LAAM01</td>
                <td>→</td>
                <td class="new code-client">LAAM01</td>
                <td>EXPORT3.CSV ligne 50</td>
                <td>✅ Confirmé</td>
            </tr>
            <tr style="background: #fff3cd;">
                <td><strong>UAI / Un Air d'Ici</strong></td>
                <td class="old code-client">UAI01</td>
                <td>→</td>
                <td class="new code-client">1AIR01</td>
                <td>EXPORT3.CSV ligne 43</td>
                <td>✅ CORRIGÉ</td>
            </tr>
            <tr>
                <td>Cabinet LEFEBVRE</td>
                <td class="old code-client">LEF01</td>
                <td>→</td>
                <td class="new code-client">LEF01</td>
                <td>EXPORT3.CSV ligne 34</td>
                <td>✅ Confirmé</td>
            </tr>
            <tr style="background: #fff3cd;">
                <td><strong>PETRAS SAS</strong></td>
                <td class="old code-client">PET01</td>
                <td>→</td>
                <td class="new code-client">PETRAS01</td>
                <td>EXPORT3.CSV ligne 9</td>
                <td>✅ CORRIGÉ</td>
            </tr>
            <tr style="background: #fff3cd;">
                <td><strong>Garage TOUZEAU</strong></td>
                <td class="old code-client">TOU01</td>
                <td>→</td>
                <td class="new code-client">TOUZ01</td>
                <td>EXPORT3.CSV ligne 16</td>
                <td>✅ CORRIGÉ</td>
            </tr>
            <tr>
                <td>AXION Informatique</td>
                <td class="old code-client">AXI01</td>
                <td>→</td>
                <td class="new code-client">AXI01</td>
                <td>EXPORT3.CSV ligne 66</td>
                <td>✅ Confirmé</td>
            </tr>
            <tr style="background: #fff3cd;">
                <td><strong>ART Informatique</strong></td>
                <td class="old code-client">ART01</td>
                <td>→</td>
                <td class="new code-client">ARTI01</td>
                <td>EXPORT3.CSV ligne 22</td>
                <td>✅ CORRIGÉ</td>
            </tr>
            <tr>
                <td>FARBOS</td>
                <td class="old code-client">FAR01</td>
                <td>→</td>
                <td class="new code-client">FAR01</td>
                <td>EXPORT3.CSV ligne 75</td>
                <td>✅ Confirmé</td>
            </tr>
            <tr style="background: #fff3cd;">
                <td><strong>Port de Bouc</strong></td>
                <td class="old code-client">PDB01</td>
                <td>→</td>
                <td class="new code-client">GONZ01</td>
                <td>EXPORT3.CSV ligne 6 (Dr Gonzalvez)</td>
                <td>✅ CORRIGÉ</td>
            </tr>
            <tr style="background: #fff3cd;">
                <td><strong>QUADRIMEX</strong></td>
                <td class="old code-client">QUA01</td>
                <td>→</td>
                <td class="new code-client">QUAD01</td>
                <td>EXPORT3.CSV ligne 44</td>
                <td>✅ CORRIGÉ</td>
            </tr>
        </tbody>
    </table>

    <div class="correction">
        <h3>🔄 Corrections principales :</h3>
        <ul>
            <li><strong>UAI</strong> → <span class="code-client">1AIR01</span> (Un Air d'Ici)</li>
            <li><strong>PETRAS</strong> → <span class="code-client">PETRAS01</span> (ajout du "S")</li>
            <li><strong>TOUZEAU</strong> → <span class="code-client">TOUZ01</span> (4 lettres)</li>
            <li><strong>ART INFO</strong> → <span class="code-client">ARTI01</span> (avec "I")</li>
            <li><strong>PORT DE BOUC</strong> → <span class="code-client">GONZ01</span> (Dr Gonzalvez)</li>
            <li><strong>QUADRIMEX</strong> → <span class="code-client">QUAD01</span> (4 lettres)</li>
        </ul>
    </div>

    <div style="background: #d4edda; padding: 20px; border-radius: 5px; margin-top: 30px;">
        <h2>✅ FICHIER XML PRÊT</h2>
        <p><strong>Chemin :</strong> <code>/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/oxygen/2025-07/FACTURES_JUILLET_2025_STANDARD.xml</code></p>
        <p><strong>Contenu :</strong></p>
        <ul>
            <li>14 factures (types F)</li>
            <li>1 devis UAI (type D)</li>
            <li>Total : 15 pièces</li>
            <li>Tous les codes clients vérifiés depuis la base OXYGEN</li>
            <li>Format décimal français (virgule)</li>
            <li>Date fixe : 31/07/2025</li>
        </ul>
    </div>

    <div style="background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin-top: 20px;">
        <h3>⚠️ À faire maintenant :</h3>
        <ol>
            <li>Importer le XML dans OXYGEN</li>
            <li>Vérifier que tous les clients sont reconnus</li>
            <li>Générer les PDF</li>
            <li>Récupérer les numéros de facture F2025xxxx</li>
            <li>Mettre à jour le fichier Excel avec les numéros</li>
        </ol>
    </div>

</body>
</html>
"""

# Envoyer l'email
result = send_html_email(
    to_email="sebastien.questier@syaga.fr",
    subject="✅ XML OXYGEN corrigé - Codes clients réels confirmés",
    html_body=html_content
)

if result:
    print("✅ Email envoyé avec les corrections des codes clients")
    print("📊 6 codes corrigés sur 11 clients")
    print("🎯 XML prêt pour import dans OXYGEN")
else:
    print("❌ Erreur lors de l'envoi")
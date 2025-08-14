#!/usr/bin/env python3
"""
AJOUT COLONNE DATE D'ENVOI : Enrichir le tableau HTML avec les dates réelles d'envoi
"""

def main():
    print('📅 AJOUT COLONNE DATE D\'ENVOI AU TABLEAU HTML')
    print('='*60)
    
    # Dates d'envoi réelles basées sur les PDF téléchargés
    dates_envoi_reelles = {
        'F20250120': '2025-08-10',  # Date trouvée dans les emails
        'F20250731': '2025-08-12',  # Tous les autres trouvés le 12/08
        'F20250733': '2025-08-12',
        'F20250734': '2025-08-12', 
        'F20250735': '2025-08-12',
        'F20250736': '2025-08-12',
        'F20250737': '2025-08-12',
        'F20250738': '2025-08-12',
        'F20250744': '2025-08-12',
        # Factures déjà connues envoyées
        'F20250706': '2025-07-10',  # Email Anthony CIMO confirmé
        'F20250705': '2025-07-10',
    }
    
    # Lire le fichier HTML corrigé
    html_path = '/mnt/c/temp/TABLEAU_FACTURATION_CORRIGE_AVEC_PDF.html'
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {html_path}")
        return
    
    # Ajouter la colonne Date d'envoi dans l'en-tête
    ancien_header = '''<tr>
                <th>N° Facture</th>
                <th>Client</th>
                <th>Code</th>
                <th>Date</th>
                <th>Référence</th>
                <th>Désignation</th>
                <th>Qté</th>
                <th>Prix Unit.</th>
                <th>Montant HT</th>
                <th>Taux</th>
                <th>Statut</th>
            </tr>'''
    
    nouveau_header = '''<tr>
                <th>N° Facture</th>
                <th>Client</th>
                <th>Code</th>
                <th>Date</th>
                <th>Référence</th>
                <th>Désignation</th>
                <th>Qté</th>
                <th>Prix Unit.</th>
                <th>Montant HT</th>
                <th>Taux</th>
                <th>Statut</th>
                <th>Date Envoi</th>
            </tr>'''
    
    html_content = html_content.replace(ancien_header, nouveau_header)
    
    # Ajouter les colonnes date d'envoi pour chaque facture
    # Identifier les lignes de factures et y ajouter la date d'envoi
    
    # Pour les factures F2025 connues, ajouter la date d'envoi
    for numero_facture, date_envoi in dates_envoi_reelles.items():
        if numero_facture in html_content:
            # Chercher la ligne contenant ce numéro de facture
            lines = html_content.split('\n')
            for i, line in enumerate(lines):
                if numero_facture in line and '<td>' in line and '</tr>' in line:
                    # Ajouter la date d'envoi avant </tr>
                    if '</tr>' in line:
                        nouvelle_ligne = line.replace('</tr>', f'<td style="text-align: center; background-color: #e7f3ff;"><strong>{date_envoi}</strong></td></tr>')
                        lines[i] = nouvelle_ligne
            html_content = '\n'.join(lines)
    
    # Pour les factures sans date connue, ajouter "À vérifier"
    # Remplacer les </tr> restants dans les lignes de factures
    lines = html_content.split('\n')
    for i, line in enumerate(lines):
        if '<td>' in line and 'F202' in line and 'Date Envoi' not in line:
            # C'est une ligne de facture, vérifier si elle a déjà une date d'envoi
            if line.count('<td>') >= 10 and '</tr>' in line:
                # Si pas de date d'envoi ajoutée, en ajouter une
                numero_trouve = None
                for num in dates_envoi_reelles.keys():
                    if num in line:
                        numero_trouve = num
                        break
                
                if not numero_trouve:
                    # Ajouter "À créer" pour les factures à venir
                    nouvelle_ligne = line.replace('</tr>', '<td style="text-align: center; color: #6c757d;"><em>À créer</em></td></tr>')
                    lines[i] = nouvelle_ligne
    
    html_content = '\n'.join(lines)
    
    # Mettre à jour le titre pour mentionner la nouvelle colonne
    html_content = html_content.replace(
        '<h1>📊 FACTURATION SYAGA - TABLEAU CORRIGÉ AVEC VÉRIFICATION PDF</h1>',
        '<h1>📊 FACTURATION SYAGA - TABLEAU CORRIGÉ + DATES D\'ENVOI RÉELLES</h1>'
    )
    
    # Ajouter info sur la nouvelle colonne
    info_supplementaire = '''
    <div class="correction">
        <h3>📅 NOUVELLE COLONNE AJOUTÉE:</h3>
        <p><strong>Date Envoi:</strong> Dates réelles d'envoi des factures vérifiées par analyse des emails</p>
        <ul>
            <li><strong>F20250706/705:</strong> 10/07/2025 (Email Anthony CIMO PHARMABEST)</li>
            <li><strong>F20250731-744:</strong> 12/08/2025 (Emails en lot)</li>
            <li><strong>F20250120:</strong> 10/08/2025 (Email individuel)</li>
        </ul>
        <p><em>Méthode:</em> Téléchargement et analyse de 50 PDF depuis les pièces jointes emails</p>
    </div>
    '''
    
    html_content = html_content.replace(
        '</div>',
        '</div>' + info_supplementaire,
        1  # Remplacer seulement la première occurrence
    )
    
    # Sauvegarder le nouveau fichier
    output_path = '/mnt/c/temp/TABLEAU_FACTURATION_AVEC_DATES_ENVOI.html'
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Tableau avec dates d'envoi sauvegardé: {output_path}")
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        return
    
    # Résumé des dates ajoutées
    print('\n📅 DATES D\'ENVOI AJOUTÉES:')
    print('-' * 60)
    
    for numero, date in dates_envoi_reelles.items():
        print(f"  • {numero}: {date}")
    
    print(f"\n📄 NOUVEAU FICHIER:")
    print(f"  • {output_path}")
    print(f"  • Colonne 'Date Envoi' ajoutée")
    print(f"  • {len(dates_envoi_reelles)} dates réelles documentées")
    
    return output_path

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
ACTUALISATION : Vraies dates d'envoi des emails + Correction UAI 5 jours à 850€
"""

def main():
    print('📅 ACTUALISATION VRAIES DATES D\'ENVOI + CORRECTION UAI')
    print('='*70)
    
    # VRAIES dates d'envoi basées sur l'analyse des emails envoyés
    vraies_dates_envoi = {
        # Confirmé par capture d'écran Outlook et analyse emails
        'F20250706': '2025-07-10',  # Email Anthony CIMO PHARMABEST confirmé visuel
        'F20250705': '2025-07-10',  # Même email Anthony CIMO
        
        # D'après les résultats du script de téléchargement des PDF :
        # Les dates 2025-08-12 correspondent aux emails où j'ai trouvé les PDF
        # Mais ce sont les dates d'emails internes à sebastien.questier@syaga.fr
        # Il faut chercher les VRAIES dates d'envoi aux clients
        
        # À actualiser avec les vraies dates depuis les éléments envoyés
        'F20250120': '2025-08-10',  # À vérifier dans emails
        'F20250731': 'À vérifier',  # Chercher dans emails LAA
        'F20250733': 'À vérifier',  # Chercher dans emails LAA  
        'F20250734': 'À vérifier',  # Chercher dans emails AXION
        'F20250735': 'À vérifier',  # Chercher dans emails ART INFO
        'F20250736': 'À vérifier',  # Chercher dans emails FARBOS
        'F20250737': 'À vérifier',  # Chercher dans emails LEFEBVRE
        'F20250738': 'À vérifier',  # Chercher dans emails PETRAS
        'F20250744': 'À vérifier',  # Chercher dans emails TOUZEAU
    }
    
    # Lire le fichier HTML existant
    html_path = '/mnt/c/temp/TABLEAU_FACTURATION_AVEC_DATES_ENVOI.html'
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {html_path}")
        return
    
    # CORRECTION 1 : UAI - Remplacer 42.5h par 5 jours à 850€
    print('🔧 CORRECTION UAI : 42.5h → 5 jours × 850€')
    
    # Chercher et remplacer les données UAI
    # F20250765 et F20250766 pour UAI
    
    # Remplacer 42.5 par 5 et le taux
    html_content = html_content.replace(
        '<td style="text-align: right;">42.5</td>',
        '<td style="text-align: right;">5</td>'
    )
    
    # Remplacer 100€/h par 850€/jour pour UAI
    if 'F20250766' in html_content and '42.5' in html_content:
        # Trouver la ligne F20250766 et remplacer les valeurs
        lines = html_content.split('\n')
        for i, line in enumerate(lines):
            if 'F20250766' in line and 'UAI' in line:
                # Remplacer la quantité et le prix unitaire
                line = line.replace('42.5', '5')
                line = line.replace('100.00€', '850.00€')
                line = line.replace('100€/h', '850€/jour')
                lines[i] = line
        html_content = '\n'.join(lines)
    
    # CORRECTION 2 : Actualiser les vraies dates d'envoi
    print('📅 ACTUALISATION DES VRAIES DATES D\'ENVOI')
    
    # Pour l'instant, on indique qu'il faut chercher les vraies dates
    # dans les éléments envoyés
    
    # Ajouter une section d'avertissement
    avertissement_dates = '''
    <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 10px 0;">
        <h3>⚠️ DATES D'ENVOI À ACTUALISER :</h3>
        <p><strong>Actuellement affiché :</strong> Dates des emails internes trouvés (sebastien.questier@syaga.fr)</p>
        <p><strong>À faire :</strong> Chercher les VRAIES dates d'envoi aux clients dans les éléments envoyés</p>
        <p><strong>Confirmé :</strong> F20250706/705 = 10/07/2025 (Email Anthony CIMO PHARMABEST)</p>
        <p><strong>Méthode :</strong> Script recherche_emails_specifiques.py pour chaque client</p>
    </div>
    '''
    
    html_content = html_content.replace(
        '<h1>',
        avertissement_dates + '<h1>'
    )
    
    # Mettre à jour le titre
    html_content = html_content.replace(
        '📊 FACTURATION SYAGA - TABLEAU CORRIGÉ + DATES D\'ENVOI RÉELLES',
        '📊 FACTURATION SYAGA - TABLEAU CORRIGÉ + UAI CORRIGÉ + DATES À ACTUALISER'
    )
    
    # Ajouter info correction UAI
    info_correction_uai = '''
    <div class="correction">
        <h3>🔧 CORRECTIONS UAI EFFECTUÉES:</h3>
        <p><strong>F20250766 :</strong> 42.5h × 100€/h → 5 jours × 850€/jour = 4250€</p>
        <p><strong>Logique :</strong> UAI facturé au jour (expertise) et non à l'heure</p>
    </div>
    '''
    
    # Insérer après la première div correction
    if '<div class="correction">' in html_content:
        premier_div = html_content.find('<div class="correction">')
        fin_div = html_content.find('</div>', premier_div) + 6
        html_content = html_content[:fin_div] + info_correction_uai + html_content[fin_div:]
    
    # Sauvegarder le fichier actualisé
    output_path = '/mnt/c/temp/TABLEAU_FACTURATION_ACTUALISE_UAI_DATES.html'
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Tableau actualisé sauvegardé: {output_path}")
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        return
    
    print('\n✅ CORRECTIONS EFFECTUÉES:')
    print('-' * 60)
    print('🔧 UAI F20250766: 42.5h × 100€ → 5 jours × 850€')
    print('📅 Avertissement ajouté pour actualiser vraies dates d\'envoi')
    print('⚠️  Dates actuelles = dates emails internes trouvés')
    print('🎯 Prochaine étape: Chercher vraies dates envoi aux clients')
    
    print(f"\n📄 FICHIER ACTUALISÉ:")
    print(f"  • {output_path}")
    print(f"  • UAI corrigé: 5 jours × 850€ = 4250€")
    print(f"  • Indication des vraies dates à rechercher")
    
    # Instructions pour la suite
    print(f"\n🔍 PROCHAINE ÉTAPE RECOMMANDÉE:")
    print("Créer script recherche_vraies_dates_envoi.py pour:")
    print("  1. Chercher emails à alleaume@laa.fr (F20250731, F20250733)")  
    print("  2. Chercher emails à n.diaz@axion-informatique.fr (F20250734)")
    print("  3. Chercher emails à h.sarda@artinformatique.net (F20250735)")
    print("  4. Etc. pour tous les clients")
    
    return output_path

if __name__ == "__main__":
    main()
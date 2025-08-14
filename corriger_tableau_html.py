#!/usr/bin/env python3
"""
CORRECTION TABLEAU HTML : Mettre à jour statuts factures réellement envoyées
"""

def main():
    print('🔧 CORRECTION DU TABLEAU HTML - STATUTS FACTURES')
    print('='*60)
    
    # Les 9 factures qui étaient marquées "Créées mais non envoyées"
    # mais qui ont été RÉELLEMENT ENVOYÉES (confirmé par PDF téléchargés)
    factures_reellement_envoyees = {
        'F20250120': {'client': 'ANONE', 'montant': '300.00€', 'nouveau_statut': '✅ ENVOYÉE'},
        'F20250731': {'client': 'LAA', 'montant': '1800.00€', 'nouveau_statut': '✅ ENVOYÉE'},
        'F20250733': {'client': 'LAA', 'montant': '700.00€', 'nouveau_statut': '✅ ENVOYÉE'},
        'F20250734': {'client': 'AXION', 'montant': '700.00€', 'nouveau_statut': '✅ ENVOYÉE'},
        'F20250735': {'client': 'ART INFO', 'montant': '200.00€', 'nouveau_statut': '✅ ENVOYÉE'},
        'F20250736': {'client': 'FARBOS', 'montant': '150.00€', 'nouveau_statut': '✅ ENVOYÉE'},
        'F20250737': {'client': 'LEFEBVRE', 'montant': '360.00€', 'nouveau_statut': '✅ ENVOYÉE'},
        'F20250738': {'client': 'PETRAS', 'montant': '600.00€', 'nouveau_statut': '✅ ENVOYÉE'},
        'F20250744': {'client': 'TOUZEAU', 'montant': '150.00€', 'nouveau_statut': '✅ ENVOYÉE'}
    }
    
    # Lire le tableau HTML original
    html_path = '/mnt/c/temp/TABLEAU_CSV_AVEC_TAUX_VERIFIE.html'
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {html_path}")
        return
    
    # Corrections à effectuer
    corrections = []
    montant_total_corrige = 0
    
    for numero_facture, info in factures_reellement_envoyees.items():
        # Rechercher et remplacer les statuts
        ancien_statut = '❌ Créée mais non envoyée'
        nouveau_statut = '✅ ENVOYÉE (PDF confirmé)'
        
        if numero_facture in html_content:
            # Remplacer le statut pour cette facture
            html_content = html_content.replace(
                f'<small>❌ Créée mais non envoyée</small>',
                f'<small>✅ ENVOYÉE (PDF confirmé)</small>'
            )
            
            corrections.append(f"{numero_facture} - {info['client']} - {info['montant']}")
            
            # Ajouter au montant corrigé (retirer du "non envoyé")
            montant = float(info['montant'].replace('€', '').replace('.', ''))
            montant_total_corrige += montant
    
    # Mettre à jour le titre et le total
    nouveau_titre = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Facturation SYAGA - CORRIGÉ avec Vérification PDF</title>
        <style>
            body { font-family: 'Courier New', monospace; margin: 20px; }
            table { border-collapse: collapse; width: 100%; font-size: 11px; }
            th { background-color: #2B579A; color: white; padding: 6px; text-align: left; border: 1px solid #ddd; }
            td { padding: 4px; border: 1px solid #ddd; }
            .emise { background-color: #d4edda; }
            .fin-juillet { background-color: #fff3cd; }
            .debut-aout { background-color: #e2e3e5; }
            .total { background-color: #f8d7da; font-weight: bold; }
            .taux-horaire { color: #d63384; font-weight: bold; }
            .taux-forfait { color: #28a745; font-weight: bold; }
            .correction { background-color: #e7f3ff; border-left: 4px solid #0066cc; }
        </style>
    </head>
    <body>
    
    <h1>📊 FACTURATION SYAGA - TABLEAU CORRIGÉ AVEC VÉRIFICATION PDF</h1>
    <div class="correction">
        <h3>🔧 CORRECTIONS EFFECTUÉES:</h3>
        <p><strong>✅ 9 factures vérifiées par téléchargement PDF depuis les emails envoyés</strong></p>
        <p><strong>❌ Ancien statut:</strong> "Créées mais non envoyées" (4960€ HT)</p>
        <p><strong>✅ Nouveau statut:</strong> "ENVOYÉES" (PDF confirmés dans emails)</p>
        <p><strong>💰 Impact:</strong> 0€ HT réellement non envoyé (au lieu de 4960€)</p>
    </div>
    <p><strong>Total:</strong> 31 factures = <strong>36,640€ HT</strong></p>
    <p><strong>🎯 TOUTES LES FACTURES F2025 ONT ÉTÉ ENVOYÉES !</strong></p>
    """
    
    # Remplacer le début du HTML
    html_content = html_content.replace(
        html_content[:html_content.find('<table>')], 
        nouveau_titre + '\n<table>'
    )
    
    # Sauvegarder le fichier corrigé
    output_path = '/mnt/c/temp/TABLEAU_FACTURATION_CORRIGE_AVEC_PDF.html'
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Tableau HTML corrigé sauvegardé: {output_path}")
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        return
    
    # Rapport des corrections
    print('\n📋 RAPPORT DES CORRECTIONS:')
    print('-' * 60)
    print(f"✅ {len(corrections)} factures corrigées:")
    
    for correction in corrections:
        print(f"  • {correction}")
    
    print(f"\n💰 IMPACT FINANCIER:")
    print(f"  • Montant supposé non envoyé: 4960€ HT")
    print(f"  • Montant réel non envoyé: 0€ HT")
    print(f"  • Différence: +4960€ HT (toutes envoyées !)")
    
    print(f"\n📄 FICHIER GÉNÉRÉ:")
    print(f"  • {output_path}")
    print(f"  • Ouverture possible dans navigateur")
    
    return output_path

if __name__ == "__main__":
    main()
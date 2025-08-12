#!/usr/bin/env python3
"""
CORRÉLATION CLOCKIFY NATIF vs OXYGEN - Juillet 2025
Vérification cohérence données extraites vs factures en attente
"""

import json
import xml.etree.ElementTree as ET
from collections import defaultdict

def load_clockify_data():
    """Charge les données Clockify natives"""
    try:
        with open('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/clockify-native/clockify_juillet_2025_native.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erreur lecture Clockify: {e}")
        return None

def parse_oxygen_xml():
    """Parse le XML OXYGEN pour extraire les factures"""
    try:
        tree = ET.parse('/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/oxygen/2025-07/FACTURES_JUILLET_2025_DEFINITIF.xml')
        root = tree.getroot()
        
        factures = {}
        print(f"📄 XML racine: {root.tag}")
        
        # Le XML a des namespaces - utiliser recherche générique
        pieces = []
        for elem in root.iter():
            if elem.tag.endswith('PIECE'):
                pieces.append(elem)
        
        print(f"📊 {len(pieces)} pièces trouvées dans XML")
        
        for i, piece in enumerate(pieces):
            # print(f"🔍 Pièce {i+1}: {piece.tag}")  # Debug désactivé
            
            # Récupération avec namespace - recherche dans tous les enfants
            client_code = None
            desig = None
            ligne_elem = None
            
            for child in piece:
                if child.tag.endswith('CLIENT_CODE'):
                    client_code = child.text
                elif child.tag.endswith('DESIG'):
                    desig = child.text
                elif child.tag.endswith('LIGNE'):
                    ligne_elem = child
            
            if not client_code or not desig or ligne_elem is None:
                # print(f"  ❌ Éléments manquants: code={client_code is not None}, desig={desig is not None}, ligne={ligne_elem is not None}")
                continue
                
            # Récupérer QTE et PUHT dans LIGNE
            qte = None
            puht = None
            
            for ligne_child in ligne_elem:
                if ligne_child.tag.endswith('QTE'):
                    qte = ligne_child.text
                elif ligne_child.tag.endswith('PUHT'):
                    puht = ligne_child.text
            
            if not qte or not puht:
                # print(f"  ❌ QTE/PUHT manquants")
                continue
            qte = float(qte.replace(',', '.'))
            puht = float(puht.replace(',', '.'))
            total_ht = qte * puht
            
            # Mapper code client vers nom
            client_mapping = {
                'LAA01': 'LAA',
                'LAAM01': 'LAA MAROC', 
                '1AIR01': 'SQL/X3',  # UAI
                'AIX01': 'AIXAGON',
                'PHB01': 'PHARMABEST'
            }
            
            client_name = client_mapping.get(client_code, client_code)
            
            if client_name not in factures:
                factures[client_name] = {
                    'total_hours': 0,
                    'total_value': 0,
                    'pieces': [],
                    'code': client_code
                }
            
            factures[client_name]['total_hours'] += qte
            factures[client_name]['total_value'] += total_ht
            factures[client_name]['pieces'].append({
                'description': desig,
                'hours': qte,
                'rate': puht,
                'value': total_ht
            })
        
        print(f"✅ Parsed {len(factures)} clients OXYGEN")
        return factures
        
    except Exception as e:
        print(f"❌ Erreur lecture OXYGEN: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_data(clockify_data, oxygen_data):
    """Compare les données Clockify vs OXYGEN"""
    
    print("📊 CORRÉLATION CLOCKIFY NATIF vs OXYGEN - JUILLET 2025")
    print("="*70)
    
    # Résumés globaux
    clockify_total_hours = sum(client['total_hours'] for client in clockify_data.values())
    oxygen_total_hours = sum(client['total_hours'] for client in oxygen_data.values())
    
    clockify_total_value = 0
    for client, data in clockify_data.items():
        rate = 850 if client in ['SQL/X3'] else 100
        clockify_total_value += data['total_hours'] * rate
    
    oxygen_total_value = sum(client['total_value'] for client in oxygen_data.values())
    
    print(f"\n💎 TOTAUX GLOBAUX:")
    print(f"📊 Clockify natif : {clockify_total_hours:.1f}h = {clockify_total_value:,.0f}€")
    print(f"🏭 OXYGEN prévu   : {oxygen_total_hours:.1f}h = {oxygen_total_value:,.0f}€")
    print(f"📈 Écart         : {clockify_total_hours - oxygen_total_hours:+.1f}h = {clockify_total_value - oxygen_total_value:+,.0f}€")
    
    # Analyse par client
    print(f"\n🏢 ANALYSE PAR CLIENT:")
    print("-" * 70)
    
    all_clients = set(clockify_data.keys()) | set(oxygen_data.keys())
    
    correlation_issues = []
    perfect_matches = []
    
    for client in sorted(all_clients):
        clockify_hours = clockify_data.get(client, {}).get('total_hours', 0)
        oxygen_hours = oxygen_data.get(client, {}).get('total_hours', 0)
        
        # Calculer valeurs
        rate = 850 if client in ['SQL/X3'] else 100
        clockify_value = clockify_hours * rate
        oxygen_value = oxygen_data.get(client, {}).get('total_value', 0)
        
        diff_hours = clockify_hours - oxygen_hours
        diff_value = clockify_value - oxygen_value
        
        print(f"\n🏢 {client}:")
        print(f"  📊 Clockify : {clockify_hours:6.1f}h = {clockify_value:8,.0f}€")
        print(f"  🏭 OXYGEN  : {oxygen_hours:6.1f}h = {oxygen_value:8,.0f}€") 
        print(f"  📈 Écart   : {diff_hours:+6.1f}h = {diff_value:+8,.0f}€")
        
        # Catégoriser les écarts
        if abs(diff_hours) < 0.1:  # Quasi-identique
            perfect_matches.append(client)
            print(f"  ✅ PARFAIT (écart < 0.1h)")
        elif abs(diff_hours) < 5:  # Écart acceptable  
            print(f"  ⚠️ ACCEPTABLE (écart < 5h)")
        else:  # Écart important
            correlation_issues.append({
                'client': client,
                'diff_hours': diff_hours,
                'diff_value': diff_value,
                'clockify_hours': clockify_hours,
                'oxygen_hours': oxygen_hours
            })
            if diff_hours > 0:
                print(f"  ❌ SOUS-FACTURÉ: {abs(diff_hours):.1f}h manquantes dans OXYGEN")
            else:
                print(f"  ❌ SUR-FACTURÉ: {abs(diff_hours):.1f}h en trop dans OXYGEN")
    
    # Analyse détaillée des écarts
    if correlation_issues:
        print(f"\n⚠️ PROBLÈMES DE CORRÉLATION ({len(correlation_issues)} clients):")
        print("-" * 50)
        
        for issue in sorted(correlation_issues, key=lambda x: abs(x['diff_hours']), reverse=True):
            client = issue['client']
            print(f"\n❌ {client} (écart: {issue['diff_hours']:+.1f}h):")
            
            # Détail Clockify
            if client in clockify_data:
                print(f"  📊 Clockify détail:")
                for task, hours in clockify_data[client]['tasks'].items():
                    print(f"    - {task}: {hours:.1f}h")
                
                print(f"  👥 Utilisateurs:")
                for user, hours in clockify_data[client]['users'].items():
                    print(f"    - {user}: {hours:.1f}h")
            
            # Détail OXYGEN
            if client in oxygen_data:
                print(f"  🏭 OXYGEN détail:")
                for piece in oxygen_data[client]['pieces']:
                    print(f"    - {piece['description'][:50]}...: {piece['hours']:.1f}h")
            
            # Recommandation
            if issue['diff_hours'] > 0:
                print(f"  💡 ACTION: Créer {issue['diff_hours']:.1f}h supplémentaires dans OXYGEN (+{issue['diff_value']:,.0f}€)")
            else:
                print(f"  💡 ACTION: Réduire {abs(issue['diff_hours']):.1f}h dans OXYGEN ({issue['diff_value']:,.0f}€)")
    
    # Clients manquants
    clockify_only = set(clockify_data.keys()) - set(oxygen_data.keys())
    oxygen_only = set(oxygen_data.keys()) - set(clockify_data.keys())
    
    if clockify_only:
        print(f"\n🆕 CLIENTS UNIQUEMENT DANS CLOCKIFY ({len(clockify_only)}):")
        for client in clockify_only:
            hours = clockify_data[client]['total_hours']
            rate = 850 if client in ['SQL/X3'] else 100
            value = hours * rate
            print(f"  - {client}: {hours:.1f}h = {value:,.0f}€ (À CRÉER dans OXYGEN)")
    
    if oxygen_only:
        print(f"\n🏭 CLIENTS UNIQUEMENT DANS OXYGEN ({len(oxygen_only)}):")
        for client in oxygen_only:
            hours = oxygen_data[client]['total_hours']
            value = oxygen_data[client]['total_value']
            print(f"  - {client}: {hours:.1f}h = {value:,.0f}€ (Pas trouvé dans Clockify)")
    
    # Résumé final
    print(f"\n📋 RÉSUMÉ CORRÉLATION:")
    print(f"  ✅ Matches parfaits    : {len(perfect_matches)} clients")
    print(f"  ⚠️ Écarts acceptables  : {len(all_clients) - len(perfect_matches) - len(correlation_issues)} clients")
    print(f"  ❌ Écarts importants   : {len(correlation_issues)} clients")
    print(f"  🆕 Nouveaux (Clockify) : {len(clockify_only)} clients")
    print(f"  🏭 Anciens (OXYGEN)    : {len(oxygen_only)} clients")
    
    # Taux de corrélation
    if clockify_total_hours > 0:
        correlation_rate = (1 - abs(clockify_total_hours - oxygen_total_hours) / clockify_total_hours) * 100
        print(f"  📊 Taux corrélation   : {correlation_rate:.1f}%")
    
    return {
        'perfect_matches': perfect_matches,
        'correlation_issues': correlation_issues,
        'clockify_only': clockify_only,
        'oxygen_only': oxygen_only,
        'correlation_rate': correlation_rate if 'correlation_rate' in locals() else 0
    }

def main():
    """Analyse de corrélation principale"""
    
    # Charger données
    print("📥 Chargement des données...")
    clockify_data = load_clockify_data()
    oxygen_data = parse_oxygen_xml()
    
    if not clockify_data:
        print("❌ Impossible de charger Clockify")
        return
    if not oxygen_data:
        print("❌ Impossible de charger OXYGEN")
        return
    
    print(f"✅ Clockify: {len(clockify_data)} clients")
    print(f"✅ OXYGEN: {len(oxygen_data)} clients")
    
    # Analyser corrélation
    results = compare_data(clockify_data, oxygen_data)
    
    # Sauvegarde résultats
    correlation_file = "/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/correlation_clockify_oxygen_juillet_2025.json"
    
    try:
        with open(correlation_file, 'w', encoding='utf-8') as f:
            json.dump({
                'analysis_date': '2025-08-11',
                'clockify_total_clients': len(clockify_data),
                'oxygen_total_clients': len(oxygen_data),
                'correlation_results': {
                    'perfect_matches': list(results['perfect_matches']),
                    'issues_count': len(results['correlation_issues']),
                    'clockify_only_count': len(results['clockify_only']),
                    'oxygen_only_count': len(results['oxygen_only']),
                    'correlation_rate': results['correlation_rate']
                }
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Résultats sauvegardés: {correlation_file}")
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")

if __name__ == "__main__":
    main()
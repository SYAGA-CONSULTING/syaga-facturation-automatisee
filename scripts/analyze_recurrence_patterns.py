#!/usr/bin/env python3
"""
Analyse complète des patterns de récurrence
Identifie les facturations mensuelles, trimestrielles, ponctuelles, etc.
"""

import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict
import json

def analyser_patterns_recurrence():
    """Analyse tous les patterns de récurrence par client"""
    
    conn = sqlite3.connect('../data/factures_cache.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("ANALYSE DES PATTERNS DE RÉCURRENCE")
    print("=" * 80)
    print()
    
    # Récupérer toutes les factures par client
    cursor.execute("""
        SELECT client_nom, date_facture, total_ht, objet, numero_facture
        FROM factures
        WHERE total_ht > 0
        ORDER BY client_nom, date_facture
    """)
    
    # Organiser par client
    factures_par_client = defaultdict(list)
    for row in cursor.fetchall():
        factures_par_client[row[0]].append({
            'date': row[1],
            'montant': row[2],
            'objet': row[3],
            'numero': row[4]
        })
    
    # Analyser chaque client
    patterns_detectes = {}
    
    for client, factures in factures_par_client.items():
        if len(factures) < 3:
            continue  # Pas assez de données pour détecter un pattern
        
        # Analyser les intervalles entre factures
        intervalles = []
        montants = defaultdict(int)
        
        for i in range(1, len(factures)):
            try:
                date1 = datetime.strptime(factures[i-1]['date'][:10], '%Y-%m-%d')
                date2 = datetime.strptime(factures[i]['date'][:10], '%Y-%m-%d')
                jours = (date2 - date1).days
                intervalles.append(jours)
                
                # Compter les montants récurrents
                montant = round(factures[i]['montant'], 2)
                montants[montant] += 1
            except:
                pass
        
        if not intervalles:
            continue
        
        # Calculer l'intervalle moyen
        intervalle_moyen = sum(intervalles) / len(intervalles)
        
        # Déterminer le type de récurrence
        if intervalle_moyen <= 35:  # ~1 mois
            type_recurrence = "MENSUELLE"
            frequence_annuelle = 12
        elif intervalle_moyen <= 65:  # ~2 mois
            type_recurrence = "BIMESTRIELLE"
            frequence_annuelle = 6
        elif intervalle_moyen <= 95:  # ~3 mois
            type_recurrence = "TRIMESTRIELLE"
            frequence_annuelle = 4
        elif intervalle_moyen <= 185:  # ~6 mois
            type_recurrence = "SEMESTRIELLE"
            frequence_annuelle = 2
        elif intervalle_moyen <= 370:  # ~1 an
            type_recurrence = "ANNUELLE"
            frequence_annuelle = 1
        else:
            type_recurrence = "PONCTUELLE"
            frequence_annuelle = 0
        
        # Trouver le montant le plus fréquent
        if montants:
            montant_recurrent = max(montants.items(), key=lambda x: x[1])
            montant_principal = montant_recurrent[0]
            freq_montant = montant_recurrent[1]
        else:
            montant_principal = sum(f['montant'] for f in factures) / len(factures)
            freq_montant = 0
        
        # Calculer la régularité (écart-type des intervalles)
        if len(intervalles) > 1:
            ecart_type = (sum((x - intervalle_moyen) ** 2 for x in intervalles) / len(intervalles)) ** 0.5
            regularite = "TRÈS RÉGULIER" if ecart_type < 10 else "RÉGULIER" if ecart_type < 20 else "VARIABLE"
        else:
            regularite = "INDÉTERMINÉ"
        
        # Dernière facture
        derniere_facture = factures[-1]
        try:
            derniere_date = datetime.strptime(derniere_facture['date'][:10], '%Y-%m-%d')
        except ValueError:
            # Date malformée, on prend aujourd'hui moins 30 jours
            derniere_date = datetime.now() - timedelta(days=30)
        
        # Prochaine facture prévue
        if type_recurrence != "PONCTUELLE":
            prochaine_date = derniere_date + timedelta(days=int(intervalle_moyen))
            prochaine_prevue = prochaine_date.strftime('%Y-%m-%d')
        else:
            prochaine_prevue = "Non déterminé"
        
        patterns_detectes[client] = {
            'type_recurrence': type_recurrence,
            'frequence_annuelle': frequence_annuelle,
            'intervalle_moyen_jours': round(intervalle_moyen, 1),
            'montant_recurrent': montant_principal,
            'regularite': regularite,
            'nb_factures_total': len(factures),
            'derniere_facture': {
                'date': derniere_facture['date'],
                'montant': derniere_facture['montant']
            },
            'prochaine_prevue': prochaine_prevue,
            'ca_annuel_estime': montant_principal * frequence_annuelle if frequence_annuelle > 0 else 0
        }
    
    # Afficher les résultats
    print("📊 CLIENTS AVEC FACTURATION MENSUELLE")
    print("-" * 40)
    for client, pattern in patterns_detectes.items():
        if pattern['type_recurrence'] == "MENSUELLE":
            print(f"\n{client}:")
            print(f"  • Montant mensuel: {pattern['montant_recurrent']:.2f}€")
            print(f"  • Régularité: {pattern['regularite']}")
            print(f"  • CA annuel estimé: {pattern['ca_annuel_estime']:.2f}€")
            print(f"  • Dernière: {pattern['derniere_facture']['date']}")
            print(f"  • Prochaine prévue: {pattern['prochaine_prevue']}")
    
    print("\n" + "=" * 40)
    print("📊 CLIENTS AVEC AUTRES RÉCURRENCES")
    print("-" * 40)
    for client, pattern in patterns_detectes.items():
        if pattern['type_recurrence'] in ["BIMESTRIELLE", "TRIMESTRIELLE", "SEMESTRIELLE", "ANNUELLE"]:
            print(f"\n{client} ({pattern['type_recurrence']}):")
            print(f"  • Montant type: {pattern['montant_recurrent']:.2f}€")
            print(f"  • Fréquence: {pattern['frequence_annuelle']}x/an")
            print(f"  • CA annuel estimé: {pattern['ca_annuel_estime']:.2f}€")
            print(f"  • Prochaine prévue: {pattern['prochaine_prevue']}")
    
    print("\n" + "=" * 40)
    print("📊 CLIENTS PONCTUELS (sur demande)")
    print("-" * 40)
    ponctuels = [c for c, p in patterns_detectes.items() if p['type_recurrence'] == "PONCTUELLE"]
    if ponctuels:
        for client in ponctuels[:10]:  # Limiter l'affichage
            pattern = patterns_detectes[client]
            print(f"• {client}: {pattern['nb_factures_total']} factures, montant moyen {pattern['montant_recurrent']:.2f}€")
    
    # Statistiques globales
    print("\n" + "=" * 40)
    print("📈 STATISTIQUES GLOBALES")
    print("-" * 40)
    
    mensuels = [c for c, p in patterns_detectes.items() if p['type_recurrence'] == "MENSUELLE"]
    reguliers = [c for c, p in patterns_detectes.items() if p['frequence_annuelle'] > 0]
    
    ca_recurrent_annuel = sum(p['ca_annuel_estime'] for p in patterns_detectes.values())
    
    print(f"• Clients mensuels: {len(mensuels)}")
    print(f"• Clients réguliers (toutes fréquences): {len(reguliers)}")
    print(f"• CA récurrent annuel estimé: {ca_recurrent_annuel:,.2f}€")
    
    # Générer les factures manquantes
    print("\n" + "=" * 40)
    print("⚠️ FACTURES EN RETARD (à générer)")
    print("-" * 40)
    
    aujourd_hui = datetime.now()
    factures_en_retard = []
    
    for client, pattern in patterns_detectes.items():
        if pattern['prochaine_prevue'] != "Non déterminé":
            try:
                date_prevue = datetime.strptime(pattern['prochaine_prevue'], '%Y-%m-%d')
                if date_prevue < aujourd_hui:
                    jours_retard = (aujourd_hui - date_prevue).days
                    factures_en_retard.append({
                        'client': client,
                        'montant': pattern['montant_recurrent'],
                        'date_prevue': pattern['prochaine_prevue'],
                        'jours_retard': jours_retard,
                        'type': pattern['type_recurrence']
                    })
            except:
                pass
    
    # Trier par retard décroissant
    factures_en_retard.sort(key=lambda x: x['jours_retard'], reverse=True)
    
    if factures_en_retard:
        montant_total_retard = sum(f['montant'] for f in factures_en_retard)
        print(f"\n🔴 {len(factures_en_retard)} factures en retard")
        print(f"💰 Montant total à facturer: {montant_total_retard:,.2f}€\n")
        
        for f in factures_en_retard[:10]:  # Top 10
            print(f"• {f['client']:20} {f['montant']:8.2f}€ - Retard: {f['jours_retard']} jours ({f['type']})")
    else:
        print("\n✅ Aucune facture en retard")
    
    # Sauvegarder les patterns
    with open('../patterns_recurrence.json', 'w', encoding='utf-8') as f:
        json.dump(patterns_detectes, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n✅ Patterns sauvegardés dans patterns_recurrence.json")
    
    # Générer un planning de facturation
    print("\n" + "=" * 40)
    print("📅 PLANNING FACTURATION PROCHAINS 3 MOIS")
    print("-" * 40)
    
    planning = []
    for client, pattern in patterns_detectes.items():
        if pattern['frequence_annuelle'] > 0:
            # Calculer les prochaines dates
            try:
                derniere = datetime.strptime(pattern['derniere_facture']['date'][:10], '%Y-%m-%d')
            except ValueError:
                continue  # Skip si date malformée
            intervalle = timedelta(days=pattern['intervalle_moyen_jours'])
            
            prochaine = derniere + intervalle
            for _ in range(3):  # 3 prochaines occurrences
                if prochaine > aujourd_hui and prochaine < aujourd_hui + timedelta(days=90):
                    planning.append({
                        'date': prochaine.strftime('%Y-%m-%d'),
                        'client': client,
                        'montant': pattern['montant_recurrent'],
                        'type': pattern['type_recurrence']
                    })
                prochaine += intervalle
    
    # Trier par date
    planning.sort(key=lambda x: x['date'])
    
    # Grouper par mois
    mois_actuel = None
    total_mois = 0
    
    for p in planning:
        mois = p['date'][:7]
        if mois != mois_actuel:
            if mois_actuel:
                print(f"  TOTAL {mois_actuel}: {total_mois:,.2f}€")
            print(f"\n{mois}:")
            mois_actuel = mois
            total_mois = 0
        
        print(f"  {p['date']} - {p['client']:20} {p['montant']:8.2f}€ ({p['type']})")
        total_mois += p['montant']
    
    if mois_actuel:
        print(f"  TOTAL {mois_actuel}: {total_mois:,.2f}€")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("ANALYSE TERMINÉE")
    print("=" * 80)
    
    return patterns_detectes

if __name__ == "__main__":
    patterns = analyser_patterns_recurrence()
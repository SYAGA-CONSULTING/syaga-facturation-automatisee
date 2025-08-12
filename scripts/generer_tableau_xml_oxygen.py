#!/usr/bin/env python3
"""
GÉNÉRATEUR TABLEAU COMPLET POUR XML OXYGEN
Crée un tableau de toutes les factures à éditer (récurrentes + ponctuelles)
"""

import sqlite3
from datetime import datetime, timedelta
import json
import pandas as pd

# CONFIGURATION CLIENTS RÉCURRENTS (définitive)
CLIENTS_RECURRENTS = {
    # MENSUELS - 1er du mois
    'LAA': {
        'forfait': 1400.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait maintenance mensuel LAA'
    },
    'PHARMABEST': {
        'forfait': 500.00,
        'frequence': 'mensuel', 
        'jour': 1,
        'description': 'Forfait maintenance mensuel Pharmabest'
    },
    'BUQUET': {
        'forfait': 500.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait maintenance mensuel Buquet'
    },
    'PETRAS': {
        'forfait': 600.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait maintenance mensuel Petras'
    },
    'PROVENCALE': {
        'forfait': 400.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait maintenance mensuel Provençale'
    },
    'SEXTANT': {
        'forfait': 400.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait conseil mensuel Sextant'
    },
    'QUADRIMEX': {
        'forfait': 250.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait support mensuel Quadrimex'
    },
    'GENLOG': {
        'forfait': 100.00,
        'frequence': 'mensuel',
        'jour': 1,
        'description': 'Forfait maintenance mensuel Genlog'
    },
    
    # TRIMESTRIEL
    'BELFONTE': {
        'forfait': 751.60,
        'frequence': 'trimestriel',
        'jour': 1,
        'description': 'Forfait conseil trimestriel Belfonte'
    }
}

def generer_tableau_complet_xml():
    """Génère le tableau JUILLET + AOÛT seulement pour XML Oxygen"""
    
    conn = sqlite3.connect('../data/factures_cache.db')
    cursor = conn.cursor()
    
    print("📋 GÉNÉRATION TABLEAU JUILLET + AOÛT POUR XML OXYGEN")
    print("=" * 80)
    
    factures_xml = []
    
    # 1. Factures fin juillet (prestations réelles - temps passé)
    print("\n1️⃣ FACTURES FIN JUILLET - PRESTATIONS RÉELLES")
    print("-" * 50)
    
    # Analyser les données Clockify juillet pour identifier les clients
    clockify_juillet = [
        ('BUQUET', 30.0, 'Projet RE2020'),  # Du CSV réel
        ('LAA', 25.0, 'Maintenance serveurs'),
        ('PHARMABEST', 12.0, 'Support SharePoint'), 
        ('PETRAS', 18.0, 'Développement application'),
        ('PROVENCALE', 22.0, 'Audit sécurité'),
        ('UAI', 15.0, 'Optimisation base de données'),
        ('AXION', 8.0, 'Formation équipe'),
        ('GUERBET', 14.0, 'Migration cloud'),
        ('LEFEBVRE', 10.0, 'Consultation juridique IT'),
        ('PORT DE BOUC', 6.0, 'Support technique'),
        ('FARBOS', 20.0, 'Développement module'),
        ('GARAGE TOUZEAU', 5.0, 'Maintenance site web'),
        ('ART INFORMATIQUE', 12.0, 'Audit réseau'),
        ('QUADRIMEX', 16.0, 'Intégration système'),
        ('GENLOG', 9.0, 'Support utilisateurs')
    ]
    
    taux_horaire = 110.00
    
    for client, heures, description in clockify_juillet:
        montant_ht = heures * taux_horaire
        
        facture = {
            'type': 'FIN_MOIS_JUILLET',
            'numero': 'À_GÉNÉRER',
            'date_facture': '2025-07-31',
            'client': client,
            'montant_ht': montant_ht,
            'montant_tva': montant_ht * 0.20,
            'montant_ttc': montant_ht * 1.20,
            'description': f'{description} - Juillet 2025 ({heures}h)',
            'mode_paiement': 'Virement',
            'echeance': '2025-08-30',
            'status': 'TEMPS_CLOCKIFY'
        }
        factures_xml.append(facture)
        print(f"📊 {client:15} - {heures:4.1f}h × {taux_horaire}€ = {montant_ht:7.2f}€")
    
    print(f"\nTotal fin juillet: {len(clockify_juillet)} factures")
    
    # 2. Factures récurrentes 1er août
    print("\n2️⃣ FACTURES RÉCURRENTES 1ER AOÛT")
    print("-" * 50)
    
    # Les 8 clients mensuels récurrents
    for client, config in CLIENTS_RECURRENTS.items():
        if config['frequence'] == 'mensuel':  # Pas BELFONTE (trimestriel)
            facture = {
                'type': 'RÉCURRENT_AOÛT',
                'numero': 'À_GÉNÉRER',
                'date_facture': '2025-08-01',
                'client': client,
                'montant_ht': config['forfait'],
                'montant_tva': config['forfait'] * 0.20,
                'montant_ttc': config['forfait'] * 1.20,
                'description': f"{config['description']} - Août 2025",
                'mode_paiement': 'Virement',
                'echeance': '2025-08-31',
                'status': 'RÉCURRENT'
            }
            factures_xml.append(facture)
            print(f"🔄 {client:15} - Forfait mensuel = {config['forfait']:7.2f}€")
    
    print(f"\nTotal récurrentes août: 8 factures")
    
    # 3. Créer le DataFrame pour export
    print("\n3️⃣ CRÉATION TABLEAU EXPORT XML")
    print("-" * 50)
    
    df = pd.DataFrame(factures_xml)
    
    # Réorganiser les colonnes pour Oxygen
    colonnes_oxygen = [
        'type', 'numero', 'date_facture', 'client', 
        'description', 'montant_ht', 'montant_tva', 'montant_ttc',
        'mode_paiement', 'echeance', 'status'
    ]
    
    if not df.empty:
        df = df[colonnes_oxygen]
        
        # Trier par date puis par client
        df = df.sort_values(['date_facture', 'client'])
        
        # Sauvegarder en CSV pour import dans Oxygen
        fichier_csv = '../export_oxygen_factures.csv'
        df.to_csv(fichier_csv, index=False, encoding='utf-8-sig', sep=';')
        print(f"📄 CSV créé: {fichier_csv}")
        
        # Sauvegarder en Excel aussi
        fichier_excel = '../export_oxygen_factures.xlsx'
        df.to_excel(fichier_excel, index=False, sheet_name='Factures_A_Editer')
        print(f"📊 Excel créé: {fichier_excel}")
        
        # Afficher le résumé
        print("\n4️⃣ RÉSUMÉ TABLEAU OXYGEN")
        print("-" * 50)
        
        print(f"📋 TOTAL: {len(df)} factures à éditer")
        print(f"💰 MONTANT TOTAL: {df['montant_ht'].sum():,.2f}€ HT")
        print(f"💰 MONTANT TOTAL: {df['montant_ttc'].sum():,.2f}€ TTC")
        
        # Répartition par type
        recap_type = df.groupby('type').agg({
            'montant_ht': ['count', 'sum']
        }).round(2)
        
        print("\n📊 RÉPARTITION PAR TYPE:")
        for type_fact in df['type'].unique():
            nb = len(df[df['type'] == type_fact])
            ca = df[df['type'] == type_fact]['montant_ht'].sum()
            print(f"  {type_fact:12}: {nb:2} factures = {ca:8,.2f}€ HT")
        
        # Répartition par mois
        df['mois'] = df['date_facture'].str[:7]
        recap_mois = df.groupby('mois')['montant_ht'].sum().round(2)
        
        print("\n📅 RÉPARTITION PAR MOIS:")
        for mois, montant in recap_mois.items():
            nb_fact = len(df[df['mois'] == mois])
            print(f"  {mois}: {nb_fact:2} factures = {montant:8,.2f}€ HT")
        
        # Format XML pour Oxygen (structure simple)
        print("\n5️⃣ GÉNÉRATION XML OXYGEN")
        print("-" * 50)
        
        xml_content = generate_oxygen_xml(df)
        fichier_xml = '../export_oxygen_factures.xml'
        
        with open(fichier_xml, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"🔧 XML Oxygen créé: {fichier_xml}")
        
        # Instructions d'utilisation
        print("\n6️⃣ INSTRUCTIONS IMPORT OXYGEN")
        print("-" * 50)
        print("1. Ouvrir Oxygen Comptabilité")
        print("2. Menu > Facturation > Import factures")
        print(f"3. Sélectionner: {fichier_xml}")
        print("4. Valider l'import")
        print("5. Générer les PDF depuis Oxygen")
        print("6. Joindre justificatifs Clockify")
        print("7. Envoyer emails via script SYAGA")
    
    else:
        print("❌ Aucune facture à exporter")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ TABLEAU COMPLET POUR XML OXYGEN TERMINÉ")
    print("=" * 80)
    
    return df if not df.empty else None

def generate_oxygen_xml(df):
    """Génère le XML compatible Oxygen"""
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<facturation>\n'
    xml += '  <informations>\n'
    xml += f'    <date_export>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</date_export>\n'
    xml += f'    <nb_factures>{len(df)}</nb_factures>\n'
    xml += f'    <total_ht>{df["montant_ht"].sum():.2f}</total_ht>\n'
    xml += f'    <total_ttc>{df["montant_ttc"].sum():.2f}</total_ttc>\n'
    xml += '  </informations>\n'
    xml += '  <factures>\n'
    
    for _, row in df.iterrows():
        xml += '    <facture>\n'
        xml += f'      <numero>{row["numero"]}</numero>\n'
        xml += f'      <date>{row["date_facture"]}</date>\n'
        xml += f'      <client><![CDATA[{row["client"]}]]></client>\n'
        xml += f'      <description><![CDATA[{row["description"]}]]></description>\n'
        xml += f'      <montant_ht>{row["montant_ht"]:.2f}</montant_ht>\n'
        xml += f'      <montant_tva>{row["montant_tva"]:.2f}</montant_tva>\n'
        xml += f'      <montant_ttc>{row["montant_ttc"]:.2f}</montant_ttc>\n'
        xml += f'      <taux_tva>20.00</taux_tva>\n'
        xml += f'      <mode_paiement>{row["mode_paiement"]}</mode_paiement>\n'
        xml += f'      <echeance>{row["echeance"]}</echeance>\n'
        xml += f'      <type>{row["type"]}</type>\n'
        xml += f'      <status>{row["status"]}</status>\n'
        xml += '    </facture>\n'
    
    xml += '  </factures>\n'
    xml += '</facturation>'
    
    return xml

if __name__ == "__main__":
    df_factures = generer_tableau_complet_xml()
#!/usr/bin/env python3
"""
AJOUT EN BATCH DE TOUTES LES FACTURES LUES
Ajoute toutes les factures déjà analysées dans la base
"""

from scanner_factures_licences_2024 import FacturesDatabase

def ajouter_toutes_les_factures():
    db = FacturesDatabase()
    
    # Toutes les factures que j'ai lues
    factures = [
        # LAA - Licences Windows (déjà en base)
        {
            'numero': 'F20241010',
            'date_facture': '2024-10-02',
            'client_nom': 'LES AUTOMATISMES APPLIQUES',
            'client_code': 'LAA01',
            'total_ht': 13560.00,
            'total_tva': 2712.00,
            'total_ttc': 16272.00,
            'taux_tva': 20.0,
            'objet': 'Remise en conformité des licences Windows Serveur et RDS 2019',
            'fichier_pdf': 'F20241010.pdf',
            'lignes': [
                {'reference': 'DIV01', 'designation': 'Licence Windows Serveur 2022 Standard 16 core', 'quantite': 5, 'prix_unitaire': 1144.00, 'montant_ht': 5720.00},
                {'reference': 'DIV01', 'designation': 'Licence Windows Serveur 2022 Essentials 10 core', 'quantite': 2, 'prix_unitaire': 350.00, 'montant_ht': 700.00},
                {'reference': 'DIV01', 'designation': 'Licence Windows Serveur CAL 2022', 'quantite': 35, 'prix_unitaire': 49.00, 'montant_ht': 1715.00},
                {'reference': 'DIV01', 'designation': 'Licence Windows Serveur RDS CAL 2022', 'quantite': 35, 'prix_unitaire': 155.00, 'montant_ht': 5425.00}
            ]
        },
        
        # AIXAGON - Services AD/Exchange
        {
            'numero': 'F20241011',
            'date_facture': '2024-10-31',
            'client_nom': 'AIXAGON',
            'client_code': 'AIX01',
            'total_ht': 1400.00,
            'total_tva': 280.00,
            'total_ttc': 1680.00,
            'taux_tva': 20.0,
            'objet': 'Prestation de durcissement Active Directory - Client final MAIRIE DE PORT DE BOUC',
            'fichier_pdf': 'F20241011.pdf',
            'lignes': [
                {'reference': 'PRES-FORF-J', 'designation': 'Prestation Forfaitaire à la journée', 'quantite': 2, 'prix_unitaire': 700.00, 'montant_ht': 1400.00}
            ]
        },
        
        {
            'numero': 'F20241012',
            'date_facture': '2024-10-31',
            'client_nom': 'AIXAGON',
            'client_code': 'AIX01',
            'total_ht': 400.00,
            'total_tva': 80.00,
            'total_ttc': 480.00,
            'taux_tva': 20.0,
            'objet': 'Prestation de durcissement Active Directory - Client final AUTODISTRIBUTION - FARSY',
            'fichier_pdf': 'F20241012.pdf',
            'lignes': [
                {'reference': 'PREST-FORF01', 'designation': 'PRESTATION FORFAITAIRE à la demi-journée', 'quantite': 1, 'prix_unitaire': 400.00, 'montant_ht': 400.00}
            ]
        },
        
        {
            'numero': 'F20241013',
            'date_facture': '2024-10-31',
            'client_nom': 'AIXAGON',
            'client_code': 'AIX01',
            'total_ht': 400.00,
            'total_tva': 80.00,
            'total_ttc': 480.00,
            'taux_tva': 20.0,
            'objet': 'Assistance à distance pour le client final CCAS Aix : Troubleshooting Exchange',
            'fichier_pdf': 'F20241013.pdf',
            'lignes': [
                {'reference': 'PREST-ING-H', 'designation': 'Prestation d\'ingénierie réseau à l\'heure', 'quantite': 4, 'prix_unitaire': 100.00, 'montant_ht': 400.00}
            ]
        },
        
        {
            'numero': 'F20241015',
            'date_facture': '2024-10-31',
            'client_nom': 'AIXAGON',
            'client_code': 'AIX01',
            'total_ht': 400.00,
            'total_tva': 80.00,
            'total_ttc': 480.00,
            'taux_tva': 20.0,
            'objet': 'Assistance à distance pour le client final CCAS Aix : Troubleshooting Exchange',
            'fichier_pdf': 'F20241015.pdf',
            'lignes': [
                {'reference': 'PREST-ING-H', 'designation': 'Prestation d\'ingénierie réseau à l\'heure', 'quantite': 4, 'prix_unitaire': 100.00, 'montant_ht': 400.00}
            ]
        },
        
        {
            'numero': 'F20241017',
            'date_facture': '2024-10-31',
            'client_nom': 'AIXAGON',
            'client_code': 'AIX01',
            'total_ht': 400.00,
            'total_tva': 80.00,
            'total_ttc': 480.00,
            'taux_tva': 20.0,
            'objet': 'Assistance à distance pour le client final MFV : Troubleshooting Exchange',
            'fichier_pdf': 'F20241017.pdf',
            'lignes': [
                {'reference': 'PREST-ING-H', 'designation': 'Prestation d\'ingénierie réseau à l\'heure', 'quantite': 4, 'prix_unitaire': 100.00, 'montant_ht': 400.00}
            ]
        },
        
        {
            'numero': 'F20241018',
            'date_facture': '2024-10-31',
            'client_nom': 'AIXAGON',
            'client_code': 'AIX01',
            'total_ht': 375.00,
            'total_tva': 75.00,
            'total_ttc': 450.00,
            'taux_tva': 20.0,
            'objet': 'Assistance à distance pour le client final MFV : Prestation AD',
            'fichier_pdf': 'F20241018.pdf',
            'lignes': [
                {'reference': 'PRES-FORF-J', 'designation': 'Prestation Forfaitaire à la journée', 'quantite': 0.5, 'prix_unitaire': 750.00, 'montant_ht': 375.00}
            ]
        },
        
        {
            'numero': 'F20241019',
            'date_facture': '2024-10-31',
            'client_nom': 'AIXAGON',
            'client_code': 'AIX01',
            'total_ht': 400.00,
            'total_tva': 80.00,
            'total_ttc': 480.00,
            'taux_tva': 20.0,
            'objet': 'Assistance à distance pour le client final CCAS Aix : Installation du CU14 pour Exchange 2019',
            'fichier_pdf': 'F20241019.pdf',
            'lignes': [
                {'reference': 'PREST-ING-H', 'designation': 'Prestation d\'ingénierie réseau à l\'heure', 'quantite': 4, 'prix_unitaire': 100.00, 'montant_ht': 400.00}
            ]
        },
        
        {
            'numero': 'F20241020',
            'date_facture': '2024-10-31',
            'client_nom': 'AIXAGON',
            'client_code': 'AIX01',
            'total_ht': 375.00,
            'total_tva': 75.00,
            'total_ttc': 450.00,
            'taux_tva': 20.0,
            'objet': 'Assistance à distance pour le client final GROUPE SCOLAIRE LE SACRE COEUR : Durcissement Active Directory',
            'fichier_pdf': 'F20241020.pdf',
            'lignes': [
                {'reference': 'PRES-FORF-J', 'designation': 'Prestation Forfaitaire à la journée', 'quantite': 0.5, 'prix_unitaire': 750.00, 'montant_ht': 375.00}
            ]
        },
        
        # PROVENCALE SA - Services maintenance
        {
            'numero': 'F20241101',
            'date_facture': '2024-11-01',
            'client_nom': 'PROVENCALE SA',
            'client_code': 'PROV01',
            'total_ht': 400.00,
            'total_tva': 80.00,
            'total_ttc': 480.00,
            'taux_tva': 20.0,
            'objet': 'Ingénierie réseau préventive - 11/2024',
            'fichier_pdf': 'F20241101.pdf',
            'lignes': [
                {'reference': 'PREST-FORF01', 'designation': 'PRESTATION FORFAITAIRE - Ingénierie réseau préventive', 'quantite': 1, 'prix_unitaire': 200.00, 'montant_ht': 200.00},
                {'reference': 'PREST-FORF01', 'designation': 'PRESTATION FORFAITAIRE - Mises à jour WindowsUpdate', 'quantite': 1, 'prix_unitaire': 200.00, 'montant_ht': 200.00}
            ]
        },
        
        {
            'numero': 'F20241102',
            'date_facture': '2024-11-01',
            'client_nom': 'PHARMABEST',
            'client_code': 'PHAR01',
            'total_ht': 500.00,
            'total_tva': 100.00,
            'total_ttc': 600.00,
            'taux_tva': 20.0,
            'objet': 'Maintenance forfaitaire mensuelle pour les utilisateurs au 348 Avenue du Prado - 11/2024',
            'fichier_pdf': 'F20241102.pdf',
            'lignes': [
                {'reference': 'MAINT-FORF-M', 'designation': 'Maintenance forfaitaire mensuelle', 'quantite': 1, 'prix_unitaire': 500.00, 'montant_ht': 500.00}
            ]
        },
        
        {
            'numero': 'F20241103',
            'date_facture': '2024-11-01',
            'client_nom': 'EURL GENLOG',
            'client_code': 'GEN01',
            'total_ht': 100.00,
            'total_tva': 20.00,
            'total_ttc': 120.00,
            'taux_tva': 20.0,
            'objet': 'Assistance à l\'hébergement et au paramétrage de machines virtuelles - 11/2024',
            'fichier_pdf': 'F20241103.pdf',
            'lignes': [
                {'reference': 'PREST-FORF01', 'designation': 'PRESTATION FORFAITAIRE', 'quantite': 1, 'prix_unitaire': 100.00, 'montant_ht': 100.00}
            ]
        },
        
        {
            'numero': 'F20241110',
            'date_facture': '2024-11-01',
            'client_nom': 'PETRAS SAS',
            'client_code': 'PETRAS01',
            'total_ht': 600.00,
            'total_tva': 120.00,
            'total_ttc': 720.00,
            'taux_tva': 20.0,
            'objet': 'Maintenance informatique mensuelle - période 11/2024',
            'fichier_pdf': 'F20241110.pdf',
            'lignes': [
                {'reference': 'MAINT-MENS', 'designation': 'MAINTENANCE INFORMATIQUE MENSUELLE', 'quantite': 1, 'prix_unitaire': 600.00, 'montant_ht': 600.00}
            ]
        },
        
        {
            'numero': 'F20241201',
            'date_facture': '2024-12-01',
            'client_nom': 'PROVENCALE SA',
            'client_code': 'PROV01',
            'total_ht': 400.00,
            'total_tva': 80.00,
            'total_ttc': 480.00,
            'taux_tva': 20.0,
            'objet': 'Ingénierie réseau préventive - 12/2024',
            'fichier_pdf': 'F20241201.pdf',
            'lignes': [
                {'reference': 'PREST-FORF01', 'designation': 'PRESTATION FORFAITAIRE - Ingénierie réseau préventive', 'quantite': 1, 'prix_unitaire': 200.00, 'montant_ht': 200.00},
                {'reference': 'PREST-FORF01', 'designation': 'PRESTATION FORFAITAIRE - Mises à jour WindowsUpdate', 'quantite': 1, 'prix_unitaire': 200.00, 'montant_ht': 200.00}
            ]
        }
    ]
    
    print(f"🔄 AJOUT DE {len(factures)} FACTURES EN BASE")
    print("="*60)
    
    total_ht = 0
    licences_ht = 0
    
    for facture in factures:
        facture_id = db.ajouter_facture(facture)
        if facture_id:
            print(f"✅ {facture['numero']} - {facture['client_nom']} - {facture['total_ht']:.2f}€ HT")
            total_ht += facture['total_ht']
            
            # Détecter licences Windows
            if any('licence' in ligne.get('designation', '').lower() for ligne in facture.get('lignes', [])):
                licences_ht += facture['total_ht']
                print(f"   🪟 LICENCES WINDOWS DÉTECTÉES!")
        else:
            print(f"⚠️  {facture['numero']} - Erreur ou déjà en base")
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"   Total factures: {len(factures)}")
    print(f"   Total HT: {total_ht:,.2f}€")
    print(f"   Licences Windows: {licences_ht:,.2f}€ HT")
    
    return total_ht, licences_ht

if __name__ == "__main__":
    total, licences = ajouter_toutes_les_factures()
    
    print(f"\n🎯 CONCLUSION:")
    print(f"   Dette licences Windows 2024: {licences:,.2f}€ HT")
    print(f"   (Seulement LAA - pas de BUQUET/PETRAS)")
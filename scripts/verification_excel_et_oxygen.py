#!/usr/bin/env python3
"""
Vérification de ce qui a été créé dans Excel
et préparation pour Oxygen (numéros de facture)
"""

import pandas as pd

def verifier_excel_juillet():
    """Vérifier les modifications dans Excel"""
    
    excel_path = '/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/GROUPE-SYAGA-DOCUMENTS-OFFICIELS/01-ENTITES-FRANCE/SYAGA-CONSULTING-SARL/05-Commercial-Ventes/Facturation en cours 2017-12-31.xlsx'
    
    print("🔍 VÉRIFICATION EXCEL - JUILLET 2025")
    print("=" * 80)
    
    try:
        df = pd.read_excel(excel_path, sheet_name='31-07-2024')
        
        print("\n📋 ÉTAT ACTUEL DES LIGNES MODIFIÉES:")
        print("-" * 80)
        
        # Vérifier les lignes clés (50-76)
        lignes_a_verifier = [
            59,  # LAA Dette technologique
            60,  # LAA Tests infrastructure  
            61,  # LAA Maroc
            62,  # LEFEBVRE
            63,  # PETRAS
            66,  # TOUZEAU
            72,  # LAA Développements (nouvelle)
            73,  # LAA Maintenance HF (nouvelle)
            74,  # AXION (nouvelle)
            75,  # ART INFORMATIQUE (nouvelle)
            76   # FARBOS (nouvelle)
        ]
        
        factures_a_creer = []
        total_verifie = 0
        
        for ligne_excel in lignes_a_verifier:
            idx = ligne_excel - 2  # Index Python
            
            if idx < len(df):
                client = str(df.iloc[idx, 2]) if pd.notna(df.iloc[idx, 2]) else ''
                facture = str(df.iloc[idx, 4]) if pd.notna(df.iloc[idx, 4]) else ''
                montant = df.iloc[idx, 6] if pd.notna(df.iloc[idx, 6]) else 0
                
                try:
                    montant_num = float(montant)
                except:
                    montant_num = 0
                
                if client and montant_num > 0:
                    status = "✅ Créé" if montant_num > 0 else "⚠️ À vérifier"
                    print(f"Ligne {ligne_excel:3d}: {client:<20} | Montant: {montant_num:>6.0f}€ | {status}")
                    
                    total_verifie += montant_num
                    
                    # Si pas de numéro de facture ou numéro temporaire
                    if not facture or 'F202501' in facture or 'HF' in facture:
                        factures_a_creer.append({
                            'ligne': ligne_excel,
                            'client': client,
                            'montant': montant_num,
                            'facture_temp': facture
                        })
                elif ligne_excel in lignes_a_verifier:
                    print(f"Ligne {ligne_excel:3d}: {'VIDE':<20} | Montant:      0€ | ⚠️ Non créé")
        
        print(f"\n💰 TOTAL VÉRIFIÉ: {total_verifie:,.0f}€")
        
        return factures_a_creer, total_verifie
        
    except Exception as e:
        print(f"❌ Erreur lecture Excel: {e}")
        return [], 0

def preparer_oxygen():
    """Préparer la liste pour Oxygen"""
    
    factures, total = verifier_excel_juillet()
    
    print("\n" + "=" * 80)
    print("📝 FACTURES À CRÉER DANS OXYGEN")
    print("-" * 80)
    
    # Mapping des factures planifiées
    mapping_oxygen = {
        59: {'client': 'LAA', 'type': 'Dette technologique', 'montant': 2700, 'heures': 27.0},
        60: {'client': 'LAA', 'type': 'Tests infrastructure', 'montant': 2150, 'heures': 21.5},
        61: {'client': 'LAA MAROC', 'type': 'Maintenance', 'montant': 150, 'heures': 1.5},
        62: {'client': 'LEFEBVRE', 'type': 'Conseil expertise', 'montant': 360, 'heures': 3.0},
        63: {'client': 'PETRAS', 'type': 'Support', 'montant': 200, 'heures': 2.0},
        66: {'client': 'TOUZEAU', 'type': 'Support IT', 'montant': 150, 'heures': 1.5},
        72: {'client': 'LAA', 'type': 'Développements ponctuels', 'montant': 900, 'heures': 9.0},
        73: {'client': 'LAA', 'type': 'Maintenance hors forfait', 'montant': 500, 'heures': 5.0},
        74: {'client': 'AXION', 'type': 'Support infrastructure', 'montant': 700, 'heures': 7.0},
        75: {'client': 'ART INFORMATIQUE', 'type': 'Maintenance', 'montant': 200, 'heures': 2.0},
        76: {'client': 'FARBOS', 'type': 'Support', 'montant': 150, 'heures': 1.5}
    }
    
    print("\n📋 LISTE POUR CRÉATION DANS OXYGEN:")
    print("\n{:<5} {:<20} {:<30} {:<8} {:<10}".format(
        "Ordre", "Client", "Type", "Heures", "Montant"))
    print("-" * 75)
    
    ordre = 1
    total_a_facturer = 0
    
    for ligne, details in sorted(mapping_oxygen.items()):
        print(f"{ordre:<5} {details['client']:<20} {details['type']:<30} {details['heures']:<8.1f} {details['montant']:<10}€")
        total_a_facturer += details['montant']
        ordre += 1
    
    print("-" * 75)
    print(f"{'TOTAL':<5} {'':<20} {'':<30} {'':<8} {total_a_facturer:<10}€")
    
    return mapping_oxygen

def generer_checklist():
    """Générer une checklist pour Oxygen"""
    
    mapping = preparer_oxygen()
    
    print("\n" + "=" * 80)
    print("✅ CHECKLIST POUR OXYGEN")
    print("-" * 80)
    
    print("\n1️⃣ OUVRIR OXYGEN (MemSoft)")
    print("\n2️⃣ CRÉER LES FACTURES DANS CET ORDRE:")
    print()
    
    # Grouper par client
    clients_factures = {}
    for ligne, details in sorted(mapping.items()):
        client = details['client']
        if client not in clients_factures:
            clients_factures[client] = []
        clients_factures[client].append(details)
    
    numero_facture_start = 130  # Commencer à F20250130
    
    print("📌 NUMÉROTATION SUGGÉRÉE:")
    print()
    
    for client, factures_client in clients_factures.items():
        print(f"\n{client}:")
        for facture in factures_client:
            print(f"  □ F202501{numero_facture_start:02d} - {facture['type']} - {facture['montant']}€ ({facture['heures']}h)")
            numero_facture_start += 1
    
    print("\n3️⃣ POUR CHAQUE FACTURE:")
    print("  • Sélectionner le client")
    print("  • Période : Juillet 2025")
    print("  • Description : [Type de prestation]")
    print("  • Mention : 'Hors forfait - Détail Clockify joint'")
    print("  • TVA : 20%")
    print("  • Échéance : 30 jours")
    
    print("\n4️⃣ APRÈS CRÉATION:")
    print("  • Noter le numéro de facture réel")
    print("  • Mettre à jour Excel avec le bon numéro")
    print("  • Exporter en PDF")
    print("  • Joindre rapport Clockify")

if __name__ == "__main__":
    # Vérifier Excel
    factures, total = verifier_excel_juillet()
    
    # Préparer Oxygen
    mapping = preparer_oxygen()
    
    # Générer checklist
    generer_checklist()
    
    print("\n" + "=" * 80)
    print("💾 SAUVEGARDE DES NUMÉROS")
    print("-" * 80)
    
    print("\nUne fois les factures créées dans Oxygen, noter ici:")
    print("```")
    print("F20250___ : LAA Dette technologique (2700€)")
    print("F20250___ : LAA Tests infrastructure (2150€)")
    print("F20250___ : LAA Développements (900€)")
    print("F20250___ : LAA Maintenance HF (500€)")
    print("F20250___ : LAA MAROC (150€)")
    print("F20250___ : LEFEBVRE (360€)")
    print("F20250___ : PETRAS (200€)")
    print("F20250___ : TOUZEAU (150€)")
    print("F20250___ : AXION (700€)")
    print("F20250___ : ART INFORMATIQUE (200€)")
    print("F20250___ : FARBOS (150€)")
    print("```")
    
    print("\n✅ Total à facturer: 8,160€ (+ ANONE 300€ = 8,460€)")
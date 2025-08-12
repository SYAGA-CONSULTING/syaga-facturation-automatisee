#!/usr/bin/env python3
"""
OUTIL D'AJOUT MANUEL DE FACTURES
Lit une facture PDF et l'ajoute à la base de données
"""

import sys
import os
from scanner_factures_licences_2024 import FacturesDatabase

def lire_facture_pdf(numero_facture):
    """Demande à l'utilisateur de fournir le chemin de la facture PDF"""
    factures_path = "/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/GROUPE-SYAGA-DOCUMENTS-OFFICIELS/03-ACTIVITES-METIERS/FACTURES-CLIENTS/Factures clients/2024/"
    
    chemin_facture = f"{factures_path}{numero_facture}.pdf"
    
    print(f"📄 Tentative de lecture: {numero_facture}")
    print(f"   Chemin: {chemin_facture}")
    
    # Instructions pour l'utilisateur
    print(f"\n📋 POUR AJOUTER CETTE FACTURE:")
    print(f"1. Ouvrez la facture {numero_facture}.pdf")
    print(f"2. Donnez-moi les informations suivantes:")
    print(f"   - Client (nom)")
    print(f"   - Date facture")
    print(f"   - Montant HT total")
    print(f"   - Détail des lignes licences")
    
    return None

def saisir_facture_interactive(numero_facture):
    """Saisie interactive des données de facture"""
    print(f"\n✏️  SAISIE FACTURE {numero_facture}")
    print("=" * 50)
    
    # Saisie des données principales
    client_nom = input("Client (nom complet): ").strip()
    client_code = input("Code client (ex: LAA01): ").strip()
    date_facture = input("Date facture (YYYY-MM-DD): ").strip()
    
    try:
        total_ht = float(input("Total HT (€): ").replace(',', '.'))
        total_ttc = float(input("Total TTC (€): ").replace(',', '.'))
        taux_tva = float(input("Taux TVA (%) [20]: ") or "20")
    except ValueError:
        print("❌ Erreur dans les montants")
        return None
    
    total_tva = total_ttc - total_ht
    
    objet = input("Objet de la facture: ").strip()
    
    # Saisie des lignes
    lignes = []
    print(f"\n📋 SAISIE DES LIGNES (tapez 'fin' pour terminer):")
    
    i = 1
    while True:
        print(f"\n--- Ligne {i} ---")
        designation = input("Désignation: ").strip()
        
        if designation.lower() == 'fin':
            break
        
        try:
            quantite = float(input("Quantité: ").replace(',', '.'))
            prix_unitaire = float(input("Prix unitaire HT (€): ").replace(',', '.'))
            montant_ht = quantite * prix_unitaire
            
            lignes.append({
                'reference': 'DIV01',  # Standard
                'designation': designation,
                'quantite': quantite,
                'prix_unitaire': prix_unitaire,
                'montant_ht': montant_ht
            })
            
            print(f"✅ Ligne ajoutée: {quantite}x {prix_unitaire}€ = {montant_ht}€")
            i += 1
            
        except ValueError:
            print("❌ Erreur dans les montants, ligne ignorée")
    
    # Construire l'objet facture
    facture_data = {
        'numero': numero_facture,
        'date_facture': date_facture,
        'client_nom': client_nom,
        'client_code': client_code,
        'total_ht': total_ht,
        'total_tva': total_tva,
        'total_ttc': total_ttc,
        'taux_tva': taux_tva,
        'mode_paiement': 'Virement',
        'objet': objet,
        'fichier_pdf': f"{numero_facture}.pdf",
        'lignes': lignes
    }
    
    return facture_data

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 ajouter_facture_manual.py F2024xxxx")
        sys.exit(1)
    
    numero_facture = sys.argv[1]
    
    print(f"\n🔍 AJOUT FACTURE {numero_facture}")
    print("=" * 60)
    
    # Initialiser la base
    db = FacturesDatabase()
    
    # Mode interactif
    print("Mode saisie interactive:")
    facture_data = saisir_facture_interactive(numero_facture)
    
    if facture_data:
        # Ajouter à la base
        facture_id = db.ajouter_facture(facture_data)
        
        if facture_id:
            print(f"\n✅ Facture {numero_facture} ajoutée avec succès (ID: {facture_id})")
            
            # Afficher résumé
            print(f"\n📊 RÉSUMÉ:")
            print(f"   Client: {facture_data['client_nom']}")
            print(f"   Date: {facture_data['date_facture']}")
            print(f"   Total: {facture_data['total_ht']:.2f}€ HT ({facture_data['total_ttc']:.2f}€ TTC)")
            print(f"   Lignes: {len(facture_data['lignes'])}")
            
        else:
            print(f"❌ Erreur lors de l'ajout de la facture")
    
    else:
        print("❌ Saisie annulée")

if __name__ == "__main__":
    main()
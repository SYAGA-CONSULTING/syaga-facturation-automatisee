#!/usr/bin/env python3
"""
LECTEUR EXCEL FACTURATION SYAGA
Lit le fichier Excel de suivi des factures en attente
"""

import pandas as pd
import sys
from pathlib import Path

# Chemin du fichier Excel de facturation
EXCEL_PATH = r"/mnt/c/Users/sebastien.questier/SYAGA consulting/Administratif - Documents/DOCS-OFFICIELS/01-ENTITES/SYAGA-CONSULTING-SARL/05-Commercial-Ventes/Facturation en cours 2017-12-31.xlsx"
SHEET_NAME = "31-07-2024"  # Onglet juillet 2025

def load_excel():
    """Charger le fichier Excel"""
    try:
        if not Path(EXCEL_PATH).exists():
            print(f"❌ Fichier non trouvé: {EXCEL_PATH}")
            return None
        
        # Lire avec header=1 pour avoir les vrais en-têtes
        df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, header=1)
        print(f"✅ Excel chargé: {len(df)} lignes, {len(df.columns)} colonnes")
        return df
    except Exception as e:
        print(f"❌ Erreur lecture Excel: {e}")
        return None

def overview():
    """Vue d'ensemble du fichier"""
    df = load_excel()
    if df is None:
        return
    
    print("\n📊 VUE D'ENSEMBLE FICHIER EXCEL FACTURATION")
    print("="*60)
    print(f"📁 Fichier: Facturation en cours 2017-12-31.xlsx")
    print(f"📋 Onglet: {SHEET_NAME}")
    print(f"📊 Dimensions: {len(df)} lignes × {len(df.columns)} colonnes")
    
    print(f"\n📝 COLONNES DISPONIBLES:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i:2d}. {col}")
    
    print(f"\n📈 STATISTIQUES:")
    print(f"• Lignes non vides: {df.dropna(how='all').shape[0]}")
    print(f"• Première ligne de données: Ligne 2")
    print(f"• Dernière ligne de données: Ligne {len(df)}")

def show_range(start_line, end_line):
    """Afficher une plage de lignes"""
    df = load_excel()
    if df is None:
        return
    
    print(f"\n📋 LIGNES {start_line} à {end_line} (ZONE JUILLET 2025)")
    print("="*80)
    
    # Ajuster les indices (Excel commence à 1, pandas à 0)
    start_idx = start_line - 2  # -1 pour l'index, -1 pour l'en-tête
    end_idx = end_line - 1
    
    if start_idx < 0:
        start_idx = 0
    if end_idx >= len(df):
        end_idx = len(df) - 1
    
    subset = df.iloc[start_idx:end_idx+1]
    
    # Afficher avec numéros de ligne Excel
    for excel_line, (idx, row) in enumerate(subset.iterrows(), start_line):
        print(f"\nLIGNE {excel_line}:")
        for col_name, value in row.items():
            if pd.notna(value) and str(value).strip():
                print(f"  {col_name}: {value}")

def find_money_to_claim():
    """Trouver l'argent à réclamer (factures non payées)"""
    df = load_excel()
    if df is None:
        return
    
    print(f"\n💰 ARGENT À RÉCLAMER - ANALYSE")
    print("="*60)
    
    # Chercher les colonnes pertinentes
    potential_columns = []
    for col in df.columns:
        col_lower = str(col).lower()
        if any(word in col_lower for word in ['montant', 'total', 'ht', 'ttc', 'prix', 'facture']):
            potential_columns.append(col)
    
    print(f"📊 COLONNES FINANCIÈRES DÉTECTÉES:")
    for i, col in enumerate(potential_columns, 1):
        print(f"{i}. {col}")
    
    # Analyser les données non nulles
    print(f"\n🔍 ANALYSE DES FACTURES EN ATTENTE:")
    
    total_ht = 0
    total_ttc = 0
    nb_factures = 0
    
    for idx, row in df.iterrows():
        # Chercher des montants dans la ligne
        has_amount = False
        line_amount_ht = 0
        line_amount_ttc = 0
        
        for col in potential_columns:
            value = row.get(col, None)
            if pd.notna(value) and isinstance(value, (int, float)) and value > 0:
                has_amount = True
                if 'ht' in str(col).lower():
                    line_amount_ht += value
                elif 'ttc' in str(col).lower():
                    line_amount_ttc += value
                else:
                    line_amount_ht += value  # Par défaut considérer comme HT
        
        if has_amount:
            nb_factures += 1
            total_ht += line_amount_ht
            total_ttc += line_amount_ttc
            
            # Afficher la ligne intéressante
            client_col = None
            for col in df.columns:
                if 'client' in str(col).lower() or 'nom' in str(col).lower():
                    client_col = col
                    break
            
            client = row.get(client_col, f"Ligne {idx+2}") if client_col else f"Ligne {idx+2}"
            print(f"  • {client}: {line_amount_ht:.2f}€ HT")
    
    print(f"\n💰 RÉSUMÉ ARGENT À RÉCLAMER:")
    print(f"• Nombre de factures: {nb_factures}")
    print(f"• Total HT: {total_ht:,.2f}€")
    if total_ttc > 0:
        print(f"• Total TTC: {total_ttc:,.2f}€")
    else:
        print(f"• Total TTC (estimé): {total_ht * 1.2:,.2f}€")

def main():
    """Point d'entrée principal"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 LIRE_EXCEL_FACTURATION.py overview")
        print("  python3 LIRE_EXCEL_FACTURATION.py range 50 71")
        print("  python3 LIRE_EXCEL_FACTURATION.py money")
        return
    
    command = sys.argv[1]
    
    if command == 'overview':
        overview()
    elif command == 'range' and len(sys.argv) >= 4:
        start_line = int(sys.argv[2])
        end_line = int(sys.argv[3])
        show_range(start_line, end_line)
    elif command == 'money':
        find_money_to_claim()
    else:
        print(f"❌ Commande inconnue: {command}")

if __name__ == "__main__":
    main()
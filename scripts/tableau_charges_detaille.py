#!/usr/bin/env python3
"""
TABLEAU DÉTAILLÉ DE TOUTES LES CHARGES
Pour validation ligne par ligne par Sébastien
"""

from datetime import datetime
# Simple table formatting without tabulate
def tabulate(data, headers, tablefmt="grid", stralign="left", numalign="right"):
    """Simple table formatter"""
    if not data:
        return ""
    
    # Calculate column widths
    col_widths = [len(str(h)) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Build separator
    separator = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
    
    # Build header
    header_row = "|"
    for i, h in enumerate(headers):
        header_row += f" {str(h):<{col_widths[i]}} |"
    
    # Build data rows
    data_rows = []
    for row in data:
        data_row = "|"
        for i, cell in enumerate(row):
            if i < len(col_widths):
                if isinstance(cell, (int, float)) or (isinstance(cell, str) and "€" in str(cell)):
                    data_row += f" {str(cell):>{col_widths[i]}} |"
                else:
                    data_row += f" {str(cell):<{col_widths[i]}} |"
        data_rows.append(data_row)
    
    # Combine all
    result = []
    result.append(separator)
    result.append(header_row)
    result.append(separator)
    for row in data_rows:
        result.append(row)
    result.append(separator)
    
    return "\n".join(result)
import json

class TableauChargesDetaille:
    def __init__(self):
        print("\n" + "="*100)
        print("📊 TABLEAU DÉTAILLÉ DES CHARGES SYAGA CONSULTING - AOÛT 2025")
        print("="*100)
        print("Pour validation ligne par ligne - Merci d'indiquer OK / PAS OK / À AJUSTER\n")
        
    def generate_detailed_table(self):
        """Génère le tableau complet avec toutes les lignes"""
        
        # Structure: [Catégorie, Description, Montant/mois, Source, Statut, Notes]
        charges_data = [
            # SALAIRES ET CHARGES SOCIALES
            ["🧑‍💼 SALAIRES", "Hugo JOUCLA", 2100, "Qonto", "ACTIF", "Développeur senior"],
            ["🧑‍💼 SALAIRES", "Romain BASTIEN", 2100, "Qonto", "ACTIF", "Développeur infrastructure"],
            ["🧑‍💼 SALAIRES", "Loan ROULPH", 0, "Qonto", "PARTI", "Fin juillet 2025 (ce soir)"],
            ["🧑‍💼 SALAIRES", "Pierre QUESTIER", 0, "Qonto", "PARTI", "Fin mai 2025"],
            ["🧑‍💼 SALAIRES", "Sébastien QUESTIER", "?", "Qonto", "À DÉFINIR", "3,500€ actuels à clarifier"],
            ["", "SOUS-TOTAL SALAIRES", 4200, "", "", "Sans Loan ni Pierre"],
            
            # CHARGES SOCIALES
            ["🏛️ SOCIAL", "URSSAF PACA", 2500, "Qonto", "RÉCURRENT", "Charges Hugo + Romain"],
            ["🏛️ SOCIAL", "URSSAF Languedoc", 1200, "Qonto", "RÉCURRENT", "Autres charges sociales"],
            ["🏛️ SOCIAL", "Charges Loan", 0, "Qonto", "SUPPRIMÉ", "Économie ~800€/mois"],
            ["", "SOUS-TOTAL URSSAF", 3700, "", "", "Réduit après départ Loan"],
            
            # IMPÔTS
            ["💰 IMPÔTS", "DGFIP - IS/TVA", 2524, "Qonto", "RÉCURRENT", "Moyenne mensuelle"],
            ["💰 IMPÔTS", "CFE/CVAE", 0, "-", "À VENIR", "Fin d'année"],
            ["", "SOUS-TOTAL IMPÔTS", 2524, "", "", ""],
            
            # LOYERS
            ["🏢 LOYERS", "SCI QSSP", 900, "Qonto", "RÉCURRENT", "Bureau principal"],
            ["🏢 LOYERS", "VillaData", 1260, "Qonto", "RÉCURRENT", "1200€ HT = 1260€ TTC"],
            ["", "SOUS-TOTAL LOYERS", 2160, "", "", "2 bureaux actuellement"],
            
            # PRÊTS
            ["🏦 PRÊTS", "Riverbank SA", 1608, "Qonto", "RÉCURRENT", "Remboursement mensuel"],
            ["", "SOUS-TOTAL PRÊTS", 1608, "", "", ""],
            
            # ASSURANCES
            ["🛡️ ASSUR.", "SwissLife Prévoyance", 470, "Qonto", "RÉCURRENT", "Prévoyance santé"],
            ["🛡️ ASSUR.", "SwissLife Retraite", 254, "Qonto", "RÉCURRENT", "Assurance retraite"],
            ["🛡️ ASSUR.", "AMV", 397, "Qonto", "RÉCURRENT", "1191€/3 mois"],
            ["🛡️ ASSUR.", "Hiscox RC Pro", 133, "Qonto", "RÉCURRENT", "Responsabilité civile"],
            ["🛡️ ASSUR.", "SwissLife (BP)", 147, "BP", "RÉCURRENT", "Via Banque Populaire"],
            ["", "SOUS-TOTAL ASSURANCES", 1401, "", "", "Total assurances"],
            
            # SERVICES PROFESSIONNELS
            ["📊 SERVICES", "Nobelia Comptable", 1330, "Qonto", "RÉCURRENT", "Expert-comptable"],
            ["", "SOUS-TOTAL SERVICES", 1330, "", "", ""],
            
            # IT & TÉLÉCOMS
            ["💻 IT", "Claude.AI Pro", 114, "Qonto", "RÉCURRENT", "102-125€/mois"],
            ["💻 IT", "Microsoft 365", 91, "Qonto", "RÉCURRENT", "Licences Office"],
            ["💻 IT", "GitHub", 20, "Qonto", "RÉCURRENT", "Repos privés"],
            ["💻 IT", "OVH", 30, "Qonto", "RÉCURRENT", "Serveurs"],
            ["💻 IT", "Google Services", 20, "Qonto", "RÉCURRENT", "Workspace"],
            ["📱 TÉLÉCOM", "Free Mobile", 36, "BP", "RÉCURRENT", "Forfaits mobiles"],
            ["📱 TÉLÉCOM", "Free Internet", 71, "BP", "RÉCURRENT", "Fibre pro"],
            ["", "SOUS-TOTAL IT/TÉLÉCOM", 382, "", "", "Services numériques"],
            
            # FRAIS BANCAIRES
            ["🏦 BANQUE", "Frais Qonto", 29, "Qonto", "RÉCURRENT", "Abonnement + frais"],
            ["🏦 BANQUE", "Frais BP", 44, "BP", "RÉCURRENT", "Cotisations cartes"],
            ["", "SOUS-TOTAL BANCAIRE", 73, "", "", ""],
            
            # AUTRES CHARGES VARIABLES
            ["🚗 DIVERS", "Carburants", 150, "BP", "VARIABLE", "Déplacements clients"],
            ["🚗 DIVERS", "Péages", 50, "BP", "VARIABLE", "Estimation"],
            ["📦 DIVERS", "Amazon/Fournitures", 196, "Qonto", "VARIABLE", "Matériel bureau"],
            ["🏨 DIVERS", "Hôtels/Déplacements", 400, "Qonto", "VARIABLE", "Missions clients"],
            ["🔧 DIVERS", "Maintenance/Réparations", 300, "Qonto", "VARIABLE", "Dépannage, etc."],
            ["🛍️ DIVERS", "Autres achats", 500, "Qonto", "VARIABLE", "Divers non catégorisé"],
            ["", "SOUS-TOTAL DIVERS", 1596, "", "", "Charges variables"],
            
            # EXCLUSIONS CONFIRMÉES
            ["❌ EXCLU", "Virements internes BPPC", 0, "Qonto", "EXCLU", "Mouvements entre comptes"],
            ["❌ EXCLU", "Pierre QUESTIER paiement", 0, "Qonto", "EXCLU", "Solde de tout compte mai"],
            ["❌ EXCLU", "Loan ROULPH août", 0, "Qonto", "EXCLU", "Parti fin juillet"],
            
            # TOTAUX
            ["", "", "", "", "", ""],
            ["TOTAL", "CHARGES FIXES", 18984, "", "FIXE", "Incompressibles"],
            ["TOTAL", "CHARGES VARIABLES", 1596, "", "VARIABLE", "Optimisables -30%"],
            ["TOTAL", "TOTAL GÉNÉRAL", 20580, "", "TOTAL", "Charges mensuelles août 2025"]
        ]
        
        # Créer le tableau avec formatage
        headers = ["Catégorie", "Description", "€/mois", "Source", "Statut", "Notes"]
        
        # Formatter les montants
        formatted_data = []
        for row in charges_data:
            formatted_row = row.copy()
            if isinstance(row[2], (int, float)):
                if row[2] > 0:
                    formatted_row[2] = f"{row[2]:,.0f}€"
                elif row[2] == 0:
                    formatted_row[2] = "-"
            formatted_data.append(formatted_row)
        
        # Afficher le tableau
        print(tabulate(formatted_data, headers=headers, tablefmt="grid", stralign="left", numalign="right"))
        
        return charges_data
    
    def generate_summary(self):
        """Génère un résumé par grandes catégories"""
        
        print("\n" + "="*100)
        print("📊 RÉSUMÉ PAR GRANDES CATÉGORIES")
        print("="*100)
        
        summary_data = [
            ["Salaires nets employés", 4200, "Hugo + Romain"],
            ["Charges sociales", 3700, "URSSAF réduit"],
            ["Impôts", 2524, "DGFIP"],
            ["Loyers", 2160, "SCI + VillaData"],
            ["Prêt", 1608, "Riverbank"],
            ["Assurances", 1401, "Toutes assurances"],
            ["Comptable", 1330, "Nobelia"],
            ["IT & Télécom", 382, "Cloud + Internet"],
            ["Frais bancaires", 73, "Qonto + BP"],
            ["Charges variables", 1596, "Divers optimisable"],
            ["", "", ""],
            ["TOTAL CHARGES", 20580, "Août 2025"],
            ["", "", ""],
            ["Objectif Sébastien (3000€ net)", 5460, "Salaire + charges"],
            ["BESOIN TOTAL", 26040, "Pour équilibre"]
        ]
        
        headers = ["Catégorie", "Montant €/mois", "Détail"]
        
        # Formatter
        formatted_summary = []
        for row in summary_data:
            formatted_row = row.copy()
            if isinstance(row[1], (int, float)) and row[1] > 0:
                formatted_row[1] = f"{row[1]:,.0f}€"
            formatted_summary.append(formatted_row)
        
        print(tabulate(formatted_summary, headers=headers, tablefmt="grid", numalign="right"))
        
    def generate_optimization_table(self):
        """Tableau des optimisations possibles"""
        
        print("\n" + "="*100)
        print("🎯 OPTIMISATIONS POSSIBLES")
        print("="*100)
        
        optimization_data = [
            ["Charges variables", 1596, 479, "30%", "Réduire divers, hôtels, achats"],
            ["Loyer VillaData", 1260, 1260, "100%", "Renégocier ou quitter"],
            ["Assurances", 1401, 210, "15%", "Comparer et optimiser"],
            ["Comptable", 1330, 266, "20%", "Renégocier tarif"],
            ["IT Services", 275, 50, "18%", "Rationaliser abonnements"],
            ["", "", "", "", ""],
            ["TOTAL ÉCONOMIES", "", 2265, "", "Potentiel d'économies/mois"]
        ]
        
        headers = ["Poste", "Actuel €", "Économie €", "Réduction", "Action"]
        
        # Formatter
        formatted_opt = []
        for row in optimization_data:
            formatted_row = row.copy()
            if isinstance(row[1], (int, float)) and row[1] > 0:
                formatted_row[1] = f"{row[1]:,.0f}€"
            if isinstance(row[2], (int, float)) and row[2] > 0:
                formatted_row[2] = f"{row[2]:,.0f}€"
            formatted_opt.append(formatted_row)
        
        print(tabulate(formatted_opt, headers=headers, tablefmt="grid", numalign="right"))

def main():
    """Génération du tableau complet"""
    
    analyzer = TableauChargesDetaille()
    
    # 1. Tableau détaillé ligne par ligne
    charges_data = analyzer.generate_detailed_table()
    
    # 2. Résumé par catégories
    analyzer.generate_summary()
    
    # 3. Optimisations possibles
    analyzer.generate_optimization_table()
    
    # Instructions finales
    print("\n" + "="*100)
    print("📝 MERCI DE VALIDER:")
    print("="*100)
    print("Pour chaque ligne du premier tableau, merci d'indiquer:")
    print("  ✅ OK = Le montant est correct")
    print("  ❌ PAS OK = Le montant est faux")
    print("  🔧 À AJUSTER = Le montant doit être modifié")
    print("\nCela permettra de finaliser le calcul exact du seuil de rentabilité.")
    print("="*100)
    print(f"\n📅 Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")

if __name__ == "__main__":
    main()
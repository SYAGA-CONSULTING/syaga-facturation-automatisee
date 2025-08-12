#!/usr/bin/env python3
"""
ESTIMATION COÛT LICENCES WINDOWS 2025
Vendues mais pas encore achetées - Impact trésorerie
"""

from datetime import datetime

def main():
    print("\n" + "="*80)
    print("       💰 ESTIMATION COÛT LICENCES WINDOWS 2025")
    print("           Vendues en 2024 - À acheter maintenant")
    print("="*80)
    
    # Profils clients identifiés
    clients_profiles = {
        "PROVENÇALE": {
            "secteur": "ETI Manufacturière",
            "ca": "59,5M€",
            "effectif": 200,
            "serveurs_estimes": 8,  # HOST01-07 + backup
            "infrastructure": "Hyper-V, migration Windows 2022",
            "budget_it": "275k€/an"
        },
        "LAA": {
            "secteur": "Automatismes industriels",
            "ca": "18,5M€", 
            "effectif": 35,
            "serveurs_estimes": 4,  # Environnement SalesLogix + prod
            "infrastructure": "Windows Server, SalesLogix, SQL",
            "budget_it": "23k€/an"
        },
        "PETRAS": {
            "secteur": "Équipements hydrauliques", 
            "ca": "3,2M€",
            "effectif": 25,
            "serveurs_estimes": 2,  # Serveur principal + backup
            "infrastructure": "PME, infrastructure basique",
            "budget_it": "10k€/an"
        }
    }
    
    # Tarifs licences Windows 2025 (estimation marché)
    tarifs_licences = {
        "windows_server_2025_standard": {
            "prix_unitaire": 950,  # €HT par licence
            "description": "Windows Server 2025 Standard (16 cœurs)"
        },
        "windows_server_2025_datacenter": {
            "prix_unitaire": 6800,  # €HT par licence
            "description": "Windows Server 2025 Datacenter (16 cœurs)"
        },
        "windows_client_2025_pro": {
            "prix_unitaire": 280,  # €HT par licence
            "description": "Windows 11 Pro 2025"
        },
        "sql_server_2025_std": {
            "prix_unitaire": 3500,  # €HT par licence
            "description": "SQL Server 2025 Standard"
        }
    }
    
    print("\n📊 PROFILS CLIENTS")
    print("-" * 60)
    
    estimations = {}
    
    for client, profile in clients_profiles.items():
        print(f"\n🏢 {client}")
        print(f"   Secteur: {profile['secteur']}")
        print(f"   CA: {profile['ca']} | Effectif: {profile['effectif']} personnes")
        print(f"   Serveurs estimés: {profile['serveurs_estimes']}")
        print(f"   Budget IT: {profile['budget_it']}")
        
        # Estimation licences selon profil
        if client == "PROVENÇALE":
            # ETI avec infrastructure complexe
            licences = {
                "Windows Server 2025 Standard": 6,  # 6 hosts physiques  
                "Windows Server 2025 Datacenter": 2,  # 2 hosts virtualisés
                "Windows 11 Pro 2025": 50,  # 25% parc à renouveler
                "SQL Server 2025 Standard": 2  # 2 instances
            }
        elif client == "LAA":
            # PME industrielle SalesLogix
            licences = {
                "Windows Server 2025 Standard": 3,  # Prod + dev + backup
                "Windows 11 Pro 2025": 20,  # ~50% parc
                "SQL Server 2025 Standard": 1  # SalesLogix DB
            }
        else:  # PETRAS
            # Petite PME
            licences = {
                "Windows Server 2025 Standard": 2,  # Principal + backup
                "Windows 11 Pro 2025": 10  # ~40% parc
            }
        
        # Calculer coûts
        total_ht = 0
        print(f"\n   💡 Estimation licences vendues:")
        
        for licence_type, quantite in licences.items():
            if "Windows Server" in licence_type and "Standard" in licence_type:
                prix_unit = tarifs_licences["windows_server_2025_standard"]["prix_unitaire"]
            elif "Windows Server" in licence_type and "Datacenter" in licence_type:
                prix_unit = tarifs_licences["windows_server_2025_datacenter"]["prix_unitaire"]
            elif "Windows 11" in licence_type:
                prix_unit = tarifs_licences["windows_client_2025_pro"]["prix_unitaire"]
            elif "SQL Server" in licence_type:
                prix_unit = tarifs_licences["sql_server_2025_std"]["prix_unitaire"]
            
            sous_total = quantite * prix_unit
            total_ht += sous_total
            print(f"     • {licence_type}: {quantite}x {prix_unit}€ = {sous_total:,}€")
        
        tva = total_ht * 0.20
        total_ttc = total_ht + tva
        
        estimations[client] = {
            "total_ht": total_ht,
            "tva": tva,
            "total_ttc": total_ttc
        }
        
        print(f"\n   💰 ESTIMATION COÛT:")
        print(f"     Total HT  : {total_ht:,}€")
        print(f"     TVA 20%   : {tva:,}€")
        print(f"     Total TTC : {total_ttc:,}€")
    
    # SYNTHÈSE GLOBALE
    print("\n" + "="*80)
    print("📊 SYNTHÈSE - IMPACT TRÉSORERIE")
    print("="*80)
    
    total_global_ht = sum(e["total_ht"] for e in estimations.values())
    total_global_tva = sum(e["tva"] for e in estimations.values())
    total_global_ttc = sum(e["total_ttc"] for e in estimations.values())
    
    print(f"\nPAR CLIENT:")
    for client, montants in estimations.items():
        print(f"  {client:<12}: {montants['total_ht']:>8,}€ HT ({montants['total_ttc']:>8,}€ TTC)")
    
    print(f"\n" + "-"*50)
    print(f"  {'TOTAL':<12}: {total_global_ht:>8,}€ HT ({total_global_ttc:>8,}€ TTC)")
    
    # Impact sur analyse financière précédente
    print(f"\n📉 IMPACT SUR ANALYSE FINANCIÈRE:")
    print(f"   Excédent apparent précédent : +17,876€/an")
    print(f"   Coût licences à acheter     : -{total_global_ht:,}€")
    print(f"   " + "="*40)
    
    impact_net = 17876 - total_global_ht
    if impact_net > 0:
        print(f"   RESTE EXCÉDENT             : +{impact_net:,}€")
    else:
        print(f"   DEVIENT DÉFICIT            : {impact_net:,}€")
    
    print(f"\n⚠️  DETTE FOURNISSEUR À PROVISIONNER:")
    print(f"   Microsoft/Distributeur     : {total_global_ht:,}€ HT")
    print(f"   TVA récupérable            : {total_global_tva:,}€")
    print(f"   Impact trésorerie nette    : -{total_global_ht:,}€")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    print(f"""
    1. NÉGOCIATION PAIEMENT:
       • Étaler sur 3 mois : {total_global_ttc/3:,.0f}€/mois
       • Négocier 60 jours au lieu de 30
       • Demander remise volume (3 clients)
    
    2. FACTURATION CLIENTS:
       • Vérifier encaissement déjà fait en 2024
       • Si pas encore facturé : facturer immédiatement
       • Appliquer marge habituelle sur coût d'achat
    
    3. TRÉSORERIE:
       • Provisionner {total_global_ht:,}€ d'ici fin août
       • Impact sur projection septembre
       • Évaluer besoin financement pont si nécessaire
    """)
    
    return total_global_ht, total_global_ttc

if __name__ == "__main__":
    cout_ht, cout_ttc = main()
    
    print("\n" + "="*80)
    print("✅ ESTIMATION TERMINÉE")
    print("="*80)
    print(f"""
    DETTE À PROVISIONNER: {cout_ht:,}€ HT
    IMPACT TRÉSORERIE: -{cout_ht:,}€
    
    Cette analyse doit être validée avec les montants réels
    des factures de vente avant mise à jour définitive.
    """)
    print(f"Analyse générée le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
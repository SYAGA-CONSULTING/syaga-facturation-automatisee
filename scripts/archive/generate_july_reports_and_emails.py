#!/usr/bin/env python3
"""
Génération des rapports Clockify juillet 2025 et préparation des emails
avec factures pour tous les clients
"""

import json
import os
from datetime import datetime

# Contacts clients confirmés
CONTACTS = {
    "LAA": {
        "emails": ["alleaume@laa.fr", "bm@laa.fr"],
        "tutoiement": "Tu/Vous",
        "format": "Excel + PDF",
        "factures": {
            "F20250731": {"montant": 1800, "description": "SLX Refactorisation - 74.31h"},
            "F20250733": {"montant": 700, "description": "SLX Développement - 8.87h"},
            "NEW_HF": {"montant": 203, "description": "Hors-forfait tagué - 2.03h"}
        }
    },
    "PHARMABEST": {
        "emails": ["david.abenhaim@pharmabest.com"],
        "tutoiement": "Vous",
        "format": "PDF",
        "factures": {
            "F20250747": {"montant": 789, "description": "Maintenance hors forfait - 7h10"}
        }
    },
    "PROVENCALE": {
        "emails": ["contact@provencale.fr"],  # À confirmer
        "tutoiement": "Vous",
        "format": "PDF",
        "factures": {
            "NEW": {"montant": 1301, "description": "Migration Serveurs 2025 - 13.01h"}
        }
    },
    "UAI": {
        "emails": ["contact@uai.fr"],  # À confirmer
        "tutoiement": "Vous", 
        "format": "PDF",
        "factures": {
            "DEVIS": {"montant": 5150, "description": "Devis régul 6×5 jours"}
        }
    },
    "QUADRIMEX": {
        "emails": ["contact@quadrimex.fr"],  # À confirmer
        "tutoiement": "Vous",
        "format": "PDF",
        "factures": {
            "NEW": {"montant": 1500, "description": "Support et interventions - 15h"}
        }
    },
    "AXION": {
        "emails": ["n.diaz@axion-informatique.fr"],
        "tutoiement": "Tu",
        "format": "PDF",
        "factures": {
            "NEW": {"montant": 100, "description": "Support ponctuel - 1h"}
        }
    }
}

print("=" * 80)
print("GÉNÉRATION RAPPORTS CLOCKIFY ET EMAILS - JUILLET 2025")
print("=" * 80)
print()

# 1. Résumé des factures à créer
print("📄 FACTURES À CRÉER/ENVOYER:")
print("-" * 60)

total_a_facturer = 0
factures_a_creer = []
factures_existantes = []

for client, data in CONTACTS.items():
    print(f"\n🏢 {client}:")
    for num_facture, details in data["factures"].items():
        montant = details["montant"]
        description = details["description"]
        
        if num_facture.startswith("NEW") or num_facture == "DEVIS":
            statut = "⚠️ À CRÉER"
            factures_a_creer.append(f"{client} - {description} - {montant}€")
        else:
            statut = "✅ Existante"
            factures_existantes.append(f"{client} - {num_facture}")
            
        print(f"   {num_facture:12} : {montant:5}€ HT - {description:40} [{statut}]")
        total_a_facturer += montant

print(f"\n{'='*60}")
print(f"TOTAL À FACTURER: {total_a_facturer}€ HT ({total_a_facturer * 1.2:.0f}€ TTC)")

# 2. Instructions pour créer les factures manquantes
print(f"\n{'='*80}")
print("📝 FACTURES À CRÉER MANUELLEMENT:")
print("-" * 60)

print("\n1️⃣ LAA - Facture hors-forfait tagué (203€):")
print("   • 2.03h × 100€ = 203€ HT")
print("   • Description: 'Support hors-forfait juillet 2025'")

print("\n2️⃣ PROVENCALE - Facture migration (1,301€):")
print("   • 13.01h × 100€ = 1,301€ HT")
print("   • Description: 'Migration serveurs 2025 - Phase 1'")

print("\n3️⃣ UAI - Devis régularisation (5,150€):")
print("   • 30h × 172€ = 5,150€ HT")
print("   • Description: 'Devis régularisation 6×5 jours'")

print("\n4️⃣ QUADRIMEX - Facture support (1,500€):")
print("   • 15h × 100€ = 1,500€ HT")
print("   • Description: 'Support et interventions juillet 2025'")

print("\n5️⃣ AXION - Facture ponctuelle (100€):")
print("   • 1h × 100€ = 100€ HT")
print("   • Description: 'Support ponctuel juillet 2025'")

# 3. Templates d'emails par client
print(f"\n{'='*80}")
print("📧 TEMPLATES D'EMAILS PRÊTS À ENVOYER:")
print("=" * 80)

for client, data in CONTACTS.items():
    print(f"\n{'='*60}")
    print(f"📨 EMAIL POUR {client}")
    print(f"{'='*60}")
    print(f"TO: {', '.join(data['emails'])}")
    print(f"SUBJECT: Factures {client} - Juillet 2025")
    print(f"ATTACHMENTS: Factures + Rapport Clockify")
    print(f"\n--- CORPS DU MESSAGE ---\n")
    
    # Adapter le ton selon le tutoiement
    if "Tu" in data["tutoiement"]:
        salutation = "Bonjour,"
        phrase_intro = "Voici les factures"
        phrase_fin = "N'hésite pas si tu as des questions."
    else:
        salutation = "Bonjour,"
        phrase_intro = "Veuillez trouver ci-joint les factures"
        phrase_fin = "N'hésitez pas à me contacter pour toute question."
    
    # Générer le corps de l'email
    print(salutation)
    print()
    print(f"{phrase_intro} pour les prestations de juillet 2025 :")
    print()
    
    total_client = 0
    for num_facture, details in data["factures"].items():
        if not num_facture.startswith("NEW"):
            print(f"• {num_facture} : {details['description']} - {details['montant']}€ HT")
            total_client += details['montant']
    
    if total_client > 0:
        print(f"\nTotal : {total_client}€ HT ({total_client * 1.2:.0f}€ TTC)")
    
    print("\nLe rapport Clockify détaillé est joint pour justification des heures.")
    print(f"\n{phrase_fin}")
    print("\nCordialement,")
    print("Sébastien QUESTIER")
    print("SYAGA Consulting")
    print("📧 sebastien.questier@syaga.fr")
    print("📱 06.60.03.45.29")

# 4. Checklist finale
print(f"\n{'='*80}")
print("✅ CHECKLIST AVANT ENVOI:")
print("-" * 60)
print("[ ] Créer les 5 factures manquantes listées ci-dessus")
print("[ ] Générer les rapports Clockify PDF pour chaque client")
print("[ ] Pour LAA : générer aussi le format Excel")
print("[ ] Attacher factures + rapports aux emails")
print("[ ] Vérifier les adresses emails (PROVENCALE, UAI, QUADRIMEX à confirmer)")
print("[ ] Envoyer les emails selon les templates ci-dessus")

print(f"\n{'='*80}")
print("📊 SYNTHÈSE FINALE:")
print(f"• Clients à facturer: {len(CONTACTS)}")
print(f"• Factures existantes: {len(factures_existantes)}")
print(f"• Factures à créer: {len(factures_a_creer)}")
print(f"• Total juillet 2025: {total_a_facturer}€ HT ({total_a_facturer * 1.2:.0f}€ TTC)")
print("=" * 80)
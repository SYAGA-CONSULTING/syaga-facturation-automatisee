#!/usr/bin/env python3
"""
MISE À JOUR TABLEAU AVEC EMAIL LEFEBVRE
Ajouter l'adresse email trouvée: mjlefebvre@selasu-mjl-avocats.com
"""

import sqlite3
from datetime import datetime

# Connexion à la base de données
conn = sqlite3.connect('data/factures_cache.db')
cursor = conn.cursor()

print('🔄 MISE À JOUR EMAIL LEFEBVRE')
print('='*40)

# Email trouvé pour LEFEBVRE
email_lefebvre = "mjlefebvre@selasu-mjl-avocats.com"

print(f"📧 Email LEFEBVRE: {email_lefebvre}")

# Mettre à jour les factures LEFEBVRE avec l'email trouvé
factures_lefebvre = ['F20250737', 'F20250760']

for facture in factures_lefebvre:
    print(f"\n🔄 Mise à jour {facture}...")
    
    # Vérifier si la facture existe
    cursor.execute("SELECT numero_facture, client_nom, total_ht FROM factures WHERE numero_facture = ?", (facture,))
    result = cursor.fetchone()
    
    if result:
        print(f"   ✅ Trouvée: {result[0]} - {result[1]} - {result[2]}€")
        
        # Mettre à jour avec l'email LEFEBVRE
        cursor.execute("""
        UPDATE factures 
        SET destinataire_client_final = ?,
            statut_envoi_reel = 'NON_ENVOYE',
            type_destinataire = 'CLIENT_POTENTIEL'
        WHERE numero_facture = ?
        """, (email_lefebvre, facture))
        
        print(f"   🎯 Mis à jour avec: {email_lefebvre}")
        
    else:
        print(f"   ❌ {facture} non trouvée en base")

# Commit des changements
conn.commit()
print(f"\n✅ Base de données mise à jour")

# Vérifier les mises à jour
print(f"\n📊 VÉRIFICATION DES FACTURES LEFEBVRE:")
print("-" * 40)

cursor.execute("""
SELECT numero_facture, client_nom, total_ht, destinataire_client_final, statut_envoi_reel
FROM factures 
WHERE client_nom = 'LEFEBVRE'
ORDER BY numero_facture
""")

for row in cursor.fetchall():
    print(f"   {row[0]} - {row[1]} - {row[2]}€ → {row[3]} ({row[4]})")

conn.close()
print(f"\n🎯 Mise à jour terminée - Email LEFEBVRE ajouté")
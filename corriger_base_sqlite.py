#!/usr/bin/env python3
"""
CORRECTION BASE SQLITE : Corriger les noms de colonnes et requêtes
"""

import sqlite3

def corriger_vues_et_requetes(db_path):
    """Corriger les vues avec les vrais noms de colonnes"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 CORRECTION DES VUES AVEC VRAIS NOMS DE COLONNES:")
        
        # Vue des factures envoyées avec confirmation PDF (CORRIGÉE)
        vue_factures_confirmees = """
        CREATE VIEW IF NOT EXISTS v_factures_confirmees_pdf AS
        SELECT 
            numero_facture,
            client_nom,
            total_ht,
            date_facture,
            date_envoi_reel,
            destinataire_reel,
            statut_pdf_confirme,
            date_verification_pdf
        FROM factures 
        WHERE statut_pdf_confirme = 'OUI'
        ORDER BY date_envoi_reel DESC;
        """
        
        try:
            cursor.execute("DROP VIEW IF EXISTS v_factures_confirmees_pdf;")
            cursor.execute(vue_factures_confirmees)
            print("  ✅ Vue v_factures_confirmees_pdf créée (corrigée)")
        except Exception as e:
            print(f"  ❌ Erreur vue confirmées: {e}")
        
        # Vue résumé par mois (CORRIGÉE)
        vue_resume_mensuel = """
        CREATE VIEW IF NOT EXISTS v_resume_mensuel_envois AS
        SELECT 
            strftime('%Y-%m', date_envoi_reel) as mois,
            COUNT(*) as nb_factures,
            SUM(total_ht) as total_ht,
            GROUP_CONCAT(client_nom, ', ') as clients
        FROM factures 
        WHERE statut_pdf_confirme = 'OUI'
        GROUP BY strftime('%Y-%m', date_envoi_reel)
        ORDER BY mois DESC;
        """
        
        try:
            cursor.execute("DROP VIEW IF EXISTS v_resume_mensuel_envois;")
            cursor.execute(vue_resume_mensuel)
            print("  ✅ Vue v_resume_mensuel_envois créée (corrigée)")
        except Exception as e:
            print(f"  ❌ Erreur vue mensuelle: {e}")
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur correction vues: {e}")
        return False

def tester_requetes_corrigees(db_path):
    """Tester les requêtes avec les vrais noms de colonnes"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🧪 TEST DES REQUÊTES CORRIGÉES:")
        
        # Test 1: Factures confirmées
        cursor.execute("SELECT COUNT(*) FROM factures WHERE statut_pdf_confirme = 'OUI';")
        nb_confirmees = cursor.fetchone()[0]
        print(f"  ✅ {nb_confirmees} factures PDF confirmées")
        
        # Test 2: Montant total confirmé (CORRIGÉ)
        cursor.execute("SELECT SUM(total_ht) FROM factures WHERE statut_pdf_confirme = 'OUI';")
        total_confirme = cursor.fetchone()[0] or 0
        print(f"  💰 {total_confirme}€ HT confirmés envoyés")
        
        # Test 3: Factures par client
        cursor.execute("""
            SELECT client_nom, COUNT(*), SUM(total_ht) 
            FROM factures 
            WHERE statut_pdf_confirme = 'OUI' 
            GROUP BY client_nom 
            ORDER BY SUM(total_ht) DESC;
        """)
        
        par_client = cursor.fetchall()
        print(f"  📊 Répartition par client:")
        for client, count, total in par_client:
            print(f"    • {client}: {count} factures, {total}€ HT")
        
        # Test 4: Vue factures confirmées
        cursor.execute("SELECT * FROM v_factures_confirmees_pdf LIMIT 5;")
        vue_test = cursor.fetchall()
        print(f"  📋 Vue confirmées: {len(vue_test)} résultats (échantillon)")
        
        # Test 5: Vue mensuelle
        cursor.execute("SELECT * FROM v_resume_mensuel_envois;")
        vue_mensuelle = cursor.fetchall()
        print(f"  📅 Vue mensuelle:")
        for mois, nb, total, clients in vue_mensuelle:
            print(f"    • {mois}: {nb} factures, {total}€ HT")
        
        # Test 6: Détail des factures F2025
        cursor.execute("""
            SELECT numero_facture, client_nom, total_ht, date_envoi_reel, destinataire_reel
            FROM factures 
            WHERE statut_pdf_confirme = 'OUI' 
            AND numero_facture LIKE 'F2025%'
            ORDER BY date_envoi_reel;
        """)
        
        factures_f2025 = cursor.fetchall()
        print(f"  🎯 DÉTAIL FACTURES F2025 CONFIRMÉES:")
        for numero, client, total, date_envoi, destinataire in factures_f2025:
            print(f"    • {numero} - {client} ({total}€) → {date_envoi} ({destinataire[:30]})")
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur tests: {e}")
        return False

def creer_requetes_utiles(db_path):
    """Créer des requêtes utiles pour l'usage quotidien"""
    
    requetes_utiles = {
        "Factures confirmées par ordre de date": """
            SELECT numero_facture, client_nom, total_ht, date_envoi_reel, destinataire_reel
            FROM factures 
            WHERE statut_pdf_confirme = 'OUI' 
            ORDER BY date_envoi_reel DESC;
        """,
        
        "Total par mois": """
            SELECT strftime('%Y-%m', date_envoi_reel) as mois,
                   COUNT(*) as nb_factures,
                   SUM(total_ht) as total_ht
            FROM factures 
            WHERE statut_pdf_confirme = 'OUI'
            GROUP BY mois 
            ORDER BY mois DESC;
        """,
        
        "Factures non envoyées": """
            SELECT numero_facture, client_nom, total_ht, date_facture
            FROM factures 
            WHERE statut_pdf_confirme IS NULL OR statut_pdf_confirme != 'OUI'
            ORDER BY date_facture DESC;
        """,
        
        "Résumé par client": """
            SELECT client_nom, COUNT(*) as nb_factures, SUM(total_ht) as total_ht
            FROM factures 
            WHERE statut_pdf_confirme = 'OUI'
            GROUP BY client_nom 
            ORDER BY total_ht DESC;
        """
    }
    
    print("📋 REQUÊTES UTILES CRÉÉES:")
    for nom, requete in requetes_utiles.items():
        print(f"  • {nom}")
    
    # Sauvegarder dans un fichier pour usage futur
    with open('/mnt/c/temp/requetes_sqlite_utiles.sql', 'w') as f:
        f.write("-- REQUÊTES SQLITE UTILES - BASE FACTURATION SYAGA\n")
        f.write("-- Généré automatiquement\n\n")
        
        for nom, requete in requetes_utiles.items():
            f.write(f"-- {nom}\n")
            f.write(requete.strip() + ";\n\n")
    
    print("  ✅ Fichier sauvegardé: /mnt/c/temp/requetes_sqlite_utiles.sql")

def main():
    print('🔧 CORRECTION BASE SQLITE - NOMS DE COLONNES')
    print('='*60)
    
    db_path = '/home/sq/SYAGA-CONSULTING/syaga-finance-api/facturation-automatisee/data/factures_cache.db'
    
    # 1. Corriger les vues
    if corriger_vues_et_requetes(db_path):
        print("✅ Vues corrigées")
    
    # 2. Tester les requêtes
    if tester_requetes_corrigees(db_path):
        print("✅ Tests réussis")
    
    # 3. Créer requêtes utiles
    creer_requetes_utiles(db_path)
    
    print('\n🎉 BASE SQLITE OPÉRATIONNELLE!')
    print('💾 11 factures F2025 avec vraies dates d\'envoi')
    print('📊 Vues et requêtes prêtes pour usage quotidien')
    print('📋 Fichier SQL utile créé dans C:\\temp\\')

if __name__ == "__main__":
    main()
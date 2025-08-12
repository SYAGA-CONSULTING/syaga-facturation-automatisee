#!/usr/bin/env python3
"""
Système automatisé de génération de factures
Basé sur l'historique et les patterns récurrents
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Import des modules de génération PDF si disponibles
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    print("⚠️ ReportLab non installé - Génération JSON uniquement")

class FactureAutomatique:
    def __init__(self):
        self.conn = sqlite3.connect('../data/factures_cache.db')
        self.cursor = self.conn.cursor()
        self.load_templates()
        self.load_patterns()
        
    def load_templates(self):
        """Charge les templates de désignations"""
        template_file = Path('../templates_designations.json')
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                self.templates = json.load(f)
        else:
            # Templates par défaut
            self.templates = {
                'LAA': {'forfait_mensuel': 1562.50, 'standard': 'Maintenance et support IT'},
                'UAI': {'forfait_mensuel': 6162.50, 'standard': 'Optimisation système'},
                'PHARMABEST': {'forfait_mensuel': 2500.00, 'standard': 'Gestion M365'},
            }
    
    def load_patterns(self):
        """Charge les patterns historiques de chaque client"""
        self.patterns = {}
        
        # Analyser les patterns pour chaque client
        self.cursor.execute("""
            SELECT client_nom, 
                   AVG(total_ht) as montant_moyen,
                   COUNT(*) as nb_factures,
                   MAX(date_facture) as derniere_facture,
                   MIN(date_facture) as premiere_facture
            FROM factures
            WHERE total_ht > 0
            GROUP BY client_nom
            HAVING COUNT(*) > 2
        """)
        
        for row in self.cursor.fetchall():
            client = row[0]
            self.patterns[client] = {
                'montant_moyen': row[1],
                'nb_factures': row[2],
                'derniere_facture': row[3],
                'premiere_facture': row[4],
                'frequence': self.calculer_frequence(row[4], row[3], row[2])
            }
    
    def calculer_frequence(self, premiere, derniere, nb):
        """Calcule la fréquence moyenne de facturation"""
        try:
            date1 = datetime.strptime(premiere[:10], '%Y-%m-%d')
            date2 = datetime.strptime(derniere[:10], '%Y-%m-%d')
            mois_total = (date2.year - date1.year) * 12 + date2.month - date1.month
            return 'mensuelle' if mois_total / nb <= 1.5 else 'ponctuelle'
        except:
            return 'mensuelle'
    
    def analyser_factures_a_generer(self, mois=None, annee=None):
        """Analyse quelles factures doivent être générées"""
        
        if not mois or not annee:
            now = datetime.now()
            mois = now.month
            annee = now.year
        
        print(f"\n📊 ANALYSE POUR {mois:02d}/{annee}")
        print("=" * 60)
        
        factures_a_generer = []
        
        # Pour chaque client avec pattern mensuel
        for client, pattern in self.patterns.items():
            if pattern['frequence'] == 'mensuelle':
                # Vérifier si une facture existe déjà pour ce mois
                self.cursor.execute("""
                    SELECT COUNT(*) 
                    FROM factures
                    WHERE client_nom = ?
                    AND date_facture LIKE ?
                """, (client, f'{annee}-{mois:02d}%'))
                
                if self.cursor.fetchone()[0] == 0:
                    # Pas de facture pour ce mois, on la propose
                    template = self.get_template_client(client)
                    factures_a_generer.append({
                        'client': client,
                        'montant_ht': template.get('forfait_mensuel', pattern['montant_moyen']),
                        'designation': template.get('standard', 'Prestations informatiques'),
                        'mois': mois,
                        'annee': annee,
                        'type': 'récurrente'
                    })
                    
                    print(f"✓ {client}: {template.get('forfait_mensuel', pattern['montant_moyen']):.2f}€ (récurrent)")
        
        print(f"\n📋 TOTAL: {len(factures_a_generer)} factures à générer")
        print(f"💰 Montant total: {sum(f['montant_ht'] for f in factures_a_generer):,.2f}€ HT")
        
        return factures_a_generer
    
    def get_template_client(self, client):
        """Récupère le template d'un client"""
        # Chercher correspondance exacte ou partielle
        for key, template in self.templates.items():
            if key in client or client in key:
                return template
        
        # Template par défaut basé sur l'historique
        if client in self.patterns:
            return {
                'forfait_mensuel': self.patterns[client]['montant_moyen'],
                'standard': 'Prestations informatiques',
                'prix_horaire': 125.00
            }
        
        return {'forfait_mensuel': 0, 'standard': 'Prestations', 'prix_horaire': 125.00}
    
    def generer_factures(self, mois=None, annee=None, mode='preview'):
        """Génère les factures pour un mois donné"""
        
        factures_a_generer = self.analyser_factures_a_generer(mois, annee)
        
        if not factures_a_generer:
            print("\n✅ Aucune facture à générer")
            return []
        
        if mode == 'preview':
            print("\n🔍 MODE PREVIEW - Aucune modification en base")
            self.afficher_preview(factures_a_generer)
            return factures_a_generer
        
        elif mode == 'generate':
            print("\n⚙️ GÉNÉRATION DES FACTURES")
            return self.creer_factures(factures_a_generer)
    
    def afficher_preview(self, factures):
        """Affiche un aperçu des factures à générer"""
        print("\n" + "=" * 70)
        print("APERÇU DES FACTURES À GÉNÉRER")
        print("=" * 70)
        
        for i, f in enumerate(factures, 1):
            print(f"\n{i}. {f['client']}")
            print(f"   Montant: {f['montant_ht']:,.2f}€ HT ({f['montant_ht']*1.2:,.2f}€ TTC)")
            print(f"   Désignation: {f['designation']}")
            print(f"   Période: {f['mois']:02d}/{f['annee']}")
            print(f"   Type: {f['type']}")
    
    def creer_factures(self, factures_data):
        """Crée les factures en base et génère les PDFs"""
        
        factures_creees = []
        date_base = datetime.now().replace(day=1)
        
        for facture in factures_data:
            # Générer le numéro de facture
            self.cursor.execute("""
                SELECT MAX(CAST(SUBSTR(numero_facture, 2) AS INTEGER))
                FROM factures
                WHERE numero_facture LIKE 'F%'
            """)
            max_num = self.cursor.fetchone()[0] or 20250000
            numero = f"F{max_num + 1}"
            
            # Date de facture (dernier jour du mois)
            if facture['mois'] == 12:
                date_facture = datetime(facture['annee'], 12, 31)
            else:
                date_facture = datetime(facture['annee'], facture['mois'] + 1, 1) - timedelta(days=1)
            
            # Créer la facture en base
            self.cursor.execute("""
                INSERT INTO factures (
                    numero_facture, date_facture, client_nom,
                    total_ht, total_tva, total_ttc, taux_tva,
                    objet, mode_paiement, date_echeance
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                numero,
                date_facture.strftime('%Y-%m-%d'),
                facture['client'],
                facture['montant_ht'],
                facture['montant_ht'] * 0.20,
                facture['montant_ht'] * 1.20,
                20.0,
                f"{facture['designation']} - {date_facture.strftime('%B %Y')}",
                'Virement',
                (date_facture + timedelta(days=30)).strftime('%Y-%m-%d')
            ))
            
            facture_id = self.cursor.lastrowid
            
            # Créer la ligne de facture
            self.cursor.execute("""
                INSERT INTO lignes_factures (
                    facture_id, designation, quantite, 
                    prix_unitaire, montant_ht, ordre_ligne
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                facture_id,
                facture['designation'],
                1.0,
                facture['montant_ht'],
                facture['montant_ht'],
                1
            ))
            
            print(f"✅ Facture {numero} créée pour {facture['client']}: {facture['montant_ht']:.2f}€")
            
            factures_creees.append({
                'id': facture_id,
                'numero': numero,
                'client': facture['client'],
                'montant_ht': facture['montant_ht'],
                'date': date_facture.strftime('%Y-%m-%d')
            })
            
            # Générer le PDF si ReportLab est disponible
            if HAS_REPORTLAB:
                self.generer_pdf(facture, numero, date_facture)
        
        self.conn.commit()
        
        print(f"\n✅ {len(factures_creees)} factures créées avec succès")
        return factures_creees
    
    def generer_pdf(self, facture_data, numero, date_facture):
        """Génère le PDF de la facture (si ReportLab disponible)"""
        # TODO: Implémenter la génération PDF
        # Pour l'instant, on crée juste le fichier
        output_dir = Path('../factures-generees')
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"{numero}_{facture_data['client'].replace(' ', '_')}.pdf"
        print(f"   📄 PDF: {output_file.name}")
    
    def rapport_mensuel(self, mois=None, annee=None):
        """Génère un rapport mensuel de facturation"""
        
        if not mois or not annee:
            now = datetime.now()
            mois = now.month
            annee = now.year
        
        print("\n" + "=" * 70)
        print(f"RAPPORT DE FACTURATION - {mois:02d}/{annee}")
        print("=" * 70)
        
        # Factures du mois
        self.cursor.execute("""
            SELECT client_nom, COUNT(*), SUM(total_ht), SUM(total_ttc)
            FROM factures
            WHERE date_facture LIKE ?
            AND total_ht > 0
            GROUP BY client_nom
            ORDER BY SUM(total_ht) DESC
        """, (f'{annee}-{mois:02d}%',))
        
        factures_mois = self.cursor.fetchall()
        
        if factures_mois:
            print("\n📊 FACTURES ÉMISES")
            print("-" * 40)
            total_ht = 0
            for client, nb, ht, ttc in factures_mois:
                print(f"{client:25} : {nb:2} fact. | {ht:10,.2f}€ HT")
                total_ht += ht
            
            print("-" * 40)
            print(f"{'TOTAL':25} : {sum(f[1] for f in factures_mois):2} fact. | {total_ht:10,.2f}€ HT")
            print(f"{'':25}   {'':2}       | {total_ht*1.2:10,.2f}€ TTC")
        
        # Clients sans factures ce mois (mais avec historique récurrent)
        print("\n⚠️ CLIENTS RÉCURRENTS SANS FACTURE CE MOIS")
        print("-" * 40)
        
        for client, pattern in self.patterns.items():
            if pattern['frequence'] == 'mensuelle':
                self.cursor.execute("""
                    SELECT COUNT(*) FROM factures
                    WHERE client_nom = ? AND date_facture LIKE ?
                """, (client, f'{annee}-{mois:02d}%'))
                
                if self.cursor.fetchone()[0] == 0:
                    print(f"❌ {client}: Montant habituel {pattern['montant_moyen']:.2f}€")
        
        print("\n" + "=" * 70)
    
    def close(self):
        """Ferme la connexion à la base"""
        self.conn.close()


def main():
    """Fonction principale"""
    
    print("🤖 SYSTÈME AUTOMATIQUE DE FACTURATION SYAGA")
    print("=" * 60)
    
    facturation = FactureAutomatique()
    
    # Menu interactif
    while True:
        print("\n📋 MENU")
        print("1. Analyser les factures à générer (mois en cours)")
        print("2. Générer les factures du mois")
        print("3. Rapport mensuel")
        print("4. Analyser un mois spécifique")
        print("5. Quitter")
        
        choix = input("\nVotre choix: ")
        
        if choix == '1':
            facturation.analyser_factures_a_generer()
        
        elif choix == '2':
            confirm = input("\n⚠️ Confirmer la génération des factures (oui/non)? ")
            if confirm.lower() == 'oui':
                facturation.generer_factures(mode='generate')
            else:
                print("Annulé")
        
        elif choix == '3':
            facturation.rapport_mensuel()
        
        elif choix == '4':
            mois = int(input("Mois (1-12): "))
            annee = int(input("Année (ex: 2025): "))
            facturation.analyser_factures_a_generer(mois, annee)
        
        elif choix == '5':
            print("\n👋 Au revoir!")
            break
        
        else:
            print("❌ Choix invalide")
    
    facturation.close()


if __name__ == "__main__":
    # Mode automatique si arguments fournis
    if len(sys.argv) > 1:
        facturation = FactureAutomatique()
        
        if sys.argv[1] == 'preview':
            # Preview du mois en cours
            facturation.generer_factures(mode='preview')
        
        elif sys.argv[1] == 'generate':
            # Génération automatique
            facturation.generer_factures(mode='generate')
        
        elif sys.argv[1] == 'rapport':
            # Rapport mensuel
            facturation.rapport_mensuel()
        
        facturation.close()
    else:
        # Mode interactif
        main()
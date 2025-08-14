#!/usr/bin/env python3
"""
CAPTURE D'ÉCRAN : Email Outlook du 10 juillet Anthony CIMO
"""

import subprocess
import time
from datetime import datetime

def main():
    print('📸 PRÉPARATION CAPTURE D\'ÉCRAN EMAIL OUTLOOK')
    print('='*50)
    
    # Générer nom de fichier avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"/mnt/c/temp/outlook_email_10juillet_cimo_{timestamp}.png"
    
    print(f"🎯 INSTRUCTIONS POUR L'UTILISATEUR:")
    print(f"1. Ouvre Outlook/OWA dans Windows")
    print(f"2. Navigue vers l'email du 10 juillet à Anthony CIMO")
    print(f"3. Assure-toi que les pièces jointes sont visibles")
    print(f"4. Lance la capture dans 10 secondes...")
    
    # Compte à rebours
    for i in range(10, 0, -1):
        print(f"⏳ {i}...")
        time.sleep(1)
    
    # Prendre la capture d'écran avec l'outil Snipping Tool Windows
    try:
        print("📸 Capture d'écran en cours...")
        
        # Utiliser PowerShell pour prendre la capture
        ps_command = f"""
        Add-Type -AssemblyName System.Windows.Forms,System.Drawing
        $bounds = [Drawing.Rectangle]::FromLTRB(0, 0, 1920, 1080)
        $bmp = New-Object Drawing.Bitmap $bounds.width, $bounds.height
        $graphics = [Drawing.Graphics]::FromImage($bmp)
        $graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size)
        $bmp.Save('{screenshot_path.replace('/mnt/c', 'C:')}', [Drawing.Imaging.ImageFormat]::Png)
        $graphics.Dispose()
        $bmp.Dispose()
        """
        
        # Exécuter la commande PowerShell
        result = subprocess.run([
            '/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe',
            '-Command', ps_command
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Capture sauvegardée: {screenshot_path}")
            print(f"🔍 Prêt pour analyse d'image avec Claude Code")
            
            # Retourner le chemin pour analyse
            return screenshot_path.replace('/mnt/c', 'C:')
        else:
            print(f"❌ Erreur capture: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

if __name__ == "__main__":
    screenshot_path = main()
    if screenshot_path:
        print(f"\n📋 PROCHAINE ÉTAPE:")
        print(f"Utiliser Read tool pour analyser: {screenshot_path}")
#!/usr/bin/env python3
"""
CAPTURE D'ÉCRAN : Écran secondaire avec email Outlook
"""

import subprocess
import time
from datetime import datetime

def main():
    print('📸 CAPTURE ÉCRAN SECONDAIRE - EMAIL OUTLOOK')
    print('='*50)
    
    # Générer nom de fichier avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"/mnt/c/temp/ecran_secondaire_outlook_{timestamp}.png"
    
    try:
        print("📸 Capture de l'écran secondaire en cours...")
        
        # PowerShell pour capturer écran secondaire (écran 2)
        ps_command = f"""
        Add-Type -AssemblyName System.Windows.Forms,System.Drawing
        $screen = [System.Windows.Forms.Screen]::AllScreens[1]
        $bounds = $screen.Bounds
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
            print(f"✅ Capture écran secondaire: {screenshot_path}")
            return screenshot_path
        else:
            print(f"❌ Erreur capture: {result.stderr}")
            print("🔄 Tentative capture tous écrans...")
            
            # Fallback: capturer tous les écrans
            ps_command_all = f"""
            Add-Type -AssemblyName System.Windows.Forms,System.Drawing
            $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
            foreach ($screen in [System.Windows.Forms.Screen]::AllScreens) {{
                $bounds = [Drawing.Rectangle]::Union($bounds, $screen.Bounds)
            }}
            $bmp = New-Object Drawing.Bitmap $bounds.width, $bounds.height
            $graphics = [Drawing.Graphics]::FromImage($bmp)
            $graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size)
            $bmp.Save('{screenshot_path.replace('/mnt/c', 'C:')}', [Drawing.Imaging.ImageFormat]::Png)
            $graphics.Dispose()
            $bmp.Dispose()
            """
            
            result2 = subprocess.run([
                '/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe',
                '-Command', ps_command_all
            ], capture_output=True, text=True)
            
            if result2.returncode == 0:
                print(f"✅ Capture tous écrans: {screenshot_path}")
                return screenshot_path
            else:
                print(f"❌ Erreur capture complète: {result2.stderr}")
                return None
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

if __name__ == "__main__":
    screenshot_path = main()
    if screenshot_path:
        print(f"\n🔍 ANALYSE AVEC CLAUDE CODE:")
        print(f"Read file: {screenshot_path}")
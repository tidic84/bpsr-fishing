"""
Script de calibration pour l'automatisation de pêche
Permet de capturer les images de référence nécessaires pour la détection
"""

import pyautogui
import cv2
import numpy as np
from PIL import Image
import os
import time

class CalibrationTool:
    def __init__(self):
        self.images_dir = "images_reference"
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
    
    def capture_region(self, name, description):
        """Capture une région de l'écran sélectionnée par l'utilisateur"""
        print(f"\n{'='*60}")
        print(f"CAPTURE: {description}")
        print(f"{'='*60}")
        print("\nInstructions:")
        print("1. Positionnez votre jeu de manière à ce que l'élément soit visible")
        print("2. Appuyez sur ENTRÉE pour commencer la capture")
        print("3. Vous aurez 3 secondes pour positionner votre souris")
        print("4. Cliquez et faites glisser pour sélectionner la zone")
        
        input("\nAppuyez sur ENTRÉE pour commencer...")
        print("Préparation... Positionnez-vous sur le jeu!")
        
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        print("\n✓ Prenez une capture d'écran maintenant!")
        print("  Utilisez l'outil de capture Windows (Win + Shift + S)")
        print("  OU appuyez sur F12 après avoir sélectionné manuellement la zone")
        print("\nAppuyez sur ENTRÉE une fois la capture faite...")
        input()
        
        # Alternative: capture de coordonnées manuelles
        print("\nVoulez-vous saisir les coordonnées manuellement? (o/n)")
        manual = input().lower()
        
        if manual == 'o':
            print("\nDéplacez votre souris en haut à gauche de la zone et appuyez sur ENTRÉE")
            input()
            x1, y1 = pyautogui.position()
            print(f"Position enregistrée: ({x1}, {y1})")
            
            print("\nDéplacez votre souris en bas à droite de la zone et appuyez sur ENTRÉE")
            input()
            x2, y2 = pyautogui.position()
            print(f"Position enregistrée: ({x2}, {y2})")
            
            # Capture de la région
            screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
            filepath = os.path.join(self.images_dir, f"{name}.png")
            screenshot.save(filepath)
            print(f"\n✓ Image sauvegardée: {filepath}")
            
            # Afficher un aperçu
            img = cv2.imread(filepath)
            if img is not None:
                cv2.imshow(f"Aperçu - {description}", img)
                print("\nAppuyez sur une touche dans la fenêtre d'aperçu pour continuer...")
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            
            return True
        else:
            print(f"\n⚠ Veuillez sauvegarder manuellement l'image comme: {self.images_dir}/{name}.png")
            return False
    
    def capture_click_position(self, name, description):
        """Capture une position de clic"""
        print(f"\n{'='*60}")
        print(f"POSITION DE CLIC: {description}")
        print(f"{'='*60}")
        print("\nInstructions:")
        print("1. Positionnez votre jeu")
        print("2. Appuyez sur ENTRÉE pour commencer")
        print("3. Vous aurez 3 secondes")
        print("4. Placez votre souris à l'endroit exact où cliquer")
        
        input("\nAppuyez sur ENTRÉE pour commencer...")
        
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        x, y = pyautogui.position()
        print(f"\n✓ Position capturée: ({x}, {y})")
        
        # Sauvegarder dans un fichier de configuration
        config_file = os.path.join(self.images_dir, "positions.txt")
        with open(config_file, "a", encoding="utf-8") as f:
            f.write(f"{name}={x},{y}\n")
        
        print(f"✓ Position sauvegardée dans {config_file}")
        return x, y
    
    def run_calibration(self):
        """Lance le processus de calibration complet"""
        print("\n" + "="*60)
        print(" OUTIL DE CALIBRATION - AUTOMATISATION DE PÊCHE")
        print("="*60)
        
        print("\nCet outil va vous aider à capturer les éléments nécessaires:")
        print("1. Le point d'exclamation (!) qui apparaît")
        print("2. Le bouton 'Continue'")
        print("3. (Optionnel) La position de clic initiale")
        
        input("\nAppuyez sur ENTRÉE pour commencer la calibration...")
        
        # Capture 1: Point d'exclamation
        self.capture_region(
            "exclamation_point",
            "Point d'exclamation (!)"
        )
        
        # Capture 2: Bouton Continue
        self.capture_region(
            "button_continue",
            "Bouton 'Continue'"
        )
        
        # Capture 3: Bouton Exit (optionnel)
        print("\nVoulez-vous aussi capturer le bouton 'Exit'? (o/n)")
        if input().lower() == 'o':
            self.capture_region(
                "button_exit",
                "Bouton 'Exit'"
            )
        
        # Position de clic pour commencer la pêche
        print("\nVoulez-vous enregistrer une position de clic pour commencer la pêche? (o/n)")
        if input().lower() == 'o':
            self.capture_click_position(
                "fishing_start",
                "Position pour commencer la pêche"
            )
        
        print("\n" + "="*60)
        print(" ✓ CALIBRATION TERMINÉE!")
        print("="*60)
        print(f"\nVos images sont sauvegardées dans: {self.images_dir}/")
        print("\nVous pouvez maintenant utiliser le script principal: fishing_bot.py")
        print("\nConseils:")
        print("- Vérifiez que les images capturées sont claires")
        print("- Évitez de capturer trop de zone autour des éléments")
        print("- Gardez la même résolution de jeu lors de l'utilisation du bot")

if __name__ == "__main__":
    calibrator = CalibrationTool()
    try:
        calibrator.run_calibration()
    except KeyboardInterrupt:
        print("\n\n⚠ Calibration interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()


"""
Bot d'automatisation de pêche - VERSION AVEC LIBÉRATION ESC
Pour les jeux où la souris est capturée mais ESC la libère
"""

import pyautogui
import cv2
import numpy as np
from PIL import Image
import time
import os
import sys
from datetime import datetime
import keyboard

class FishingBotWithESC:
    def __init__(self, release_key='esc', confidence=0.8):
        """
        Initialise le bot de pêche avec libération de souris
        
        Args:
            release_key: Touche pour libérer la souris (défaut: 'esc')
            confidence: Niveau de confiance pour la détection d'images (0.0 à 1.0)
        """
        self.release_key = release_key
        self.confidence = confidence
        self.images_dir = "images_reference"
        self.running = False
        self.stats = {
            "fish_caught": 0,
            "fishing_attempts": 0,
            "start_time": None,
            "errors": 0
        }
        
        # Charger les images de référence
        self.templates = {}
        self.load_templates()
        
        # Charger les positions
        self.positions = {}
        self.load_positions()
        
        # Configuration
        self.wait_after_click = 0.5
        self.release_delay = 0.3  # Délai après libération de souris
        self.return_delay = 0.3   # Délai après retour en jeu
        self.exclamation_timeout = 30
        self.continue_button_timeout = 10
        self.qte_wait_time = 8
        
        print("\n" + "="*60)
        print(" BOT DE PÊCHE - MODE AVEC LIBÉRATION ESC")
        print("="*60)
        print(f"Touche de libération: {self.release_key.upper()}")
        print(f"Confiance de détection: {confidence*100}%")
        print(f"Images chargées: {len(self.templates)}")
        print(f"Positions chargées: {len(self.positions)}")
        print("\nTouche d'arrêt d'urgence: F1")
        print("="*60 + "\n")
    
    def load_templates(self):
        """Charge les images de référence pour la détection"""
        template_files = {
            "exclamation": "exclamation_point.png",
            "continue": "button_continue.png",
        }
        
        for key, filename in template_files.items():
            filepath = os.path.join(self.images_dir, filename)
            if os.path.exists(filepath):
                img = cv2.imread(filepath)
                if img is not None:
                    self.templates[key] = img
                    print(f"✓ Image chargée: {filename}")
        
        if not self.templates:
            print("\n❌ ERREUR: Aucune image de référence trouvée!")
            print("   Veuillez exécuter calibration.py d'abord.\n")
            sys.exit(1)
    
    def load_positions(self):
        """Charge les positions de clic depuis le fichier de configuration"""
        config_file = os.path.join(self.images_dir, "positions.txt")
        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line:
                        name, coords = line.split("=")
                        x, y = coords.split(",")
                        self.positions[name] = (int(x), int(y))
                        print(f"✓ Position chargée: {name} = ({x}, {y})")
    
    def find_on_screen(self, template_key, region=None, timeout=5):
        """Cherche une image template sur l'écran"""
        if template_key not in self.templates:
            return None
        
        template = self.templates[template_key]
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if keyboard.is_pressed('f1'):  # F1 au lieu de ESC
                print("\n⚠ Arrêt demandé par l'utilisateur (F1)")
                self.running = False
                return None
            
            screenshot = pyautogui.screenshot(region=region)
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= self.confidence:
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                
                if region:
                    center_x += region[0]
                    center_y += region[1]
                
                return (center_x, center_y)
            
            time.sleep(0.1)
        
        return None
    
    def click_with_release(self, x=None, y=None, position_name=None):
        """
        Effectue un clic en libérant d'abord la souris
        
        Args:
            x, y: Coordonnées du clic, ou
            position_name: Nom d'une position pré-enregistrée
        """
        if position_name and position_name in self.positions:
            x, y = self.positions[position_name]
        
        if x is None or y is None:
            print("⚠ Position de clic invalide")
            return False
        
        try:
            # 1. Libérer la souris
            print(f"  → Libération de la souris ({self.release_key.upper()})...")
            pyautogui.press(self.release_key)
            time.sleep(self.release_delay)
            
            # 2. Déplacer et cliquer
            print(f"  → Déplacement vers ({x}, {y})...")
            pyautogui.moveTo(x, y, duration=0.2)
            time.sleep(0.1)
            
            print(f"  → Clic gauche...")
            pyautogui.click(x, y, button='left')
            print(f"  ✓ Clic effectué!")
            time.sleep(self.wait_after_click)
            
            # 3. Revenir en jeu (optionnel - le clic peut suffire)
            # Décommentez si nécessaire :
            # print(f"  → Retour en jeu ({self.release_key.upper()})...")
            # pyautogui.press(self.release_key)
            # time.sleep(self.return_delay)
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du clic: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def safe_click(self, x, y):
        """Clic simple pour les menus (souris déjà libre)"""
        try:
            print(f"  → Clic à ({x}, {y})...")
            pyautogui.click(x, y, button='left')
            print(f"  ✓ Clic effectué!")
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"❌ Erreur lors du clic: {e}")
            return False
    
    def fishing_cycle(self):
        """Exécute un cycle complet de pêche"""
        try:
            # Étape 1: Cliquer pour commencer la pêche (avec libération)
            print("\n[Étape 1] Démarrage de la pêche...")
            self.stats["fishing_attempts"] += 1
            
            if "fishing_start" in self.positions:
                click_success = self.click_with_release(position_name="fishing_start")
            else:
                screen_width, screen_height = pyautogui.size()
                print(f"  ℹ Aucune position enregistrée, clic au centre")
                click_success = self.click_with_release(screen_width // 2, screen_height // 2)
            
            if not click_success:
                print("  ⚠ Le clic de démarrage a échoué, nouvelle tentative...")
                time.sleep(1)
                return False
            
            time.sleep(0.5)
            
            # Étape 2: Attendre et détecter le point d'exclamation
            print("[Étape 2] Attente du point d'exclamation...")
            exclamation_pos = self.find_on_screen("exclamation", timeout=self.exclamation_timeout)
            
            if exclamation_pos is None:
                print("⚠ Point d'exclamation non détecté - Timeout")
                self.stats["errors"] += 1
                time.sleep(2)
                return False
            
            print(f"✓ Point d'exclamation détecté à {exclamation_pos}")
            
            # Cliquer sur le point d'exclamation (avec libération si nécessaire)
            # Note: Parfois le point d'exclamation apparaît dans un menu (souris libre)
            # Essayons d'abord sans libération
            self.safe_click(*exclamation_pos)
            
            # Étape 3: Attendre le QTE ou le succès direct
            print("[Étape 3] Attente du résultat (QTE ou succès direct)...")
            time.sleep(self.qte_wait_time)
            
            # Étape 4: Chercher le bouton Continue
            print("[Étape 4] Recherche du bouton Continue...")
            continue_pos = self.find_on_screen("continue", timeout=self.continue_button_timeout)
            
            if continue_pos is None:
                print("⚠ Bouton Continue non détecté - Nouvelle tentative...")
                time.sleep(3)
                continue_pos = self.find_on_screen("continue", timeout=5)
            
            if continue_pos:
                print(f"✓ Bouton Continue détecté à {continue_pos}")
                self.safe_click(*continue_pos)
                self.stats["fish_caught"] += 1
                print(f"🎣 Poisson pêché! Total: {self.stats['fish_caught']}")
                time.sleep(1)
                return True
            else:
                print("⚠ Impossible de trouver le bouton Continue")
                self.stats["errors"] += 1
                pyautogui.press('esc')
                time.sleep(1)
                return False
                
        except Exception as e:
            print(f"❌ Erreur dans le cycle de pêche: {e}")
            self.stats["errors"] += 1
            return False
    
    def print_stats(self):
        """Affiche les statistiques"""
        if self.stats["start_time"]:
            elapsed = time.time() - self.stats["start_time"]
            elapsed_min = elapsed / 60
            fish_per_hour = (self.stats["fish_caught"] / elapsed * 3600) if elapsed > 0 else 0
            
            print("\n" + "="*60)
            print(" STATISTIQUES")
            print("="*60)
            print(f"Poissons pêchés: {self.stats['fish_caught']}")
            print(f"Tentatives totales: {self.stats['fishing_attempts']}")
            print(f"Erreurs: {self.stats['errors']}")
            print(f"Temps écoulé: {elapsed_min:.1f} minutes")
            print(f"Taux: {fish_per_hour:.1f} poissons/heure")
            print("="*60 + "\n")
    
    def run(self, max_cycles=None):
        """Lance le bot"""
        print("\n🎣 Démarrage du bot de pêche (MODE AVEC LIBÉRATION)...")
        print("⚠ Assurez-vous que le jeu est au premier plan!")
        print(f"⚠ Le bot utilisera {self.release_key.upper()} pour libérer la souris")
        print("\nLe bot démarrera dans 5 secondes...")
        print("(Appuyez sur F1 à tout moment pour arrêter)\n")
        
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        self.running = True
        self.stats["start_time"] = time.time()
        cycle_count = 0
        
        print("\n🚀 Bot démarré!\n")
        
        try:
            while self.running:
                if max_cycles and cycle_count >= max_cycles:
                    print(f"\n✓ Nombre maximum de cycles atteint ({max_cycles})")
                    break
                
                cycle_count += 1
                print(f"\n{'='*60}")
                print(f" CYCLE #{cycle_count}")
                print(f"{'='*60}")
                
                self.fishing_cycle()
                
                if cycle_count % 10 == 0:
                    self.print_stats()
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n⚠ Interruption par l'utilisateur (Ctrl+C)")
        finally:
            self.running = False
            self.print_stats()
            print("\n✓ Bot arrêté proprement")

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print(" BOT D'AUTOMATISATION DE PÊCHE - MODE LIBÉRATION")
    print("="*60)
    
    # Configuration de la touche de libération
    print("\nQuelle touche libère la souris dans votre jeu?")
    print("(Généralement: esc, tab, ou alt)")
    
    release_key = input("\nTouche de libération [défaut: esc]: ").strip().lower()
    if not release_key:
        release_key = 'esc'
    
    print(f"\n✓ Touche de libération: {release_key.upper()}")
    
    # Configuration de la confiance
    print("\nMode de détection:")
    print("1. Mode normal (confiance 80%)")
    print("2. Mode précis (confiance 90%)")
    print("3. Mode souple (confiance 70%)")
    
    choice = input("\nChoisissez un mode (1-3) [défaut: 1]: ").strip()
    
    confidence_map = {
        "1": 0.8,
        "2": 0.9,
        "3": 0.7,
        "": 0.8
    }
    confidence = confidence_map.get(choice, 0.8)
    
    # Nombre de cycles
    print("\nNombre de cycles de pêche:")
    max_cycles_input = input("(Appuyez sur ENTRÉE pour illimité): ").strip()
    max_cycles = int(max_cycles_input) if max_cycles_input.isdigit() else None
    
    # Créer et lancer le bot
    bot = FishingBotWithESC(release_key=release_key, confidence=confidence)
    bot.run(max_cycles=max_cycles)

if __name__ == "__main__":
    main()


"""
Bot d'automatisation de pêche - VERSION CLAVIER
Pour les jeux où la souris est capturée et qui utilisent des touches pour pêcher
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

class FishingBotKeyboard:
    def __init__(self, fishing_key='e', confidence=0.8):
        """
        Initialise le bot de pêche avec contrôle clavier
        
        Args:
            fishing_key: Touche pour démarrer la pêche (défaut: 'e')
            confidence: Niveau de confiance pour la détection d'images (0.0 à 1.0)
        """
        self.fishing_key = fishing_key
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
        
        # Configuration
        self.wait_after_key = 0.5
        self.exclamation_timeout = 30
        self.continue_button_timeout = 10
        self.qte_wait_time = 8
        
        print("\n" + "="*60)
        print(" BOT DE PÊCHE - MODE CLAVIER")
        print("="*60)
        print(f"Touche de pêche: {self.fishing_key.upper()}")
        print(f"Confiance de détection: {confidence*100}%")
        print(f"Images chargées: {len(self.templates)}")
        print("\nTouche d'arrêt d'urgence: ESC")
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
    
    def find_on_screen(self, template_key, region=None, timeout=5):
        """Cherche une image template sur l'écran"""
        if template_key not in self.templates:
            return None
        
        template = self.templates[template_key]
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if keyboard.is_pressed('esc'):
                print("\n⚠ Arrêt demandé par l'utilisateur (ESC)")
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
    
    def press_key(self, key):
        """Appuie sur une touche"""
        try:
            print(f"  → Appui sur la touche '{key.upper()}'...")
            pyautogui.press(key)
            print(f"  ✓ Touche '{key.upper()}' envoyée!")
            time.sleep(self.wait_after_key)
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'appui sur la touche: {e}")
            return False
    
    def safe_click(self, x, y):
        """Effectue un clic (pour les boutons de menu comme Continue)"""
        try:
            print(f"  → Clic à la position ({x}, {y})...")
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
            # Étape 1: Appuyer sur la touche pour commencer la pêche
            print("\n[Étape 1] Démarrage de la pêche...")
            self.stats["fishing_attempts"] += 1
            
            key_success = self.press_key(self.fishing_key)
            
            if not key_success:
                print("  ⚠ L'appui sur la touche a échoué, nouvelle tentative...")
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
            
            # Re-appuyer sur la touche pour attraper le poisson
            self.press_key(self.fishing_key)
            
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
                # Tenter d'appuyer sur ESC pour fermer
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
        print("\n🎣 Démarrage du bot de pêche (MODE CLAVIER)...")
        print("⚠ Assurez-vous que le jeu est au premier plan!")
        print(f"⚠ Le bot utilisera la touche '{self.fishing_key.upper()}' pour pêcher")
        print("\nLe bot démarrera dans 5 secondes...")
        print("(Appuyez sur ESC à tout moment pour arrêter)\n")
        
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
    print(" BOT D'AUTOMATISATION DE PÊCHE - MODE CLAVIER")
    print("="*60)
    
    # Configuration de la touche
    print("\nQuelle touche votre jeu utilise-t-il pour pêcher?")
    print("Exemples courants: e, f, space (espace), r, q")
    
    fishing_key = input("\nTouche de pêche [défaut: e]: ").strip().lower()
    if not fishing_key:
        fishing_key = 'e'
    
    # Si l'utilisateur tape "espace" ou "space"
    if fishing_key in ["espace", "space"]:
        fishing_key = "space"
    
    print(f"\n✓ Touche sélectionnée: {fishing_key.upper()}")
    
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
    bot = FishingBotKeyboard(fishing_key=fishing_key, confidence=confidence)
    bot.run(max_cycles=max_cycles)

if __name__ == "__main__":
    main()



"""
Bot d'automatisation de pêche
Automatise le processus de pêche dans le jeu
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

class FishingBot:
    def __init__(self, confidence=0.8):
        """
        Initialise le bot de pêche
        
        Args:
            confidence: Niveau de confiance pour la détection d'images (0.0 à 1.0)
        """
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
        
        # Charger les positions si elles existent
        self.positions = {}
        self.load_positions()
        
        # Configuration
        self.wait_after_click = 0.5  # Délai après chaque clic (secondes)
        self.exclamation_timeout = 30  # Temps max d'attente pour le point d'exclamation
        self.continue_button_timeout = 10  # Temps max d'attente pour le bouton Continue
        self.qte_wait_time = 8  # Temps d'attente pour le QTE avant de vérifier le bouton Continue
        
        # Désactiver le fail-safe de pyautogui si souhaité (décommenter avec précaution)
        # pyautogui.FAILSAFE = False
        
        print("\n" + "="*60)
        print(" BOT DE PÊCHE - Initialisé")
        print("="*60)
        print(f"Confiance de détection: {confidence*100}%")
        print(f"Images chargées: {len(self.templates)}")
        print(f"Positions chargées: {len(self.positions)}")
        print("\nTouche d'arrêt d'urgence: ESC")
        print("="*60 + "\n")
    
    def load_templates(self):
        """Charge les images de référence pour la détection"""
        template_files = {
            "exclamation": "exclamation_point.png",
            "continue": "button_continue.png",
            "exit": "button_exit.png"
        }
        
        for key, filename in template_files.items():
            filepath = os.path.join(self.images_dir, filename)
            if os.path.exists(filepath):
                img = cv2.imread(filepath)
                if img is not None:
                    self.templates[key] = img
                    print(f"✓ Image chargée: {filename}")
                else:
                    print(f"⚠ Impossible de charger: {filename}")
            else:
                print(f"⚠ Fichier non trouvé: {filename}")
        
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
        """
        Cherche une image template sur l'écran
        
        Args:
            template_key: Clé du template à chercher
            region: Région de recherche (x, y, width, height) ou None pour tout l'écran
            timeout: Temps maximum de recherche en secondes
            
        Returns:
            Tuple (x, y) du centre de l'image trouvée, ou None si non trouvé
        """
        if template_key not in self.templates:
            print(f"⚠ Template '{template_key}' non disponible")
            return None
        
        template = self.templates[template_key]
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Vérifier si l'utilisateur veut arrêter
            if keyboard.is_pressed('esc'):
                print("\n⚠ Arrêt demandé par l'utilisateur (ESC)")
                self.running = False
                return None
            
            # Capture d'écran
            screenshot = pyautogui.screenshot(region=region)
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # Matching de template
            result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= self.confidence:
                # Calculer le centre de l'image trouvée
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                
                # Ajuster pour la région si nécessaire
                if region:
                    center_x += region[0]
                    center_y += region[1]
                
                return (center_x, center_y)
            
            time.sleep(0.1)  # Petite pause entre les vérifications
        
        return None
    
    def safe_click(self, x=None, y=None, position_name=None):
        """
        Effectue un clic en toute sécurité
        
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
            print(f"  → Déplacement de la souris vers ({x}, {y})...")
            pyautogui.moveTo(x, y, duration=0.2)
            time.sleep(0.1)
            
            print(f"  → Clic gauche à la position ({x}, {y})...")
            pyautogui.click(x, y, button='left')
            
            print(f"  ✓ Clic effectué avec succès!")
            time.sleep(self.wait_after_click)
            return True
        except Exception as e:
            print(f"❌ Erreur lors du clic: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def fishing_cycle(self):
        """Exécute un cycle complet de pêche"""
        try:
            # Étape 1: Cliquer pour commencer la pêche
            print("\n[Étape 1] Démarrage de la pêche...")
            self.stats["fishing_attempts"] += 1
            
            if "fishing_start" in self.positions:
                click_success = self.safe_click(position_name="fishing_start")
            else:
                # Clic au centre de l'écran si pas de position définie
                screen_width, screen_height = pyautogui.size()
                print(f"  ℹ Aucune position enregistrée, clic au centre: ({screen_width // 2}, {screen_height // 2})")
                click_success = self.safe_click(screen_width // 2, screen_height // 2)
            
            if not click_success:
                print("  ⚠ Le clic de démarrage a échoué, nouvelle tentative...")
                time.sleep(1)
                return False
            
            # Petit délai supplémentaire après le clic initial
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
            self.safe_click(*exclamation_pos)
            
            # Étape 3: Attendre le QTE ou le succès direct
            print("[Étape 3] Attente du résultat (QTE ou succès direct)...")
            time.sleep(self.qte_wait_time)
            
            # Étape 4: Chercher le bouton Continue
            print("[Étape 4] Recherche du bouton Continue...")
            continue_pos = self.find_on_screen("continue", timeout=self.continue_button_timeout)
            
            if continue_pos is None:
                print("⚠ Bouton Continue non détecté - Nouvelle tentative...")
                # Peut-être encore dans le QTE, attendre un peu plus
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
                # Tenter un clic ESC ou retour
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
        """
        Lance le bot
        
        Args:
            max_cycles: Nombre maximum de cycles (None = infini)
        """
        print("\n🎣 Démarrage du bot de pêche...")
        print("⚠ Assurez-vous que le jeu est au premier plan!")
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
                
                # Afficher les stats tous les 10 cycles
                if cycle_count % 10 == 0:
                    self.print_stats()
                
                # Petite pause entre les cycles
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
    print(" BOT D'AUTOMATISATION DE PÊCHE")
    print("="*60)
    
    # Vérifier que les images de référence existent
    if not os.path.exists("images_reference"):
        print("\n❌ ERREUR: Dossier 'images_reference' non trouvé!")
        print("   Veuillez exécuter calibration.py d'abord.\n")
        return
    
    # Configuration
    print("\nConfiguration:")
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
    bot = FishingBot(confidence=confidence)
    bot.run(max_cycles=max_cycles)

if __name__ == "__main__":
    main()


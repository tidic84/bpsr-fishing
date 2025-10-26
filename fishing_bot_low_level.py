"""
Bot d'automatisation de pêche - VERSION BAS NIVEAU (SendInput)
Utilise les API Windows comme les auto-clickers (OP Auto Clicker)
Compatible avec les jeux qui bloquent PyAutoGUI standard
"""

import cv2
import numpy as np
from PIL import Image
import time
import os
import sys
from datetime import datetime
import keyboard
import ctypes

# Importer PyAutoGUI uniquement pour screenshot et position
import pyautogui

# Constantes Windows pour SendInput
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000

# Structures Windows
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]
    
    _anonymous_ = ("_input",)
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("_input", _INPUT)
    ]

class FishingBotLowLevel:
    def __init__(self, confidence=0.8):
        """
        Initialise le bot de pêche avec clics bas niveau
        
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
        
        # Charger les positions
        self.positions = {}
        self.load_positions()
        
        # Configuration
        self.wait_after_click = 0.5
        self.exclamation_timeout = 30
        self.continue_button_timeout = 10
        self.qte_wait_time = 8
        
        # Obtenir la taille de l'écran pour SendInput
        self.screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        self.screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        
        print("\n" + "="*60)
        print(" BOT DE PÊCHE - MODE BAS NIVEAU (SendInput)")
        print("="*60)
        print(f"Méthode: API Windows SendInput (comme OP Auto Clicker)")
        print(f"Confiance de détection: {confidence*100}%")
        print(f"Images chargées: {len(self.templates)}")
        print(f"Positions chargées: {len(self.positions)}")
        print(f"Résolution: {self.screen_width}x{self.screen_height}")
        print("\nTouche d'arrêt d'urgence: ESC")
        print("="*60 + "\n")
    
    def load_templates(self):
        """Charge les images de référence pour la détection"""
        template_files = {
            "exclamation": "exclamation_point.png",
            "continue": "button_continue.png",
            "ready": "fishing_ready.png",  # Optionnel : canne prête
            "rod_broken": "rod_broken.png",  # Optionnel : canne cassée
            "use_button": "use_button.png",  # Bouton "Use" dans le menu
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
    
    def low_level_click(self, x, y):
        """
        Effectue un clic bas niveau en utilisant SendInput Windows
        Même méthode que les auto-clickers comme OP Auto Clicker
        
        Args:
            x, y: Coordonnées du clic en pixels
        """
        # Convertir les coordonnées pixel en coordonnées absolues (0-65535)
        abs_x = int(x * 65535 / self.screen_width)
        abs_y = int(y * 65535 / self.screen_height)
        
        # Déplacer la souris
        move_input = INPUT()
        move_input.type = 0  # INPUT_MOUSE
        move_input.mi = MOUSEINPUT(
            abs_x, abs_y, 0,
            MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE,
            0, None
        )
        
        # Bouton gauche enfoncé
        down_input = INPUT()
        down_input.type = 0
        down_input.mi = MOUSEINPUT(
            abs_x, abs_y, 0,
            MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_ABSOLUTE,
            0, None
        )
        
        # Bouton gauche relâché
        up_input = INPUT()
        up_input.type = 0
        up_input.mi = MOUSEINPUT(
            abs_x, abs_y, 0,
            MOUSEEVENTF_LEFTUP | MOUSEEVENTF_ABSOLUTE,
            0, None
        )
        
        # Envoyer les événements
        ctypes.windll.user32.SendInput(1, ctypes.byref(move_input), ctypes.sizeof(INPUT))
        time.sleep(0.01)
        ctypes.windll.user32.SendInput(1, ctypes.byref(down_input), ctypes.sizeof(INPUT))
        time.sleep(0.05)
        ctypes.windll.user32.SendInput(1, ctypes.byref(up_input), ctypes.sizeof(INPUT))
    
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
    
    def check_and_repair_rod(self):
        """
        Vérifie si la canne est cassée et la remplace si nécessaire
        
        Returns:
            True si tout est OK, False en cas d'erreur
        """
        print("[Vérification] Contrôle de l'état de la canne...")
        
        # Vérification optionnelle : détecter visuellement si la canne est cassée
        if "rod_broken" in self.templates:
            broken_detected = self.find_on_screen("rod_broken", timeout=1)
            if broken_detected:
                print("  ⚠️ Canne cassée détectée visuellement!")
            else:
                # Si l'indicateur existe mais n'est pas détecté, la canne est OK
                print("  ✓ Canne en bon état (détection visuelle)")
                return True
        
        # Ouvrir le menu de sélection de canne avec ","
        print("  → Ouverture du menu de cannes (touche ',')...")
        pyautogui.press(',')
        time.sleep(0.8)  # Laisser le menu s'ouvrir
        
        # Chercher le bouton "Use"
        if "use_button" in self.templates:
            print("  → Recherche du bouton 'Use'...")
            use_pos = self.find_on_screen("use_button", timeout=3)
            
            if use_pos:
                print(f"  ✓ Bouton 'Use' trouvé à {use_pos}")
                self.safe_click(*use_pos)
                time.sleep(0.5)
                
                # Fermer le menu (appuyer à nouveau sur ,)
                print("  → Fermeture du menu...")
                pyautogui.press(',')
                time.sleep(0.5)
                
                print("  ✓ Canne équipée avec succès!")
                return True
            else:
                print("  ⚠️ Bouton 'Use' non trouvé")
                # Fermer le menu quand même
                pyautogui.press(',')
                time.sleep(0.5)
                return True  # Continuer quand même
        else:
            # Si pas d'image du bouton Use, on suppose que c'est OK
            print("  → Pas de détection du bouton 'Use' configurée")
            print("  → Fermeture du menu...")
            pyautogui.press(',')
            time.sleep(0.5)
            return True
    
    def safe_click(self, x=None, y=None, position_name=None):
        """
        Effectue un clic en utilisant SendInput (bas niveau)
        
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
            print(f"  → Clic bas niveau (SendInput) à ({x}, {y})...")
            self.low_level_click(x, y)
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
            # Étape 0: Vérifier et réparer la canne AVANT de commencer
            self.check_and_repair_rod()

            time.sleep(3)
            
            # Étape 1: Cliquer pour commencer la pêche
            print("\n[Étape 1] Démarrage de la pêche...")
            self.stats["fishing_attempts"] += 1
            
            if "fishing_start" in self.positions:
                click_success = self.safe_click(position_name="fishing_start")
            else:
                # Clic au centre de l'écran si pas de position définie
                print(f"  ℹ Aucune position enregistrée, clic au centre: ({self.screen_width // 2}, {self.screen_height // 2})")
                click_success = self.safe_click(self.screen_width // 2, self.screen_height // 2)
            
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
            self.safe_click(*exclamation_pos)
            
            # Étape 3: Vérifier immédiatement si Continue apparaît (succès direct)
            print("[Étape 3] Vérification du résultat...")
            time.sleep(3)  # Petit délai pour que l'interface réagisse
            
            # Chercher Continue immédiatement (timeout court)
            continue_pos = self.find_on_screen("continue", timeout=2)
            
            if continue_pos is None:
                # Pas de Continue = QTE en cours
                print("  → QTE détecté, on laisse expirer (pas de bouton Continue après)...")
                time.sleep(self.qte_wait_time)
                
                # Après le QTE, PAS de bouton Continue, juste attendre que la canne soit prête
                print("[Étape 4] QTE expiré, attente que la canne soit prête...")
                
                if "ready" in self.templates:
                    ready_pos = self.find_on_screen("ready", timeout=15)
                    if ready_pos:
                        print("  ✓ Canne prête!")
                    else:
                        print("  ⚠ Indicateur non détecté, attente de 3 secondes...")
                        time.sleep(3)
                else:
                    # Si pas d'image de référence, attendre un délai fixe
                    print("  ⚠ Pas d'indicateur configuré, attente de 3 secondes...")
                    time.sleep(3)
                
                # La vérification de canne se fera au début du prochain cycle
                self.stats["fishing_attempts"] += 1  # Tentative mais pas de poisson
                return True
            else:
                # Continue trouvé immédiatement = succès direct !
                print("  ✓ Succès direct (pas de QTE)!")
                print(f"✓ Bouton Continue détecté à {continue_pos}")
                self.safe_click(*continue_pos)
                self.stats["fish_caught"] += 1
                print(f"🎣 Poisson pêché! Total: {self.stats['fish_caught']}")
                
                # Étape 5: Attendre que la canne soit prête (si image disponible)
                print("[Étape 5] Attente que la canne soit prête...")
                if "ready" in self.templates:
                    ready_pos = self.find_on_screen("ready", timeout=10)
                    if ready_pos:
                        print("  ✓ Canne prête!")
                    else:
                        # Si pas détecté, attendre un délai fixe
                        print("  ⚠ Indicateur non détecté, attente de 2 secondes...")
                        time.sleep(2)
                else:
                    # Si pas d'image de référence, attendre un peu
                    print("  ⚠ Pas d'indicateur configuré, attente de 1 seconde...")
                    time.sleep(1)
                
                # La vérification de canne se fera au début du prochain cycle
                return True
                
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
        print("\n🎣 Démarrage du bot de pêche (MODE BAS NIVEAU)...")
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
        
        # Vérification initiale de la canne avant de commencer
        print("═" * 60)
        print(" VÉRIFICATION INITIALE")
        print("═" * 60)
        self.check_and_repair_rod()
        print()
        
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
    print(" BOT D'AUTOMATISATION DE PÊCHE - MODE BAS NIVEAU")
    print("="*60)
    print("\nCe bot utilise SendInput (API Windows) comme OP Auto Clicker")
    print("Compatible avec les jeux qui bloquent PyAutoGUI standard\n")
    
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
    bot = FishingBotLowLevel(confidence=confidence)
    bot.run(max_cycles=max_cycles)

if __name__ == "__main__":
    main()



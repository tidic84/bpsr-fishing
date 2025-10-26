"""
Script de debug pour la détection d'images
Aide à identifier pourquoi le point d'exclamation n'est pas détecté
"""

import cv2
import numpy as np
from PIL import Image
import pyautogui
import time
import os
import sys

print("\n" + "="*70)
print(" 🔍 OUTIL DE DEBUG - DÉTECTION D'IMAGES")
print("="*70 + "\n")

# Vérifier que les images existent
images_dir = "images_reference"
exclamation_file = os.path.join(images_dir, "exclamation_point.png")

if not os.path.exists(exclamation_file):
    print("❌ ERREUR: Image du point d'exclamation non trouvée!")
    print(f"   Fichier attendu: {exclamation_file}")
    print("\n   Veuillez d'abord lancer: python calibration.py\n")
    sys.exit(1)

# Charger l'image template
template = cv2.imread(exclamation_file)
if template is None:
    print("❌ ERREUR: Impossible de charger l'image!")
    sys.exit(1)

h, w = template.shape[:2]
print(f"✓ Image du point d'exclamation chargée: {w}x{h} pixels\n")

# Afficher l'image capturée
print("Aperçu de votre capture:")
print(f"  Taille: {w}x{h} pixels")
if w > 200 or h > 200:
    print("  ⚠️ ATTENTION: L'image est très grande!")
    print("     Recommandation: Capturez une zone plus petite (30-100 pixels)")
elif w < 20 or h < 20:
    print("  ⚠️ ATTENTION: L'image est très petite!")
    print("     Recommandation: Capturez une zone légèrement plus grande")
else:
    print("  ✓ Taille correcte")

# Afficher l'image pour vérification
cv2.imshow("Votre capture - Point d'exclamation", template)
print("\nUne fenêtre s'est ouverte avec votre capture.")
print("Vérifiez qu'elle est nette et bien visible.")
print("Appuyez sur une touche dans la fenêtre pour continuer...\n")
cv2.waitKey(0)
cv2.destroyAllWindows()

print("="*70)
print(" TEST DE DÉTECTION EN TEMPS RÉEL")
print("="*70 + "\n")

print("Instructions:")
print("  1. Ouvrez votre jeu")
print("  2. Commencez à pêcher MANUELLEMENT")
print("  3. Quand le point d'exclamation apparaît, NE BOUGEZ PAS")
print("  4. Le script va tester la détection")
print("\nLe test commencera dans 5 secondes...")

input("\nAppuyez sur ENTRÉE pour commencer...")

for i in range(5, 0, -1):
    print(f"{i}...")
    time.sleep(1)

print("\n🔍 RECHERCHE DU POINT D'EXCLAMATION...\n")

# Différents niveaux de confiance à tester
confidence_levels = [0.9, 0.8, 0.7, 0.6, 0.5]

for confidence in confidence_levels:
    print(f"Test avec confiance {confidence*100:.0f}%...")
    
    # Capture d'écran
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    
    # Matching
    result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    print(f"  Score de correspondance: {max_val*100:.1f}%")
    
    if max_val >= confidence:
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        print(f"  ✅ DÉTECTÉ à la position ({center_x}, {center_y})!")
        
        # Dessiner un rectangle sur la détection
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(screenshot_cv, top_left, bottom_right, (0, 255, 0), 3)
        
        # Afficher le résultat
        # Redimensionner si trop grand
        display_img = screenshot_cv.copy()
        max_display_width = 1280
        if display_img.shape[1] > max_display_width:
            scale = max_display_width / display_img.shape[1]
            new_width = int(display_img.shape[1] * scale)
            new_height = int(display_img.shape[0] * scale)
            display_img = cv2.resize(display_img, (new_width, new_height))
        
        cv2.imshow("DÉTECTION RÉUSSIE (rectangle vert)", display_img)
        print("\n  Une fenêtre montre où le point d'exclamation a été détecté.")
        print("  Appuyez sur une touche pour continuer...\n")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        print("="*70)
        print(" ✅ RÉSULTAT: DÉTECTION RÉUSSIE!")
        print("="*70)
        print(f"\nLe point d'exclamation a été détecté avec confiance {confidence*100:.0f}%")
        print(f"\nRECOMMANDATION:")
        print(f"  Modifiez fishing_bot_low_level.py:")
        print(f"  Changez confidence={confidence} dans le code")
        print(f"  Ou choisissez le mode correspondant au lancement\n")
        sys.exit(0)
    else:
        print(f"  ❌ Non détecté (score trop bas: {max_val*100:.1f}% < {confidence*100:.0f}%)")

print("\n" + "="*70)
print(" ❌ RÉSULTAT: DÉTECTION ÉCHOUÉE À TOUS LES NIVEAUX")
print("="*70 + "\n")

print("Le point d'exclamation n'a pas été détecté même avec 50% de confiance.")
print(f"Score maximum obtenu: {max_val*100:.1f}%\n")

print("CAUSES POSSIBLES:\n")

if max_val < 0.3:
    print("1. ⚠️ L'image capturée ne correspond PAS à ce qui apparaît à l'écran")
    print("   Raisons possibles:")
    print("   - Vous avez capturé le mauvais élément")
    print("   - Le point d'exclamation a une apparence différente")
    print("   - La résolution du jeu a changé")
    print("   - Il y a des effets visuels/animations\n")
    
    print("SOLUTION:")
    print("  1. Supprimez l'ancienne capture:")
    print(f"     del {exclamation_file}")
    print("  2. Relancez la calibration: python calibration.py")
    print("  3. Capturez le point d'exclamation quand il apparaît")
    print("  4. Capturez UNIQUEMENT le symbole (!), sans fond")
    print("  5. Assurez-vous que l'image est nette\n")

elif max_val < 0.5:
    print("1. ⚠️ La capture contient trop d'éléments variables")
    print("   - Fond animé")
    print("   - Effets de particules")
    print("   - Zone trop large\n")
    
    print("SOLUTION:")
    print("  Recalibrez en capturant une zone PLUS PETITE")
    print("  Capturez JUSTE le symbole (!) central")
    print("  Évitez d'inclure le fond ou les effets\n")

else:
    print("1. ⚠️ Le score est proche mais pas assez élevé")
    print(f"   Score actuel: {max_val*100:.1f}%")
    print("   Score requis: 50%\n")
    
    print("SOLUTION:")
    print("  Option 1: Recalibrez avec une capture plus précise")
    print("  Option 2: Attendez quelques secondes et relancez ce script")
    print("           (Le point d'exclamation était peut-être en animation)\n")

print("2. ⚠️ VÉRIFICATIONS:")
print("   - Le point d'exclamation était-il visible à l'écran pendant le test?")
print("   - La résolution du jeu est-elle la même qu'à la calibration?")
print("   - Y a-t-il des overlays (Discord, FPS counter) qui cachent le symbole?\n")

print("3. 💡 TEST MANUEL:")
print("   Relancez ce script PENDANT que le point d'exclamation est visible")
print("   Si le test échoue encore, la capture doit être refaite\n")

# Sauvegarder la capture d'écran pour analyse
debug_file = "debug_screenshot.png"
screenshot_pil = pyautogui.screenshot()
screenshot_pil.save(debug_file)
print(f"📸 Capture d'écran sauvegardée: {debug_file}")
print("   Comparez visuellement avec votre image de référence\n")

print("="*70 + "\n")



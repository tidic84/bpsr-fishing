"""
Script de test pour vérifier que toutes les dépendances sont correctement installées
Lancez ce script après l'installation pour diagnostiquer les problèmes potentiels
"""

import sys
import os

print("\n" + "="*70)
print(" TEST D'INSTALLATION - BOT DE PÊCHE")
print("="*70 + "\n")

# Test des imports
tests_passed = 0
tests_failed = 0
errors = []

def test_import(module_name, package_name=None):
    """Teste l'import d'un module"""
    global tests_passed, tests_failed
    package = package_name or module_name
    try:
        __import__(module_name)
        print(f"✓ {package:20} - OK")
        tests_passed += 1
        return True
    except ImportError as e:
        print(f"✗ {package:20} - ERREUR")
        errors.append(f"{package}: {str(e)}")
        tests_failed += 1
        return False

print("Test des modules Python requis:\n")

# Test des imports principaux
pyautogui_ok = test_import("pyautogui", "PyAutoGUI")
cv2_ok = test_import("cv2", "OpenCV")
numpy_ok = test_import("numpy", "NumPy")
pil_ok = test_import("PIL", "Pillow")
keyboard_ok = test_import("keyboard", "Keyboard")

print("\n" + "-"*70 + "\n")

# Tests supplémentaires
print("Tests fonctionnels:\n")

# Test 1: Vérifier la version de Python
python_version = sys.version_info
if python_version.major >= 3 and python_version.minor >= 8:
    print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro} - OK (>= 3.8 requis)")
    tests_passed += 1
else:
    print(f"✗ Python {python_version.major}.{python_version.minor}.{python_version.micro} - TROP ANCIEN (>= 3.8 requis)")
    errors.append("Python: Version trop ancienne, installez Python 3.8 ou supérieur")
    tests_failed += 1

# Test 2: Vérifier la structure des dossiers
if os.path.exists("images_reference"):
    print("✓ Dossier images_reference - OK")
    tests_passed += 1
else:
    print("✗ Dossier images_reference - MANQUANT")
    errors.append("Dossier images_reference introuvable")
    tests_failed += 1

# Test 3: Vérifier les fichiers principaux
files_to_check = ["fishing_bot.py", "calibration.py", "requirements.txt"]
for filename in files_to_check:
    if os.path.exists(filename):
        print(f"✓ Fichier {filename:20} - OK")
        tests_passed += 1
    else:
        print(f"✗ Fichier {filename:20} - MANQUANT")
        errors.append(f"Fichier {filename} introuvable")
        tests_failed += 1

# Test 4: Test fonctionnel de PyAutoGUI (si disponible)
if pyautogui_ok:
    try:
        import pyautogui
        screen_size = pyautogui.size()
        print(f"✓ PyAutoGUI fonctionnel - Résolution détectée: {screen_size[0]}x{screen_size[1]}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ PyAutoGUI test fonctionnel - ERREUR: {e}")
        errors.append(f"PyAutoGUI: Impossible de détecter la résolution d'écran")
        tests_failed += 1

# Test 5: Test fonctionnel d'OpenCV (si disponible)
if cv2_ok and numpy_ok:
    try:
        import cv2
        import numpy as np
        # Créer une petite image de test
        test_img = np.zeros((100, 100, 3), dtype=np.uint8)
        result = cv2.matchTemplate(test_img, test_img, cv2.TM_CCOEFF_NORMED)
        print("✓ OpenCV fonctionnel - Test de template matching réussi")
        tests_passed += 1
    except Exception as e:
        print(f"✗ OpenCV test fonctionnel - ERREUR: {e}")
        errors.append(f"OpenCV: {str(e)}")
        tests_failed += 1

print("\n" + "="*70)
print(f" RÉSUMÉ: {tests_passed} tests réussis, {tests_failed} tests échoués")
print("="*70 + "\n")

if tests_failed > 0:
    print("❌ ERREURS DÉTECTÉES:\n")
    for i, error in enumerate(errors, 1):
        print(f"{i}. {error}")
    
    print("\n" + "="*70)
    print(" SOLUTIONS RECOMMANDÉES")
    print("="*70 + "\n")
    
    # Suggestions de solutions
    if not pyautogui_ok:
        print("→ PyAutoGUI manquant:")
        print("  pip install pyautogui\n")
    
    if not cv2_ok:
        print("→ OpenCV manquant:")
        print("  pip install opencv-python\n")
    
    if not numpy_ok:
        print("→ NumPy manquant:")
        print("  pip install numpy\n")
    
    if not pil_ok:
        print("→ Pillow manquant:")
        print("  pip install Pillow\n")
    
    if not keyboard_ok:
        print("→ Keyboard manquant:")
        print("  pip install keyboard")
        print("  Note: Sur Windows, peut nécessiter les droits administrateur\n")
    
    print("Pour installer toutes les dépendances d'un coup:")
    print("  pip install -r requirements.txt\n")
    
else:
    print("✅ TOUTES LES VÉRIFICATIONS SONT PASSÉES!\n")
    print("Votre installation est prête. Vous pouvez maintenant:")
    print("  1. Lancer la calibration : python calibration.py")
    print("  2. Lancer le bot        : python fishing_bot.py")
    print("  3. Ou utilisez          : start_bot.bat (Windows) / ./start_bot.sh (Linux/macOS)\n")

print("="*70 + "\n")

# Informations système supplémentaires
print("INFORMATIONS SYSTÈME:\n")
print(f"Système d'exploitation : {sys.platform}")
print(f"Version Python         : {sys.version.split()[0]}")
print(f"Chemin Python          : {sys.executable}")
print(f"Répertoire actuel      : {os.getcwd()}\n")

print("="*70)


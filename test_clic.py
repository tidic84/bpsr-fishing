"""
Script de test pour diagnostiquer les problèmes de clic
Utilisez ce script pour vérifier que PyAutoGUI peut cliquer correctement
"""

import pyautogui
import time
import sys

print("\n" + "="*70)
print(" TEST DE DIAGNOSTIC DES CLICS")
print("="*70 + "\n")

# Vérifier les paramètres de PyAutoGUI
print("Configuration actuelle de PyAutoGUI:")
print(f"  - PAUSE entre actions : {pyautogui.PAUSE}s")
print(f"  - FAILSAFE activé     : {pyautogui.FAILSAFE}")
print(f"  - Résolution écran    : {pyautogui.size()}")
print()

# Test 1: Position actuelle de la souris
print("="*70)
print(" TEST 1: Position de la souris")
print("="*70)
print("\nDéplacez votre souris et observez les coordonnées pendant 5 secondes...")
print("(Appuyez sur Ctrl+C pour arrêter)")

try:
    for i in range(50):  # 5 secondes (50 * 0.1s)
        x, y = pyautogui.position()
        print(f"\rPosition actuelle: X={x:4d}, Y={y:4d}", end='', flush=True)
        time.sleep(0.1)
    print("\n")
except KeyboardInterrupt:
    print("\n\n⚠ Interrompu par l'utilisateur\n")

# Test 2: Déplacement de la souris
print("="*70)
print(" TEST 2: Déplacement de la souris")
print("="*70)
print("\nLe curseur va se déplacer vers différentes positions dans 3 secondes...")
print("⚠ NE TOUCHEZ PAS la souris pendant le test!")

for i in range(3, 0, -1):
    print(f"{i}...")
    time.sleep(1)

try:
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    positions = [
        (center_x, center_y, "Centre de l'écran"),
        (100, 100, "Coin supérieur gauche"),
        (screen_width - 100, 100, "Coin supérieur droit"),
        (center_x, center_y, "Retour au centre"),
    ]
    
    for x, y, description in positions:
        print(f"\n→ Déplacement vers {description} ({x}, {y})...")
        pyautogui.moveTo(x, y, duration=0.5)
        time.sleep(0.5)
        actual_x, actual_y = pyautogui.position()
        
        if abs(actual_x - x) < 5 and abs(actual_y - y) < 5:
            print(f"  ✓ Position atteinte: ({actual_x}, {actual_y})")
        else:
            print(f"  ⚠ Écart détecté! Visée: ({x}, {y}), Réelle: ({actual_x}, {actual_y})")
    
    print("\n✓ Test de déplacement terminé avec succès!")
    
except Exception as e:
    print(f"\n❌ Erreur lors du déplacement: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Clic de souris
print("\n" + "="*70)
print(" TEST 3: Clics de souris")
print("="*70)
print("\nLe bot va effectuer 3 clics au centre de l'écran dans 5 secondes...")
print("⚠ Assurez-vous qu'une fenêtre de test est ouverte (ex: Bloc-notes, navigateur)")
print("⚠ Vous devriez voir les clics s'effectuer!")

input("\nAppuyez sur ENTRÉE pour continuer (ou Ctrl+C pour annuler)...")

try:
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    print("\nDéplacement vers le centre de l'écran...")
    pyautogui.moveTo(center_x, center_y, duration=0.3)
    time.sleep(1)
    
    for i in range(1, 4):
        print(f"\nClic #{i}...")
        print(f"  → Position: ({center_x}, {center_y})")
        
        # Méthode 1: Clic simple
        pyautogui.click(center_x, center_y)
        print(f"  ✓ Clic effectué!")
        
        time.sleep(1)
    
    print("\n✓ Test de clic terminé!")
    
except Exception as e:
    print(f"\n❌ Erreur lors du clic: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Clic avec différentes méthodes
print("\n" + "="*70)
print(" TEST 4: Méthodes alternatives de clic")
print("="*70)

print("\nTest de différentes méthodes de clic...")

input("\nAppuyez sur ENTRÉE pour tester les méthodes alternatives...")

try:
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    # Méthode 1: click() simple
    print("\n1. Méthode: pyautogui.click(x, y)")
    pyautogui.moveTo(center_x, center_y, duration=0.2)
    time.sleep(0.2)
    pyautogui.click()
    print("   ✓ Clic envoyé")
    time.sleep(1)
    
    # Méthode 2: click avec coordonnées
    print("\n2. Méthode: pyautogui.click(x, y) avec coordonnées")
    pyautogui.click(center_x, center_y)
    print("   ✓ Clic envoyé")
    time.sleep(1)
    
    # Méthode 3: mouseDown + mouseUp
    print("\n3. Méthode: mouseDown() + mouseUp()")
    pyautogui.moveTo(center_x, center_y, duration=0.2)
    time.sleep(0.1)
    pyautogui.mouseDown(button='left')
    time.sleep(0.05)
    pyautogui.mouseUp(button='left')
    print("   ✓ Clic envoyé")
    time.sleep(1)
    
    # Méthode 4: click avec button explicite
    print("\n4. Méthode: pyautogui.click(x, y, button='left')")
    pyautogui.click(center_x, center_y, button='left')
    print("   ✓ Clic envoyé")
    time.sleep(1)
    
    print("\n✓ Toutes les méthodes testées!")
    
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Permissions et limitations
print("\n" + "="*70)
print(" TEST 5: Vérification des permissions")
print("="*70)

print("\nVérification des limitations du système...")

# Vérifier si on est sous Windows avec UAC
if sys.platform == 'win32':
    print("\n⚠ Système Windows détecté")
    print("\nLimitations possibles:")
    print("  - Les applications en mode administrateur peuvent bloquer PyAutoGUI")
    print("  - Les jeux en plein écran exclusif peuvent ne pas recevoir les clics")
    print("  - Certains antivirus peuvent bloquer l'automatisation")
    print("\nSolutions recommandées:")
    print("  1. Lancez le jeu en mode fenêtré (ou fenêtré sans bordure)")
    print("  2. Ajoutez une exception dans votre antivirus pour Python")
    print("  3. N'exécutez PAS le jeu en mode administrateur")
    print("  4. Désactivez temporairement les overlays (Discord, GeForce, etc.)")

# Test de permission d'écriture
print("\n" + "="*70)
print(" RÉSUMÉ DU DIAGNOSTIC")
print("="*70)

print("\n✓ Si vous avez vu la souris bouger et les messages de succès,")
print("  PyAutoGUI fonctionne correctement sur votre système.")

print("\n⚠ Si le bot ne clique toujours pas dans le jeu:")
print("  1. Le jeu doit être en mode FENÊTRÉ (pas plein écran exclusif)")
print("  2. Ne lancez PAS le jeu en administrateur")
print("  3. Le jeu doit être au PREMIER PLAN")
print("  4. Ajoutez des délais plus longs (augmentez wait_after_click)")
print("  5. Certains jeux bloquent les entrées virtuelles")

print("\n💡 Essayez maintenant avec le jeu:")
print("  1. Ouvrez votre jeu en mode FENÊTRÉ")
print("  2. Placez une fenêtre de Bloc-notes par-dessus")
print("  3. Relancez ce test pour voir si les clics fonctionnent")

print("\n" + "="*70)
print(" Test terminé!")
print("="*70 + "\n")


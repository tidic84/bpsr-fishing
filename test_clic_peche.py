"""
Test spécifique pour le clic de démarrage de pêche
Ce script permet de tester uniquement l'étape 1 du bot
"""

import pyautogui
import time
import os

print("\n" + "="*70)
print(" TEST DU CLIC DE DÉMARRAGE DE PÊCHE")
print("="*70 + "\n")

# Désactiver la pause automatique pour des clics plus rapides si nécessaire
pyautogui.PAUSE = 0.1

print("Configuration PyAutoGUI:")
print(f"  - Résolution: {pyautogui.size()}")
print(f"  - FAILSAFE: {pyautogui.FAILSAFE}")
print()

# Charger la position si elle existe
position_file = os.path.join("images_reference", "positions.txt")
fishing_start_pos = None

if os.path.exists(position_file):
    print(f"✓ Fichier de positions trouvé: {position_file}")
    with open(position_file, "r", encoding="utf-8") as f:
        for line in f:
            if "fishing_start=" in line:
                coords = line.split("=")[1].strip()
                x, y = coords.split(",")
                fishing_start_pos = (int(x), int(y))
                print(f"✓ Position de pêche chargée: {fishing_start_pos}")
                break
else:
    print("⚠ Aucun fichier de positions trouvé")

# Si pas de position, demander à l'utilisateur
if fishing_start_pos is None:
    print("\nAucune position enregistrée.")
    print("\nOptions:")
    print("1. Utiliser le centre de l'écran")
    print("2. Définir manuellement une position")
    print("3. Quitter et lancer calibration.py")
    
    choice = input("\nVotre choix (1-3): ").strip()
    
    if choice == "1":
        screen_width, screen_height = pyautogui.size()
        fishing_start_pos = (screen_width // 2, screen_height // 2)
        print(f"✓ Position définie: Centre de l'écran {fishing_start_pos}")
    
    elif choice == "2":
        print("\nDéplacez votre souris à l'endroit où vous voulez cliquer")
        print("et appuyez sur ENTRÉE...")
        input()
        fishing_start_pos = pyautogui.position()
        print(f"✓ Position capturée: {fishing_start_pos}")
    
    else:
        print("\n⚠ Veuillez d'abord lancer: python calibration.py")
        exit(0)

# Test du clic
print("\n" + "="*70)
print(" TEST DU CLIC")
print("="*70)

print(f"\nPosition de clic: {fishing_start_pos}")
print("\n⚠ IMPORTANT:")
print("  1. Ouvrez votre jeu")
print("  2. Placez-vous à l'endroit de pêche")
print("  3. Mettez le jeu au PREMIER PLAN")
print("  4. Le jeu doit être en mode FENÊTRÉ (pas plein écran)")

print("\nLe test démarrera dans 5 secondes...")
input("\nAppuyez sur ENTRÉE pour continuer (ou Ctrl+C pour annuler)...")

print("\nPréparation...")
for i in range(5, 0, -1):
    print(f"{i}...")
    time.sleep(1)

print("\n🎣 TEST EN COURS...\n")

# Effectuer 3 clics de test
for i in range(1, 4):
    print(f"Test #{i}:")
    
    # Afficher la position actuelle
    current_x, current_y = pyautogui.position()
    print(f"  Position actuelle de la souris: ({current_x}, {current_y})")
    
    # Déplacer vers la cible
    print(f"  → Déplacement vers {fishing_start_pos}...")
    # pyautogui.moveTo(fishing_start_pos[0], fishing_start_pos[1], duration=0.3)
    # time.sleep(0.2)
    
    # Vérifier la position
    actual_x, actual_y = pyautogui.position()
    print(f"  Position après déplacement: ({actual_x}, {actual_y})")
    
    # Effectuer le clic
    print(f"  → CLIC GAUCHE...")
    pyautogui.click(current_x, current_y, button='left')
    
    print(f"  ✓ Clic #{i} envoyé!")
    
    # Attendre avant le prochain test
    if i < 3:
        print(f"  Attente de 2 secondes avant le prochain clic...\n")
        time.sleep(2)

print("\n" + "="*70)
print(" TEST TERMINÉ")
print("="*70)

print("\n📊 Résultat:")
print(f"  - Position testée: {fishing_start_pos}")
print(f"  - Nombre de clics: 3")

print("\n❓ Questions de diagnostic:")
print("\n1. Avez-vous vu la souris se déplacer?")
response1 = input("   (oui/non): ").lower()

print("\n2. Avez-vous vu des clics s'effectuer dans le jeu?")
response2 = input("   (oui/non): ").lower()

print("\n3. Est-ce que la pêche a démarré dans le jeu?")
response3 = input("   (oui/non): ").lower()

print("\n" + "="*70)
print(" DIAGNOSTIC")
print("="*70 + "\n")

if response1 == "non":
    print("❌ PROBLÈME: La souris ne bouge pas")
    print("\nCauses possibles:")
    print("  - PyAutoGUI n'a pas les permissions nécessaires")
    print("  - Un antivirus bloque l'automatisation")
    print("  - Problème d'installation de PyAutoGUI")
    print("\nSolutions:")
    print("  1. Lancez Python en tant qu'administrateur")
    print("  2. Réinstallez PyAutoGUI: pip install --force-reinstall pyautogui")
    print("  3. Vérifiez votre antivirus")

elif response2 == "non":
    print("❌ PROBLÈME: La souris bouge mais les clics ne fonctionnent pas")
    print("\nCauses possibles:")
    print("  - Le jeu est en plein écran EXCLUSIF")
    print("  - Le jeu bloque les entrées virtuelles")
    print("  - Le jeu tourne en mode administrateur")
    print("\nSolutions:")
    print("  1. Mettez le jeu en mode FENÊTRÉ ou FENÊTRÉ SANS BORDURE")
    print("  2. Ne lancez PAS le jeu en mode administrateur")
    print("  3. Désactivez les overlays (Discord, Steam, etc.)")
    print("  4. Essayez d'ajouter un délai plus long entre déplacement et clic")

elif response3 == "non":
    print("⚠ PROBLÈME: Les clics fonctionnent mais la pêche ne démarre pas")
    print("\nCauses possibles:")
    print("  - La position de clic est incorrecte")
    print("  - Il faut un double-clic au lieu d'un simple clic")
    print("  - Il faut maintenir le clic enfoncé")
    print("  - Il y a un prérequis (équiper une canne, ouvrir un menu, etc.)")
    print("\nSolutions:")
    print("  1. Vérifiez la position exacte où vous devez cliquer")
    print("  2. Recalibrez avec: python calibration.py")
    print("  3. Vérifiez les prérequis du jeu pour commencer à pêcher")
    
    print("\n💡 Test de double-clic:")
    print("   Voulez-vous tester avec un double-clic? (oui/non)")
    if input("   ").lower() == "oui":
        print("\n   Test dans 3 secondes...")
        time.sleep(3)
        pyautogui.doubleClick(fishing_start_pos[0], fishing_start_pos[1])
        print("   ✓ Double-clic effectué!")
        print("   Est-ce que ça a fonctionné? Notez-le pour la configuration.")

else:
    print("✅ SUCCÈS: Tout fonctionne correctement!")
    print("\nLe bot devrait fonctionner. Si ce n'est pas le cas:")
    print("  - Vérifiez que la calibration des autres éléments est bonne")
    print("  - Lancez: python fishing_bot.py")

print("\n💡 CONSEILS SUPPLÉMENTAIRES:")
print("  - Le jeu DOIT être en mode fenêtré (pas plein écran exclusif)")
print("  - Ne déplacez pas la fenêtre du jeu entre les sessions")
print("  - Gardez toujours la même résolution")
print("  - Fermez les overlays (Discord, Steam, GeForce Experience)")

print("\n" + "="*70 + "\n")


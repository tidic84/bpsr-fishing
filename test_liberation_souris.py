"""
Test pour identifier comment libérer la souris dans votre jeu
"""

import pyautogui
import time

print("\n" + "="*70)
print(" TEST DE LIBÉRATION DE SOURIS")
print("="*70 + "\n")

print("Ce script va tester différentes touches pour libérer la souris.\n")
print("⚠ IMPORTANT:")
print("  1. Ouvrez votre jeu")
print("  2. Allez à l'endroit de pêche")
print("  3. Mettez le jeu au PREMIER PLAN")
print("  4. NE TOUCHEZ À RIEN pendant les tests\n")

input("Appuyez sur ENTRÉE quand vous êtes prêt...")

print("\nLe test commencera dans 5 secondes...")
for i in range(5, 0, -1):
    print(f"{i}...")
    time.sleep(1)

print("\n🧪 DÉBUT DES TESTS\n")

touches_a_tester = [
    ('esc', 'ESC'),
    ('tab', 'Tab'),
    ('alt', 'Alt'),
    ('m', 'M (Menu)'),
    ('i', 'I (Inventaire)'),
    ('e', 'E'),
    ('f1', 'F1'),
]

for touche, nom in touches_a_tester:
    print("="*70)
    print(f" TEST : Touche {nom}")
    print("="*70)
    
    print(f"\n1. Appui sur {nom}...")
    pyautogui.press(touche)
    time.sleep(1)
    
    print(f"2. Tentative de déplacement de souris...")
    # Sauvegarder position actuelle
    start_x, start_y = pyautogui.position()
    
    # Essayer de bouger la souris
    target_x, target_y = start_x + 100, start_y + 100
    pyautogui.moveTo(target_x, target_y, duration=0.3)
    time.sleep(0.3)
    
    # Vérifier où est la souris
    actual_x, actual_y = pyautogui.position()
    
    if abs(actual_x - target_x) < 10 and abs(actual_y - target_y) < 10:
        print(f"   ✅ LA SOURIS A BOUGÉ! {nom} LIBÈRE LA SOURIS!")
        print(f"   Position atteinte: ({actual_x}, {actual_y})")
        
        print(f"\n3. Test de clic...")
        pyautogui.click(actual_x, actual_y)
        time.sleep(0.5)
        
        print(f"4. Retour avec {nom}...")
        pyautogui.press(touche)
        time.sleep(1)
        
        print(f"\n   ⭐ RÉSULTAT: La touche {nom} fonctionne!")
        print(f"   → Utilisez cette touche dans fishing_bot_with_esc.py\n")
    else:
        print(f"   ❌ La souris n'a pas bougé")
        print(f"   Visée: ({target_x}, {target_y})")
        print(f"   Réelle: ({actual_x}, {actual_y})")
        print(f"   {nom} ne libère PAS la souris\n")
    
    # Pause entre les tests
    time.sleep(2)
    
    # Essayer de revenir à l'état normal
    pyautogui.press('esc')
    time.sleep(0.5)

print("\n" + "="*70)
print(" TESTS TERMINÉS")
print("="*70 + "\n")

print("📊 RAPPORT:")
print("\nRésumez vos observations:")
print("1. Quelle touche a libéré la souris?")
touche_reponse = input("   Réponse: ")

print("\n2. Quand cette touche est pressée, que se passe-t-il?")
print("   a) Un menu s'ouvre")
print("   b) Le jeu se met en pause")
print("   c) L'interface change")
print("   d) Rien de visible mais la souris est libre")
menu_reponse = input("   Réponse (a/b/c/d): ")

print("\n3. Où devez-vous cliquer pour commencer la pêche?")
print("   a) Au centre de l'écran")
print("   b) Sur un bouton/NPC spécifique")
print("   c) Sur l'eau")
print("   d) Dans un menu")
clic_reponse = input("   Réponse (a/b/c/d): ")

print("\n" + "="*70)
print(" RECOMMANDATION")
print("="*70 + "\n")

if touche_reponse:
    print(f"✅ Utilisez fishing_bot_with_esc.py avec la touche: {touche_reponse}")
    print(f"\nCommandes:")
    print(f"  1. python calibration.py")
    print(f"     → Capturez le point d'exclamation (!)")
    print(f"     → Capturez le bouton Continue")
    
    if clic_reponse in ['b', 'c', 'd']:
        print(f"     → Capturez la POSITION de clic pour démarrer la pêche")
    
    print(f"\n  2. python fishing_bot_with_esc.py")
    print(f"     → Entrez '{touche_reponse}' quand demandé\n")
    
    print(f"💡 Le bot va:")
    print(f"   1. Appuyer sur {touche_reponse} pour libérer la souris")
    print(f"   2. Cliquer pour démarrer la pêche")
    print(f"   3. Détecter le point d'exclamation")
    print(f"   4. Cliquer sur Continue")
else:
    print("❌ AUCUNE TOUCHE NE LIBÈRE LA SOURIS")
    print("\nPossibilités:")
    print("  1. Vérifiez les PARAMÈTRES du jeu:")
    print("     → Cherchez 'Verrouiller la souris' / 'Mouse Lock'")
    print("     → DÉSACTIVEZ cette option")
    print("\n  2. Le jeu utilise peut-être une mécanique différente")
    print("     → Quel est le nom de votre jeu?")
    print("     → Comment pêchez-vous manuellement?")
    print("\n  3. Essayez d'ouvrir un menu spécifique:")
    print("     → Menu de pêche / Fishing menu")
    print("     → Inventaire")
    print("     → Carte")

print("\n" + "="*70 + "\n")



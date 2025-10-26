"""
Test de clic bas niveau (SendInput) - Comme OP Auto Clicker
"""

import ctypes
import time
import pyautogui

# Constantes Windows
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

def low_level_click(x, y):
    """Clic bas niveau avec SendInput (comme OP Auto Clicker)"""
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    
    # Convertir en coordonnées absolues
    abs_x = int(x * 65535 / screen_width)
    abs_y = int(y * 65535 / screen_height)
    
    # Déplacer
    move_input = INPUT()
    move_input.type = 0
    move_input.mi = MOUSEINPUT(
        abs_x, abs_y, 0,
        MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE,
        0, None
    )
    
    # Clic bas
    down_input = INPUT()
    down_input.type = 0
    down_input.mi = MOUSEINPUT(
        abs_x, abs_y, 0,
        MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_ABSOLUTE,
        0, None
    )
    
    # Clic haut
    up_input = INPUT()
    up_input.type = 0
    up_input.mi = MOUSEINPUT(
        abs_x, abs_y, 0,
        MOUSEEVENTF_LEFTUP | MOUSEEVENTF_ABSOLUTE,
        0, None
    )
    
    # Envoyer
    ctypes.windll.user32.SendInput(1, ctypes.byref(move_input), ctypes.sizeof(INPUT))
    time.sleep(0.01)
    ctypes.windll.user32.SendInput(1, ctypes.byref(down_input), ctypes.sizeof(INPUT))
    time.sleep(0.05)
    ctypes.windll.user32.SendInput(1, ctypes.byref(up_input), ctypes.sizeof(INPUT))

print("\n" + "="*70)
print(" TEST DE CLIC BAS NIVEAU (SendInput)")
print("="*70 + "\n")

print("Ce test utilise la même méthode que OP Auto Clicker")
print("(API Windows SendInput - bas niveau)\n")

# Déterminer la position
print("Où voulez-vous tester le clic?")
print("1. Centre de l'écran")
print("2. Position de la souris actuelle")
print("3. Position manuelle\n")

choice = input("Choix (1-3): ").strip()

if choice == "1":
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    x, y = screen_width // 2, screen_height // 2
    print(f"\n✓ Position: Centre ({x}, {y})")

elif choice == "2":
    print("\nDéplacez votre souris à l'endroit désiré...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    x, y = pyautogui.position()
    print(f"\n✓ Position capturée: ({x}, {y})")

else:
    x = int(input("X: "))
    y = int(input("Y: "))
    print(f"\n✓ Position: ({x}, {y})")

print("\n⚠ IMPORTANT:")
print("  1. Ouvrez votre JEU")
print("  2. Mettez le jeu au PREMIER PLAN")
print("  3. Positionnez-vous pour pêcher")
print("\nLe test commencera dans 5 secondes...")

input("\nAppuyez sur ENTRÉE pour continuer...")

for i in range(5, 0, -1):
    print(f"{i}...")
    time.sleep(1)

print("\n🧪 TEST EN COURS...\n")

# Effectuer 3 clics de test
for i in range(1, 4):
    print(f"Test #{i}:")
    print(f"  → Clic bas niveau (SendInput) à ({x}, {y})...")
    
    low_level_click(x, y)
    
    print(f"  ✓ Clic #{i} envoyé!")
    
    if i < 3:
        print(f"  Attente de 2 secondes...\n")
        time.sleep(2)

print("\n" + "="*70)
print(" TEST TERMINÉ")
print("="*70 + "\n")

print("❓ QUESTIONS:")
print("\n1. Avez-vous vu la souris se déplacer?")
response1 = input("   (oui/non): ").lower()

print("\n2. Est-ce que la pêche a démarré dans le jeu?")
response2 = input("   (oui/non): ").lower()

print("\n" + "="*70)
print(" DIAGNOSTIC")
print("="*70 + "\n")

if response1 == "non":
    print("❌ PROBLÈME: La souris n'a pas bougé")
    print("\nPossible que:")
    print("  - Python n'a pas les permissions")
    print("  - Un antivirus bloque SendInput")
    print("\nSolution:")
    print("  - Lancez en administrateur")

elif response2 == "non":
    print("⚠ PROBLÈME: La souris bouge mais la pêche ne démarre pas")
    print("\nVérifiez:")
    print("  1. La POSITION de clic est-elle correcte?")
    print("  2. Faut-il MAINTENIR le clic au lieu d'un simple clic?")
    print("  3. Faut-il un DOUBLE-CLIC?")
    print("\n💡 Test de maintien du clic:")
    test = input("   Voulez-vous tester un clic maintenu? (oui/non): ")
    
    if test.lower() == "oui":
        print("\n   Test dans 3 secondes...")
        time.sleep(3)
        
        # Clic maintenu
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        abs_x = int(x * 65535 / screen_width)
        abs_y = int(y * 65535 / screen_height)
        
        # Bas
        down_input = INPUT()
        down_input.type = 0
        down_input.mi = MOUSEINPUT(abs_x, abs_y, 0, MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_ABSOLUTE, 0, None)
        ctypes.windll.user32.SendInput(1, ctypes.byref(down_input), ctypes.sizeof(INPUT))
        
        print("   → Clic maintenu pendant 2 secondes...")
        time.sleep(2)
        
        # Haut
        up_input = INPUT()
        up_input.type = 0
        up_input.mi = MOUSEINPUT(abs_x, abs_y, 0, MOUSEEVENTF_LEFTUP | MOUSEEVENTF_ABSOLUTE, 0, None)
        ctypes.windll.user32.SendInput(1, ctypes.byref(up_input), ctypes.sizeof(INPUT))
        
        print("   ✓ Relâché!")
        print("\n   Est-ce que ça a fonctionné?")

else:
    print("✅ SUCCÈS! Les clics bas niveau fonctionnent!")
    print("\nUtilisez maintenant:")
    print("  python fishing_bot_low_level.py")
    print("\nCe bot utilisera SendInput pour tous les clics,")
    print("exactement comme OP Auto Clicker!")

print("\n" + "="*70 + "\n")


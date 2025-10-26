"""
Script de lancement interactif pour choisir la bonne version du bot
"""

import os
import sys

def clear_screen():
    """Efface l'écran"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Affiche l'en-tête"""
    print("\n" + "="*70)
    print(" 🎣 LANCEUR DE BOT DE PÊCHE")
    print("="*70 + "\n")

def main():
    clear_screen()
    print_header()
    
    print("Ce script va vous aider à choisir la bonne version du bot.\n")
    
    # Question préliminaire importante
    print("="*70)
    print(" QUESTION PRÉLIMINAIRE")
    print("="*70)
    print("\nAvez-vous testé avec OP Auto Clicker (ou similaire) ?")
    print("\n1. OUI - OP Auto Clicker FONCTIONNE dans mon jeu")
    print("2. NON - Je n'ai pas testé")
    print("3. Je ne sais pas ce qu'est OP Auto Clicker\n")
    
    prelim = input("Votre réponse (1-3): ").strip()
    
    if prelim == "1":
        # OP Auto Clicker fonctionne - Solution directe
        clear_screen()
        print_header()
        print("✅ SOLUTION IDENTIFIÉE!\n")
        print("Si OP Auto Clicker fonctionne, votre jeu bloque PyAutoGUI")
        print("mais accepte les clics bas niveau (SendInput).\n")
        print("Utilisez: fishing_bot_low_level.py\n")
        print("Cette version utilise SendInput (API Windows)")
        print("exactement comme OP Auto Clicker!\n")
        print("Commandes:")
        print("  1. python test_clic_bas_niveau.py  (tester d'abord)")
        print("  2. python calibration.py           (capturer images)")
        print("  3. python fishing_bot_low_level.py (lancer le bot)\n")
        
        launch = input("Voulez-vous lancer le test maintenant? (o/n): ").lower()
        if launch == 'o':
            print("\n🚀 Lancement de test_clic_bas_niveau.py...\n")
            os.system('python test_clic_bas_niveau.py')
        return
    
    print("Répondez à quelques questions simples...\n")
    
    # Question 1
    print("="*70)
    print(" QUESTION 1 : La souris est-elle libre dans le jeu ?")
    print("="*70)
    print("\n(Pouvez-vous bouger le curseur librement comme dans un menu ?)\n")
    print("1. OUI - La souris est libre, je peux la déplacer")
    print("2. NON - La souris est bloquée/capturée par le jeu")
    print("3. Je ne sais pas / Besoin d'aide\n")
    
    q1 = input("Votre réponse (1-3): ").strip()
    
    if q1 == "1":
        # Souris libre - Bot normal
        clear_screen()
        print_header()
        print("✅ RECOMMANDATION: Bot SOURIS NORMALE\n")
        print("Votre jeu ne capture pas la souris, utilisez le bot standard.\n")
        print("Commandes:")
        print("  1. python calibration.py   (si pas encore fait)")
        print("  2. python fishing_bot.py\n")
        
        launch = input("Voulez-vous lancer le bot maintenant? (o/n): ").lower()
        if launch == 'o':
            print("\n🚀 Lancement de fishing_bot.py...\n")
            os.system('python fishing_bot.py')
        return
    
    elif q1 == "3":
        # Besoin d'aide
        clear_screen()
        print_header()
        print("📖 AIDE: Comment savoir si la souris est capturée ?\n")
        print("1. Lancez votre jeu")
        print("2. Allez dans la zone de jeu (pas un menu)")
        print("3. Essayez de déplacer votre souris")
        print("\nSi :")
        print("  - Le curseur bouge librement → Souris LIBRE")
        print("  - Le curseur est invisible ou bloqué → Souris CAPTURÉE")
        print("  - La caméra tourne quand vous bougez la souris → Souris CAPTURÉE\n")
        
        input("Appuyez sur Entrée pour relancer le questionnaire...")
        main()
        return
    
    # Question 2 - Souris capturée
    clear_screen()
    print_header()
    print("="*70)
    print(" QUESTION 2 : Comment démarrez-vous la pêche manuellement ?")
    print("="*70)
    print("\n1. J'appuie sur une TOUCHE (E, F, Espace, etc.)")
    print("2. Je CLIQUE à un endroit précis")
    print("3. J'ouvre un MENU puis je clique")
    print("4. Autre / Je ne sais pas\n")
    
    q2 = input("Votre réponse (1-4): ").strip()
    
    if q2 == "1":
        # Touche clavier - Bot keyboard
        clear_screen()
        print_header()
        print("✅ RECOMMANDATION: Bot CLAVIER\n")
        print("Votre jeu utilise une touche pour pêcher.\n")
        print("Cette version:")
        print("  - Appuie sur votre touche de pêche")
        print("  - Détecte le point d'exclamation")
        print("  - Re-appuie sur la touche pour attraper")
        print("  - Clique sur Continue dans le menu\n")
        
        print("Commandes:")
        print("  1. python calibration.py         (capturer ! et Continue)")
        print("  2. python fishing_bot_keyboard.py\n")
        
        print("💡 Le bot vous demandera quelle touche utiliser (E, F, espace, etc.)\n")
        
        launch = input("Voulez-vous lancer le bot maintenant? (o/n): ").lower()
        if launch == 'o':
            print("\n🚀 Lancement de fishing_bot_keyboard.py...\n")
            os.system('python fishing_bot_keyboard.py')
        return
    
    elif q2 == "2":
        # Clic - Bot with ESC
        clear_screen()
        print_header()
        print("="*70)
        print(" QUESTION 3 : Quelle touche libère la souris ?")
        print("="*70)
        print("\n(Essayez ESC, Tab ou Alt dans le jeu)\n")
        print("1. ESC libère la souris")
        print("2. Tab libère la souris")
        print("3. Alt libère la souris")
        print("4. Aucune touche ne libère la souris\n")
        
        q3 = input("Votre réponse (1-4): ").strip()
        
        if q3 in ["1", "2", "3"]:
            clear_screen()
            print_header()
            print("✅ RECOMMANDATION: Bot LIBÉRATION ESC\n")
            print("Cette version:")
            print("  - Appuie sur la touche pour libérer la souris")
            print("  - Clique à la position de pêche")
            print("  - Détecte le point d'exclamation")
            print("  - Clique sur Continue\n")
            
            print("Commandes:")
            print("  1. python calibration.py           (tout calibrer)")
            print("  2. python fishing_bot_with_esc.py\n")
            
            print("💡 Le bot vous demandera quelle touche utiliser\n")
            
            launch = input("Voulez-vous lancer le bot maintenant? (o/n): ").lower()
            if launch == 'o':
                print("\n🚀 Lancement de fishing_bot_with_esc.py...\n")
                os.system('python fishing_bot_with_esc.py')
        else:
            clear_screen()
            print_header()
            print("⚠️ SITUATION DIFFICILE\n")
            print("Votre jeu capture la souris ET ne la libère pas facilement.\n")
            print("Solutions possibles:\n")
            print("1. Cherchez dans les paramètres du jeu:")
            print("   - 'Verrouiller la souris' / 'Mouse Lock'")
            print("   - Désactivez cette option\n")
            print("2. Vérifiez si votre jeu utilise une touche:")
            print("   - Relancez et choisissez option 1\n")
            print("3. Utilisez des macros matériels:")
            print("   - Souris/clavier programmable\n")
            print("4. Utilisez AutoHotkey (Windows):")
            print("   - Plus bas niveau que PyAutoGUI\n")
            
            print("\n📖 Consultez SOLUTION_SOURIS_CAPTUREE.md pour plus de détails\n")
        return
    
    elif q2 == "3":
        # Menu
        clear_screen()
        print_header()
        print("✅ RECOMMANDATION: Bot LIBÉRATION ESC\n")
        print("Cette version gère l'ouverture de menus.\n")
        print("Commandes:")
        print("  1. python calibration.py")
        print("  2. python fishing_bot_with_esc.py\n")
        
        launch = input("Voulez-vous lancer le bot maintenant? (o/n): ").lower()
        if launch == 'o':
            print("\n🚀 Lancement de fishing_bot_with_esc.py...\n")
            os.system('python fishing_bot_with_esc.py')
        return
    
    else:
        # Autre
        clear_screen()
        print_header()
        print("❓ BESOIN DE PLUS D'INFORMATIONS\n")
        print("Pour vous aider au mieux, consultez:\n")
        print("  - CHOISIR_VERSION.md         (Guide complet)")
        print("  - SOLUTION_SOURIS_CAPTUREE.md (Solutions détaillées)")
        print("\nOu relancez ce script et essayez différentes réponses.\n")
        return

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Annulé par l'utilisateur\n")
    except Exception as e:
        print(f"\n❌ Erreur: {e}\n")


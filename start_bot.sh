#!/bin/bash
# Script de lancement rapide pour Linux/macOS

echo "=========================================="
echo "   BOT D'AUTOMATISATION DE PECHE"
echo "=========================================="
echo ""

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "[ERREUR] Environnement virtuel non trouvé!"
    echo "Veuillez d'abord exécuter: python3 -m venv venv"
    echo "Puis: source venv/bin/activate"
    echo "Et: pip install -r requirements.txt"
    echo ""
    read -p "Appuyez sur Entrée pour continuer..."
    exit 1
fi

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source venv/bin/activate

# Vérifier si la calibration a été faite
if [ ! -f "images_reference/exclamation_point.png" ]; then
    echo ""
    echo "[ATTENTION] Aucune image de calibration trouvée!"
    echo ""
    read -p "Voulez-vous lancer la calibration maintenant? (O/N) " choice
    case "$choice" in 
        o|O|oui|OUI|Oui )
            python calibration.py
            ;;
        * )
            echo ""
            echo "Veuillez exécuter la calibration d'abord: python calibration.py"
            read -p "Appuyez sur Entrée pour continuer..."
            exit 1
            ;;
    esac
fi

# Lancer le bot
echo ""
echo "=========================================="
echo "   CHOIX DU BOT"
echo "=========================================="
echo ""
echo "Quelle version voulez-vous lancer?"
echo ""
echo "1. Lanceur interactif (RECOMMANDE)"
echo "2. Bot CLAVIER (touche pour pecher)"
echo "3. Bot avec liberation ESC"
echo "4. Bot NORMAL (souris libre)"
echo "5. Calibration"
echo ""

read -p "Votre choix (1-5): " choice

case "$choice" in
    1)
        python lancer_bot.py
        ;;
    2)
        python fishing_bot_keyboard.py
        ;;
    3)
        python fishing_bot_with_esc.py
        ;;
    4)
        python fishing_bot.py
        ;;
    5)
        python calibration.py
        ;;
    *)
        echo "Choix invalide, lancement du lanceur interactif..."
        python lancer_bot.py
        ;;
esac

read -p "Appuyez sur Entrée pour continuer..."


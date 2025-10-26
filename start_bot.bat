@echo off
REM Script de lancement rapide pour Windows
echo ==========================================
echo   BOT D'AUTOMATISATION DE PECHE
echo ==========================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\" (
    echo [ERREUR] Environnement virtuel non trouve!
    echo Veuillez d'abord executer: python -m venv venv
    echo Puis: venv\Scripts\activate
    echo Et: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Vérifier si la calibration a été faite
if not exist "images_reference\exclamation_point.png" (
    echo.
    echo [ATTENTION] Aucune image de calibration trouvee!
    echo.
    echo Voulez-vous lancer la calibration maintenant? (O/N)
    set /p choice=
    if /i "%choice%"=="O" (
        python calibration.py
    ) else (
        echo.
        echo Veuillez executer la calibration d'abord: python calibration.py
        pause
        exit /b 1
    )
)

REM Lancer le bot
echo.
echo ==========================================
echo   CHOIX DU BOT
echo ==========================================
echo.
echo Quelle version voulez-vous lancer?
echo.
echo 1. Lanceur interactif (RECOMMANDE)
echo 2. Bot BAS NIVEAU (comme OP Auto Clicker) NOUVEAU!
echo 3. Bot CLAVIER (touche pour pecher)
echo 4. Bot avec liberation ESC
echo 5. Bot NORMAL (souris libre)
echo 6. Calibration
echo 7. Test clic bas niveau
echo.

set /p choice="Votre choix (1-7): "

if "%choice%"=="1" (
    python lancer_bot.py
) else if "%choice%"=="2" (
    python fishing_bot_low_level.py
) else if "%choice%"=="3" (
    python fishing_bot_keyboard.py
) else if "%choice%"=="4" (
    python fishing_bot_with_esc.py
) else if "%choice%"=="5" (
    python fishing_bot.py
) else if "%choice%"=="6" (
    python calibration.py
) else if "%choice%"=="7" (
    python test_clic_bas_niveau.py
) else (
    echo Choix invalide, lancement du lanceur interactif...
    python lancer_bot.py
)

pause


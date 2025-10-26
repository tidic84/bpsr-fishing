╔══════════════════════════════════════════════════════════════════════════════╗
║                    GUIDE DES IMAGES DE RÉFÉRENCE                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

Ce dossier contient les images capturées lors de la calibration.
Ces images sont utilisées par le bot pour détecter les éléments du jeu.

┌──────────────────────────────────────────────────────────────────────────────┐
│ FICHIERS ATTENDUS                                                             │
└──────────────────────────────────────────────────────────────────────────────┘

📄 exclamation_point.png
   → Image du point d'exclamation (!) qui apparaît quand le poisson mord
   → Capturez UNIQUEMENT le symbole, sans trop d'espace autour
   → Exemple de taille : 30x30 à 100x100 pixels

📄 button_continue.png
   → Image du bouton "Continue" (ou "Continuer")
   → Capturez le bouton entier avec son texte
   → Exemple de taille : 100x50 à 200x100 pixels

📄 button_exit.png (optionnel)
   → Image du bouton "Exit" ou "Quitter"
   → Utile pour des fonctionnalités avancées

📄 positions.txt
   → Fichier texte contenant les positions de clic
   → Format : nom=x,y
   → Exemple : fishing_start=960,540

┌──────────────────────────────────────────────────────────────────────────────┐
│ CONSEILS POUR DE BONNES CAPTURES                                              │
└──────────────────────────────────────────────────────────────────────────────┘

✓ QUALITÉ DE L'IMAGE
  - Assurez-vous que l'image est nette et claire
  - Évitez les captures floues ou pixelisées
  - Utilisez toujours la même résolution de jeu

✓ CADRAGE
  - Capturez uniquement l'élément ciblé
  - Évitez d'inclure trop d'arrière-plan
  - Le bot cherche une correspondance exacte

✓ ÉCLAIRAGE ET EFFETS
  - Capturez l'élément dans des conditions d'éclairage normales
  - Évitez les captures pendant des effets spéciaux
  - Si l'élément change de couleur, capturez sa version la plus commune

✓ POSITION ET RÉSOLUTION
  - Gardez toujours la même résolution de jeu
  - Ne changez pas la position de la fenêtre du jeu
  - Si vous changez de résolution, recalibrez tout

┌──────────────────────────────────────────────────────────────────────────────┐
│ EXEMPLES DE BONNES VS MAUVAISES CAPTURES                                      │
└──────────────────────────────────────────────────────────────────────────────┘

❌ MAUVAIS : Capture trop large avec beaucoup d'arrière-plan
✓ BON     : Capture serrée autour de l'élément

❌ MAUVAIS : Image floue ou en mouvement
✓ BON     : Image nette et statique

❌ MAUVAIS : Capture pendant un effet visuel (flash, particules)
✓ BON     : Capture de l'élément seul, sans effets

❌ MAUVAIS : Capture avec des variations d'éclairage
✓ BON     : Capture avec l'éclairage par défaut du jeu

┌──────────────────────────────────────────────────────────────────────────────┐
│ QUE FAIRE SI LA DÉTECTION NE FONCTIONNE PAS                                   │
└──────────────────────────────────────────────────────────────────────────────┘

1. VÉRIFIER LES IMAGES
   → Ouvrez les fichiers .png dans ce dossier
   → Vérifiez qu'ils contiennent bien les bons éléments
   → Comparez avec ce qui apparaît dans le jeu

2. RECALIBRER
   → Supprimez les images existantes
   → Relancez : python calibration.py
   → Capturez à nouveau avec plus de précision

3. AJUSTER LA CONFIANCE
   → Dans fishing_bot.py, modifiez le paramètre confidence
   → Essayez 0.7 (moins strict) ou 0.9 (plus strict)

4. TESTER AVEC DES VARIATIONS
   → Si l'élément change d'apparence, capturez plusieurs versions
   → Renommez-les : exclamation_point_1.png, exclamation_point_2.png
   → Modifiez le code pour chercher toutes les versions

┌──────────────────────────────────────────────────────────────────────────────┐
│ FORMAT DU FICHIER positions.txt                                               │
└──────────────────────────────────────────────────────────────────────────────┘

Exemple de contenu :

fishing_start=960,540
backup_position=800,600

Format : nom_position=coordonnée_x,coordonnée_y

┌──────────────────────────────────────────────────────────────────────────────┐
│ SAUVEGARDES ET VERSIONS                                                       │
└──────────────────────────────────────────────────────────────────────────────┘

💡 Conseil : Faites une copie de vos bonnes calibrations!

Créez un dossier "backup_calibrations" et copiez-y vos images quand la
détection fonctionne bien. Vous pourrez les restaurer en cas de problème.

┌──────────────────────────────────────────────────────────────────────────────┐
│ NOTES TECHNIQUES                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

• Le bot utilise OpenCV pour la correspondance de template (template matching)
• L'algorithme utilisé : cv2.TM_CCOEFF_NORMED
• Seuil de confiance par défaut : 0.8 (80%)
• Format supporté : PNG (recommandé), JPG (acceptable)

╔══════════════════════════════════════════════════════════════════════════════╗
║  Si ce dossier est vide, lancez d'abord : python calibration.py             ║
╚══════════════════════════════════════════════════════════════════════════════╝


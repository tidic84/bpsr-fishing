"""
Fichier de configuration d'exemple pour le bot de pêche

Copiez ce fichier en 'config.py' et modifiez les valeurs selon vos besoins.
Le bot chargera automatiquement config.py s'il existe.
"""

# ============================================
# PARAMÈTRES DE DÉTECTION
# ============================================

# Niveau de confiance pour la détection d'images (0.0 à 1.0)
# Plus élevé = plus précis mais peut rater des détections
# Plus bas = détecte plus facilement mais risque de fausses détections
CONFIDENCE = 0.8

# ============================================
# DÉLAIS ET TIMEOUTS (en secondes)
# ============================================

# Délai après chaque clic
WAIT_AFTER_CLICK = 0.5

# Temps maximum d'attente pour le point d'exclamation
# Si le poisson ne mord pas après ce délai, le bot recommence
EXCLAMATION_TIMEOUT = 30

# Temps maximum d'attente pour le bouton Continue
CONTINUE_BUTTON_TIMEOUT = 10

# Temps d'attente après avoir cliqué sur le point d'exclamation
# Ce délai couvre le temps du QTE ou le succès direct
QTE_WAIT_TIME = 8

# Délai entre chaque cycle de pêche
CYCLE_DELAY = 1

# ============================================
# POSITIONS PERSONNALISÉES
# ============================================

# Si vous voulez forcer une position de clic pour démarrer la pêche
# Format: (x, y) ou None pour utiliser la position du fichier de calibration
FISHING_START_POSITION = None

# Exemples:
# FISHING_START_POSITION = (960, 540)  # Centre d'un écran 1920x1080
# FISHING_START_POSITION = None  # Utiliser la position de calibration

# ============================================
# OPTIONS AVANCÉES
# ============================================

# Désactiver le fail-safe de PyAutoGUI
# Si True, déplacer la souris dans le coin ne stoppe pas le bot
# ATTENTION: Utilisez avec précaution!
DISABLE_FAILSAFE = False

# Afficher les aperçus de détection (pour debug)
# Si True, affiche les zones détectées dans des fenêtres
SHOW_DETECTION_PREVIEW = False

# Région de recherche pour le point d'exclamation
# Format: (x, y, largeur, hauteur) ou None pour tout l'écran
# Réduire la zone de recherche peut accélérer la détection
EXCLAMATION_SEARCH_REGION = None

# Exemples pour un écran 1920x1080:
# EXCLAMATION_SEARCH_REGION = (860, 440, 200, 200)  # Zone centrale
# EXCLAMATION_SEARCH_REGION = None  # Tout l'écran

# Région de recherche pour le bouton Continue
CONTINUE_BUTTON_SEARCH_REGION = None

# ============================================
# STATISTIQUES ET LOGS
# ============================================

# Fréquence d'affichage des statistiques (tous les X cycles)
STATS_FREQUENCY = 10

# Sauvegarder les statistiques dans un fichier
SAVE_STATS = True
STATS_FILENAME = "fishing_stats.txt"

# Sauvegarder les captures d'écran en cas d'erreur
SAVE_ERROR_SCREENSHOTS = True
ERROR_SCREENSHOTS_DIR = "error_screenshots"

# ============================================
# SÉCURITÉ
# ============================================

# Nombre maximum de tentatives consécutives en cas d'erreur
# Le bot s'arrêtera après ce nombre d'échecs consécutifs
MAX_CONSECUTIVE_ERRORS = 5

# Pause de sécurité après plusieurs erreurs (en secondes)
SAFETY_PAUSE_AFTER_ERRORS = 10

# ============================================
# HOTKEYS (raccourcis clavier)
# ============================================

# Touche pour arrêter le bot
STOP_KEY = 'esc'

# Touche pour mettre en pause/reprendre (optionnel)
PAUSE_KEY = 'p'

# ============================================
# NOTIFICATIONS (fonctionnalité future)
# ============================================

# Activer les notifications sonores
ENABLE_SOUND = False

# Son à jouer après X poissons pêchés
NOTIFICATION_EVERY_X_FISH = 50

# ============================================
# NOTES
# ============================================

"""
Conseils pour optimiser votre configuration:

1. CONFIDENCE:
   - Commencez avec 0.8
   - Si trop de fausses détections: augmenter à 0.85-0.9
   - Si le bot rate des détections: diminuer à 0.7-0.75

2. TIMEOUTS:
   - EXCLAMATION_TIMEOUT: Dépend du temps de morsure dans votre jeu
   - QTE_WAIT_TIME: Ajustez selon la durée de vos QTE
   
3. RÉGIONS DE RECHERCHE:
   - Réduire les zones de recherche accélère la détection
   - Utilisez le mode debug pour identifier les bonnes zones
   
4. SÉCURITÉ:
   - Ne désactivez DISABLE_FAILSAFE que si vous êtes sûr de vous
   - MAX_CONSECUTIVE_ERRORS évite les boucles infinies d'erreurs
"""


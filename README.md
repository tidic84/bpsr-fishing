# 🎣 Bot d'Automatisation de Pêche

Bot Python pour automatiser la pêche dans votre jeu préféré en utilisant la reconnaissance d'image.

## 📋 Fonctionnalités

- ✅ Détection automatique du point d'exclamation
- ✅ Gestion automatique du bouton "Continue"
- ✅ Gestion des QTE (attente automatique)
- ✅ Statistiques en temps réel
- ✅ Arrêt d'urgence (touche ESC)
- ✅ Configuration flexible
- ✅ Outil de calibration intégré

## 🔧 Installation

### Prérequis

- Python 3.8 ou supérieur
- Windows (recommandé) / Linux / macOS

### Étapes d'installation

1. **Cloner ou télécharger ce dossier**

2. **Créer un environnement virtuel (recommandé)**

```bash
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Linux/macOS:
source venv/bin/activate
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

**Note importante pour Windows**: L'installation de `keyboard` peut nécessiter des privilèges administrateur. Si vous rencontrez des problèmes, lancez votre terminal en tant qu'administrateur.

## 🎯 Utilisation

### Étape 1: Calibration (OBLIGATOIRE)

Avant d'utiliser le bot, vous devez capturer les images de référence :

```bash
python calibration.py
```

Le script de calibration vous guidera pour capturer :
1. Le **point d'exclamation** qui apparaît pendant la pêche
2. Le **bouton "Continue"** qui apparaît après avoir pêché un poisson
3. (Optionnel) La **position de clic** pour démarrer la pêche

**Conseils pour une bonne calibration :**
- Capturez uniquement l'élément souhaité (pas trop de zone autour)
- Assurez-vous que l'image est nette et bien visible
- Gardez toujours la même résolution de jeu
- Si la détection ne fonctionne pas bien, recalibrez avec différentes captures

### Étape 2: Lancer le bot

```bash
python fishing_bot.py
```

Le bot vous demandera :
1. Le **mode de confiance** (précision de la détection)
   - Mode normal (80%) : Recommandé pour la plupart des cas
   - Mode précis (90%) : Si vous avez des fausses détections
   - Mode souple (70%) : Si le bot ne détecte pas assez souvent

2. Le **nombre de cycles** (optionnel)
   - Laisser vide pour une exécution illimitée
   - Entrer un nombre pour arrêter après X poissons

### Étape 3: Positionner le jeu

- Mettez votre jeu **au premier plan** (fenêtre active)
- Positionnez-vous à l'endroit où vous souhaitez pêcher
- Le bot démarrera après un compte à rebours de 5 secondes

### Arrêt du bot

- **Touche ESC** : Arrêt d'urgence à tout moment
- **Ctrl+C** : Arrêt dans le terminal
- Le bot s'arrêtera automatiquement si vous avez défini un nombre de cycles

## ⚙️ Configuration avancée

### Modifier les délais

Éditez `fishing_bot.py` et modifiez ces valeurs dans `__init__` :

```python
self.wait_after_click = 0.5          # Délai après chaque clic (secondes)
self.exclamation_timeout = 30        # Temps max pour détecter le point d'exclamation
self.continue_button_timeout = 10    # Temps max pour détecter le bouton Continue
self.qte_wait_time = 8              # Temps d'attente pour le QTE
```

### Désactiver le fail-safe

Par défaut, PyAutoGUI arrête le bot si vous déplacez la souris dans le coin supérieur gauche de l'écran. Pour désactiver cette fonctionnalité (décommenter dans `fishing_bot.py`) :

```python
pyautogui.FAILSAFE = False
```

## 📊 Statistiques

Le bot affiche des statistiques tous les 10 cycles :
- Nombre de poissons pêchés
- Nombre de tentatives totales
- Nombre d'erreurs
- Temps écoulé
- Taux de pêche (poissons/heure)

## 🐛 Dépannage

### Le bot ne détecte pas le point d'exclamation

1. Recalibrez avec `python calibration.py`
2. Capturez une zone plus petite autour du point d'exclamation
3. Essayez le mode "souple" (confiance 70%)
4. Vérifiez que la résolution du jeu n'a pas changé

### Le bot ne trouve pas le bouton Continue

1. Recalibrez le bouton Continue
2. Augmentez `self.qte_wait_time` si le QTE prend plus de temps
3. Capturez uniquement le texte "Continue" sans trop de bordure

### Le bot clique au mauvais endroit

1. Recalibrez la position de clic avec `calibration.py`
2. Vérifiez que le jeu est en plein écran ou toujours à la même position

### Erreur "No module named 'cv2'"

```bash
pip install opencv-python
```

### Erreur avec le module 'keyboard' sur Windows

Lancez votre terminal en tant qu'administrateur et réinstallez :

```bash
pip uninstall keyboard
pip install keyboard
```

## ⚠️ Avertissements

- **Utilisation à vos risques et périls** : L'utilisation de bots peut être contraire aux conditions d'utilisation de certains jeux
- **Supervision recommandée** : Ne laissez pas le bot tourner sans surveillance
- **Performances** : Le bot utilise la reconnaissance d'image, ce qui peut être gourmand en ressources

## 📁 Structure des fichiers

```
automation_peche/
├── fishing_bot.py          # Script principal du bot
├── calibration.py          # Outil de calibration
├── requirements.txt        # Dépendances Python
├── README.md              # Ce fichier
└── images_reference/      # Dossier des images capturées
    ├── exclamation_point.png
    ├── button_continue.png
    └── positions.txt
```

## 🔄 Workflow typique

1. **Première utilisation** :
   ```bash
   python calibration.py  # Capturer les images
   python fishing_bot.py  # Lancer le bot
   ```

2. **Utilisations suivantes** :
   ```bash
   python fishing_bot.py  # Le bot utilise les images déjà capturées
   ```

3. **Si la détection ne fonctionne plus** :
   ```bash
   python calibration.py  # Recalibrer
   python fishing_bot.py  # Relancer
   ```

## 💡 Astuces

- **Résolution constante** : Gardez toujours la même résolution et position de fenêtre de jeu
- **Éclairage** : Les conditions d'éclairage dans le jeu doivent être similaires à la calibration
- **Mode fenêtré** : Le mode fenêtré borderless est souvent plus stable que le plein écran
- **Captures multiples** : Si un élément change d'apparence, vous pouvez créer plusieurs templates et modifier le code pour les chercher tous

## 📝 Logs et débug

Pour activer des logs plus détaillés, vous pouvez modifier le code et ajouter des impressions (print) supplémentaires dans les fonctions clés.

## 🤝 Contribution

N'hésitez pas à améliorer ce bot selon vos besoins :
- Ajouter la détection de plus d'éléments
- Implémenter la résolution automatique des QTE
- Ajouter un système de notification (son, webhook, etc.)
- Optimiser la vitesse de détection

## 📜 Licence

Ce projet est fourni "tel quel" à des fins éducatives. Utilisez-le de manière responsable.

---

**Bon courage et bonne pêche ! 🎣**


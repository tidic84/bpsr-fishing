# 🎓 Guide pour Débutants Complets

Ce guide est pour vous si vous n'avez **jamais utilisé Python** ou si vous êtes **nouveau dans l'automatisation de jeux**.

## 📚 Table des matières

1. [Installation de Python](#installation-de-python)
2. [Configuration de l'environnement](#configuration-de-lenvironnement)
3. [Comprendre les fichiers](#comprendre-les-fichiers)
4. [Première utilisation](#première-utilisation)
5. [Dépannage pour débutants](#dépannage-pour-débutants)
6. [Questions fréquentes](#questions-fréquentes)

---

## 1. Installation de Python

### Vérifier si Python est déjà installé

Ouvrez un terminal (PowerShell sur Windows, Terminal sur macOS/Linux) et tapez :

```bash
python --version
```

Ou essayez :

```bash
python3 --version
```

Si vous voyez quelque chose comme `Python 3.x.x`, Python est installé ! ✅

### Si Python n'est pas installé

#### Windows
1. Allez sur [python.org](https://www.python.org/downloads/)
2. Téléchargez la dernière version (3.8 ou supérieur)
3. **IMPORTANT** : Cochez "Add Python to PATH" pendant l'installation
4. Cliquez sur "Install Now"

#### macOS
```bash
# Installer Homebrew d'abord (si pas déjà fait)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Puis installer Python
brew install python3
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

---

## 2. Configuration de l'environnement

### Étape 1 : Ouvrir un terminal dans le bon dossier

#### Windows
1. Ouvrez l'explorateur de fichiers
2. Naviguez vers le dossier `automation_peche`
3. Dans la barre d'adresse en haut, tapez `cmd` et appuyez sur Entrée
   
   OU
   
4. Faites Shift + Clic droit dans le dossier → "Ouvrir dans le terminal"

#### macOS/Linux
1. Ouvrez Terminal
2. Utilisez la commande `cd` pour naviguer :
   ```bash
   cd /chemin/vers/automation_peche
   ```

### Étape 2 : Créer un environnement virtuel

Un environnement virtuel garde vos dépendances Python isolées. C'est une bonne pratique !

```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

Vous verrez un nouveau dossier `venv` apparaître. C'est normal ! ✅

### Étape 3 : Activer l'environnement virtuel

**IMPORTANT** : Vous devez faire ceci **à chaque fois** que vous ouvrez un nouveau terminal.

```bash
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate
```

Vous devriez voir `(venv)` apparaître au début de votre ligne de commande. C'est bon ! ✅

### Étape 4 : Installer les dépendances

```bash
pip install -r requirements.txt
```

Cela va télécharger et installer tous les modules nécessaires. Ça peut prendre quelques minutes. ☕

### Étape 5 : Vérifier l'installation

```bash
python test_installation.py
```

Ce script vérifie que tout est bien installé. Si tout est ✅, vous êtes prêt !

---

## 3. Comprendre les fichiers

Voici à quoi sert chaque fichier :

| Fichier | Description | Quand l'utiliser |
|---------|-------------|------------------|
| `fishing_bot.py` | Le bot principal | Après la calibration |
| `calibration.py` | Outil pour capturer les images | Avant la première utilisation |
| `test_installation.py` | Vérifie que tout est installé | Après l'installation |
| `requirements.txt` | Liste des dépendances | Pour `pip install` |
| `README.md` | Documentation complète | Pour en savoir plus |
| `DEMARRAGE_RAPIDE.txt` | Guide rapide | Référence rapide |
| `start_bot.bat` / `.sh` | Lanceur automatique | Pour démarrer facilement |

---

## 4. Première utilisation

### Étape A : Calibration (OBLIGATOIRE la première fois)

1. **Lancez votre jeu** et allez à l'endroit où vous voulez pêcher

2. **Lancez la calibration** :
   ```bash
   python calibration.py
   ```

3. **Suivez les instructions** pour capturer :
   
   - **Le point d'exclamation (!)** qui apparaît quand le poisson mord
     - Attendez qu'il apparaisse dans le jeu
     - Capturez JUSTE le symbole, pas toute la zone autour
   
   - **Le bouton "Continue"** qui apparaît après avoir pêché
     - Pêchez un poisson manuellement
     - Capturez le bouton quand il apparaît
   
   - **La position de clic** pour démarrer la pêche (optionnel)
     - Placez votre souris où vous cliquez habituellement pour pêcher
     - Appuyez sur Entrée quand demandé

4. **Vérifiez les captures**
   - Allez dans le dossier `images_reference`
   - Ouvrez les fichiers PNG
   - Assurez-vous qu'ils sont nets et corrects

### Étape B : Lancer le bot

1. **Assurez-vous que votre jeu est ouvert** et au premier plan

2. **Lancez le bot** :
   ```bash
   python fishing_bot.py
   ```
   
   Ou double-cliquez sur `start_bot.bat` (Windows) / `start_bot.sh` (Linux/macOS)

3. **Choisissez vos options** :
   - Mode de confiance : Tapez `1` et appuyez sur Entrée (recommandé pour débuter)
   - Nombre de cycles : Appuyez juste sur Entrée pour illimité

4. **Préparez-vous** :
   - Vous avez 5 secondes
   - Mettez votre jeu au premier plan
   - Positionnez-vous pour pêcher

5. **Le bot démarre !** 🎣
   - Observez-le pour les premiers cycles
   - Appuyez sur **ESC** pour arrêter à tout moment

---

## 5. Dépannage pour débutants

### ❌ "python n'est pas reconnu comme une commande"

**Cause** : Python n'est pas dans le PATH de votre système.

**Solution Windows** :
1. Réinstallez Python en cochant "Add Python to PATH"
2. OU ajoutez Python au PATH manuellement :
   - Cherchez "Variables d'environnement" dans Windows
   - Ajoutez le chemin de Python (ex: `C:\Python3x\`)

**Solution macOS/Linux** :
- Utilisez `python3` au lieu de `python`

### ❌ "Accès refusé" lors de l'installation de keyboard

**Cause** : Le module keyboard nécessite des droits administrateur.

**Solution Windows** :
1. Clic droit sur PowerShell → "Exécuter en tant qu'administrateur"
2. Réexécutez : `pip install keyboard`

### ❌ Le bot ne détecte rien

**Causes possibles** :
- La calibration n'a pas été faite
- Les images capturées sont de mauvaise qualité
- La résolution du jeu a changé

**Solutions** :
1. Recalibrez avec `python calibration.py`
2. Capturez des zones plus petites et plus précises
3. Assurez-vous que le jeu est à la même résolution qu'à la calibration

### ❌ Le bot clique au mauvais endroit

**Cause** : La position du jeu ou la résolution a changé.

**Solutions** :
1. Gardez toujours le jeu à la même position
2. Recalibrez les positions
3. Utilisez le mode fenêtré au lieu du plein écran

### ❌ "ModuleNotFoundError: No module named 'xxx'"

**Cause** : Une dépendance n'est pas installée.

**Solution** :
```bash
# Assurez-vous que l'environnement virtuel est activé
# Vous devriez voir (venv) au début de la ligne

pip install -r requirements.txt
```

---

## 6. Questions fréquentes

### Q : Est-ce que je risque de me faire bannir ?

**R** : Possiblement. L'utilisation de bots peut être contraire aux conditions d'utilisation de certains jeux. Utilisez à vos propres risques.

### Q : Le bot fonctionne-t-il en arrière-plan ?

**R** : Non, le jeu doit être au premier plan. Le bot contrôle la souris et le clavier.

### Q : Puis-je utiliser mon ordinateur pendant que le bot tourne ?

**R** : Non recommandé. Le bot prend le contrôle de la souris et du clavier. Utilisez un ordinateur dédié si possible.

### Q : Combien de temps pour configurer tout ça ?

**R** : 
- Installation de Python : 5-10 minutes
- Installation des dépendances : 5 minutes
- Calibration : 5-10 minutes
- **Total : ~20-30 minutes** pour la première fois

### Q : Puis-je l'utiliser sur plusieurs jeux ?

**R** : Oui ! Il suffit de recalibrer pour chaque jeu. Les images sont spécifiques à chaque jeu.

### Q : Le bot consomme-t-il beaucoup de ressources ?

**R** : La reconnaissance d'image utilise modérément le CPU. Sur un ordinateur récent, ça ne devrait pas poser de problème.

### Q : Que faire si mon antivirus bloque le bot ?

**R** : Certains antivirus peuvent détecter PyAutoGUI comme suspect (car il contrôle la souris/clavier). Ajoutez une exception si vous êtes sûr de la source du code.

### Q : Puis-je modifier le code ?

**R** : Absolument ! Le code est en Python pur, vous pouvez le modifier comme vous voulez. Consultez les commentaires dans le code.

### Q : Y a-t-il une version GUI (interface graphique) ?

**R** : Pas pour le moment, mais vous pouvez en créer une en utilisant tkinter ou PyQt si vous êtes à l'aise en Python.

---

## 🎯 Checklist finale avant de commencer

- [ ] Python 3.8+ installé
- [ ] Environnement virtuel créé (`python -m venv venv`)
- [ ] Environnement virtuel activé (vous voyez `(venv)`)
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Test d'installation passé (`python test_installation.py`)
- [ ] Calibration effectuée (`python calibration.py`)
- [ ] Images vérifiées dans `images_reference/`
- [ ] Jeu ouvert et prêt

Si toutes les cases sont cochées, vous êtes prêt ! Lancez `python fishing_bot.py` et profitez ! 🎣

---

## 📞 Besoin d'aide supplémentaire ?

- Consultez le `README.md` pour plus de détails techniques
- Lisez `DEMARRAGE_RAPIDE.txt` pour une référence rapide
- Vérifiez `images_reference/README_IMAGES.txt` pour les conseils de calibration

**Bonne pêche et bon apprentissage ! 🎓🎣**


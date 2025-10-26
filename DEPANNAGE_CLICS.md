# 🔧 Guide de Dépannage - Problèmes de Clic

Ce guide vous aide à résoudre les problèmes où **le bot ne clique pas** ou où **les clics ne sont pas détectés par le jeu**.

---

## 🔍 Diagnostic rapide

Avant tout, lancez le script de test :

```bash
python test_clic_peche.py
```

Ce script vous guidera à travers différents tests pour identifier le problème.

---

## ❌ Problème 1 : La souris ne bouge pas du tout

### Symptômes
- Vous lancez le bot
- Aucun mouvement de souris n'est visible
- Le message "[Étape 1] Démarrage de la pêche..." apparaît mais rien ne se passe

### Causes possibles

1. **PyAutoGUI n'a pas les permissions**
2. **Antivirus bloque l'automatisation**
3. **Problème d'installation**

### Solutions

#### Solution 1 : Vérifier l'installation
```bash
python test_installation.py
```

Si PyAutoGUI n'est pas correctement installé :
```bash
pip uninstall pyautogui
pip install pyautogui==0.9.54
```

#### Solution 2 : Permissions administrateur (Windows)

1. Clic droit sur PowerShell → "Exécuter en tant qu'administrateur"
2. Naviguez vers le dossier :
   ```bash
   cd C:\chemin\vers\automation_peche
   ```
3. Activez l'environnement virtuel :
   ```bash
   venv\Scripts\activate
   ```
4. Relancez le bot :
   ```bash
   python fishing_bot.py
   ```

#### Solution 3 : Antivirus

Ajoutez une exception pour :
- Le dossier `automation_peche`
- L'exécutable Python (`python.exe`)
- Le module PyAutoGUI

**Antivirus courants :**
- **Windows Defender** : Paramètres → Virus et menaces → Gérer les paramètres → Exclusions
- **Avast/AVG** : Paramètres → Général → Exclusions
- **Kaspersky** : Paramètres → Avancé → Menaces et exclusions

---

## ❌ Problème 2 : La souris bouge mais ne clique pas

### Symptômes
- La souris se déplace à la bonne position
- Mais aucun clic n'est effectué
- Ou les clics sont effectués mais le jeu ne réagit pas

### Causes possibles

1. **Le jeu est en plein écran exclusif**
2. **Le jeu bloque les entrées virtuelles**
3. **Le jeu tourne avec des privilèges élevés**

### Solutions

#### Solution 1 : Mode d'affichage du jeu ✅ RECOMMANDÉ

**IMPORTANT** : Changez le mode d'affichage du jeu :

1. Dans les paramètres du jeu
2. Cherchez "Mode d'affichage" ou "Display Mode"
3. Choisissez :
   - ✅ **Fenêtré sans bordure** (Borderless Windowed) - IDÉAL
   - ✅ **Fenêtré** (Windowed) - Fonctionne bien
   - ❌ **Plein écran** (Fullscreen) - Ne fonctionne PAS

**Pourquoi ?**
Le plein écran exclusif empêche Windows de transmettre les entrées virtuelles (souris/clavier) de PyAutoGUI au jeu.

#### Solution 2 : Désactiver les overlays

Certains overlays peuvent interférer. Désactivez :

- **Discord** : Paramètres → Overlay de jeu → Désactiver
- **Steam** : Paramètres → En jeu → Désactiver l'overlay Steam
- **GeForce Experience** : Alt+Z → Paramètres → Overlay de partage → Désactiver
- **Xbox Game Bar** : Windows → Paramètres → Jeux → Désactiver

#### Solution 3 : Ne PAS lancer le jeu en administrateur

Si le jeu tourne en administrateur mais pas Python, PyAutoGUI ne peut pas contrôler le jeu.

**Vérifier** :
1. Clic droit sur l'exécutable du jeu
2. Propriétés → Compatibilité
3. ❌ Décochez "Exécuter ce programme en tant qu'administrateur"

**Alternative** :
Lancez Python en administrateur (voir Problème 1, Solution 2)

#### Solution 4 : Augmenter les délais

Modifiez `fishing_bot.py` :

```python
# Dans la fonction __init__
self.wait_after_click = 1.0  # Au lieu de 0.5
```

Ou dans `safe_click`, augmentez les `time.sleep()`.

---

## ❌ Problème 3 : Les clics fonctionnent mais au mauvais endroit

### Symptômes
- La souris clique
- Mais pas à l'endroit voulu dans le jeu
- La pêche ne démarre pas

### Causes possibles

1. **Position de clic incorrecte**
2. **Résolution du jeu a changé**
3. **Fenêtre du jeu a été déplacée**
4. **Mise à l'échelle Windows (DPI)**

### Solutions

#### Solution 1 : Recalibrer

```bash
python calibration.py
```

Capturez à nouveau la position de clic pour démarrer la pêche.

#### Solution 2 : Tester la position manuellement

1. Lancez Python interactif :
   ```bash
   python
   ```

2. Trouvez la bonne position :
   ```python
   import pyautogui
   import time
   
   # Déplacez votre souris au bon endroit
   time.sleep(3)
   x, y = pyautogui.position()
   print(f"Position: {x}, {y}")
   ```

3. Notez ces coordonnées

4. Modifiez `images_reference/positions.txt` :
   ```
   fishing_start=X,Y
   ```

#### Solution 3 : Mise à l'échelle Windows (DPI)

Sur Windows, si vous avez une mise à l'échelle (125%, 150%, etc.) :

1. Clic droit sur `python.exe` (dans `venv\Scripts\`)
2. Propriétés → Compatibilité
3. Modifier les paramètres PPP élevés
4. ✅ Cochez "Remplacer le comportement de mise à l'échelle PPP élevée"
5. Choisissez "Application"

**Ou** dans le code, au début de `fishing_bot.py`, ajoutez :

```python
# Après les imports
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
```

---

## ❌ Problème 4 : Le clic fonctionne en test mais pas dans le bot

### Symptômes
- `test_clic_peche.py` fonctionne
- Mais `fishing_bot.py` ne clique pas

### Causes possibles

1. **Le jeu perd le focus**
2. **Délais insuffisants**
3. **Le jeu n'est pas prêt**

### Solutions

#### Solution 1 : Forcer le focus sur le jeu

Modifiez `fishing_bot.py`, ajoutez après l'import :

```python
import win32gui
import win32con

def focus_window(window_title):
    """Met une fenêtre au premier plan"""
    try:
        hwnd = win32gui.FindWindow(None, window_title)
        win32gui.SetForegroundWindow(hwnd)
        return True
    except:
        return False
```

Puis avant chaque clic :
```python
focus_window("Nom de votre jeu")  # Remplacez par le titre exact
```

**Installation** :
```bash
pip install pywin32
```

#### Solution 2 : Ajouter un délai au démarrage

Dans `fishing_bot.py`, fonction `run()`, augmentez le compte à rebours :

```python
for i in range(10, 0, -1):  # 10 secondes au lieu de 5
    print(f"{i}...")
    time.sleep(1)
```

#### Solution 3 : Vérifier que le jeu est prêt

Ajoutez une vérification visuelle avant de commencer :

```python
# Au début de fishing_cycle()
print("  ⚠ Assurez-vous que le jeu est prêt!")
time.sleep(2)
```

---

## ❌ Problème 5 : Le jeu nécessite un type de clic spécial

### Symptômes
- Les clics simples ne fonctionnent pas
- La pêche nécessite un double-clic, clic maintenu, etc.

### Solutions

#### Option 1 : Double-clic

Modifiez `safe_click` dans `fishing_bot.py` :

```python
# Remplacez cette ligne
pyautogui.click(x, y, button='left')

# Par
pyautogui.doubleClick(x, y)
```

#### Option 2 : Clic maintenu

```python
# Remplacez par
pyautogui.mouseDown(x, y, button='left')
time.sleep(0.5)  # Maintenir pendant 0.5 secondes
pyautogui.mouseUp(button='left')
```

#### Option 3 : Clic droit

```python
# Remplacez par
pyautogui.click(x, y, button='right')
```

#### Option 4 : Séquence de touches

Peut-être que le jeu utilise une touche au lieu d'un clic :

```python
# Au lieu de click
pyautogui.press('e')  # Ou 'space', 'f', etc.
```

---

## 🧪 Tests de diagnostic

### Test 1 : Vérification basique
```bash
python test_installation.py
```

### Test 2 : Test des clics
```bash
python test_clic.py
```

### Test 3 : Test spécifique pêche
```bash
python test_clic_peche.py
```

### Test 4 : Test manuel dans Python
```bash
python
>>> import pyautogui
>>> pyautogui.click(960, 540)  # Remplacez par vos coordonnées
```

---

## 📝 Checklist complète

Avant de dire que "ça ne fonctionne pas", vérifiez :

- [ ] PyAutoGUI est installé (`pip list | grep pyautogui`)
- [ ] Python est en mode administrateur (si nécessaire)
- [ ] Le jeu est en mode **fenêtré** ou **fenêtré sans bordure**
- [ ] Le jeu n'est PAS lancé en administrateur (sauf si Python l'est aussi)
- [ ] Les overlays sont désactivés (Discord, Steam, etc.)
- [ ] L'antivirus n'a pas bloqué PyAutoGUI
- [ ] La position de clic est correcte (`test_clic_peche.py`)
- [ ] Le jeu est au premier plan
- [ ] La résolution du jeu n'a pas changé
- [ ] La fenêtre du jeu n'a pas été déplacée

---

## 💡 Astuces supplémentaires

### Astuce 1 : Mode debug avec screenshots

Ajoutez dans `fishing_bot.py` après chaque clic :

```python
screenshot = pyautogui.screenshot()
screenshot.save(f"debug_screenshot_{time.time()}.png")
```

Vous pourrez voir où la souris a cliqué exactement.

### Astuce 2 : Logs détaillés

Activez plus de logs en ajoutant des `print()` partout :

```python
print(f"[DEBUG] Position souris: {pyautogui.position()}")
print(f"[DEBUG] Taille écran: {pyautogui.size()}")
print(f"[DEBUG] Clic envoyé à: ({x}, {y})")
```

### Astuce 3 : Tester dans un autre jeu/application

Pour vérifier que PyAutoGUI fonctionne, testez dans :
- Bloc-notes (Notepad)
- Paint
- Un navigateur web

Si ça fonctionne là mais pas dans le jeu, c'est le jeu qui bloque.

---

## 🆘 Dernier recours

Si **rien ne fonctionne** :

1. **Vérifiez que le jeu accepte l'automatisation**
   - Certains jeux anti-cheat bloquent PyAutoGUI
   - Exemples : VAC, EasyAntiCheat, BattlEye

2. **Essayez une alternative**
   - AutoHotkey (Windows) : Plus bas niveau
   - DirectInput : Contourne certaines protections
   - Macro matériel : Souris/clavier programmable

3. **Contactez la communauté**
   - Reddit : r/learnpython, r/automation
   - Discord : Serveurs de développement de bots
   - Forums du jeu : Vérifiez si d'autres ont réussi

---

## ✅ Solutions qui ont fonctionné pour d'autres

**Cas 1** : "Le bot ne cliquait pas dans Final Fantasy XIV"
- **Solution** : Passer en mode fenêtré sans bordure

**Cas 2** : "La souris bougeait mais ne cliquait pas dans Minecraft"
- **Solution** : Désactiver le Discord overlay

**Cas 3** : "Rien ne fonctionnait"
- **Solution** : L'antivirus Avast bloquait PyAutoGUI silencieusement

**Cas 4** : "Le clic était décalé"
- **Solution** : Mise à l'échelle Windows 150%, correction DPI nécessaire

---

**Bonne chance pour résoudre votre problème ! 🎣**


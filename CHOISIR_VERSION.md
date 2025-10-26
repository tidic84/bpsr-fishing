# 🎮 Quelle Version du Bot Utiliser ?

Vous avez maintenant **3 versions** du bot adaptées à différentes situations.

---

## 📊 Comparaison Rapide

| Version | Quand l'utiliser | Fichier |
|---------|------------------|---------|
| **🎹 CLAVIER** | Le jeu utilise une **touche** pour pêcher | `fishing_bot_keyboard.py` |
| **🔓 LIBÉRATION ESC** | Vous devez **cliquer** mais la souris est capturée | `fishing_bot_with_esc.py` |
| **🖱️ SOURIS NORMALE** | Les clics fonctionnent normalement (menus) | `fishing_bot.py` (original) |

---

## 🎹 Version CLAVIER - `fishing_bot_keyboard.py`

### ✅ Utilisez cette version si :
- Votre jeu utilise une **touche** pour démarrer la pêche (E, F, Espace, etc.)
- La souris est capturée pendant le jeu
- Les menus utilisent la souris normalement

### Comment ça marche :
1. Appuie sur votre touche de pêche (ex: E)
2. Détecte le point d'exclamation
3. Re-appuie sur la touche pour attraper
4. Détecte et clique sur "Continue" dans le menu

### Lancement :
```bash
python fishing_bot_keyboard.py
```

Le bot vous demandera quelle touche utiliser.

### Exemple de jeux compatibles :
- Jeux avec action "E" ou "F" pour pêcher
- Jeux où on maintient une touche
- Minecraft (touche pour lancer, pas de clic)

---

## 🔓 Version LIBÉRATION ESC - `fishing_bot_with_esc.py`

### ✅ Utilisez cette version si :
- Vous **devez cliquer** à un endroit précis pour pêcher
- La souris est **capturée** en jeu
- **ESC** (ou Tab/Alt) libère la souris temporairement

### Comment ça marche :
1. Appuie sur ESC pour libérer la souris
2. Clique à la position de pêche
3. (ESC refermé automatiquement ou par le clic)
4. Détecte le point d'exclamation
5. Clique sur Continue dans le menu

### Lancement :
```bash
python fishing_bot_with_esc.py
```

Le bot vous demandera quelle touche libère la souris.

### Exemple de jeux compatibles :
- Jeux avec menu de pêche accessible par ESC
- Jeux où ESC met en pause et libère la souris
- MMO avec UI cliquable

---

## 🖱️ Version SOURIS NORMALE - `fishing_bot.py`

### ✅ Utilisez cette version si :
- Les clics fonctionnent **normalement** dans le jeu
- La souris n'est **PAS capturée**
- C'est un jeu 2D ou un jeu de gestion

### Comment ça marche :
1. Clique directement à la position de pêche
2. Détecte le point d'exclamation
3. Clique sur le point d'exclamation
4. Détecte et clique sur Continue

### Lancement :
```bash
python fishing_bot.py
```

### Exemple de jeux compatibles :
- Jeux 2D (Stardew Valley, Terraria)
- Jeux de gestion/simulation
- Jeux navigateur
- Applications de pêche en fenêtre

---

## 🤔 Vous ne savez pas laquelle choisir ?

### Test rapide :

1. **Lancez votre jeu**
2. **Testez ceci :**
   - Pouvez-vous bouger librement la souris dans le jeu ? 
     - **OUI** → Version SOURIS NORMALE ✅
     - **NON** → Continuez...

3. **La souris est bloquée au centre ?**
   - **OUI** → Continuez...

4. **Pour pêcher manuellement, vous :**
   - Appuyez sur une **touche** (E, F, Espace...) → Version CLAVIER 🎹
   - **Cliquez** à un endroit → Continuez...

5. **Appuyez sur ESC dans le jeu, est-ce que :**
   - La souris redevient **libre** ? → Version LIBÉRATION ESC 🔓
   - Rien ne change → Le jeu bloque vraiment tout (voir solutions avancées)

---

## 🚀 Guide de Démarrage selon Votre Cas

### Cas 1 : Jeu avec touche de pêche (PLUS COURANT)

```bash
# 1. Lancez la calibration (pour le point d'exclamation et Continue)
python calibration.py

# 2. Lancez le bot clavier
python fishing_bot_keyboard.py

# 3. Entrez votre touche (ex: e)
```

### Cas 2 : Jeu avec clic mais souris capturée

```bash
# 1. Lancez la calibration complète
python calibration.py

# 2. Lancez le bot avec libération
python fishing_bot_with_esc.py

# 3. Entrez la touche qui libère la souris (généralement: esc)
```

### Cas 3 : Jeu normal avec souris libre

```bash
# 1. Lancez la calibration complète
python calibration.py

# 2. Lancez le bot normal
python fishing_bot.py
```

---

## 📝 Récapitulatif des Fichiers

| Fichier | Usage |
|---------|-------|
| `fishing_bot.py` | Bot original (souris libre) |
| `fishing_bot_keyboard.py` | **Bot avec touche clavier** ⭐ RECOMMANDÉ |
| `fishing_bot_with_esc.py` | Bot avec libération ESC |
| `calibration.py` | Outil de calibration (toujours nécessaire) |
| `test_clic_peche.py` | Test de diagnostic |

---

## 💡 Conseils

### Pour la Version CLAVIER :
- ✅ C'est souvent la plus fiable
- ✅ Pas besoin de position de clic précise
- ✅ Fonctionne même si l'interface bouge
- ⚠️ Assurez-vous de capturer le point d'exclamation et Continue

### Pour la Version LIBÉRATION ESC :
- ⚠️ Vérifiez que ESC revient bien au jeu après
- ⚠️ Certains jeux nécessitent 2x ESC (ouvrir/fermer menu)
- 💡 Ajustez les délais si nécessaire (voir code)

### Pour la Version SOURIS :
- ✅ La plus simple si elle fonctionne
- ⚠️ Ne fonctionne que si la souris est libre

---

## ❓ Questions Fréquentes

### Q : Puis-je mélanger les versions ?

Non, utilisez une seule version à la fois. Mais vous pouvez modifier le code d'une version pour ajouter des fonctionnalités d'une autre.

### Q : Aucune version ne fonctionne !

Votre jeu utilise peut-être une protection anti-bot. Alternatives :
- Macro matériel (souris/clavier programmable)
- AutoHotkey (Windows, plus bas niveau)
- Contacter la communauté du jeu

### Q : Je veux utiliser une touche ET des clics

Modifiez `fishing_bot_keyboard.py` et adaptez la fonction `fishing_cycle()` selon vos besoins.

### Q : Mon jeu utilise maintenir la touche/clic

Dans le code, remplacez :
```python
pyautogui.press('e')
```

Par :
```python
pyautogui.keyDown('e')
time.sleep(2)  # Durée du maintien
pyautogui.keyUp('e')
```

Ou pour un clic :
```python
pyautogui.mouseDown(x, y)
time.sleep(2)
pyautogui.mouseUp()
```

---

## 🎯 Recommandation Finale

**Pour 90% des jeux où la souris est capturée :**

→ Utilisez **`fishing_bot_keyboard.py`** (Version CLAVIER) 🎹

C'est la solution la plus robuste et la plus simple !

---

**Besoin d'aide ? Consultez `SOLUTION_SOURIS_CAPTUREE.md` pour plus de détails !**



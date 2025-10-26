# 🎣 Gestion Automatique des Cannes à Pêche

## 🆕 Nouvelle Fonctionnalité

Le bot peut maintenant **détecter et remplacer automatiquement** les cannes à pêche cassées !

---

## 🔧 Comment ça Fonctionne

### **Logique Complète**

```
Fin de pêche (succès ou échec)
    ↓
Attente que la canne soit "prête"
    ↓
[Vérification de la canne] ← NOUVEAU !
    ↓
    ┌─────────────┴──────────────┐
    │                            │
Canne OK ?              Canne cassée ?
    │                            │
    ↓                            ↓
Recommencer          Appuyer sur ","
                            ↓
                    Ouvrir menu cannes
                            ↓
                    Cliquer sur "Use"
                            ↓
                    Fermer le menu
                            ↓
                        Recommencer
```

### **Ce que fait le bot**

À la fin de chaque cycle (succès ou échec), le bot :

1. **Vérifie visuellement** si la canne est cassée (optionnel)
2. **Ouvre le menu** de cannes avec la touche **`,`** (virgule)
3. **Détecte et clique** sur le bouton **"Use"**
4. **Ferme le menu** avec **`,`**
5. **Recommence** la pêche

---

## 📸 Calibration

### **Images à Capturer**

Pour activer cette fonctionnalité, lancez :

```bash
python calibration.py
```

Le script vous demandera de capturer **2 nouveaux éléments** :

#### **1. Bouton "Use"** ⭐ (Recommandé)

**Quand demandé :**
> 💡 GESTION DES CANNES: Voulez-vous capturer le bouton 'Use'?

Répondez **OUI**

**Comment capturer :**
1. Dans le jeu, appuyez sur **`,`** pour ouvrir le menu de cannes
2. Capturez le bouton **"Use"** à côté d'une canne disponible
3. Capturez **juste le bouton**, pas toute la ligne

**Exemple de bouton :**
```
[ Canne à pêche en bambou ]  [Use]  ← Capturez juste "Use"
[ Canne à pêche renforcée ]  [Use]
```

#### **2. Indicateur "Canne Cassée"** (Optionnel)

**Quand demandé :**
> 💡 DÉTECTION AVANCÉE: Voulez-vous capturer l'indicateur 'canne cassée'?

Répondez **OUI** (optionnel mais utile)

**Comment capturer :**
- Capturez un élément qui **apparaît uniquement** quand la canne est cassée
- Peut être : une icône, un texte "Broken", un symbole ⚠️, etc.
- Si vous capturez cet élément, le bot ne vérifiera le menu **que si** cet indicateur est détecté

---

## ⚙️ Configuration

### **Mode 1 : Avec Détection de Canne Cassée** (Optimal)

**Avantages :**
- ✅ Ne vérifie le menu que si la canne est vraiment cassée
- ✅ Plus rapide (pas de vérification inutile)
- ✅ Moins d'ouvertures de menu

**Comment :**
Capturez les **2 images** : `use_button.png` ET `rod_broken.png`

**Comportement :**
```python
if canne_cassée_détectée:
    ouvrir_menu()
    cliquer_use()
    fermer_menu()
else:
    # Canne OK, continuer directement
```

### **Mode 2 : Vérification Systématique** (Plus Simple)

**Avantages :**
- ✅ Fonctionne sans image de canne cassée
- ✅ Vérifie toujours (plus sûr)
- ⚠️ Ouvre le menu à chaque cycle

**Comment :**
Capturez **uniquement** `use_button.png` (pas `rod_broken.png`)

**Comportement :**
```python
# À chaque fin de cycle
ouvrir_menu()
cliquer_use()  # Si bouton trouvé
fermer_menu()
```

### **Mode 3 : Sans Détection** (Basique)

Si vous ne capturez **aucune** image :
- Le bot ouvrira et fermera le menu à chaque cycle
- Pas de clic sur "Use"
- Fonctionne si le jeu garde la canne sélectionnée

---

## 🎮 Utilisation

Une fois calibré, **rien de plus à faire** ! Le bot gère tout automatiquement.

```bash
python fishing_bot_low_level.py
```

**Vous verrez dans les logs :**

### **Si canne OK :**
```
[Vérification] Contrôle de l'état de la canne...
  ✓ Canne en bon état
```

### **Si canne cassée (avec détection) :**
```
[Vérification] Contrôle de l'état de la canne...
  ⚠️ Canne cassée détectée visuellement!
  → Ouverture du menu de cannes (touche ',')...
  → Recherche du bouton 'Use'...
  ✓ Bouton 'Use' trouvé à (1024, 768)
  → Clic bas niveau (SendInput) à (1024, 768)...
  ✓ Clic effectué avec succès!
  → Fermeture du menu...
  ✓ Canne équipée avec succès!
```

### **Si vérification systématique :**
```
[Vérification] Contrôle de l'état de la canne...
  → Ouverture du menu de cannes (touche ',')...
  → Recherche du bouton 'Use'...
  ✓ Bouton 'Use' trouvé à (1024, 768)
  → Fermeture du menu...
  ✓ Canne équipée avec succès!
```

---

## 🔧 Paramètres Ajustables

### **Délais du Menu**

Si le menu met du temps à s'ouvrir/fermer, modifiez dans `fishing_bot_low_level.py` :

```python
# Ligne ~234
pyautogui.press(',')
time.sleep(0.8)  # ← Augmentez si menu lent (ex: 1.2)
```

### **Timeout de Recherche**

Si le bouton "Use" met du temps à apparaître :

```python
# Ligne ~239
use_pos = self.find_on_screen("use_button", timeout=3)  # ← Augmentez (ex: 5)
```

### **Désactiver la Vérification**

Si vous voulez désactiver complètement cette fonctionnalité :

```python
# Dans fishing_cycle(), commentez ces lignes :
# self.check_and_repair_rod()
```

---

## 📊 Impact sur les Performances

| Situation | Temps Ajouté | Fréquence |
|-----------|--------------|-----------|
| Canne OK (avec détection) | ~0.5s | À chaque cycle |
| Canne cassée | ~3-4s | Quand cassée |
| Vérification systématique | ~2-3s | À chaque cycle |

**Recommandation :** Utilisez le **Mode 1** (avec détection) pour de meilleures performances.

---

## 🐛 Dépannage

### ❌ Le bouton "Use" n'est pas détecté

**Causes possibles :**
- Capture trop grande ou trop petite
- Le menu n'a pas eu le temps de s'ouvrir
- Plusieurs boutons "Use" et il clique sur le mauvais

**Solutions :**
1. Recalibrez avec une capture plus précise
2. Augmentez le délai après ouverture du menu (`time.sleep(0.8)` → `1.2`)
3. Capturez le bouton de la **première** canne dans la liste

### ❌ Le menu ne se ferme pas

**Solution :**
Vérifiez que la touche **`,`** ouvre/ferme bien le menu dans votre jeu.
Si c'est une autre touche, modifiez :

```python
# Ligne ~233 et ~248
pyautogui.press(',')  # Changez ',' par votre touche
```

### ❌ Le bot clique sur le mauvais "Use"

Si plusieurs cannes ont un bouton "Use" :
- Capturez le bouton **spécifiquement** de la canne que vous voulez
- Ou capturez une zone plus large incluant le nom de la canne

### ❌ La détection de canne cassée ne fonctionne pas

**Solutions :**
1. Recalibrez l'indicateur de canne cassée
2. Ou désactivez la détection et passez en mode "vérification systématique"
3. Supprimez `rod_broken.png` pour forcer la vérification systématique

---

## 💡 Conseils

### **Pour une Détection Optimale**

1. **Capturez le bouton "Use" quand le menu est complètement ouvert**
2. **Capturez juste le texte "Use"**, pas la bordure du bouton
3. **Taille recommandée** : 40-80 pixels de large
4. **Évitez** de capturer des éléments qui changent (sélection, hover, etc.)

### **Ordre des Cannes**

Si vous avez plusieurs cannes dans le menu :
- Le bot cliquera sur le **premier** bouton "Use" trouvé
- Organisez vos cannes pour que la meilleure soit **en haut** de la liste
- Ou gardez plusieurs cannes identiques

### **Cannes Infinies**

Si vos cannes ne cassent **jamais** :
- Vous pouvez **ne pas capturer** ces images
- Le bot ouvrira/fermera le menu rapidement sans impact

---

## 🎯 Résumé

### **Configuration Minimale (Recommandée)**

Capturez **uniquement** :
1. ✅ Point d'exclamation
2. ✅ Bouton Continue
3. ✅ Indicateur canne prête
4. ✅ **Bouton "Use"** ← NOUVEAU !

### **Configuration Optimale**

Capturez **tout** :
1. ✅ Point d'exclamation
2. ✅ Bouton Continue
3. ✅ Indicateur canne prête
4. ✅ **Bouton "Use"** ← NOUVEAU !
5. ✅ **Indicateur canne cassée** ← NOUVEAU ! (optionnel)

---

**Avec cette fonctionnalité, le bot est maintenant 100% autonome ! 🎣🤖**


# ⚡ Guide d'Optimisations du Bot

## 🎯 Optimisations Implémentées

Le bot a été optimisé pour être **plus rapide** et **plus intelligent** !

---

## ✨ Optimisation #1 : Détection Intelligente du QTE

### **Avant** (lent) :
```
Clic sur ! → Attendre 8 secondes → Chercher Continue
```
- ❌ On attendait toujours 8 secondes même sans QTE
- ❌ Perte de temps sur les succès directs

### **Maintenant** (rapide) :
```
Clic sur ! → Chercher Continue immédiatement
    ↓
    Si trouvé → Clic direct ! (gain de 7-8 secondes) ✅
    Si pas trouvé → QTE détecté → Attente auto → Chercher Continue
```

**Gain de temps** : **7-8 secondes** par poisson pêché directement (sans QTE)

---

## ⚡ Optimisation #2 : Détection de Canne Prête (Optionnel)

### Principe :
Au lieu d'attendre un délai fixe après "Continue", le bot détecte quand la canne est **vraiment prête**.

### Comment l'activer :

**Étape 1** : Capturez l'indicateur "prêt"
```bash
python calibration.py
```

Quand demandé "Voulez-vous capturer l'indicateur 'canne prête'?" → Répondez **OUI**

**Capturez** un élément qui indique que vous pouvez pêcher à nouveau :
- 🎣 Icône de canne active
- ✅ Texte "Ready" / "Prêt"
- 🔵 Barre de cooldown pleine
- 🟢 Indicateur visuel quelconque

**Étape 2** : Le bot utilisera automatiquement cette détection

### Gains :
- ✅ Plus besoin d'attendre un temps fixe
- ✅ Le bot relance dès que possible
- ✅ S'adapte automatiquement aux variations

---

## 📊 Comparaison Performances

### **Sans optimisations** (version originale) :
```
Cycle complet : ~15-20 secondes
- Clic démarrage : 1s
- Attente ! : variable
- Clic sur ! : 1s
- Attente QTE fixe : 8s ❌
- Chercher Continue : 2-5s
- Clic Continue : 1s
- Attente fixe : 1s ❌
Total : ~15-20 secondes
```

### **Avec optimisations** (version actuelle) :
```
Cycle sans QTE : ~8-10 secondes ✅
- Clic démarrage : 1s
- Attente ! : variable
- Clic sur ! : 1s
- Check Continue immédiat : 1-2s ✅
- Clic Continue : 1s
- Détection prête : 1-2s ✅
Total : ~8-10 secondes

Cycle avec QTE : ~15-18 secondes
- Clic démarrage : 1s
- Attente ! : variable
- Clic sur ! : 1s
- Check Continue : 1s (pas trouvé)
- Attente QTE : 8s
- Chercher Continue : 2-3s
- Clic Continue : 1s
- Détection prête : 1-2s
Total : ~15-18 secondes
```

**Amélioration** : **~40-50% plus rapide** sur les succès directs !

---

## 🎮 Logique du Bot Optimisé

```
┌─────────────────────────────────────┐
│  1. Clic pour démarrer la pêche     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  2. Détection point d'exclamation   │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  3. Clic sur !                      │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  4. Check Continue (timeout 2s)     │ ← NOUVEAU !
└──────────────┬──────────────────────┘
               ↓
        ┌──────┴──────┐
        │             │
    Trouvé ?      Pas trouvé ?
        │             │
        ↓             ↓
  ┌─────────┐   ┌──────────────┐
  │ Succès  │   │ QTE détecté  │
  │ direct! │   │ Attente 8s   │
  └────┬────┘   └──────┬───────┘
       │               │
       │               ↓
       │      ┌──────────────────┐
       │      │ Chercher Continue│
       │      └──────┬───────────┘
       │             │
       └─────────────┘
               ↓
    ┌──────────────────────┐
    │  Clic sur Continue   │
    └──────────┬───────────┘
               ↓
    ┌──────────────────────┐
    │ Attente canne prête  │ ← NOUVEAU !
    │ (si image disponible)│
    └──────────┬───────────┘
               ↓
         Recommencer
```

---

## 🛠️ Configuration Avancée

### Ajuster les Timeouts

Modifiez `fishing_bot_low_level.py` :

```python
# Dans __init__ (ligne ~70-80)
self.wait_after_click = 0.5          # Délai après clic
self.exclamation_timeout = 30        # Temps max pour détecter !
self.continue_button_timeout = 10    # Temps max pour Continue après QTE
self.qte_wait_time = 8               # Durée d'attente pendant QTE
```

**Recommandations** :
- Si votre QTE dure plus longtemps : augmentez `qte_wait_time` à 10-12
- Si le ! apparaît très lentement : augmentez `exclamation_timeout` à 45-60
- Pour accélérer encore : réduisez `wait_after_click` à 0.3

---

## 💡 Conseils pour Maximiser la Vitesse

### 1. **Capturez l'indicateur "prêt"**
C'est l'optimisation la plus importante ! Gain de 1-2 secondes par cycle.

### 2. **Captures précises**
Plus vos captures sont petites et précises, plus la détection est rapide.

**Tailles optimales** :
- Point d'exclamation : 30-60 pixels
- Bouton Continue : 80-150 pixels
- Indicateur prêt : 40-80 pixels

### 3. **Réduisez la zone de recherche**

Si le ! apparaît toujours au même endroit, limitez la zone :

```python
# Dans fishing_cycle(), ligne ~255
# Au lieu de chercher sur tout l'écran
exclamation_pos = self.find_on_screen("exclamation", timeout=30)

# Chercher dans une région spécifique (plus rapide)
region = (800, 400, 400, 300)  # x, y, largeur, hauteur
exclamation_pos = self.find_on_screen("exclamation", region=region, timeout=30)
```

### 4. **Baissez la confiance si détection fiable**

Si vos captures sont très bonnes et que vous n'avez jamais de fausses détections :

```python
# Au lancement, choisissez mode 3 (70%)
# Ou modifiez directement :
bot = FishingBotLowLevel(confidence=0.65)
```

**Note** : Trop bas = risque de fausses détections !

---

## 📈 Statistiques Attendues

### **Avant optimisations** :
- ~15-20 secondes par cycle
- ~180-240 poissons/heure
- Beaucoup de temps d'attente inutile

### **Après optimisations** :
- ~8-18 secondes par cycle (selon QTE)
- **~250-350 poissons/heure** ✅
- Temps d'attente minimisé

**Amélioration globale** : **+30-50% de poissons/heure !**

---

## 🔧 Dépannage

### Le bot va trop vite et rate des choses

**Solution** : Augmentez les délais
```python
self.wait_after_click = 0.8  # Au lieu de 0.5
time.sleep(1.5)  # Au lieu de time.sleep(1) après clic sur !
```

### Le bot n'attend pas assez le QTE

**Solution** : Augmentez le temps d'attente QTE
```python
self.qte_wait_time = 10  # Au lieu de 8
```

### L'indicateur "prêt" n'est pas détecté

**Solution** :
1. Recapturez avec une zone plus petite
2. Vérifiez que l'indicateur est bien visible
3. Baissez la confiance pour cet élément spécifiquement

---

## 🎯 Résumé des Optimisations

| Optimisation | Gain | Difficulté | Recommandé |
|--------------|------|------------|------------|
| Check Continue immédiat | **7-8s** par succès direct | Automatique | ✅ Activé |
| Détection canne prête | 1-2s par cycle | Calibration | ⭐ Recommandé |
| Réduction zone recherche | 0.2-0.5s par détection | Code | Optionnel |
| Confiance optimisée | 0.1-0.3s par détection | Configuration | Optionnel |

---

## 🚀 Pour Aller Plus Loin

### Optimisation Ultime : Prédiction

Si votre jeu a des patterns prévisibles :

```python
# Enregistrer les durées
import time
durations = []

# Dans fishing_cycle
start = time.time()
# ... cycle ...
duration = time.time() - start
durations.append(duration)

# Calculer la moyenne
avg_duration = sum(durations) / len(durations)

# Adapter les timeouts dynamiquement
self.exclamation_timeout = avg_duration * 1.2
```

---

**Avec ces optimisations, votre bot est maintenant au maximum de son efficacité ! 🎣⚡**


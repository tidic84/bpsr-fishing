# 🎣 Bot d'Automatisation de Pêche

Bot Python pour automatiser la pêche dans les jeux avec détection d'images.

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

### 1. Calibration (première fois)

```bash
python calibration.py
```

Capturez :
- Le point d'exclamation (!)
- Le bouton "Continue"
- L'indicateur "canne prête" (optionnel mais recommandé)
- Le bouton "Use" dans le menu de cannes (optionnel)

### 2. Lancement

```bash
python fishing_bot_low_level.py
```

Le bot va :
1. Vérifier et équiper une canne si nécessaire
2. Cliquer pour démarrer la pêche
3. Détecter le point d'exclamation
4. Cliquer dessus
5. Gérer automatiquement les QTE (attente passive)
6. Cliquer sur "Continue" si succès
7. Recommencer

## Arrêt

Appuyez sur **ESC** à tout moment pour arrêter le bot.

## Configuration

Le jeu doit être en mode **fenêtré** ou **fenêtré sans bordure** (pas plein écran).

## Fonctionnalités

- ✅ Clics bas niveau (SendInput) compatibles avec la plupart des jeux
- ✅ Détection automatique du succès/échec
- ✅ Gestion intelligente des QTE
- ✅ Remplacement automatique des cannes cassées
- ✅ Statistiques en temps réel
- ✅ 100% autonome


# 👋 Finger Counter — Compteur de doigts en temps réel

Un projet de **Computer Vision** qui utilise ta webcam pour détecter ta main et compter le nombre de doigts levés en temps réel.

> Projet idéal pour débuter avec OpenCV, MediaPipe et la vision par ordinateur en Python.

---

## 📸 Aperçu

```
Webcam → Détection de main (IA) → Comptage des doigts → Affichage à l'écran
```

Le programme affiche en temps réel le nombre de doigts levés (0 à 5) directement sur le flux vidéo de ta webcam.

---

## 🛠️ Technologies utilisées

| Bibliothèque | Rôle |
|---|---|
| `opencv-python` | Lecture webcam, affichage vidéo, dessin sur image |
| `mediapipe` | Modèle IA pour détecter les 21 points de la main |
| `cvzone` | Surcouche simplifiée au-dessus de MediaPipe |

---

## 📁 Structure du projet

```
finger-counter/
│
├── HandTrackingModule.py    # Module réutilisable (classe HandDetector)
├── finger_counter.py        # Application principale
├── requirements.txt         # Dépendances Python
└── README.md                # Ce fichier
```

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/ton-username/finger-counter.git
cd finger-counter
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv

# Sur Windows
venv\Scripts\activate

# Sur Mac/Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## ▶️ Lancer le projet

```bash
python finger_counter.py
```

- Une fenêtre s'ouvre avec le flux de ta webcam
- Lève les doigts devant la caméra
- Le nombre s'affiche en grand sur l'écran
- Appuie sur **Échap** pour quitter

---

## 📦 requirements.txt

```
opencv-python
mediapipe
cvzone
```

---

## 🧠 Comment ça marche ?

MediaPipe détecte **21 points précis** (landmarks) sur chaque main. Pour chaque doigt, le programme compare la position verticale (Y) du bout du doigt avec celle de l'articulation du milieu :

- Si le bout est **plus haut** que l'articulation → doigt **levé** ✅
- Sinon → doigt **baissé** ❌

```
Point 8 (bout index) Y < Point 6 (articulation) Y → doigt levé
```

---

## 📖 Apprendre

Consulte le fichier [`COURS.md`](./COURS.md) pour un cours complet sur toutes les bibliothèques et fonctions utilisées dans ce projet.

---

## 💡 Idées d'extension

- 🎵 **Contrôle du volume** — distance entre pouce et index
- ✂️ **Pierre-feuille-ciseaux** — reconnaître les gestes
- 🖐️ **Souris gestuelle** — déplacer le curseur avec la main
- 🔢 **Calculatrice gestuelle** — chaque combinaison = un chiffre

---

## 👤 Auteur

Projet réalisé dans le cadre d'un apprentissage personnel de la Computer Vision avec Python.

---

## 📄 Licence

Ce projet est open source sous licence MIT.

# 📚 COURS — Comprendre les bibliothèques et fonctions du projet

Ce fichier est un cours complet pour débutants. Il explique chaque bibliothèque et chaque fonction utilisée dans le projet Finger Counter.

---

## Table des matières

1. [OpenCV (`cv2`)](#1-opencv-cv2)
2. [MediaPipe](#2-mediapipe)
3. [cvzone & HandDetector](#3-cvzone--handdetector)
4. [Concepts Python utilisés](#4-concepts-python-utilisés)
5. [Comprendre les coordonnées d'image](#5-comprendre-les-coordonnées-dimage)
6. [Glossaire](#6-glossaire)

---

## 1. OpenCV (`cv2`)

**OpenCV** (Open Source Computer Vision Library) est la bibliothèque la plus utilisée au monde pour tout ce qui touche aux images et à la vidéo en Python.

### Installation

```bash
pip install opencv-python
```

### Import

```python
import cv2
```

---

### `cv2.VideoCapture(index)`

Ouvre une source vidéo (webcam ou fichier).

```python
cap = cv2.VideoCapture(0)   # 0 = première webcam
cap = cv2.VideoCapture(1)   # 1 = deuxième webcam
cap = cv2.VideoCapture("video.mp4")  # depuis un fichier
```

**Ce que ça retourne** : un objet `cap` qui représente la connexion à la caméra.

---

### `cap.read()`

Lit une image (appelée **frame**) depuis la webcam.

```python
success, img = cap.read()
```

**Paramètres** : aucun.

**Retourne** :
- `success` → `True` si la lecture a réussi, `False` sinon
- `img` → l'image sous forme de tableau numpy (hauteur × largeur × 3 canaux de couleur)

> 💡 Une image couleur en OpenCV est un tableau 3D : chaque pixel a 3 valeurs (Bleu, Vert, Rouge) — attention, l'ordre est **BGR** et non RGB !

---

### `cv2.imshow(nom_fenetre, img)`

Affiche une image dans une fenêtre à l'écran.

```python
cv2.imshow("Image", img)
```

**Paramètres** :
- `nom_fenetre` → le titre de la fenêtre (texte libre)
- `img` → l'image à afficher (tableau numpy)

---

### `cv2.waitKey(delai_ms)`

Met le programme en pause et attend qu'une touche soit pressée.

```python
cv2.waitKey(1)   # attend 1 milliseconde
cv2.waitKey(0)   # attend indéfiniment jusqu'à une touche
```

**Paramètres** :
- `delai_ms` → durée d'attente en millisecondes

**Retourne** : le code ASCII de la touche pressée (ou -1 si aucune touche).

**Utilisation typique pour quitter avec Échap :**

```python
if cv2.waitKey(1) & 0xFF == 27:  # 27 = code ASCII de la touche Échap
    break
```

> 💡 Le `& 0xFF` est un masque binaire pour compatibilité sur certains systèmes. C'est une convention à mémoriser.

---

### `cv2.putText(img, texte, position, police, taille, couleur, epaisseur)`

Écrit du texte sur une image.

```python
cv2.putText(img, str(count), (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5)
```

**Paramètres dans l'ordre** :
| Paramètre | Type | Description | Exemple |
|---|---|---|---|
| `img` | array | l'image sur laquelle écrire | `img` |
| `texte` | str | le texte à afficher | `"3"` |
| `position` | tuple (x, y) | coin inférieur gauche du texte | `(50, 100)` |
| `police` | constante | style de la police | `cv2.FONT_HERSHEY_SIMPLEX` |
| `taille` | float | échelle du texte | `3` (très grand) |
| `couleur` | tuple (B, G, R) | couleur en BGR | `(255, 0, 0)` = bleu |
| `épaisseur` | int | épaisseur du trait en pixels | `5` |

> ⚠️ Attention : OpenCV utilise **BGR** (Bleu-Vert-Rouge) et non RGB. Donc `(255, 0, 0)` = bleu, `(0, 0, 255)` = rouge !

**Polices disponibles** :
```python
cv2.FONT_HERSHEY_SIMPLEX        # police classique sans-serif
cv2.FONT_HERSHEY_PLAIN          # plus fine
cv2.FONT_HERSHEY_DUPLEX         # plus épaisse
cv2.FONT_HERSHEY_COMPLEX        # avec empattements
```

---

### `cv2.rectangle(img, pt1, pt2, couleur, epaisseur)`

Dessine un rectangle sur une image.

```python
cv2.rectangle(img, (100, 50), (300, 200), (255, 0, 255), 2)
```

**Paramètres** :
- `pt1` → coin supérieur gauche `(x, y)`
- `pt2` → coin inférieur droit `(x, y)`
- `couleur` → en BGR
- `épaisseur` → en pixels (`-1` pour remplir)

---

### `cv2.cvtColor(img, code_conversion)`

Convertit une image d'un espace colorimétrique à un autre.

```python
imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # BGR → RGB
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # BGR → niveaux de gris
```

> 💡 Utilisé dans le module car MediaPipe attend des images **RGB** alors qu'OpenCV produit du **BGR**.

---

## 2. MediaPipe

**MediaPipe** est une bibliothèque Google qui contient des modèles d'intelligence artificielle pré-entraînés pour analyser des images. Pas besoin d'entraîner un modèle soi-même !

### Installation

```bash
pip install mediapipe
```

### Import

```python
import mediapipe as mp
```

---

### Le modèle Hands

MediaPipe Hands détecte jusqu'à 2 mains dans une image et retourne **21 points 3D** (landmarks) pour chaque main.

```python
mpHands = mp.solutions.hands

hands = mpHands.Hands(
    static_image_mode=False,     # False = vidéo, True = images fixes
    max_num_hands=2,             # nombre max de mains à détecter
    model_complexity=1,          # 0 = rapide, 1 = précis
    min_detection_confidence=0.5, # seuil de confiance (0.0 à 1.0)
    min_tracking_confidence=0.5   # seuil de suivi entre frames
)
```

---

### Les 21 landmarks

Chaque main a 21 points numérotés :

```
0  = poignet
1  = base pouce
2  = phalange 1 pouce
3  = phalange 2 pouce
4  = bout pouce (TIP)

5  = base index
6  = phalange 1 index
7  = phalange 2 index
8  = bout index (TIP)

9  = base majeur
10 = phalange 1 majeur
11 = phalange 2 majeur
12 = bout majeur (TIP)

13 = base annulaire
14 = phalange 1 annulaire
15 = phalange 2 annulaire
16 = bout annulaire (TIP)

17 = base auriculaire
18 = phalange 1 auriculaire
19 = phalange 2 auriculaire
20 = bout auriculaire (TIP)
```

> 💡 Les "tips" (bouts des doigts) sont aux indices **4, 8, 12, 16, 20**.

---

### `hands.process(imgRGB)`

Analyse une image et retourne les landmarks détectés.

```python
results = hands.process(imgRGB)
```

**Retourne** un objet `results` avec :
- `results.multi_hand_landmarks` → liste des landmarks pour chaque main (ou `None` si aucune)
- `results.multi_handedness` → indique si c'est une main gauche ou droite

**Accéder aux coordonnées d'un landmark :**

```python
for handLms in results.multi_hand_landmarks:
    for id, lm in enumerate(handLms.landmark):
        # lm.x et lm.y sont entre 0.0 et 1.0 (proportionnel à la taille de l'image)
        px = int(lm.x * largeur_image)
        py = int(lm.y * hauteur_image)
        print(f"Point {id} : x={px}, y={py}")
```

---

### `mp.solutions.drawing_utils.draw_landmarks()`

Dessine automatiquement les 21 points et les connexions sur l'image.

```python
mpDraw = mp.solutions.drawing_utils
mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
```

---

## 3. cvzone & HandDetector

**cvzone** est une bibliothèque qui simplifie l'utilisation de MediaPipe. Elle encapsule toute la complexité dans des classes faciles à utiliser.

### Installation

```bash
pip install cvzone
```

### Import

```python
from cvzone.HandTrackingModule import HandDetector
```

---

### `HandDetector(detectionCon, maxHands)`

Crée un détecteur de mains.

```python
detector = HandDetector(detectionCon=0.8, maxHands=1)
```

**Paramètres principaux** :
| Paramètre | Type | Défaut | Description |
|---|---|---|---|
| `staticMode` | bool | `False` | `True` = images fixes (plus lent), `False` = vidéo |
| `maxHands` | int | `2` | Nombre maximum de mains à détecter |
| `modelComplexity` | int | `1` | `0` = rapide, `1` = précis |
| `detectionCon` | float | `0.5` | Confiance minimale pour détecter (0.0 à 1.0) |
| `minTrackCon` | float | `0.5` | Confiance minimale pour suivre entre frames |

---

### `detector.findHands(img, draw=True, flipType=True)`

Analyse l'image et retourne les informations sur les mains détectées.

```python
hands, img = detector.findHands(img)
```

**Paramètres** :
- `img` → l'image de la webcam
- `draw` → `True` pour dessiner les landmarks sur l'image
- `flipType` → `True` pour corriger l'inversion gauche/droite (miroir)

**Retourne** :
- `hands` → liste de dictionnaires, un par main détectée
- `img` → l'image avec les dessins si `draw=True`

**Structure d'un dictionnaire `hand` :**

```python
hand = {
    "lmList": [
        [x0, y0, z0],   # point 0 (poignet)
        [x1, y1, z1],   # point 1
        # ... jusqu'au point 20
        [x20, y20, z20] # bout auriculaire
    ],
    "bbox": (x, y, largeur, hauteur),  # boîte englobante
    "center": (cx, cy),                # centre de la main
    "type": "Left"  # ou "Right"
}
```

**Exemple d'utilisation :**

```python
if hands:
    hand = hands[0]               # première main
    lmList = hand["lmList"]       # liste des 21 points
    bbox = hand["bbox"]           # boîte englobante
    center = hand["center"]       # centre
    handType = hand["type"]       # "Left" ou "Right"

    # Accéder au bout de l'index (point 8)
    x_index, y_index = lmList[8][0], lmList[8][1]
```

---

### `detector.fingersUp(hand)`

Détermine quels doigts sont levés.

```python
fingers = detector.fingersUp(hand)
```

**Retourne** : une liste de 5 valeurs `[pouce, index, majeur, annulaire, auriculaire]`

```python
fingers = [1, 1, 0, 0, 1]
# signifie : pouce levé, index levé, majeur baissé, annulaire baissé, auriculaire levé

count = fingers.count(1)  # = 3 doigts levés
```

**Comment ça marche en interne :**

```python
# Pour les 4 doigts (pas le pouce) :
# si bout_y < articulation_y → doigt levé (Y augmente vers le bas en image)
if lmList[tipId][1] < lmList[tipId - 2][1]:
    fingers.append(1)  # levé
else:
    fingers.append(0)  # baissé

# Pour le pouce (utilise X car il se plie horizontalement) :
if lmList[4][0] > lmList[3][0]:   # main droite
    fingers.append(1)
```

---

### `detector.findDistance(p1, p2, img)`

Calcule la distance entre deux points landmarks.

```python
length, info, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)
```

**Paramètres** :
- `p1` → premier point `(x1, y1)`
- `p2` → deuxième point `(x2, y2)`
- `img` → image sur laquelle dessiner (optionnel)

**Retourne** :
- `length` → distance en pixels (float)
- `info` → tuple `(x1, y1, x2, y2, cx, cy)` avec le centre
- `img` → image avec la distance dessinée

**Utilisation typique — contrôle du volume :**

```python
# Distance entre pouce (4) et index (8)
length, info, img = detector.findDistance(lmList[4][0:2], lmList[8][0:2], img)

# Convertir la distance (ex: 20 à 200 pixels) en volume (0 à 100%)
volume = int(np.interp(length, [20, 200], [0, 100]))
```

---

## 4. Concepts Python utilisés

### Les listes et `.count()`

```python
fingers = [1, 0, 1, 1, 0]

# Compter les 1 dans la liste
nombre_de_1 = fingers.count(1)  # = 3

# Accéder à un élément par son index
premier = fingers[0]   # = 1
dernier = fingers[-1]  # = 0 (index négatif = depuis la fin)
```

---

### Les f-strings (formatage de texte)

```python
count = 3
handType = "Left"

# Ancienne façon
print("H1 = " + str(count))

# Avec f-string (recommandé, Python 3.6+)
print(f"H1 = {count}")
print(f"Main {handType} : {count} doigt(s) levé(s)")
```

---

### Le slicing `[0:2]`

```python
point = [150, 230, 45]  # [x, y, z]

# Prendre seulement x et y (indices 0 et 1)
xy = point[0:2]  # = [150, 230]
# Équivalent à : point[:2]
```

---

### La boucle `while True`

```python
while True:
    # Ce code s'exécute indéfiniment
    success, img = cap.read()
    
    # ...
    
    if cv2.waitKey(1) & 0xFF == 27:
        break  # sort de la boucle si Échap pressé
```

---

### `enumerate()` dans une boucle

```python
lmList = [[100,200], [110,180], [120,150]]  # exemple simplifié

for id, point in enumerate(lmList):
    print(f"Point {id} : x={point[0]}, y={point[1]}")

# Affiche :
# Point 0 : x=100, y=200
# Point 1 : x=110, y=180
# Point 2 : x=120, y=150
```

---

### `zip()` pour parcourir deux listes en parallèle

```python
types = ["Right", "Left"]
landmarks = [lms1, lms2]

for handType, handLms in zip(types, landmarks):
    print(handType)   # "Right", puis "Left"
    print(handLms)    # lms1, puis lms2
```

---

## 5. Comprendre les coordonnées d'image

C'est un point clé pour comprendre la logique de détection des doigts.

```
(0,0) ──────────────────── X croît →
  │
  │     ┌──────────────┐
  │     │   IMAGE      │
  │     │              │
  │     │  (100, 150)  │
  │     │      ●       │
  │     └──────────────┘
  │
  Y croît ↓
```

**L'origine `(0,0)` est en haut à gauche.** Y augmente vers le bas.

C'est pourquoi : si le bout du doigt (Y petit) est **au-dessus** de l'articulation (Y grand), le doigt est **levé**.

```python
# Doigt levé si :
lmList[8][1] < lmList[6][1]   # Y_bout < Y_articulation
# = "le bout est plus haut dans l'image que l'articulation"
```

---

## 6. Glossaire

| Terme | Définition |
|---|---|
| **Frame** | Une seule image dans un flux vidéo (comme une photo de film) |
| **Landmark** | Point de repère précis sur un objet (ici, les 21 points de la main) |
| **BGR** | Format couleur d'OpenCV : Bleu, Vert, Rouge (inverse de RGB) |
| **Bounding Box** | Rectangle englobant un objet détecté dans l'image |
| **Confiance (confidence)** | Score entre 0 et 1 indiquant la certitude du modèle IA |
| **Array numpy** | Tableau de nombres multidimensionnel — format standard pour les images en Python |
| **Tip** | Bout d'un doigt (landmarks 4, 8, 12, 16, 20) |
| **Computer Vision** | Domaine de l'IA qui permet aux ordinateurs d'analyser des images |
| **FPS** | Frames Per Second — nombre d'images analysées par seconde |
| **Modèle pré-entraîné** | Modèle IA déjà entraîné sur des millions d'images, prêt à l'emploi |

---

## 🚀 Pour aller plus loin

- **Documentation OpenCV** : https://docs.opencv.org
- **Documentation MediaPipe** : https://mediapipe.readthedocs.io
- **Documentation cvzone** : https://github.com/cvzone/cvzone
- **Tutoriels Computer Vision** : recherche "OpenCV Python tutorial" sur YouTube

---

*Cours rédigé pour accompagner le projet Finger Counter — niveau débutant.*

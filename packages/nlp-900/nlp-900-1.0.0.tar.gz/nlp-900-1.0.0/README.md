# NLP T9
## Pre-requis
* python 3.7

# Installation
To install nlp-900, simply use pip:
```shell
pip install nlp-900
```

To install nlp-900, on git:
```shell
git clone https://gitlab.com/red-56/t9-nlp.git
cd ./t9-nlp
python setup.py install
nlp-900 --help
```

# Help Cli
## Option

| Option                      | Type      | Example  | help|
| --------------------------- |:---------:|:--------:| ---:|
| -o, --output              | raw,stdout,voice      | raw |  Type d'ouput voulu, raw pour un fichier audio, voice pour un message automatique, et stdout pour des print.(Default = stdout)|
| -i, --input            | raw,stdin,voice |   raw | Type d'input voulu, raw pour des fichiers audio,voice pour le micro, et stdin pour une phrase prise en argument.(Default = stdin)|
| -f, --file           | PATH |   ./sample/paris_nevers.wav |  Chemin du fichier audio|
| -e, --escale            | INTEGER > 0 |   3 |  Nombre d'escales maximum à ne pas dépasser.(Default = 2)|
| -vv, --verbose            | FLAG |    |  Affiche les messages de debug.|
| --version            | FLAG |   |  Show the version and exit. |
| --help            | FLAG |   |  Show the help message and exit. |

# Examples
## Tables of contents
- [Basic Usage](#basic-example)
- [Phrase de la forme Gare d'arrivée Gare de départ](#phrase-de-la-forme-gare-darrive-gare-de-dpart)
- [Phrase longue](#phrase-longue)
- [Demande d'escale](#demande-descale)
- [Trajet avec trop d'escales](#trajet-avec-trop-descales)
- [Trajet introuvable](#trajet-introuvable)
- [Gare Introuvale](#gare-introuvable)
- [Prendre en input un fichier audio](#prendre-en-input-un-fichier-audio)
- [Prendre en input son micro](#prendre-en-input-son-micro)
- [Récuperer l'output dans un fichier audio](#rcuprer-louput-dans-un-fichier-audio)
- [Récuperer l'output sur la sortie audio standard](#rcuprer-output-sur-la-sortie-audio-standard)
- [Augmenter le nombre maximum d'escale](#augmenter-le-nombre-descales-maximum)
- [Afficher le mode debug](#afficher-le-mode-debug)
## Basic example
```shell
nlp-900 "un billet pour paris-nevers s'il vous plait"
```
output:
```shell
Le temps de trajet pour votre voyage pour Nevers en partant de Paris-austerlitz sera de 230 minutes.Vous devrez passer par Bourges.
```
## Phrase de la forme Gare d'arrivée Gare de départ
```shell
nlp-900 "je veux aller à Paris, je suis à Rouen"
```
output:
```shell
Le temps de trajet pour votre voyage pour Paris-st-lazare en partant de Rouen-rive-droite sera de 533 minutes.Vous devrez passer par Romans-bourg-de-péage, Caen.
```
## Phrase longue
```shell
nlp-900 "j'aime les pommes, j'ai fêté noël hier je veux rentrer à Paris, ma maman m'a fait des sandwitchs et je suis actuellement à Rouen."
```
output:
```shell
Le temps de trajet pour votre voyage pour Paris-st-lazare en partant de Rouen-rive-droite sera de 533 minutes.Vous devrez passer par Romans-bourg-de-péage, Caen.
```
## Demande d'escale
```shell
nlp-900 "un billet pour paris-caen en passant par rouen s'il vous plait"
```
output:
```shell
Le temps de trajet pour votre voyage pour Caen en partant de Paris-st-lazare sera de 481 minutes.Vous devrez passer par Rouen-rive-droite, Romans-bourg-de-péage.
```
## Trajet avec trop d'escales
```shell
nlp-900 "je voudrais aller à nevers, je suis à paris, et je dois passer par Rouen pour voir ma tante."
```
output: 
```shell
Trajet trouvé mais il comporte 7 escales, pour l'afficher ajouter l'option --escale 7.
```
## Trajet introuvable
```shell
nlp-900 "je souhaite me rendre à Bourges, en partance de Argentan"
```
output:
```shell
Trajet introuvable
```
## Gare introuvable
```shell
nlp-900 "je pars de epitech je veux rentrer chez moi."
```
output:
```shell
Gare Introuvable!!!
Format: je veux aller de (Gare Départ) à (Gare d'arrivée).
ex: je veux aller de bourges à nevers
```
## Prendre en input un fichier audio
```shell
nlp-900 --input raw -f ./sample/lille_nevers.wav
```
## Prendre en input son micro
```shell
nlp-900 --input voice
```
## Récupérer l'ouput dans un fichier audio
```shell
nlp-900 --output raw
```
Le fichier sera nommé output.wav
## Récupérer output sur la sortie audio standard
```shell
nlp-900 --output voice
```
## Augmenter le nombre d'escales maximum
```shell
nlp-900 --escale 7 "je voudrais aller à nevers, je suis à paris, et je dois passer par Rouen pour voir ma tante."
```
## Afficher le mode debug
```shell
nlp-900 -vv
```

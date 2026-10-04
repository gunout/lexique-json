# 📖 Dictionnaire Français JSON
> Générer un dictionnaire complet de la langue française au format JSON, avec encodage numérique alphabétique (A=1, B=2, …).
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Source: Lexique383](https://img.shields.io/badge/Source-Lexique383-blue)](http://www.lexique.org/)
[![JSON](https://img.shields.io/badge/Format-JSON-000000?logo=json&logoColor=white)](https://www.json.org/)
## 📑 Sommaire
- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Encodage](#-encodage-alphabétique)
- [Structure JSON](#-structure-du-json)
- [Dépannage](#-dépannage)
- [Licence](#-licence)
## 🎯 Présentation
Ce script Python télécharge la base lexicale **Lexique383** (~140 000 mots français), la convertit en **dictionnaire JSON structuré**, et associe à chaque mot un **code numérique alphabétique** (A=1, B=2, …, Z=26).
    json    → 10.19.15.14
    bonjour → 2.15.14.10.15.21.18
    france  → 6.18.1.14.3.5
Idéal pour le NLP, les jeux de mots, l'indexation et l'apprentissage de JSON en Python.
## ✨ Fonctionnalités
- ✅ Téléchargement automatique de Lexique383
- ✅ Normalisation Unicode des accents (`é → e`, `ç → c`)
- ✅ Encodage numérique A=1 … Z=26
- ✅ Déduplication automatique des mots
- ✅ Métadonnées : fréquence, catégorie, phonétique
- ✅ Export JSON compact
- ✅ Zéro dépendance externe (bibliothèque standard)
## 📦 Prérequis
- Python 3.8+
- Connexion Internet (premier téléchargement uniquement)
- ~100 Mo d'espace disque
## 🚀 Installation
    git clone https://github.com/votre-utilisateur/dictionnaire-fr-json.git
    cd dictionnaire-fr-json
    python3 dictionnaire.py
⚠️ **Ne nommez jamais votre script `json.py`** — cela masque le module standard `json` et provoque `AttributeError: module 'json' has no attribute 'dump'`.
## 🎮 Utilisation
    python3 dictionnaire.py
Le script va :
1. Télécharger `Lexique383.tsv` (~25 Mo)
2. Construire le dictionnaire en mémoire
3. Écrire `dictionnaire_fr.json` (~45 Mo)
4. Afficher les statistiques et exemples
### Sortie console
    ✅ Lexique383.tsv téléchargé (24.7 Mo)
    📊 Statistiques :
       - Mots uniques : 125653
       - Doublons ignorés : 17041
       - Mots sans code : 0
    💾 Écriture de dictionnaire_fr.json...
    ✅ dictionnaire_fr.json créé (45.2 Mo)
## 🔢 Encodage alphabétique
| a | b | c | d | e | f | g | h | i | j | k | l | m |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
| n | o | p | q | r | s | t | u | v | w | x | y | z |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
**Règles** : accents normalisés, casse ignorée, caractères non alphabétiques supprimés, séparateur `.`.
## 🗂 Structure du JSON
| Champ | Type | Description |
|---|---|---|
| `meta` | objet | Métadonnées (source, version, total) |
| `meta.source` | string | Source (`Lexique383`) |
| `meta.total_mots` | int | Nombre total de mots |
| `alphabet` | objet | Table `lettre → valeur` (a=1 … z=26) |
| `mots` | objet | Dictionnaire `mot → propriétés` |
| `mots[mot].code` | string | Code numérique (`"10.19.15.14"`) |
| `mots[mot].frequence` | float | Fréquence d'usage |
| `mots[mot].categorie` | string | Catégorie grammaticale |
| `mots[mot].phonetique` | string | Transcription API |
## 🐍 Utilisation en Python
    import json
    with open("dictionnaire_fr.json", encoding="utf-8") as f:
        data = json.load(f)
    print(data["meta"]["total_mots"])   # 125653
    print(data["mots"]["json"])         # {'code': '10.19.15.14', ...}
### Encoder un mot
    import unicodedata
    alphabet = data["alphabet"]
    def encoder(mot):
        mot = "".join(c for c in unicodedata.normalize("NFD", mot.lower())
                      if unicodedata.category(c) != "Mn")
        return ".".join(str(alphabet[c]) for c in mot if c in alphabet)
    print(encoder("bonjour"))   # 2.15.14.10.15.21.18
### Décoder un code
    inverse = {v: k for k, v in data["alphabet"].items()}
    def decoder(code):
        return "".join(inverse[int(n)] for n in code.split("."))
    print(decoder("2.15.14.10.15.21.18"))   # bonjour
## ⚡ Performances
| Étape | Durée |
|---|---|
| Téléchargement Lexique383 | 10–30 s |
| Lecture TSV + encodage | 3–8 s |
| Écriture JSON | 5–15 s |
| **Total** | **~30 s** |
## 🛠 Dépannage
| Erreur | Cause | Solution |
|---|---|---|
| `AttributeError: module 'json' has no attribute 'dump'` | Fichier nommé `json.py` | Renommer en `dictionnaire.py` |
| `FileNotFoundError: Lexique383.tsv` | Téléchargement échoué | Vérifier la connexion, relancer |
| `UnicodeDecodeError` | Encodage TSV | Utiliser `encoding="utf-8"` |
| JSON trop lourd (45 Mo) | Volumétrie | Passer à SQLite |
## 📚 Sources des données
- **Lexique383** — http://www.lexique.org/ (~140 000 mots, fréquences, phonétique)
- **Morphalou 3** — 159 271 lemmes, 504 898 formes fléchies
- **Wiktionnaire** — définitions, étymologies (CC-BY-SA)
- **TLFi léger** — 54 280 articles XML expurgés
## 🗺 Feuille de route
- [x] Téléchargement automatique
- [x] Encodage A=1 … Z=26
- [x] Normalisation des accents
- [x] Export JSON
- [ ] Export SQLite
- [ ] Définitions (Wiktionnaire)
- [ ] Formes fléchies (Morphalou 3)
- [ ] CLI avec `argparse`
## 🤝 Contribution
1. Forkez le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez (`git commit -m "Ajout de ..."`)
4. Pushez (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request
## 📄 Licence
Projet sous licence **MIT**. Les données **Lexique383** ont leur propre licence — voir http://www.lexique.org/.
---
<p align="center"><strong>⭐ Si ce projet vous est utile, laissez une étoile ! ⭐</strong></p>

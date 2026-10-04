#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
import unicodedata
import urllib.request
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

URL_LEXIQUE = "http://www.lexique.org/databases/Lexique383/Lexique383.tsv"
FICHIER_TSV = "Lexique383.tsv"
FICHIER_JSON = "dictionnaire_fr.json"

# Alphabet A=1, B=2, ..., Z=26
ALPHABET = {chr(96 + i): i for i in range(1, 27)}

# =============================================================================
# FONCTIONS
# =============================================================================

def telecharger_lexique():
    """Télécharge Lexique383.tsv s'il n'existe pas déjà."""
    if os.path.exists(FICHIER_TSV):
        print(f"✅ {FICHIER_TSV} déjà présent, téléchargement ignoré.")
        return
    
    print(f"⏳ Téléchargement de {URL_LEXIQUE}...")
    urllib.request.urlretrieve(URL_LEXIQUE, FICHIER_TSV)
    print(f"✅ {FICHIER_TSV} téléchargé ({os.path.getsize(FICHIER_TSV) / 1024 / 1024:.1f} Mo)")

def normaliser(texte):
    """Enlève les accents et retourne les caractères de base (é → e, ç → c)."""
    return "".join(
        c for c in unicodedata.normalize("NFD", texte)
        if unicodedata.category(c) != "Mn"
    )

def encoder(mot):
    """
    Encode un mot en code numérique (A=1, B=2...).
    Ignore les accents et les caractères hors alphabet.
    Retourne une chaîne vide si aucun caractère valide.
    """
    mot_norm = normaliser(mot.lower())
    lettres_valides = [ALPHABET[c] for c in mot_norm if c in ALPHABET]
    return ".".join(str(n) for n in lettres_valides)

def construire_dictionnaire():
    """Lit Lexique383.tsv et construit le dictionnaire JSON."""
    dictionnaire = {}
    doublons = 0
    sans_code = 0
    
    with open(FICHIER_TSV, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        
        for row in reader:
            mot = row.get("ortho", "").strip()
            if not mot:
                continue
            
            # Éviter les doublons (garder la première occurrence)
            if mot in dictionnaire:
                doublons += 1
                continue
            
            code = encoder(mot)
            if not code:
                sans_code += 1
                continue
            
            # Extraire les métadonnées utiles
            try:
                freq = float(row.get("freqlemfilms2", 0) or 0)
            except (ValueError, TypeError):
                freq = 0.0
            
            dictionnaire[mot] = {
                "code": code,
                "frequence": round(freq, 2),
                "categorie": row.get("cgram", "").strip(),
                "phonetique": row.get("phon", "").strip()
            }
    
    print(f"📊 Statistiques :")
    print(f"   - Mots uniques : {len(dictionnaire)}")
    print(f"   - Doublons ignorés : {doublons}")
    print(f"   - Mots sans code (hors alphabet) : {sans_code}")
    
    return dictionnaire

def exporter_json(dictionnaire):
    """Exporte le dictionnaire au format JSON."""
    data = {
        "meta": {
            "source": "Lexique383",
            "version": "1.0",
            "total_mots": len(dictionnaire),
            "regles": {
                "accents": "normalisés (é → e)",
                "casse": "minuscules",
                "separateur": ".",
                "alphabet": "A=1, B=2, ..., Z=26"
            }
        },
        "alphabet": ALPHABET,
        "mots": dictionnaire
    }
    
    print(f"💾 Écriture de {FICHIER_JSON}...")
    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=None)
    
    taille = os.path.getsize(FICHIER_JSON) / 1024 / 1024
    print(f"✅ {FICHIER_JSON} créé ({taille:.1f} Mo)")

# =============================================================================
# PROGRAMME PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  CRÉATION DU DICTIONNAIRE FRANÇAIS EN JSON")
    print("=" * 60)
    
    telecharger_lexique()
    dictionnaire = construire_dictionnaire()
    exporter_json(dictionnaire)
    
    # Exemples de vérification
    print("\n📝 Exemples d'encodage :")
    for mot in ["json", "bonjour", "france", "éclair"]:
        if mot in dictionnaire:
            print(f"   {mot:15} → {dictionnaire[mot]['code']}")
        else:
            print(f"   {mot:15} → (non trouvé)")
    
    print("\n✨ Terminé !")